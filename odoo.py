from time import sleep
import xmlrpc.client
import sqlite3
import logging

import schedule

import secret
from constants import DATABASE

def updateDatabase() -> None:
    logging.info("Updating database...")
    contacts, invoices = getDataFromOdoo()
    updateDatabaseWithData(contacts, invoices)

def getDataFromOdoo() -> tuple[list[dict], list[dict]]:
    url = "https://personal-testing.odoo.com"
    db = "personal-testing"
    username = secret.EMAIL
    password = secret.API_KEY

    common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
    uid: int = common.authenticate(db, username, password, {})  # type: ignore
    
    contacts = fetchData(url, db, uid, password, "res.partner", ["id", "name", "email", "phone"])
    invoices = fetchData(url, db, uid, password, "account.move", ["id", "name", "invoice_date", "amount_total", "state", "partner_id.0"])
    
    return contacts, invoices
    
def fetchData(url: str, db: str, uid: int, password: str, model: str, keysToFetch: list[str]) -> list[dict]:
    models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")
    count: int = models.execute_kw(db, uid, password, model, "search_count", [[]])  # type: ignore
    
    limit = 10
    data = []
    
    for i in range(0, count, limit):
        ids = models.execute_kw(db, uid, password, model, "search", [[]], {'limit': limit, 'offset': limit * i})
        records: dict = models.execute_kw(db, uid, password, model, "read", [ids])  # type: ignore
        for record in records:
            newData = {}
            for key in keysToFetch:
                if "." in key:
                    key, index = key.split(".")
                    newData[key] = record[key][int(index)]
                else:
                    newData[key] = record[key]
            data.append(newData)
    
    return data

def updateDatabaseWithData(contacts: list[dict], invoices: list[dict]) -> None:
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    
    cur.execute("CREATE TABLE IF NOT EXISTS contacts (id INTEGER PRIMARY KEY, name TEXT, email TEXT, phone TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS invoices (id INTEGER PRIMARY KEY, name TEXT, invoice_date TEXT, amount_total REAL, state TEXT, partner_id INTEGER)")
    
    for contact in contacts:
        cur.execute("SELECT * FROM contacts WHERE id = ?", (contact["id"],))
        if cur.fetchone() is None:
            cur.execute("INSERT INTO contacts VALUES (?, ?, ?, ?)", (contact["id"], contact["name"], contact["email"], contact["phone"]))
        else:
            cur.execute("UPDATE contacts SET name = ?, email = ?, phone = ? WHERE id = ?", (contact["name"], contact["email"], contact["phone"], contact["id"]))
    
    for invoice in invoices:
        cur.execute("SELECT * FROM invoices WHERE id = ?", (invoice["id"],))
        if cur.fetchone() is None:
            cur.execute("INSERT INTO invoices VALUES (?, ?, ?, ?, ?, ?)", (invoice["id"], invoice["name"], invoice["invoice_date"], invoice["amount_total"], invoice["state"], invoice["partner_id"]))
        else:
            cur.execute("UPDATE invoices SET name = ?, invoice_date = ?, amount_total = ?, state = ?, partner_id = ? WHERE id = ?", (invoice["name"], invoice["invoice_date"], invoice["amount_total"], invoice["state"], invoice["partner_id"], invoice["id"]))
    
    con.commit()
    con.close()

if __name__ == "__main__":
    updateDatabase()  # Run once before starting the scheduler
    logging.info("Starting scheduler...")
    schedule.every(5).minutes.do(updateDatabase)

    while True:
        schedule.run_pending()
        sleep(10)

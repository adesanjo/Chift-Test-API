import sqlite3

from fastapi import FastAPI

from constants import DATABASE

app = FastAPI()

@app.get("/contacts")
async def contacts():
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute("SELECT * FROM contacts")
    dbContacts = cur.fetchall()
    con.close()
    response = [dict(zip(("id", "name", "email", "phone"), contact)) for contact in dbContacts]
    return response

@app.get("/contacts/{contact_id}")
async def contact(contact_id: int):
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute("SELECT * FROM contacts WHERE id = ?", (contact_id,))
    dbContact = cur.fetchone()
    con.close()
    if dbContact is None:
        return {"error": "Contact not found"}
    response = dict(zip(("id", "name", "email", "phone"), dbContact))
    return response

@app.get("/invoices")
async def invoices():
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute("SELECT * FROM invoices")
    dbInvoices = cur.fetchall()
    con.close()
    response = [dict(zip(("id", "name", "invoice_date", "amount_total", "state", "partner_id"), invoice)) for invoice in dbInvoices]
    return response

@app.get("/invoices/{invoice_id}")
async def invoice(invoice_id: int):
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute("SELECT * FROM invoices WHERE id = ?", (invoice_id,))
    dbInvoice = cur.fetchone()
    con.close()
    if dbInvoice is None:
        return {"error": "Invoice not found"}
    response = dict(zip(("id", "name", "invoice_date", "amount_total", "state", "partner_id"), dbInvoice))
    return response

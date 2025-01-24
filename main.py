import sqlite3

from fastapi import FastAPI
from pydantic import BaseModel

from constants import DATABASE

app = FastAPI()

class Contact(BaseModel):
    id: int
    name: str
    email: str
    phone: str

class Invoice(BaseModel):
    id: int
    name: str
    invoice_date: str
    amount_total: float
    state: str
    status_in_payment: str
    partner_id: int

class Error(BaseModel):
    error: str

@app.get("/contacts")
async def contacts() -> list[Contact]:
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute("SELECT * FROM contacts")
    dbContacts = cur.fetchall()
    con.close()
    response = [Contact(**dict(zip(("id", "name", "email", "phone"), contact))) for contact in dbContacts]
    return response

@app.get("/contacts/{contact_id}")
async def contact(contact_id: int) -> Contact | Error:
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute("SELECT * FROM contacts WHERE id = ?", (contact_id,))
    dbContact = cur.fetchone()
    con.close()
    if dbContact is None:
        return Error(error="Contact not found")
    response = Contact(**dict(zip(("id", "name", "email", "phone"), dbContact)))
    return response

@app.get("/invoices")
async def invoices() -> list[Invoice]:
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute("SELECT * FROM invoices")
    dbInvoices = cur.fetchall()
    con.close()
    response = [Invoice(**dict(zip(("id", "name", "invoice_date", "amount_total", "state", "status_in_payment", "partner_id"), invoice))) for invoice in dbInvoices]
    return response

@app.get("/invoices/{invoice_id}")
async def invoice(invoice_id: int) -> Invoice | Error:
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute("SELECT * FROM invoices WHERE id = ?", (invoice_id,))
    dbInvoice = cur.fetchone()
    con.close()
    if dbInvoice is None:
        return Error(error="Invoice not found")
    response = Invoice(**dict(zip(("id", "name", "invoice_date", "amount_total", "state", "status_in_payment", "partner_id"), dbInvoice)))
    return response

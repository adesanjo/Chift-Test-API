# Chift Test

Access contacts and bills through an API. The contacts and bills are updated every 5 minutes.

The file `secret.py` would normally be in `.gitignore` to avoid leaking secret information. This could also be done with environment variables or any other credential injection method. This instance of `secret.py` only contains a garbage email adress used to open a testing account on Odoo containing no real data.

### Prerequisites

Python 3.10+

### How to run

```
pip install -r requirements.txt
python3 main.py
```

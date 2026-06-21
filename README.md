# Dairy Delights

A Django test project for a dairy marketplace.

## Features

- Customer signup and login
- Product listing page
- Product detail page
- Cart flow
- Seller signup
- Seller product upload
- Demo dairy product images
- Django tests

## How to Run

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
cd newproject
..\.venv\Scripts\python.exe manage.py migrate
..\.venv\Scripts\python.exe manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

## Run Tests

```powershell
cd newproject
..\.venv\Scripts\python.exe manage.py check
..\.venv\Scripts\python.exe manage.py test
```

## Environment Variables

For deployment, use:

```text
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=your-domain.com,localhost,127.0.0.1
Google_API_Key=your-google-api-key
```

## Note

Do not upload `.venv`, `.env`, `db.sqlite3`, or cache files to GitHub.


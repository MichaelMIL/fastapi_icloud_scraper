# FastAPI chat backend

## Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Usage](#usage)

## About <a name = "about"></a>

Backed for getting icloud devices locations

## Getting Started <a name = "getting_started"></a>

### Installing

Install the requirements

```
pip install -r requirements.txt
```

## Usage <a name = "usage"></a>

For starting the server:

```
python main.py
```

Then you can access it on: <href>http://0.0.0.0:8000/docs</href>

2 endpoints:

1. POST '/login' - with email and password as query params
2. GET '/devices/location' - with email, password, and 2FA code as query params

Workflow:

1. POST '/login' -> after posting for login, a code will be sent to your approved devices.
2. POST '/login' -> now with the provided MFA code (First use only)
3. GET '/devices/locations' -> returns a list of devices names and location (if there is, else is null)
4. GET '/devices/statuses -> returns list of devices with status info
5. GET '/devices/calendar -> returns events list

After first use:
Just use the GET '/devices/locations' without the MFA code

- if POST '/login' will response in 'Valid connection' - you can use GET '/devices/locations' without MFA code

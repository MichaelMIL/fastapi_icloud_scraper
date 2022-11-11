from typing import Union
from lib.pyicloud import PyiCloudService
from fastapi import FastAPI

app = FastAPI()


@app.post("/login")
async def login(email: str, password: str, mfa_code: Union[str, None] = None):
    api = PyiCloudService(
        email, password
    )  # logging in to icloud - 2FA code will be sent to the approved devices
    if not api.is_trusted_session: # checking if the session is valid (AUTHed with 2FA)
        if not mfa_code:
            return "Two-factor authentication required."
        result = api.validate_2fa_code(mfa_code) # Validating 2FA code
        if not result:
            return "Failed to verify security code"
        if not api.is_trusted_session: # checking if the session is valid (AUTHed with 2FA)
            result = api.trust_session() # Trying to validate the session
            if not result:
                return "Failed to request trust. You will likely be prompted for the code again in the coming weeks"
    return "Valid connection"


@app.get("/devices/locations")
async def locations(email: str, password: str):
    api = PyiCloudService(email, password)  # logging in to icloud - 2FA code will be sent to the approved devices
    if not api.is_trusted_session: # checking if the session is valid (AUTHed with 2FA)
        return "Two-factor authentication required."
    return [get_device_name_location(value) for _, value in api.devices.items()]

@app.get("/devices/statuses")
async def statuses(email: str, password: str):
    api = PyiCloudService(email, password)  # logging in to icloud - 2FA code will be sent to the approved devices
    if not api.is_trusted_session: # checking if the session is valid (AUTHed with 2FA)
        return "Two-factor authentication required."
    return [get_device_status(value) for _, value in api.devices.items()]


@app.get("/devices/calenders")
async def calenders_for_this_month(email: str, password: str, period: Union[str, None] = None):
    ''' period can be [day, week, month]'''
    api = PyiCloudService(email, password)  # logging in to icloud - 2FA code will be sent to the approved devices
    if not api.is_trusted_session: # checking if the session is valid (AUTHed with 2FA)
        return "Two-factor authentication required."
    calendar_service = api.calendar # Create a calendar instance
    if period:
        events = calendar_service.get_events(period=period,as_objs=True) # getting events by period
    else:
        events = calendar_service.get_events(as_objs=True) # getting this month events
    if not events:
        return 'No items'
    return [get_device_calender_event(event) for event in events]



def get_device_calender_event(evt):
    event = {}
    event['title'] = evt.title
    event['startDate'] = f'{evt.startDate[3]}/{evt.startDate[2]}/{evt.startDate[1]} {evt.startDate[4]}:{evt.startDate[5]}' # dd/mm/yyyy hh:mm
    event['endDate'] = f'{evt.endDate[3]}/{evt.endDate[2]}/{evt.endDate[1]} {evt.endDate[4]}:{evt.endDate[5]}' # dd/mm/yyyy hh:mm
    return event


def get_device_name_location(dev):
    device = {}
    device["name"] = str(dev)
    if hasattr(dev, "location"):
        if dev.location():
            device["location"] = {
                "lat": dev.location()["latitude"],
                "lon": dev.location()["longitude"],
            }
        else:
            device["location"] = None
    return device

def get_device_status(dev):
    device = {}
    device["name"] = str(dev)
    keys = dev.keys()
    if "deviceDisplayName" in keys:
            device["deviceDisplayName"] = dev['deviceDisplayName']
    if "deviceStatus" in keys:
            device["deviceStatus"] = dev['deviceStatus']
    if "batteryLevel" in keys:
            device["batteryLevel"] = dev['batteryLevel']
    
    return device


if __name__ == "__main__":
    import uvicorn

    # for running locally
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        reload=True,
        port=8000,
    )

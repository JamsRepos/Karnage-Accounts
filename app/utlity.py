# TODO: Move this to a core.py cog.

import requests
import json
from jsonmerge import merge

from config import JFA_USERNAME,JFA_PASSWORD

async def readTemplate(template):
    """To read from a template which often stores a structure.

    Args:
        template (str): Name of the template excluding .json extension.

    Returns:
        json: JSON Response of the file data.
    """
    return json.load(open(f"app/templates/{template}.json"))

async def requestType(url, type, headers, body=None):
    if type == 'post':
        response = requests.post(url=url, json=body, headers=headers)
    if type == 'get':
        response = requests.get(url=url, headers=headers)
    if type == 'put':
        response = requests.put(url=url, json=body, headers=headers)
    if type == 'del':
        response = requests.delete(url=url, json=body, headers=headers)

    return response

async def grabJfaKey():
    url = "https://account.karna.ge/token/login"
    request = requests.get(url, auth=(JFA_USERNAME, JFA_PASSWORD ))
    request = json.loads(request.content)
    request = "Bearer " + str(request["token"])
    return request

async def callJfaApi(endpoint, type, header, body=None):
    url = f"https://account.karna.ge/{endpoint}"

    headers = {
        "Authorization": await grabJfaKey()
    }
    headers = merge(header, headers)

    response = await requestType(url=url, type=type, body=body, headers=headers)
    return response.content, response.status_code
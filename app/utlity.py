# TODO: Move this to a core.py cog.

from urllib import response
import aiohttp
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

async def asyncRequestType(url, type, headers, body=None):
    async with aiohttp.ClientSession(headers=headers) as session:
        if type == 'post':
            async with session.post(url=url, json=body) as response:
                return response
        if type == 'get':
            async with session.get(url=url) as response:
                return response
        if type == 'put':
            async with session.put(url=url, json=body) as response:
                return response
        if type == 'del':
            async with session.delete(url=url, json=body) as response:
                return response

# async def requestType(url, type, headers, body=None):
#     if type == 'post':
#         response = requests.post(url=url, json=body, headers=headers)
#     if type == 'get':
#         response = requests.get(url=url, headers=headers)
#     if type == 'put':
#         response = requests.put(url=url, json=body, headers=headers)
#     if type == 'del':
#         response = requests.delete(url=url, json=body, headers=headers)

    return response

async def grabJfaKey():
    url = "https://account.karna.ge/token/login"
    auth = aiohttp.BasicAuth(login=JFA_USERNAME,password=JFA_PASSWORD)
    async with aiohttp.ClientSession(auth=auth) as session:
        async with session.get(url) as response:
            json = await response.json()
            request = "Bearer " + str(json["token"])
            return request

async def callJfaApi(endpoint, type, header, body=None):
    url = f"https://account.karna.ge/{endpoint}"

    headers = {
        "Authorization": await grabJfaKey()
    }
    headers = merge(header, headers)
    response = await asyncRequestType(url=url, type=type, body=body, headers=headers)
    return response
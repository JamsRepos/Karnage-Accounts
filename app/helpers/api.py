# TODO: Move this to a core.py cog.
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
    """Called when we need to grab a HTTP request.

    Args:
        url (str): Specifies the URL of where the request should be sent.
        type (str): Specifies the type of the request.
        headers (json): Sets the headers for the request.
        body (json, optional): Set when the request type needs a payload, often a POST. Defaults to None.

    Returns:
        object: Returns an object containing the payload response & status code.
    """

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

    return response

async def grabJfaKey():
    """"Converts basic auth to an API token."""

    url = "https://account.karna.ge/token/login"
    auth = aiohttp.BasicAuth(login=JFA_USERNAME,password=JFA_PASSWORD)
    async with aiohttp.ClientSession(auth=auth) as session:
        async with session.get(url) as response:
            json = await response.json()
            request = "Bearer " + str(json["token"])
            return request

async def callJfaApi(endpoint, type, header, body=None):
    """Creates an API call for the JFA API.

    Args:
        endpoint (str): Specifies what endpoint to call from the API.
        type (str): Specifies the type of the request.
        header (json): Sets the headers for the request.
        body (json, optional): Set when the request type needs a payload, often a POST. Defaults to None.

    Returns:
        object: Returns an object containing the payload response & status code.
    """

    url = f"https://account.karna.ge/{endpoint}"

    headers = {
        "Authorization": await grabJfaKey()
    }
    headers = merge(header, headers)
    response = await asyncRequestType(url=url, type=type, body=body, headers=headers)
    return response
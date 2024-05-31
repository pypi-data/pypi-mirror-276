# Package contains Pre defined functions, which partners can call this by passing inputs


# system and internal libaries
from cw_rpa.libraries.common import BotUtils
from cw_rpa.libraries.common.http_wrapper_service import CWHTTPRequest
import subprocess
from types import SimpleNamespace
import re
import requests
import json
import os


# Helps to create user on 0365
def create_new_o365_user(userPrincipalName, displayName, userPassword):
    """
    Objective: 
        Creates user on o365

    Parameters:
        userPrincipalName : The principal name of the user.
        displayName : The display name of the user.
        password : Password for the user(Strong password recommended).
    Description: 
        This function creates user on o365 
    """
    try:
        req = CWHTTPRequest()
        try:
            endpoint = "https://graph.microsoft.com/v1.0/users"
            headers = {
                "Content-Type": "application/json",
            }
            req_body = {
                "accountEnabled": True,
                "userPrincipalName": userPrincipalName,
                "mailNickname": re.sub(r"[^a-zA-Z0-9]", "", userPrincipalName),
                "displayName": displayName,
                "passwordProfile": {
                    "forceChangePasswordNextSignIn": True,
                    "password": userPassword,
                },
            }
            data = json.dumps(req_body)
            response = req.post(url=endpoint, headers=headers, data=data)

            if response.status_code == 201:
                response = response.json()

                #BotUtils.log_result(f"User '{response['userPrincipalName']}' has been successfully created.")
                return True

            elif response.status_code == 400:  # Bad Request
                res_json = response.json()
                if "error" in res_json:
                    if "already exists" in res_json["error"]["message"]:
                        BotUtils.log_error(f"{userPrincipalName} already exist")
                        return False
                    else:
                        BotUtils.log_error("error occured while creating new user.")
                        BotUtils.log_error(res_json["error"]["message"])
                        return False
            elif response.status_code == 404:
                BotUtils.log_error(
                    f"unable to create user. please provide valid input data. \nrequest failed with status code {response.status_code}. Response content: {response.text}"
                )
                return False
            else:
                BotUtils.log_error(
                    f"request failed with status code {response.status_code}. Response content: {response.text}"
                )
                return False

        except Exception as e:
            BotUtils.log_error(f"Failed to get details for user {userPrincipalName}:{e}")
            return False

    except Exception as e:
            BotUtils.log_error(f"{e}")
            return False


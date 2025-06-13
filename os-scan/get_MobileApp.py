from colorama import Fore, Style
import requests
from requests.exceptions import TooManyRedirects
import json
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_mobile_apps(environment,header):

    # Sending a GET request to the URL without following redirects
    url = environment+'/NativeAppBuilder/rest/NativeApps/GetNativeApps'
    try:
        response = requests.get(
            url,
            headers=header,
            verify=False,
            allow_redirects=False,
        )
    except TooManyRedirects:
        print(
            f"| {Fore.WHITE}Mobile apps check aborted due to too many redirects.{Style.RESET_ALL}"
        )
        return

    # Checking the response code
    if response.status_code == 200:
        content_type = response.headers.get("Content-Type")
        mime_type, _ = content_type.split(';')
        if mime_type == "application/json":
            data = json.loads(response.text)
            if data == []:
                print(f"| {Fore.WHITE}[404] {Style.DIM}No mobile applications found in the scanned environment.{Style.RESET_ALL}")
            else:
                print(f"| {Fore.WHITE}[200] {Style.DIM}{response.text}{Style.RESET_ALL}")
    else:
        # The request failed or was redirected
        if response.status_code in (301, 302, 303, 307, 308):
            redirect_to = response.headers.get("Location", "unknown")
            print(
                f"| {Fore.WHITE}Request redirected to: {Style.DIM}[{redirect_to}]{Style.RESET_ALL}"
            )
            print(
                f"{Fore.RED}The mobile apps endpoint redirected instead of returning data.{Style.RESET_ALL}"
            )
        else:
            # Error in request
            print(
                f"{Fore.RED}{Style.DIM}get_mobileapp.py - Erro: {response.status_code} - {response.reason}{Style.RESET_ALL}"
            )

from colorama import Fore, Style
import requests
from requests.exceptions import TooManyRedirects
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_SapInformations(environment,header):

    url = environment+'/SAPDevService/rest/SAP/CheckSAPHealth'

    # Sending a GET request to the URL without automatically following redirects
    try:
        response = requests.get(
            url,
            headers=header,
            verify=False,
            allow_redirects=False,
        )
    except TooManyRedirects:
        print(
            f"| {Fore.WHITE}SAP Check aborted due to too many redirects.{Style.RESET_ALL}"
        )
        return

    # Checking the response code
    if response.status_code == 200:
        # The request was successful
        data = response.json()

        is_sap_conect_presente = data["IsSAPConnectorPresent"]
        sap_conect_version = data["SapConnectorVersion"]

        # Print informations
        print(f"| {Fore.WHITE}SAP Connector: {Style.DIM}[{is_sap_conect_presente}]{Style.RESET_ALL}")
        print(f"| {Fore.WHITE}SAP Connector Version: {Style.DIM}[{sap_conect_version}]{Style.RESET_ALL}")
        print(f"| {Fore.WHITE}Exposed API documentation: {Style.DIM}[{environment}/SAPDevService/rest/SAP/]{Style.RESET_ALL}")
    else:
        # The request failed or was redirected
        if response.status_code in (301, 302, 303, 307, 308):
            redirect_to = response.headers.get("Location", "unknown")
            print(
                f"| {Fore.WHITE}Request redirected to: {Style.DIM}[{redirect_to}]{Style.RESET_ALL}"
            )
            print(
                f"{Fore.RED}The SAP health endpoint redirected instead of returning data.{Style.RESET_ALL}"
            )
        else:
            # Printing the response code and error message
            print(
                f"{Fore.RED}There was a problem trying to access the url, more details below:{Style.RESET_ALL}"
            )
            print(
                f"{Fore.RED}{Style.DIM}get_SAPInformations.py - Erro: {response.status_code} - {response.reason}{Style.RESET_ALL}"
            )

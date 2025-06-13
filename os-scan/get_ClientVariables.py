from colorama import Fore, Style
import requests
from requests.exceptions import TooManyRedirects
import re
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_all_clientvaribles(environment,app_module_name,header):

    potential_defaultvalue_found = False

    # Sending a GET request to the URL without following redirects
    url = environment+'/'+app_module_name+'/scripts/'+app_module_name+'.clientVariables.js'
    try:
        response = requests.get(
            url,
            headers=header,
            verify=False,
            allow_redirects=False,
        )
    except TooManyRedirects:
        print(
            f"| {Fore.WHITE}ClientVariables check aborted due to too many redirects.{Style.RESET_ALL}"
        )
        return

    # Checking the response code
    if response.status_code == 200:
        # Search for lines that begin with "return ClientVarsService."
        matching_lines = re.findall(r"^return clientVarsService\..*", response.text, flags=re.MULTILINE)

        for line in matching_lines:
            # Extract the items inside .getVariable()
            items = re.findall(r".getVariable\((.*?)\)", line)

            # Separate items
            for item in items:
                item_content = item.split(", ")
                if len(item.split(", ")) == 4:
                    print(f"| {Fore.WHITE}[200] {Fore.YELLOW}[WARNING] {item_content}{Style.RESET_ALL}")
                    if not potential_defaultvalue_found:
                        potential_defaultvalue_found = True
                else:
                    print(f"| {Fore.WHITE}[200] {Style.DIM}{item_content}{Style.RESET_ALL}")
    else:
        # The request failed or was redirected
        if response.status_code in (301, 302, 303, 307, 308):
            redirect_to = response.headers.get("Location", "unknown")
            print(
                f"| {Fore.WHITE}Request redirected to: {Style.DIM}[{redirect_to}]{Style.RESET_ALL}"
            )
            print(
                f"{Fore.RED}The ClientVariables script redirected instead of returning data.{Style.RESET_ALL}"
            )
        else:
            # Error in request
            print(
                f"{Fore.RED}{Style.DIM}get_clientvariables.py - Erro: {response.status_code} - {response.reason}{Style.RESET_ALL}"
            )
    
    if potential_defaultvalue_found:
        print(f"{Fore.RED}[i] Potential default values found in one or more ClientVar listed in{Style.RESET_ALL} {Fore.YELLOW}yellow{Style.RESET_ALL} {Fore.RED}above.{Style.RESET_ALL}")

from colorama import Fore, Style
import requests
from requests.exceptions import TooManyRedirects
import re
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_LoginScreens(environment,header):
    # Checking phone screen login
    print(f"| {Fore.WHITE}[|||] {Style.DIM}{Style.BRIGHT}[Template_PhoneSample] Checking if the sample login screen is accessible...{Style.RESET_ALL}")
    check_PhoneSampleScreen(environment,header)

    # Checking reactive screen login
    print(f"| {Fore.WHITE}[|||] {Style.DIM}{Style.BRIGHT}[Template_ReactiveSample] Checking if the sample login screen is accessible...{Style.RESET_ALL}")
    check_ReactiveSample(environment,header)

def check_PhoneSampleScreen(environment,header):
    url_PhoneSample = environment+'/Template_PhoneSampleUserApp/scripts/Template_PhoneSampleUserApp.Common.Login.mvc.js'
    # Sending a GET request to the URL
    try:
        response = requests.get(
            url_PhoneSample,
            headers=header,
            verify=False,
            allow_redirects=False,
        )
    except TooManyRedirects:
        print(
            f"| {Fore.WHITE}[|||] {Style.DIM}[Template_PhoneSample] Request aborted due to too many redirects.{Style.RESET_ALL}"
        )
        return

    # Checking the response code
    if response.status_code == 200:

        # Regular expression to capture text in single quotes
        # e.g Return "}, "Login"))];"
        regex = r'\},\s*"Login"\)\)\);'

        # Extract values
        result = re.search(regex,response.text)
        if result:
            # The request was successful
            print(f"| {Fore.WHITE}[|||] {Style.DIM}[Template_PhoneSample] The module is online and a possible Broken Access Control vulnerability exists.{Style.RESET_ALL}")
            print(f"| {Fore.WHITE}[|||] {Style.DIM}[Template_PhoneSample] Try authenticating using the demo user and then accessing the URL of the target application.{Style.RESET_ALL}")
            print(f"| {Fore.RED}[POC] {Style.DIM}[Template_PhoneSample] Login using url: {environment}/Template_PhoneSampleUserApp/Login{Style.RESET_ALL}")
        else:
            print(f"| {Fore.WHITE}[|||] {Style.DIM}[Template_PhoneSample] The login screen for the 'Template_PhoneSampleUserApp' module is online, BUT IT IS NOT THE VULNERABLE VERSION.{Style.RESET_ALL}")
    else:
        # The request failed
        print(f"| {Fore.WHITE}[|||] {Style.DIM}[Template_PhoneSample] The sample login 'Template_PhoneSampleUserApp' is not available.{Style.RESET_ALL}")

def check_ReactiveSample(environment,header):
    url_ReactiveSample = environment+'/Template_ReactiveSampleUserApp/scripts/Template_ReactiveSampleUserApp.Common.Login.mvc.js'
    # Sending a GET request to the URL
    try:
        response = requests.get(
            url_ReactiveSample,
            headers=header,
            verify=False,
            allow_redirects=False,
        )
    except TooManyRedirects:
        print(
            f"| {Fore.WHITE}[|||] {Style.DIM}[Template_ReactiveSample] Request aborted due to too many redirects.{Style.RESET_ALL}"
        )
        return

    # Checking the response code
    if response.status_code == 200:

        # Regular expression to capture text in single quotes
        # e.g Return "}, "Login"))];"
        regex = r'\},\s*"Login"\)\)\)\];'

        # Extract values
        result = re.search(regex,response.text)
        if result:
            # The request was successful
            print(f"| {Fore.WHITE}[|||] {Style.DIM}[Template_ReactiveSample] The module is online and a possible Broken Access Control vulnerability exists.{Style.RESET_ALL}")
            print(f"| {Fore.WHITE}[|||] {Style.DIM}[Template_ReactiveSample] Try authenticating using the demo user and then accessing the URL of the target application.{Style.RESET_ALL}")
            print(f"| {Fore.RED}[POC] {Style.DIM}[Template_ReactiveSample] Login using url: {environment}/Template_ReactiveSampleUserApp/Login{Style.RESET_ALL}")
        else:
            print(f"| {Fore.WHITE}[|||] {Style.DIM}[Template_ReactiveSample] The login screen for the 'Template_ReactiveSample' module is online, BUT IT IS NOT THE VULNERABLE VERSION.{Style.RESET_ALL}")
    else:
        # The request failed
        print(f"| {Fore.WHITE}[|||] {Style.DIM}[Template_ReactiveSample] The sample login 'Template_ReactiveSample' is not available.{Style.RESET_ALL}")
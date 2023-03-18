'''
This tool is used to find the sub-directory of a website to get more information on it 

It accepts an input url

This is specifically customized for my Personal use.

Tool Developed by Vinoth, TIFAC-CORE in Cyber Security, Amrita Vishwa Vidyapeetham, Coimbatore.

Credits to openai and colorama for color

'''


import requests
# colorama is used to import fore and it is used in banner
from colorama import Fore


# This is the function to find all the dir of the website.
def get_subdirectories(url):
    subdirectories = set()
    # Send a GET request to the URL
    response = requests.get(url)
    # Loop through all links in the response
    for link in response.text.split('href="')[1:]:
        # Get the link URL
        link_url = link.split('"')[0]
        print(link_url)
        # Check if the link URL is a subdirectory
        if link_url.startswith('/'):
            subdirectories.add(link_url)
    return subdirectories

# figlet banner
print(Fore.CYAN + """
[+]    
|                                                                  
|   ██░ ██  ▄▄▄       ▄████▄   ██ ▄█▀▓█████  ██▀███  
|  ▓██░ ██▒▒████▄    ▒██▀ ▀█   ██▄█▒ ▓█   ▀ ▓██ ▒ ██▒
|  ▒██▀▀██░▒██  ▀█▄  ▒▓█    ▄ ▓███▄░ ▒███   ▓██ ░▄█ ▒
|  ░▓█ ░██ ░██▄▄▄▄██ ▒▓▓▄ ▄██▒▓██ █▄ ▒▓█  ▄ ▒██▀▀█▄  
|  ░▓█▒░██▓ ▓█   ▓██▒▒ ▓███▀ ░▒██▒ █▄░▒████▒░██▓ ▒██▒
|   ▒ ░░▒░▒ ▒▒   ▓▒█░░ ░▒ ▒  ░▒ ▒▒ ▓▒░░ ▒░ ░░ ▒▓ ░▒▓░
|   ▒ ░▒░ ░  ▒   ▒▒ ░  ░  ▒   ░ ░▒ ▒░ ░ ░  ░  ░▒ ░ ▒░
|   ░  ░░ ░  ░   ▒   ░        ░ ░░ ░    ░     ░░   ░ 
|   ░  ░  ░      ░  ░░ ░      ░  ░      ░  ░   ░     
|                    ░                                                                        
|                                                                  
| by Vinoth - v1
|
|
[+]
    """)

# input url
url = input("Enter the url:")
# calls the get_subdirectories function and the parameter as the url
subdirectories = get_subdirectories(url)
# prints the results
print(subdirectories)

import requests

with open('subdomains.txt','r') as ptr:
    url = input("Enter domain name: ")
    for i in ptr:
        full_url = "https://" + i.strip() + "." + url.strip()
        try:
            response = requests.get(full_url)
            if response.status_code == 200:
                print(full_url + " exists!✅")
            else:
                print(full_url + " returned a status code of " + str(response.status_code))
        except requests.exceptions.ConnectionError:
            print(full_url + " does not exist or can't be reached.❌")

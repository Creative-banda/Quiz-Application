from time import sleep
from threading import Thread
import json



def CountingTimer():
    hr = data["Timer"][0][0]
    minu = data["Timer"][0][1]
    sec = data["Timer"][0][2]

    hr = int(hr)
    minu = int(minu)
    sec = int(sec)

    while True:
        if sec == 0 and minu != 0:
            minu-=1
            sec = 60
            
        if minu == 0 and hr != 0:
            hr-=1
            minu = 60
        if minu == 0 and sec == 0 and hr == 0:
            print("Time Over")
            return False
        sec-=1
        sleep(1)
        print(hr,minu,sec)
    
with open(f"C:/Quiz_User/Executed_Files/Grade1/sdfsdf.json","r") as f:

        data = json.load(f)
        Thread(target=CountingTimer).start()


        
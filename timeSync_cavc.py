"""
Purpose:   Time sync for Edge devices.
Licence:   This source code for Time sync for Edge devices, is intellectual property of VaaaN infra Pvt. Ltd.
           Therefore, copying, modifying or distributing this source code without authorization is strictly prohibited.
Author:    Agam Damaraju
E-Mail:    agam.damaraju@vaaaninfra.com
Version:   1.0.0.0
Comments:  This source code is upgraded version of TS1.0.0.0, which was authored by Rinku Sharma.
           This project had been executed under the guidance of Mr. Manish Arya (manish.arya@vaaaninfra.com)
"""

################################################# Importing libraries ##########################################
from threading import Thread
import os, time, logging, requests, re
import numpy as np
import xml.etree.ElementTree as ET
from datetime import datetime
from logging import FileHandler
from configFetch import DBM

########################################### Getting root ############################
os.chdir(os.getcwd())
os.chdir("..")
os.chdir("..")

###-------------------------------------- Parsing data from web app --------------------------------------
config_db_path = r"./C-AVC_config/cavc.db"
gen = DBM(config_db_path,'GEN')
genPage= gen.DBFetch(['TimeAPI'])
url = genPage[0]

os.chdir("C-AVC")

########################################## Logger initiallization #####################################
TSSlog_dir = os.path.join("Logs","timeSync")
if not os.path.isdir(TSSlog_dir):
    os.makedirs(os.path.join(TSSlog_dir))
log_format = "%(asctime)s - %(levelname)s - %(message)s"
log_level = 10
TSSlog = logging.getLogger("Rotating Log")
TSSlog.setLevel(logging.INFO)
file_handler = FileHandler(TSSlog_dir + '//' + "TS" + '.log')
file_handler.setLevel(log_level)
formatter = logging.Formatter(log_format)
file_handler.setFormatter(formatter)
TSSlog.addHandler(file_handler)
file_handler.suffix = "%Y%m%d"
file_handler.extMatch = re.compile(r"^\d{8}$")
TSSlog.addHandler(file_handler)

TSSlog.info("########################## SUMMERY START #########################")
TSSlog.info("Purpose:   Time sync for Edge devices")
TSSlog.info("Licence:   This application for Time sync for Edge devices, is intellectual property of VaaaN infra Pvt. Ltd. Therefore, using or distributing this application without authorization is strictly prohibited.")
TSSlog.info("Author:    Agam Damaraju")
TSSlog.info("E-Mail:    agam.damaraju@vaaaninfra.com")
TSSlog.info("Version:   1.1.0.0")
TSSlog.info("Comments:  This application is upgraded version of TS1.0.0.0, which was authored by Rinku Sharma.")
TSSlog.info("This project had been executed under the guidance of Mr. Manish Arya (manish.arya@vaaaninfra.com)")
TSSlog.info("############################ SUMMERY END ##########################")
TSSlog.info("############# CONFIG PARSED DATA START #############")
TSSlog.info("TSS URL LINK is   {} ".format(url))
TSSlog.info("############# CONFIG PARSED DATA END #############")

################################################### Global variable ########################################
TSS_maintrigger = True

######################################### Time sync class #######################################
class Time_Synch_service:
    def __init__(self,url):
        self.url = url

    def TSS_main(self):
        global TSS_maintrigger
        TSSlog.info("Time Synch. Service Application is started")
        equal = True
        while TSS_maintrigger:
            try:
                timeget = requests.get(self.url)
                timestring = timeget.text
                month = timestring[6:8]
                month_str = datetime.strptime(month, '%m')
                month_name = month_str.strftime('%b')
                year = timestring[1:5]
                day = timestring[9:11]
                hour = timestring[12:14]
                minute = timestring[15:17]
                seconds = timestring[18:20]
                dateAndTime = f"{day} {month_name} {year} {hour}:{minute}:{seconds}"
                currenttimedate = datetime.now().strftime("%Y-%m-%d %I:%M:%S")
                if currenttimedate != timestring:
                    os.system("sudo date -s '{}' > /dev/null 2>&1".format(dateAndTime))
                    time.sleep(5)
            except Exception as e:
                TSSlog.error(f"In TSS main: {e}")
                time.sleep(30)
                continue

            except KeyboardInterrupt as e:
                TSSlog.error("TSS Application KeyboardInterrupt has Occur {}".format(e))
                TSS_maintrigger = False
                break

######################################### Main function ###############################
def main():
    global TSS_maintrigger
    timeobject=Time_Synch_service(url)
    try:
        TimeThread = Thread(target=timeobject.TSS_main, args=())
        TimeThread.deamon = True
        TimeThread.start()
    except Exception as e:
        TSS_maintrigger =  False
        TSSlog.error("In main: {}".format(e))
    except KeyboardInterrupt:
        TSS_maintrigger =  False
        TSSlog.error("TSS main Application KeyboardInterrupt has Occur")


if __name__ == "__main__":
    print("Time sync is running...")
    main()

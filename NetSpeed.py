# NETWORK SPEED TRACKER



# IMPORTS

import time
import os
import speedtest
from plyer import notification
import requests
import socket
import sqlite3
from datetime import datetime



# TIMESTAMP

timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# SQL DATABASE

# CONNECTS TO THE DATABES ( OR CREATES IF IT DOESNT EXIST)
conn = sqlite3.connect('netspeed.db')
cursor = conn.cursor()


# ENSURE THE TABLE EXISTS
cursor.execute('''
CREATE TABLE IF NOT EXISTS NetSpeed_Tests(
        id INTEGER PRIMARY KEY,
        timestamp TEXT,
        ping REAL,
        download_speed REAL,
        upload_speed REAL         
               
)
''')


# FUNCTION TO SAVE SPEED TEST RESULTS
def save_results(ping, download_speed, upload_speed):
    
    global timestamp
    
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    cursor.execute('''
    INSERT INTO NetSpeed_Tests(timestamp, ping, download_speed, upload_speed)
    VALUES(?, ?, ?, ?)
    ''', (timestamp, ping, download_speed, upload_speed))
    conn.commit()
    print("Seed Test Results Successfully saved to the database.\n\n")


# FUNCTION TO GET DATA
def get_speed_history():
    
    global timestamp

    cursor.execute('SELECT * FROM NetSpeed_Tests ORDER BY timestamp ASC')
    results = cursor.fetchall()
    for row in results:
        print(f"ID: {row[0]}, Time: {row[1]}, Ping: {row[2]:.2f}ms, Download: {row[3]:.2f}Mbps, Upload: {row[4]:.2f}Mbps")



# FIND BEST TIME TO BE ON NETOWKR
def find_best_times(min_download, max_ping):

    global timestamp

    cursor.execute('''
    SELECT timestamp, download_speed, ping FROM NetSpeed_Tests
        WHERE download_speed >= ? AND ping <= ?
        ORDER BY timestamp                     
         ''',(min_download, max_ping))
    results = cursor.fetchall()

    if results:
        print("Best times to use the network")
        for row in results:
            print(f"Time: {row[0]}, Download: {row[1]}Mbps, Ping: {row[2]}ms")


    else:
        print("No suitable times found based on your criteria")

#CLOSE SQL
def close_connection():
    if conn:
        conn.close()
        print("Database connection closed.")


# GLOBAL VARIABLES

#local_ip = "unset"
#public_ipv4 = "unest"
#public_ipv6 = "unset"



# NOTIFICATION 
def MSG(txt):

    notification.notify(
        title = "NetSpeed",
        message = (txt),
        timeout = 15
    )


# CLEAR SCREEN COMMAND
def CLEARSCREEN():
 
 if os.name == "nt":      # FOR WINDOWS
    os.system("cls")
 else:                    # FOR MACOS OR LINUX
    os.system('clear')

# SPEED TEST
def SPEEDTEST():
        
         # NUMBER OF ATTEMPTS TAKEN TO RESTART THE SPEED TEST IF IT FAILS. MAX IS 3 

        re_attempt = 0

        while True:
            try: 
                st = speedtest.Speedtest()
                print("FINDING BEST SERVER.....")
                best_server = st.get_best_server()
                print("\n\nINITATING SPEED TEST.....")
                download_speed = st.download() / 1_000_000   # TRANSFER TO MBPS
                upload_speed = st.upload() / 1_000_000
                ping = best_server['latency']
                # SPEED TEST RESULTS

                print("\n\n----------------   SPEED TEST RESULTS  ---------------- \n\n")
                print(f"TimeStamp: {timestamp}\n")
                print(f"Ping: {ping:.2f}ms")
                print(f"Download Speed: {download_speed:.2f}mbps")
                print(f"Upload Speed: {upload_speed:.2f}mbps")
                print("\n\n-------------------------------------------------------\n\n")
                save_results(ping,download_speed,upload_speed)
                notification.notify(
                    title = "NetSpeed",
                    message = f"Ping: {ping:.2f}ms\nDownload Speed: {download_speed:.2f}mbps\nUpload Speed: {upload_speed:.2f}mbps",
                    timeout = 15
                )
                break

            except ValueError:
                print("\n\nERROR: Please input a number.")
                time.sleep(2)
                CLEARSCREEN()   
                continue

            #except error
            

            except Exception as e:
                re_attempt += 1
                print(f"ERROR: {e},   Attempt: {re_attempt}/3")
                time.sleep(.5)
                print("\nCurrently having problems trying to run tests with Speedtest.net\n\n")
                MSG(txt= f"\nERROR: Speed Test failed, currently on Attempt {re_attempt}/3")
                for i in range(2 * 60,0,-1):
                 time.sleep(1)
                 print(f"RE-ATTEMPTING SPEED TEST: {i}", end='\r', flush=True)
                
                  
                if re_attempt == 3:
                   print(f"RE-ATTEMPTED TO PERFORM SPEED TEST 3 TIMES. WILL BE TRYING AGAIN LATER!\n\n")
                   print("Sometimes when there are to many Speed Test request to Speedtest.net from the same ip, they can temporarely block access, so we will automaitcally try again soon!")
                   time.sleep(2)
                   MSG(txt=f"ERROR: 3/3 Attempts FAILED! Will automatically Re-Attempt in a couple minutes!\nOpen NetSpeed for more info on the ERROE.")
                   return

            except ConnectionError:
                print("ERROR: Please Check your internet & Try again!")
                MSG(txt="CONNECTION ERROR: Please check to make sure your connected to internet! Will automatically perform another Speed Test in a couple minutes.")
                return
            
            except TimeoutError:
                print("ERROR: Connection or system timed out, please try again!")
                MSG(txt="TIMEOUT ERROR: Please come back to NetSpeed to try again")
                MAINMENU()


            #except ExceptionGroup e:


# WELCOME MESSAGE
def WELCOME():
     
     os.system("color 0a")
     os.system("title NetSpeed -  Developed by Jabari Lucien")

     time.sleep(.2)
     print("*********************************************************************************\n")
     print("                           NETWORK SPEED TRACKER")
     print("\n*********************************************************************************\n")
     print("Developed by Jabari Lucien\n\n\n\n")
     time.sleep(.2)



# INTERVALED SPEED TEST  / NOT IN USE
def INTERVALTEST():

    while True:

        minutes = int(input("HOW LONG DO YOU WANT THE TEST TO WAIT BETWEEN EACH TEST?: "))
        for i in range(minutes * 60,0,-1):
            print(f"\n\n\n\nNEXT SPEED TEST IN: {i} seconds...")
            time.sleep(1)
            CLEARSCREEN()
            SPEEDTEST()


# OPTIONS TO CHOOSE FROM SPEED TEST
def CHOOSETEST():  
   
   while True:
       print("WELCOME")
       time.sleep(.2)
       print("\n\n----- CHOOSE THE AMOUNT OF TIME BETWEEN EACH SPEED TEST -------- \n")
       print("1. SPEED TEST EVERY 5 MINUTES.")
       print("2. SPEED TEST EVERY 15 MINUTES.")
       print("3. SPEED TEST EVERY 30 MINUTES.")
       print("4. SPEED TEST EVERY 1 HOUR.")
       print("5. SPEED TEST EVERY 2 HOURS.")
       print("6. SPEED TEST EVERY 4 HOURS.")
       print("7. EXIT")
       print("\n-----------------------------------------------------------------")
       time.sleep(.3)
       
       try:
         choice1 = int(input("\n\n\nTYPE YOUR CHOICE HERE: "))
         #intervaled_time = choice1 * 60 # USED IN THE LOOP LATER ON TO REPEAT THE SELECTED CHOICE
         if choice1 < 1 or choice1 > 7:
           raise ValueError("ERROR: PLEASE INPUT A VALID NUMBER BETWEEN (1-7)")
           


       except ValueError as ve:
           print(f"ERROR: {ve}")
           continue   
        
       except Exception as e:
           print(f"ERROR: {e}")
           continue
       
        

       if choice1 == 1:
           
           intervaled_time = 5 * 60
           CLEARSCREEN()
           WELCOME()
           for i in range(5 * 60,0,-1):  # SET TO 5 SECONDS FOR TESTING PURPOSES
               print(f"NEXT SPEED TEST IN: {i} seconds...", end='\r', flush=True)
               time.sleep(1)

           print(' ' * 40, end='\r')          # THIS CLEARS THE LAST LINE FROM THE FOR LOOP AND MAKES IT LOOK CLEANER BY DOING SO
           SPEEDTEST()
           
       elif choice1 == 2:
           
           intervaled_time = 15 * 60
           CLEARSCREEN()
           WELCOME()
           for i in range(15 * 60,0,-1):
               print(f"NEXT SPEED TEST IN: {i} seconds...", end='\r', flush=True)
           
           print(' ' * 40, end='\r')        # THIS CLEARS THE LAST LINE FROM THE FOR LOOP AND MAKES IT LOOK CLEANER BY DOING SO
           SPEEDTEST() 
                             
       elif choice1 == 3:
           
           intervaled_time = 30 * 60
           CLEARSCREEN()
           WELCOME()
           for i in range(30 * 60,0,-1):
               print(f"NEXT SPEED TEST IN: {i} seconds...", end='\r', flush=True)
           
           print(' ' * 40, end='\r')      # THIS CLEARS THE LAST LINE FROM THE FOR LOOP AND MAKES IT LOOK CLEANER BY DOING SO
           SPEEDTEST()
      
       elif choice1 == 4:
           
           intervaled_time = 60 * 60
           CLEARSCREEN()
           WELCOME()
           for i in range(60 * 60,0,-1):
               print(f"NEXT SPEED TEST IN: {i} seconds...", end='\r', flush=True)
           
           print(' ' * 40, end='\r')      # THIS CLEARS THE LAST LINE FROM THE FOR LOOP AND MAKES IT LOOK CLEANER BY DOING SO
           SPEEDTEST()
       
       elif choice1 == 5:
           
           intervaled_time = 120 * 60
           CLEARSCREEN()
           WELCOME()
           for i in range(120 * 60,0,-1):
               print(f"NEXT SPEED TEST IN: {i} seconds...", end='\r', flush=True)
           
           print(' ' * 40, end='\r')      # THIS CLEARS THE LAST LINE FROM THE FOR LOOP AND MAKES IT LOOK CLEANER BY DOING SO
           SPEEDTEST()
   
       elif choice1 == 6:
           
           intervaled_time = 240 * 60
           CLEARSCREEN()
           WELCOME()
           for i in range(240 * 60,0,-1):
               print(f"NEXT SPEED TEST IN: {i} seconds...", end='\r', flush=True)

           print(' ' * 40, end='\r')        # THIS CLEARS THE LAST LINE FROM THE FOR LOOP AND MAKES IT LOOK CLEANER BY DOING SO
           SPEEDTEST()


       elif choice1 == 7:
           CLEARSCREEN()
           
           for i in range(3,0,-1):
               print(f"NOW EXITING TO MAIN MENU {i}", end='\r', flush=True)
               time.sleep(1)
           WELCOME()
           MAINMENU()

       else:
           CLEARSCREEN()
           time.sleep(1)
           print("ERROR: PLEASE INPUT A VALID NUMBER (1-7)")
           time.sleep(2)
           input("PRESS ENTER TO TRY AGAIN: ")
           time.sleep(.8)
           CLEARSCREEN()
           continue
       

       # THIS WILL INDEFIENTLY SCAN BASED UPON THE INTERVAL THE USER CHOOSE!!!

       while True:
           for i in range(intervaled_time,0,-1):
               print(f"NEXT SPEED TEST IN: {i} seconds", end='\r', flush=True)
               time.sleep(1)

           SPEEDTEST()       # WILL INDEFIENTLY DO THE SPEED TEST ACCORDING TO THE USERS SELECTED INTERVAL CHOICE!!!


#  TEST INTERNET CONNECTIVITY BEFORE GETTING STARTED
def check_internet():
   
    global connectionstatus
    
    try:
        response = requests.get("https://www.google.com", timeout=5)
        if response.status_code == 200:
            connectionstatus = ("ACTIVE")     
            return True
        
    except requests.ConnectionError:
        connectionstatus = ("NOT ACTIVE")
        return False
    
    return False


# FETCHES LOCAL IP  /   PUBLIC IP  /  IPV6 / IPV4
def get_local_ip():

    global local_ip  #  SO U CAN USE THE VARIABLE IN THE MAINMENU FUNCTION

    try:
        hostname = socket.gethostname() # GET HOST NAME
        local_ip = socket.gethostbyname(hostname) # RESOLVE HOSTNAME TO IP
        mask_locap_ip()
        return local_ip
    
    except socket.gaierror as e:
        local_ip = f"ERROR: Retrieving Local IP: {e}"
        return  f"ERROR: Retrieving Local IP: {e}"

def get_public_ipv4():      # IPV4

    
    global public_ipv4   #  SO U CAN USE THE VARIABLE IN THE MAINMENU FUNCTION

    try: 
        response = requests.get('https://api.ipify.org?format=json')
        public_ipv4 = response.json().get('ip', 'unkown')
        mask_ipv4()  # FUNCTION TO MASK THE IP

        return public_ipv4
    
    except requests.RequestException as e:
       public_ipv4 = f"ERROR: {e}"
       return public_ipv4

def get_ipv6():       # IPV6

    global public_ipv6

    try:
        response = requests.get('https://api64.ipify.org', params={'format': 'json'})
        response.raise_for_status()  # Raise an error for bad status codes
        public_ipv6 = response.json().get('ip')
        mask_ipv6()
        return public_ipv6
    except requests.RequestException as e:
        public_ipv6 = (f"ERROR: {e}")
        return public_ipv6

# MASKING IP
def mask_ipv4():

    global public_ipv4 
    global  unmasked_ipv4 

    unmasked_ipv4 = public_ipv4   # UNMASKED IP SAVED IN ANOTHER VARIABLE FOR LATER USE.
    

    parts = public_ipv4.split('.')   # 192.168.1.1
                           
                                       #2   #3 
                                                              
    parts[2] = 'xxxx'     # 192.168.xxxx.xxxx
    parts[3] = 'xxxx' 

    masked_ipv4 = '.'.join(parts)   # REVERSE OF THE SPLIT BASICALLY JUST JOINING THEM BACK TOGETHER
     
    public_ipv4 = masked_ipv4
    return public_ipv4

def mask_ipv6():
    
    global public_ipv6
    global unmasked_ipv6   

    unmasked_ipv6 = public_ipv6    # UNMASKED IP SAVED IN ANOTHER VARIABLE FOR LATER USE. 


    parts = public_ipv6.split(':')    # SEPERATING THE OCTETS SO U CAN EDIT THEM INDIVIDUALLY

    parts[7] = 'xxxx'     # TURNING THE 7TH OCTET INTO XXXX
    parts[6] = 'xxxx'     # TURNING THE 8TH OCTET INTO XXXX
    parts[5] = 'xxxx'
    parts[4] = 'xxxx'
    parts[3] = 'xxxx'
    parts[2] = 'xxxx'
    
    masked_ipv6 = ':'.join(parts)    # COMBINED THE SEPERATED OCTETS BACK TOGETHER
    
    public_ipv6 = masked_ipv6   # CHANING THE VARIABLE INTO THE CHANGED VARIABLE WE MADE!!!
    
    return public_ipv6    # RETURNING THE CHANGED VARIABLE OUTSIDE THE FUNCTION 

def mask_locap_ip():

    global local_ip
    global unmasked_local_ip   
    
    unmasked_local_ip = local_ip  # SAVING THE ORIGINAL IP UNMASKED INSIDE A VARIABLE FOR LATER USE.

    parts = local_ip.split('.')

    parts[3] = 'xxxx'
    parts[2] = 'xxxx'
    
    masked_local_ip  = '.'.join(parts)  
      
    local_ip = masked_local_ip   

    return  local_ip

# MENU FOR FULL UNMASKED IP:
def show_unmasked_ip():
    
     os.system("title NetSpeed -  Developed by Jabari Lucien")

     time.sleep(.2)
     print("*********************************************************************************\n")
     print("                           KEEP THIS INFO CONFIDENTIAL")
     print("\n*********************************************************************************\n")
     print("Developed by Jabari Lucien\n\n\n\n")
     time.sleep(.2)

     print("------------  CONNECTION STATUS  ------------\n")
     print(f"Connection Status: {connectionstatus}")
     print(f"Local IP     : {unmasked_local_ip}")
     print(f"Public IP(v4): {unmasked_ipv4}")
     print(f"Public IP(v6): {unmasked_ipv6}")      
     print("\n--------------------------------------------\n\n\n\n")


     input("PRESS ENTER TO EXIT: ")
     CLEARSCREEN()
     WELCOME()
     MAINMENU()
       

# MAIN MENU SELECTION
def MAINMENU():
     
    # CALL UPON LOCAL / PUBLIC IP 

    get_local_ip()
    get_public_ipv4()
    get_ipv6()
    

    # DOES A CONNECTION CHECK BEFORE ALLOWING USERS TO DO ANYTHING ELSE. ( CAN PREVENT ANY FURTHER CONFUSIONS OR ERRORS, IF THE USER HAS NO CONNECTION.)  

    check_internet()
    if not check_internet:
        print("\n\nWARNING: No internet connection detected. some features may not work.")
        choice2 = input("Would you like to continue? (yes/no): ").strip().lower()
        if choice not in {'yes','y'}:
            print("\n\nExiting the program. Please reconnect to internet and try again.")
            time.sleep(1.6)
            exit()
        
    # CONNECTION STATUS

    print("------------  CONNECTION STATUS  ------------\n")
    print(f"Connection Status: {connectionstatus}")
    print(f"Local IP     : {local_ip}")
    print(f"Public IP(v4): {public_ipv4}")
    print(f"Public IP(v6): {public_ipv6}")      
    print("\n--------------------------------------------\n\n\n\n")


    print("------------  NetSpeed ------------\n")
    print("1. Start Speed Test now.")
    print("2. Start Automatic Speed Tester.")
    #print("\n------------------------------------\n")
    print("")
    print("3. View SpeedTest history")
    print("4. Find best time to be on my netowrk")
    #print("\n------------------------------------\n")
    print("")
    print("5. Unmask IP's")
    print("6. About the Script")
    print("")
    print("7. Exit ")
    print("\n------------------------------------\n") 
    
    time.sleep(0.2)

    
    while True:
            try:
                choice1 = int(input("\n\n\nTYPE YOUR CHOICE HERE: "))
                if choice1 not in [1, 2, 3, 4, 5, 6, 7, 10029]:
                    print("ERROR: Please select a valid option (1 - 3).")
                    continue

            except ValueError:
                print("ERROR: Please input a valid number.")
                continue
            break

    CLEARSCREEN()
    if choice1 == 1:
            SPEEDTEST()
            while True:
                try:
                    print("\n\n\nWOULD YOU LIKE TO PERFORM ANOTHER TEST OR EXIT TO THE MAIN MENU?\n\n")
                    print("1. PERFORM ANOTHER SPEED TEST.")
                    print("2. EXIT TO MAIN MENU.\n\n")
                    time.sleep(0.2)

                    stay1 = int(input("TYPE YOUR CHOICE HERE: "))
                    if stay1 == 1:
                        print("\n\nIF YOU'RE ENJOYING THE PROGRAM, MAKE SURE TO SUBSCRIBE FOR FUTURE UPDATES.\n\n")
                        time.sleep(0.2)
                        SPEEDTEST()
                    elif stay1 == 2:
                        CLEARSCREEN()
                        WELCOME()
                        MAINMENU()
                        break
                    else:
                        print("ERROR: Please enter 1 or 2.")
                except ValueError:
                    print("ERROR: Please input a valid number.")
    elif choice1 == 2:
            CLEARSCREEN()
            WELCOME()
            CHOOSETEST()

    elif choice1 == 3:
        CLEARSCREEN()
        get_speed_history()
        input("\n\n\nPRESS ENTER TO EXIT TO MAIN MENU: ")
        CLEARSCREEN()
        WELCOME()
        MAINMENU()

    elif choice1 == 4:
        CLEARSCREEN()
        find_best_times(min_download=700, max_ping=25)
        input("\n\n\nPRESS ENTER TO EXIT TO MAIN MENU: ")
        CLEARSCREEN()
        WELCOME()
        MAINMENU()

    elif choice1 == 5:
        if os.name == "nt":
            os.system("color 05")

        CLEARSCREEN()
        show_unmasked_ip()
        

    # WILL MAKE THIS A SECRET OPTION TO OPEN A DOS MENU, MAYBE
    elif choice1 == 10029:
        CLEARSCREEN()
        input("TOESSS")

        

    
    
    elif choice1 == 6:  # ABOUT THE SCRIPT
        print("")



    elif choice1 == 7:
        leaving()
        

# DUMMY FUNCTION TO TEST SYSTEMS

def leaving():
    close_connection()
    print("\n\nThank you for trying out my program.")
    print("If you enjoyed make sure to subscribe for more fun programs & for potential future updates (like the gui)")
    time.sleep(3.5)
    exit()

# RUN PROGRAM

WELCOME()
MAINMENU()

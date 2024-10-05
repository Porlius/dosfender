import os
import time
import requests
from flask import Flask

app = Flask(__name__)

MAX_REQUESTS_PER_SECOND = 5
IP_REQUEST_MAP = {}

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_green(text):
    print("\033[92m" + text + "\033[0m")  # 92m represents green color

def menu():
    clear_screen()
    print_green("""
  _____  _____   ____   _____ _   _   _   _______ 
 |  __ \|  __ \ / __ \ / ____| \ | | ( ) |__   __|
 | |  | | |  | | |  | | (___ |  \| |  \|    | |   
 | |  | | |  | | |  | |\___ \| . ` |        | |   
 | |__| | |__| | |__| |____) | |\  |        | |   
 |_____/|_____/ \____/|_____/|_| \_|        |_|   
                                                  
    """)
    print_green("1. Start Anti-DDoS Protection")
    print_green("2. Stop Anti-DDoS Protection")
    print_green("3. Exit")

def limit_traffic(destination):
    current_time = time.time()
    ip = "127.0.0.1"  # Simulated IP address for testing outside Flask

    if ip not in IP_REQUEST_MAP:
        IP_REQUEST_MAP[ip] = [current_time]
    else:
        requests = IP_REQUEST_MAP[ip]
        requests = [t for t in requests if current_time - t < 1]
        requests.append(current_time)
        IP_REQUEST_MAP[ip] = requests

    if len(IP_REQUEST_MAP[ip]) > MAX_REQUESTS_PER_SECOND:
        return True
    else:
        return False

def start_protection():
    requests_per_second = int(input("Enter the number of requests per second: "))
    destination = input("Enter the destination web address or IP: ")

    print(f"Starting Anti-DDoS protection for {destination}...")

    while True:
        if limit_traffic(destination):
            print("Too many requests. Please try again later.")
            time.sleep(1 / requests_per_second)
        else:
            try:
                print(f"Processing request to {destination}...")
                response = requests.get(destination)
                if response.status_code == 200:
                    print("Request accepted.")
                else:
                    print("Request rejected.")
                time.sleep(1 / requests_per_second)  # Wait according to request limit per second
            except requests.RequestException as e:
                print(f"Error processing request to {destination}: {e}")
                break

def stop_protection():
    print("Stopping Anti-DDoS protection...")
    # Your code to stop Anti-DDoS protection would go here
    time.sleep(2)  # Simulating a process that takes time
    print("Anti-DDoS protection stopped.")

@app.route('/')
def index():
    return "Homepage!"

if __name__ == "__main__":
    menu()
    while True:
        option = input("Select an option: ")

        if option == "1":
            start_protection()
        elif option == "2":
            stop_protection()
        elif option == "3":
            print("Exiting...")
            break
        else:
            print("Invalid option. Please select a valid option.")

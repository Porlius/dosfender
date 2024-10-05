import os
import subprocess
from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Create the Flask application
app = Flask(__name__)

# Configure request limiter
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"]  # Default request limits
)

# Home route with rate limiting
@app.route('/')
@limiter.limit("10 per minute")  # Limit to 10 requests per minute
def home():
    return "Hello! You are protected against DoS attacks."

# Data route with rate limiting
@app.route('/api/data')
@limiter.limit("5 per minute")  # Limit to 5 requests per minute
def data():
    return jsonify({"message": "Here is your data."})

# Handle error for exceeding request limit
@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify(error="Too many requests. Try again later."), 429

# Function to run the server
def run_server():
    app.run(host='0.0.0.0', port=8080)

# Banner for the menu
def show_banner():
    banner = """
\033[92m
  _____   ____   _____ ______ ____  _   _ _____  ______ _____  
 |  __ \ / __ \ / ____|  ____|___ \| \ | |  __ \|  ____|  __ \ 
 | |  | | |  | | (___ | |__    __) |  \| | |  | | |__  | |__) |
 | |  | | |  | |\___ \|  __|  |__ <| . ` | |  | |  __| |  _  / 
 | |__| | |__| |____) | |     ___) | |\  | |__| | |____| | \ \ 
 |_____/ \____/|_____/|_|    |____/|_| \_|_____/|______|_|  \_\
                                                              
                                                              
\033[0m
"""
    print(banner)

# Function to monitor incoming requests
def monitor_requests():
    print("\033[92mMonitoring incoming requests...\033[0m")
    try:
        # Use 'netstat' on Windows or 'ss' on Linux/Mac to check connections
        if os.name == 'nt':
            command = ['netstat', '-an']
        else:
            command = ['ss', '-tuln']  # Shows listening ports and established connections
        
        # Run the command and capture the output
        output = subprocess.check_output(command).decode('utf-8')
        print("\033[92mActive connections:\033[0m")
        print(f"\033[92m{output}\033[0m")
    except Exception as e:
        print(f"\033[91mError monitoring requests: {str(e)}\033[0m")
    
    input("\033[92mPress Enter to return to the menu.\033[0m")

# Interactive menu
def show_menu():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')  # Clear screen (Windows: cls, Linux/Mac: clear)
        show_banner()  # Show the banner
        print("\033[92m========= DoS Protection Tool =========")
        print("1. Start Flask server with DoS protection")
        print("2. Configure custom request limits")
        print("3. Monitor incoming requests")
        print("4. Exit")
        print("=======================================\033[0m")
        
        option = input("\033[92mSelect an option: \033[0m")
        
        if option == '1':
            print("\033[92m\nStarting Flask server at http://0.0.0.0:8080...\n\033[0m")
            run_server()  # Start the server
        elif option == '2':
            configure_limits()
        elif option == '3':
            monitor_requests()  # Call the request monitoring function
        elif option == '4':
            print("\033[92mExiting the program...\033[0m")
            break
        else:
            print("\033[92mInvalid option, please try again.\033[0m")

# Function to configure custom request limits
def configure_limits():
    daily_limit = input("\033[92mEnter daily request limit (e.g., '200 per day'): \033[0m")
    hourly_limit = input("\033[92mEnter hourly request limit (e.g., '50 per hour'): \033[0m")
    
    # Update the limits in the limiter configuration
    global limiter
    limiter = Limiter(
        get_remote_address,
        app=app,
        default_limits=[daily_limit, hourly_limit]  # Apply new limits
    )
    
    print(f"\033[92mLimits updated: {daily_limit} per day, {hourly_limit} per hour.\033[0m")
    input("\033[92mPress Enter to return to the menu.\033[0m")

if __name__ == '__main__':
    show_menu()

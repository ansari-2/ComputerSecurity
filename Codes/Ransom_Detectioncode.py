import os, time, datetime
import re
import subprocess, pytz
import tkinter as tk
from tkinter import messagebox

# define the directory to monitor
User_home_directory = os.path.expanduser("~")
 
Dir_path_to_monitor = os.path.join(User_home_directory,'Documents/critical/')
# Create a directory to store initial timestamps of files
initial_file_timestamps ={}

# Function to get the timestamps of the files in the directory

def get_file_timestamps(monitor_dir):
    file_timestamps ={}
    for root, _, files in os.walk(monitor_dir):
        for file in files:
            file_path = os.path.join(root,file)
            file_timestamps[file_path] = datetime.datetime.utcfromtimestamp(os.path.getmtime(file_path))\
            
    return file_timestamps


# Get the initial time stamps of the files in the directory
initial_file_timestamps = get_file_timestamps(Dir_path_to_monitor)
keys = initial_file_timestamps.keys()
# printing timestamps to check order
for i in keys:
    dt = initial_file_timestamps[i]
    print(dt)


# Infinite Loop over the directory to check for modifications made by an external process

while True:
    # get the current timestamps of the files in the directory
    current_file_timestamps = get_file_timestamps(Dir_path_to_monitor)
    # print(current_file_timestamps)

    #Loop over the directory to search for modified files
    for file_path, initial_file_timestamp in initial_file_timestamps.items():
        if file_path in current_file_timestamps:
            current_file_timestamp = current_file_timestamps[file_path]
            initial_file_timestamp = initial_file_timestamp

            if current_file_timestamp != initial_file_timestamp:
                print(current_file_timestamp)
                print(f"the file {file_path} has been modified")
                #parsing the timestamp
                parsed_timestamp = datetime.datetime.strptime(str(current_file_timestamp),"%Y-%m-%d %H:%M:%S.%f")
                # getting the time zone correction to match 
                Central_timezone = pytz.timezone('America/Chicago')
                #changing the timezone by replacing it with central timezone
                Central_datetime = parsed_timestamp.replace(tzinfo=pytz.utc).astimezone(Central_timezone)

                #Formatting timestamp 
                formatted_timestamp = Central_datetime.strftime("%H:%M:%S")

                print(formatted_timestamp)

                #converting the UTC datetime to Central time
                command = f"ausearch  -i -ts today {formatted_timestamp} -f {file_path}"

                # Running the command and capturing the output
                output = subprocess.check_output(command, shell=True).decode()

                #Parsing the output with regular expressions
                nametype =  re.findall('nametype=([^ ]+)',output)
                pid = re.findall(' pid=(\d+)',output)
                exe = re.findall('exe=([\S]+)',output)
                tty =re.findall('tty=([\S]+)',output)
                # print(tty)
                # print(exe)
                # print(pid)
                # print(nametype)
                # print(output)

                # Checking for the pattern in file modifications
                if nametype == ['NORMAL', 'PARENT', 'CREATE', 'DELETE', 'PARENT', 'PARENT']:
                    window = tk.Tk()
                    window.withdraw()  # Hide the main window
                    user_response = messagebox.askyesno("Kill Process?", f"Process {pid} is modifying all files in {file_path} kill it?")
                    if user_response:
                        window.destroy()  # Close the hidden main window
                        print(f'killing the process {exe[0]} with process ID {pid[0]}')
                        command = f'kill {pid[0]}'
                        output = subprocess.check_output(command, shell=True).decode()

                # Process the output to extract relevant information
               
                initial_file_timestamps[file_path] = current_file_timestamp
                break
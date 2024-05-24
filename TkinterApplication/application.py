# Importing required module 
from tkinter import *
from tkinter import messagebox
import customtkinter as ctk 
from PIL import ImageTk,Image
import mysql.connector
import requests
import json, os
import face_recognition
import numpy as np
import shutil

pathOfUnresolved = "UnresolvedImages"
pathOfResolved = "ResolvedImages"
pathOfImages = "Images"
# Server IP, replace it with your server IP
serverUrl = ""

# sql connection, connect to your database
mydb = mysql.connector.connect(
  host="",
  user="root",
  password="",
  database="LitterSystem"
)
mycursor = mydb.cursor()

def Resolve(i):
    global pathOfResolved
    global pathOfUnresolved
    source_path = f"{pathOfUnresolved}\\{i}.jpg"
    destination_dir = f"{pathOfResolved}\\{i}.jpg"
    shutil.move(source_path, destination_dir)

def getImages():
    global pathOfUnresolved
    for i, url in enumerate(unresolvedImagesUrl.json()["images"], start=1):
        try:
            print(url)
            response = requests.get(url)
            if response.status_code == 200:
                image_content = response.content
                # Specify the path to the folder where you want to save the images
                folder_path = f"{pathOfUnresolved}"
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)
                with open(os.path.join(folder_path, f"{i}.jpg"), "wb") as f:
                    f.write(image_content)
                print(f"Image {i} saved successfully.")
            else:
                messagebox.showwarning("Warning", "Failed to fetch Image!")
        except Exception as e:
            messagebox.showwarning("Warning", "Fatal Error Occured While Connecting to Server!")

# This will be the path to the server, replace it with your server path
unresolvedImagesUrl = requests.get(f"{serverUrl}/getUnResolvedImages")

img_count = len(os.listdir(pathOfUnresolved))
img_count_allImages = len(os.listdir(pathOfImages))

# Calculates embedding of images

def compute_encoding(image_folder):
    embedding = []  
    image_files = [f for f in os.listdir(image_folder) if f.endswith('.jpg')]
    
    for i, image_file in enumerate(image_files):
        print(f"Computing embedding for {image_file} ({i+1}/{len(image_files)})")
        image_path = os.path.join(image_folder, image_file)
        image = face_recognition.load_image_file(image_path)
        
        try:
            image_encoding = face_recognition.face_encodings(image)[0]
            embedding.insert(i+1, [image_encoding, image_file])
        except IndexError:
            print(f"No faces found in {image_file}. Skipping this file.")
    
    return embedding

embedding = compute_encoding(pathOfImages)

for x,y in embedding:
    print(x,y)


embeddingDifference= []
# Calculates Embedding Difference
def computeEmbeddingDifference(knownEncoding, newEncoding):
    return np.linalg.norm(knownEncoding - newEncoding)


# Selecting GUI theme - dark, 
ctk.set_appearance_mode("dark") 

# Selecting color theme-blue, green, dark-blue 
ctk.set_default_color_theme("dark-blue")
# Retreiving Images from backend
getImages()

# App
app = ctk.CTk() 
app.title("CleanCampus") 

# frame for our root
frame = ctk.CTkFrame(master=app) 
frame.pack(pady=20,padx=20, fill='both',expand=True) 

label = ctk.CTkLabel(master = frame,text = "CleanCampus: AI powered litter detection system",
        width=120,height=75,font = ("Arial", 24),fg_color=("white", "gray75"),corner_radius=8)
label.pack(pady=12,padx=50) 

# Event handling function for Inspect
def Inspect():
    global inspect
    inspect = ctk.CTkToplevel()
    inspect.title("Inspect")
# Function to switch to the Insert page
    def show_insert_page():
        hide_all_frames()
        insert_frame.pack(fill='both', expand=True)

# Function to switch to the Update page
    def show_update_page():
        hide_all_frames()
        update_frame.pack(fill='both', expand=True)

# Function to switch to the Delete page
    def show_delete_page():
        hide_all_frames()
        delete_frame.pack(fill='both', expand=True)

# Function to switch to the Select page
    def show_select_page():
        hide_all_frames()
        select_frame.pack(fill='both', expand=True)

# Function to hide all frames
    def hide_all_frames():
        insert_frame.pack_forget()
        update_frame.pack_forget()
        delete_frame.pack_forget()
        select_frame.pack_forget()


    # Frame for holding buttons
    button_frame = ctk.CTkFrame(inspect)
    button_frame.pack(side='left', fill='y')

    # Frame for displaying pages
    page_frame = ctk.CTkFrame(inspect)
    page_frame.pack(side='right', fill='both', expand=True)

    # Frames for different pages
    insert_frame = ctk.CTkFrame(page_frame)
    # getting student data for insertion
    student_data_name = ctk.CTkEntry(master= insert_frame,placeholder_text="Name",width=170,height=45,border_width=2,corner_radius=10)
    student_data_name.pack(padx = 10, pady = 10)
    student_data_degree = ctk.CTkEntry(master= insert_frame,placeholder_text="Degree(Short form)",width=170,height=45,border_width=2,corner_radius=10)
    student_data_degree.pack(padx = 10, pady = 10)
    student_data_cms = ctk.CTkEntry(master= insert_frame,placeholder_text="CMS",width=170,height=45,border_width=2,corner_radius=10)
    student_data_cms.pack(padx = 10, pady = 10)
    student_data_gmail = ctk.CTkEntry(master= insert_frame,placeholder_text="gmail",width=170,height=45,border_width=2,corner_radius=10)
    student_data_gmail.pack(padx = 10, pady = 10)
    student_data_dept = ctk.CTkEntry(master= insert_frame,placeholder_text="Department(Short form)",width=170,height=45,border_width=2,corner_radius=10)
    student_data_dept.pack(padx = 10, pady = 10)
    student_data_num = ctk.CTkEntry(master= insert_frame,placeholder_text="Number",width=170,height=45,border_width=2,corner_radius=10)
    student_data_num.pack(padx = 10, pady = 10)
    student_data_batch = ctk.CTkEntry(master= insert_frame,placeholder_text="Batch",width=170,height=45,border_width=2,corner_radius=10)
    student_data_batch.pack(padx = 10, pady = 10)
    # insertion button
    def insert_student():
        sql_insert = "INSERT INTO student VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val_insert = ( student_data_cms.get() , student_data_name.get(), student_data_degree.get(), student_data_batch.get(),  student_data_gmail.get(), student_data_dept.get(), student_data_num.get())
        mycursor.execute(sql_insert, val_insert)
        mydb.commit()
        insert_label = ctk.CTkLabel(master=insert_frame, text=f"{mycursor.rowcount} was inserted")
        insert_label.pack()

    insert_student_button = ctk.CTkButton(master= insert_frame, width=170, height=45,font = ("Arial", 24) ,text="Insert", command=insert_student)
    insert_student_button.pack(padx = 10, pady = 10)

    update_frame = ctk.CTkFrame(page_frame)

    student_data_cms_update = ctk.CTkEntry(master= update_frame,placeholder_text="CMS",width=170,height=45,border_width=2,corner_radius=10)
    student_data_cms_update.pack(padx = 10, pady = 10)

    fields = ["Student Name", "Degree", "Batch", "GMAIL", "Department", "Phone Number"]

    radio_var = ctk.IntVar(value = 0)
    radiobutton_1 = ctk.CTkRadioButton(master= update_frame, text="Name",
                                              variable= radio_var, value=1)
    radiobutton_2 = ctk.CTkRadioButton(master=update_frame, text="Number",
                                              variable= radio_var, value=2)
    radiobutton_3 = ctk.CTkRadioButton(master=update_frame, text="Department",
                                              variable= radio_var, value=3)
    radiobutton_4 = ctk.CTkRadioButton(master=update_frame, text="Batch",
                                              variable= radio_var, value=4)
    radiobutton_5 = ctk.CTkRadioButton(master=update_frame, text="Mail",
                                              variable= radio_var, value=5)
    
    radiobutton_1.pack(padx=10, pady=10)
    radiobutton_2.pack(padx=10, pady=10)
    radiobutton_3.pack(padx=10, pady=10)
    radiobutton_4.pack(padx=10, pady=10)
    radiobutton_5.pack(padx=10, pady=10)

    student_dataupdate = ctk.CTkEntry(master= update_frame,placeholder_text="Enter:",width=170,height=45,border_width=2,corner_radius=10)
    student_dataupdate.pack(padx = 10, pady = 10)

    def update_data():
        if(radio_var.get() == 1):
            sql = "UPDATE student SET student_name = %s WHERE cms = %s"
            val = ( student_dataupdate.get() , student_data_cms_update.get())
            mycursor.execute(sql, val)
            mydb.commit()
            update_label = ctk.CTkLabel(master= update_frame, text=f"{mycursor.rowcount} was inserted")
            update_label.pack()

    studentdata_update_button = ctk.CTkButton(master= update_frame, width=170, height=45,font = ("Arial", 24) ,text="Update", command= update_data)
    studentdata_update_button.pack(padx = 10, pady = 10)

    delete_frame = ctk.CTkFrame(page_frame)
    # getting cms for deleteion
    student_data_cms_delete = ctk.CTkEntry(master= delete_frame,placeholder_text="CMS",width=170,height=45,border_width=2,corner_radius=10)
    student_data_cms_delete.pack(padx = 10, pady = 10)
    # event handling for deletion
    def delete_student():
        sql_delete = "DELETE FROM student WHERE cms = %s"
        val_delete = (student_data_cms_delete.get(),)
        mycursor.execute(sql_delete, val_delete)
        mydb.commit()
        insert_label = ctk.CTkLabel(master= delete_frame, text= f"{mycursor.rowcount} was deleted ")
        insert_label.pack()
    delete_student_button = ctk.CTkButton(master= delete_frame, width=170, height=45,font = ("Arial", 24) ,text="Delete", command= delete_student)
    delete_student_button.pack(padx = 10, pady = 10)

    select_frame = ctk.CTkFrame(page_frame)
    # getting cms for selection
    student_data_cms_select = ctk.CTkEntry(master= select_frame,placeholder_text="CMS",width=170,height=45,border_width=2,corner_radius=10)
    student_data_cms_select.pack(padx = 10, pady = 10)
    # event handling for deletion
    def select_student():
        global pathOfImages
        sql_select = "SELECT * FROM student WHERE cms = %s"
        val_select = (student_data_cms_select.get(),)
        mycursor.execute(sql_select, val_select)
        select_result = mycursor.fetchall()

        result_label = ctk.CTkLabel(master= select_frame, text="")
        result_label.pack()

        image_label = ctk.CTkLabel(master=select_frame, text="")
        image_label.pack()

        if select_result:
        # If there are results, format them and set the label text
            formatted_result = ""
            for row in select_result:
                formatted_result += "CMS: {}\n".format(row[0])
                formatted_result += "Name: {}\n".format(row[1])
                formatted_result += "Degree: {}\n".format(row[2])
                formatted_result += "Batch: {}\n".format(row[3])
                formatted_result += "Mail: {}\n".format(row[4])
                formatted_result += "Department: {}\n".format(row[5])
                formatted_result += "Number: {}\n".format(row[6])
                result_label.configure(text=formatted_result)
            
            image_path = os.path.join(f"{pathOfImages}", f"{student_data_cms_select.get()}.jpg")  # Adjust directory as needed
        
        if os.path.exists(image_path):
            img = Image.open(image_path)
            img = img.resize((175, 175))  
            img_tk = ImageTk.PhotoImage(img)
            image_label.configure(image=img_tk)
            image_label.image = img_tk  
        else:
        # If there are no results, display a message indicating so
            result_label.configure(text="No student found with CMS: {}".format(student_data_cms_select.get()))
        
    select_student_button = ctk.CTkButton(master= select_frame, width=170, height=45,font = ("Arial", 24) ,text="Select", command= select_student)
    select_student_button.pack(padx = 10, pady = 10)
    

    # Buttons to switch between pages
    insert_button = ctk.CTkButton(master=button_frame, width=120, height=32,font = ("Arial", 24) ,text="Insert", command=show_insert_page)
    update_button = ctk.CTkButton(master=button_frame, width=120, height=32,font = ("Arial", 24) ,text="Update", command=show_update_page)
    delete_button = ctk.CTkButton(master=button_frame, width=120, height=32,font = ("Arial", 24) ,text="Delete", command=show_delete_page)
    select_button = ctk.CTkButton(master=button_frame, width=120, height=32,font = ("Arial", 24) , text="Select", command=show_select_page)

    # Pack buttons vertically
    insert_button.pack(fill='x', padx=30, pady=30)
    update_button.pack(fill='x', padx=30, pady=30)
    delete_button.pack(fill='x', padx=30, pady=30)
    select_button.pack(fill='x', padx=30, pady=30)


#before
open_Inspect = ctk.CTkButton(master= frame,width=120,height=32,border_width=0,corner_radius=8,font = ("Arial", 24),text="Inspect",command = Inspect)
open_Inspect.pack(pady=12,padx=50) 

# Event handling function for Report

def image_clicked(i):
    global pathOfUnresolved
    global pathOfImages
    # Create a new window
    match = ctk.CTkToplevel()
    match.title("Matches")
    print(f"image clicked {i}")

    upper_frame_match = ctk.CTkFrame(match)
    upper_frame_match.pack()

    label_match = ctk.CTkLabel(upper_frame_match, text="Possible Matches", width=120, height=75, font=("Arial", 20))
    label_match.pack()

    resolved = ctk.CTkButton(master= upper_frame_match,width=120,height=32,border_width=0,corner_radius=8,font = ("Arial", 24),text="Resolved",command = lambda: Resolve(i))
    resolved.pack()

    lower_frame_match = ctk.CTkFrame(match)
    lower_frame_match.pack()
    
    scroll_bar = ctk.CTkScrollableFrame(lower_frame_match, width= 750, height= 850)
    scroll_bar.pack()
    

    # Function to update the scroll region

    # layouts to hold student's data
    layout_s1 = ctk.CTkFrame(master= scroll_bar)
    layout_s1.pack()

    layout_s2 = ctk.CTkFrame(master= scroll_bar)
    layout_s2.pack()

    layout_s3 = ctk.CTkFrame(master= scroll_bar)
    layout_s3.pack()

    layout_s4 = ctk.CTkFrame(master= scroll_bar)
    layout_s4.pack()

    layout_s5 = ctk.CTkFrame(master= scroll_bar)
    layout_s5.pack()

    layout_container = [layout_s1,layout_s2,layout_s3,layout_s4,layout_s5]

    # Calculating encoding of image clicked
    image_new = face_recognition.load_image_file(f"{pathOfUnresolved}\\1.jpg")
    newImageEncoding = face_recognition.face_encodings(image_new)[0]
    print(newImageEncoding)

    embeddingDifference = []

    for j in range(1, img_count_allImages):
        print(f" j in diff = {j}")  
        difference = computeEmbeddingDifference(embedding[j-1][0], newImageEncoding)
        embeddingDifference.insert(j,[difference, embedding[j-1][1]])  

    result = sorted(embeddingDifference)[:5]

    print("embedding diff")

    i = 0
    for diff, index in result:
        cms_value = os.path.splitext(index)[0]
        image_path = f"{pathOfImages}/{cms_value}.jpg"
        img = Image.open(image_path)
        img = img.resize((175, 175))  
        img = ImageTk.PhotoImage(img)
        label_img = ctk.CTkLabel(layout_container[i], image=img, text="")
        label_img.image = img
        label_img.pack()  

        # Fetch student details from SQL
        sql_select = "SELECT * FROM student WHERE cms = %s"
        cms_value_int = int(cms_value)
        val_select = (cms_value_int,)
        mycursor.execute(sql_select, val_select)
        print(f"Executing SQL query: {sql_select} with value: {val_select}")
        student_data = mycursor.fetchall()  

        if student_data:  # Ensure data is returned
            formatted_result = "Student Details:\n"
            for row in student_data:
                formatted_result += "CMS: {}\n".format(row[0])
                formatted_result += "Name: {}\n".format(row[1])
                formatted_result += "Degree: {}\n".format(row[2])
                formatted_result += "Batch: {}\n".format(row[3])
                formatted_result += "Mail: {}\n".format(row[4])
                formatted_result += "Department: {}\n".format(row[5])
                formatted_result += "Number: {}\n".format(row[6])
                student_details_label = ctk.CTkLabel(layout_container[i], text=formatted_result, font=("Arial", 12))
                student_details_label.pack(padx = 10, pady = 10)
        i+=1


def Report():
    global pathOfUnresolved
    global report
    report = ctk.CTkToplevel()
    report.title("Report")

    # Create upper frame
    upper_frame = ctk.CTkFrame(report)
    upper_frame.pack()

    # Label for upper frame
    label = ctk.CTkLabel(upper_frame, text="Images",width=120,height=75,font = ("Arial", 20))
    label.pack()

    # Create lower frame
    lower_frame = ctk.CTkFrame(report)
    lower_frame.pack()

    #print(img_count)
    num_columns = round(img_count/2) + 1
    #print(num_columns)
    # Define spacing between images

    for i in range(1, img_count+1):  # Assuming you have 5 images
        image_path = f"{pathOfUnresolved}\\1.jpg"  
        img = Image.open(image_path)
        img = img.resize((175, 175))  
        img = ImageTk.PhotoImage(img)
        label_img = ctk.CTkLabel(lower_frame, image=img, text = "")
        label_img.image = img
        label_img.bind("<Button-1>", lambda event, i=i: image_clicked(i))
        row_index = (i - 1) // num_columns
        col_index = (i - 1) % num_columns
        label_img.grid(row=row_index, column=col_index, padx= 10, pady= 10)


open_Report = ctk.CTkButton(master= frame,width=120,height=32,border_width=0,corner_radius=8,font = ("Arial", 24),text="Report",command = Report)
open_Report.pack(pady=12,padx=50) 

# Motto
label = ctk.CTkLabel(master = frame,text = "Cleaner environment for a safer future!",width=120,height=75,font = ("Arial", 20),fg_color=("white", "gray75"),corner_radius=8)
label.pack(pady=12,padx=50) 

app.mainloop()

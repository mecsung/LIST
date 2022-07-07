import time
import os.path
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk,Image,ImageSequence
from os import path
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ****************************  Load GUI  ************************************************
app_width = 600
app_height = 400

splash_root = Tk()
splash_root.title("LIST")
splash_root.iconbitmap("assets/favicon.ico")
screen_width = splash_root.winfo_screenwidth()
screen_height = splash_root.winfo_screenheight()
x = (screen_width / 2) - (app_width / 2)
y = (screen_height / 2) - (app_height / 2)

splash_root.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')
splash_root.overrideredirect(True)

img = Image.open("assets/Logo(2).gif")
lbl = Label(splash_root)
lbl.place(x=0, y=0, relwidth=1, relheight=1)
for img in ImageSequence.Iterator(img):
    img = img.resize((800, 600), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)
    lbl.config(image=img)

    splash_root.update()

# ****************************  Functions ************************************************
def main_window():
    splash_root.destroy()

    win = tk.Tk()
    win.title("LIST version 1.4")
    win.iconbitmap("assets/favicon.ico")
    win.configure(bg="#222")
    app_width = 400
    app_height = 530
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    x = (screen_width / 2) - (app_width / 2)
    y = (screen_height / 2) - (app_height / 2)

    win.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')
    win.resizable(False, False)
    # win.overrideredirect(True)

    # Title Bar
    title_bar = tk.Frame(win, bg="#222", relief="raised", bd=0)
    title_bar.pack(fill="x", expand=False)
    title = Label(title_bar, text="              Linkedin Scraping Tool",
        bg="#222", font=("Arial", 10), fg='#EEE')
    title.pack(side="left", pady=10)

    # Help button
    global question_img, logo, username, password, job, r, folder_img, my_dir
    my_dir = StringVar()

    q1_img = Image.open("assets/question.png")
    q2_img = q1_img.resize((20, 20), Image.ANTIALIAS)
    question_img = ImageTk.PhotoImage(q2_img)
    btn = Button(win, image=question_img, borderwidth=0, bg="#222", command=popup)
    btn.place(x=10, y=10)

    # Windows Title Logo
    logo01 = Image.open("assets/004.png")
    logo02 = logo01.resize((150, 150), Image.ANTIALIAS)
    logo = ImageTk.PhotoImage(logo02)
    logo_label = Label(win, image=logo, bg="#222")
    logo_label.pack()

    # Select Browser
    r = IntVar()
    r.set("2")
    Radiobutton(win, text="Google Chrome", variable=r, value=1, 
        bg="#222", fg="#EEE", selectcolor="#222").pack()
    Radiobutton(win, text="Microsoft Edge", variable=r, value=2, 
        bg="#222", fg="#EEE", selectcolor="#222").pack()

    # Select PATH folder for csv
    if not my_dir:
        path_label = tk.Label(win, text=my_dir, bg="#222", font=("Arial", 10), 
            fg='#EEE', anchor="w")
    else:  
        path_label = tk.Label(win, text="PATH", bg="#222", font=("Arial", 10), 
            fg='#EEE', anchor="w")
    path_label.pack(anchor="w", padx=57)

    def open_folder():
        dir_path=filedialog.askdirectory()
        path_label.config(text=dir_path)
        my_dir.set(dir_path)

    f1_img = Image.open("assets/folder.png")
    f2_img = f1_img.resize((20, 20), Image.ANTIALIAS)
    folder_img = ImageTk.PhotoImage(f2_img)
    folder_btn = Button(win, image=folder_img, borderwidth=0, bg="#222", command=open_folder)
    folder_btn.place(x=30, y=246)

    # Credentials
    panel = Label(win, text="Username", bg="#222", font=("Arial", 10), fg='#EEE', anchor="w").pack(anchor="w", padx=30)
    username = Text(win, height = 2, width = 38, font=("Arial", 12))
    username.insert(END, "")
    username.pack()

    panel = Label(win, text="Password", bg="#222", font=("Arial", 10), fg='#EEE').pack(anchor="w", padx=30)
    password = Text(win, height = 2, width = 38, font=("Arial", 12))
    password.insert(END, "")
    password.pack()

    # Serch Value
    panel = Label(win, text="Job skill search value", bg="#222", font=("Arial", 10), fg='#EEE').pack(anchor="w", padx=30)
    job = Text(win, height = 2, width = 38, font=("Arial", 12))
    job.pack()

    # Start button
    button_frame = tk.Frame(win, bg="#222")
    button_frame.pack(side="bottom", fill="x", expand=False, pady=10)
    entry_button = tk.Button(button_frame, height = 3, width = 25,
                          text = "START",cursor="mouse",
                          bg="#077aa8", fg="#EEE", bd=0,
                          command = start).pack()

def start():
    user_ = username.get("1.0", END)
    pass_ = password.get("1.0", END)
    job_ = job.get("1.0", END)
    r_ = str(r.get())
    dir_ = my_dir.get()

    print(user_, pass_, job_, r_, dir_)

    session_key = str(user_)
    session_password = str(pass_)

    SEARCH_URL = "https://www.linkedin.com/search/results/people/?keywords="+job_+"&origin=SWITCH_SEARCH_VERTICAL&position=0&searchId=90dbb355-3026-4485-8be3-ca08fc5ecbe4&sid=%3A%40Z"
    if (r_ == "1"):
        s = Service("chromedriver.exe")
        driver = webdriver.Chrome(service=s)
    else:
        s = Service("msedgedriver.exe")
        driver = webdriver.Edge(service=s)
    
    driver.get(SEARCH_URL)
    time.sleep(2)

    # Create CSV file
    FileExist = 1
    fname = dir_ + "\\linkedin.csv"
    if not path.exists(fname):
        FileExist = 0
    f = open(fname, "a", encoding="utf-8")

    if FileExist == 0:
        f.write("Name, Linkedin Link, Skills, Location")

    # Logging in to Linkedin
    driver.find_element(By.CLASS_NAME,value="main__sign-in-link").click()
    time.sleep(2)
    try:
        driver.find_element(By.NAME,value="session_key").send_keys(session_key)
        driver.find_element(By.NAME,value="session_password").send_keys(session_password)
        driver.find_element(By.CLASS_NAME,value="btn__primary--large").click()
        time.sleep(2)
        print("logged in successfully")
    except:
        print("")

    def Scrape():
        main = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "reusable-search__entity-result-list"))
        )
        talents = main.find_elements(By.TAG_NAME, 'li')
        for talent in talents:
            full_name = talent.find_element(By.CLASS_NAME, 'entity-result__title-text')
            full_name = str(full_name.text)
            name, sep, other = full_name.partition('\n')
            n, s, o = name.partition(',')
            # print(name)

            link = talent.find_element(By.TAG_NAME, 'a').get_attribute('href')
            # link = link.get_attribute('href')
            # print(link)

            skills = talent.find_element(By.CLASS_NAME, 'entity-result__primary-subtitle')
            location = talent.find_element(By.CLASS_NAME, 'entity-result__secondary-subtitle')
            
            f.write("\n" + n + "," + link + "," + skills.text + "," + location.text)

            info = [n, link, skills.text, location.text]
            print('\n*******************************************\n')
            print(info)
        return info
    
    try:
        for page in range(10):
            Scrape()
            time.sleep(2)
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
            time.sleep(2)
            next_button = driver.find_element(By.CLASS_NAME, 'artdeco-pagination__button--next')
            next_button.click()
            time.sleep(2)
    finally:
        driver.quit()

    messagebox.showinfo("LinkedIN Scraping Done!", 
        "Go to your selected folder to access the csv file.")

def popup():
    messagebox.showinfo("Help Wizard", """Need Help?\n\n
    This tool takes a search query, and returns a list of LinkedIn profiles with their names, skills and location in a CSV file format.\n

    How to use:\n

    1. Turn off your linkedin verifcation
    2. Choose your browser
    3. Select file destination folder
    4. Enter your LinkedIn email address and password
    5. Enter a job skill to be searched (e.g., Python Developer)
    6. Click start and wait for the program to generate a list\n

    The software is still under development, so you might encounter some issues when running the program.\n
    How to Troubleshoot:\n
    a. Check browser version
    b. Check login creadentials if there is typographical error
    c. Check if linkedin verification is on.

    \n\nDeveloped by: Legaspi | Carpio | San Juan | Recto | Go\n
    \t\t \u00A9 Copyright 2022""")


splash_root.after(1000, main_window)

mainloop()
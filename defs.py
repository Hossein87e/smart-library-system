import json
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import random
import re
import requests
from bs4 import BeautifulSoup
import os
#######################################################

def create_json_file():
    try:
        with open("users.json", "r") as myfile:
            pass  # اگر فایل وجود داشت کاری نکن
    except:
        with open("users.json", "w") as myfile:
            json.dump({}, myfile) # اگر فایل وجود نداشت آن را با یک دیکشنری خالی در فایل ذخیره کن

#######################################################

def show_log():
    try:
        with open("log.txt", "r", encoding="utf-8") as myfile: # با کردن فایل در حالت خواندن و با رمزگذاری utf-8 
            print("Log of user activity:") # چاپ عنوان برای بخش لاگ ها
            for logs in myfile:  # حلقه روی هر خط از فایل 
                print(logs.strip()) # چاپ هر خط پس حذف جای خالی ابتدا و انتها آنها 
    except FileNotFoundError: # اگر ارور -گفته شده نمایش داده شد
        print("No log file found.") # اینو بگو

#######################################################

def register():
    username = input("Choose a username: ")
    password = input("Choose a password: ")

    try:
        with open("users.json", "r") as myfile: # باز کردن نام کاربران در حالت خواندن 
            content = myfile.read().strip() # خواندن تمام محتوای فایل و حذف فاصله ها از اول تا اخر
            users = json.loads(content) if content else {} # اگر محتوا وجود داشت آن را از جیسان به دیکشنری تبدیل کن 
            #  در غیر اینصورت یک دیکشنری جدید ایجاد کن 
    except FileNotFoundError: # اگراین ارور را نمایش داد 
        users = {} # ایجاد یک دیکشنری خالی برای کاربران

    if username in users: # بررسی وجود نام کاربری در دیکشنری کاربران
        print(" Username already taken.") # چاپ پیام خطا اگر نام کاربر تکراری باشد
        return None # خروجی از تابع با مقدار none
    else: # اگر نام کاربری تکراری نبود 
        users[username] = password # افزودن کاربر جدید به دیکشنری با نام کاربری به عنوان کلید و رمز عبور به عنوان مقدار
        with open("users.json", "w") as myfile: # بازکردن فایل در حالت نوشتن 
            json.dump(users, myfile, indent=4) # ذخیره دیکشنری کاربران در فایل با فرمت جیسان و فاصله گذاری مناسب 
        log_entry(username, "register") # ثبت رویداد ثبت نام در فایل لاگ 
        print("✅ Registration successful.") # چاپ موفقیت آمیز بودن ثبت نام 
        return username  #برگرداندن نام کاربری ثبت شده 

#######################################################

def login():
    username = input("Username: ")
    password = input("Password: ")
    
    with open("users.json", "r") as myfile: # باز کردن فایل در حالت خواندن 
        users = json.load(myfile) # بارگزاریداده های فایل

    if username in users and users[username] == password:# اگر یوزر نیم داخل دیکشنری و پسوردی که در دیکشنری برای یوزر نیم ذخیره شدهبا مقدار پسور برابر است آنگاه.. 
        # بررسی دو شرط :
        # 1 - وجود نام کاربری در دریکشنری کاربران 
        # 2 - تطابق رمز عبور ورودی با رمز ذخیره شده
        print("Login successful.") # چاپ پیام موفقیت آمیز 
        return username # برگرداندن نام کاربری به عنوان خروجی تابع در صورت موفقیت
    else: # در غیر اینصورت 
        print("Login failed.") # چاپ پیام خطای ورود ناموفق
        return None # برگرداندن نان بهعنوان خروجی تابع در صورت عدم موفقیت

#######################################################

def log_entry(username, action): 
    # تعریف تابع با دو پارامتر :
    # 1 - یوزرنیم که عمل را انجام داده 
    # 2 - نوع عملیات انجام شده
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S") # دریافت زمان فعلی سیستم و فرمت دهی
    log_line = f"{time} - {username} - {action}\n" # ساخت رشته لاگ با فرمت زمان - نام کاربری - عمل 

    try:
        with open("log.txt", "a", encoding="utf-8") as myfile: # باز کردن فایل در حالت افزودن 
            myfile.write(log_line) #نوشتن خط لاگ در فایل 
    except: # گرفتن تمام خطاهای ممکن
        print("Could not write to log file.") # چاپ پیام خطا در صورت عدم موفقیت 

#######################################################

def get_best_selling_books(): 
    url = "https://en.wikipedia.org/wiki/List_of_best-selling_books" #صفحه وب حاوی لیست پرفروش ترین کتاب ها
    response = requests.get(url) # درخواست دریافت به آدرس بالا برای دریافت محتوای صفحه
    soup = BeautifulSoup(response.text, "html.parser") # تجزیه محتوای اچدیامال صفحه با استفاده از بیوتیفولسوپ

    table = soup.find("table", {"class": "wikitable"}) # یافتن جدول مورد نظر با کلاس ویکیتیبل در صفحه 

    books = [] # ایاد لیست خالی برای ذخیره اطلاعات کتاب ها 
    for row in table.find_all("tr")[1:]: # حلقه برروی تمام سطر های جدول به جزِ سطر اول که عنوان ستون هاست
        cols = row.find_all("td") # یافتن تمام سلول های هر سطر 
        if len(cols) >= 5: # بررسی اینکه سطر حداقل 5 ستون دارد برای اطمینان از ساختار صحیح
            title = cols[0].get_text(strip=True) # استخراج عنوان کتاب از ستون اول
            author = cols[1].get_text(strip=True) # استخراج نویسنده کتاب از ستون دوم 
            gener = cols[5].get_text(strip=True) # استخراج ژانر کتاب از ستون چهارم
            books.append({
                "name": title,
                "author": author,       # افزودن اطلاعات کتاب به لیست به صورت دیکشنری
                "genre": gener
            })

    return books # برگرداندن لیست کتاب های استخراج شده 

################################################

def add_book():
    scraped_books = get_best_selling_books() # دریافت لیست پرفروش ترین کتاب ها از سایت 
    print("\nTop Best-Selling Books:") # چاپ عنوان برای لیست کتاب ها 
    for i, book in enumerate(scraped_books[:10]):  # نمایش 10 کتاب اول با شماره گذاری (روی هر کتاب و شماره اش حلقه بزن)
        print(f"{i + 1}. {book['name']} by {book['author']}") #نمایش ده کتاب اول با شماره گذاری 

    choice = input("\nSelect a book to add by number (or press Enter to skip): ") # دریافت انتخاب کاربر 

    if choice.isdigit() and 1 <= int(choice) <= len(scraped_books[:10]): # بررسی معتبر بودن انتخاب کاربر
        selected = scraped_books[int(choice) - 1] # انتخاب کتاب از لیست بر اساس شماره وارد شده
        
        count = int(input("Enter quantity for this book: ")) 
        chapters = int(input("enter chapters : ")) 
        # دریافت تعداد موجودی و تعداد فصل های کتاب
        
        new_book = {
            "name": selected["name"],
            "author": selected["author"],
            "genre": selected["genre"], # ساخت شی کتاب جدید با جزییات کامل
            "count": count,
            "chapters" : chapters
        }
    else: # اگر کاربر انتخابی نکرد
        count = int(input("Quantity: ")) # تعداد کتاب
        chapters = int(input("enter chapters : ")) # تعداد فصل ها
        new_book = {
            "count": count,
            "chapters" : chapters
            
        }

    
    if os.path.exists("books.json"): # بررسی میکند که آیا این فایل در مسیر فعلی وجود دارد یا نه
        with open("books.json", "r") as myfile: # باز کردن فایل در حالت خواندن 
            content = myfile.read().strip() # محتوای کل فایل را به صورت یک رشته میخواند و فاصله ها را حذف میکند
            books = json.loads(content) if content else []   # اگر محتوا داشت تبدیلش کن به یک لیست 
    else: # اگر نداشت 
        books = [] # تبدیل کن به یک لیست

    books.append(new_book) # افزودن کتاب جدید به لیست 
    
    with open("books.json", "w") as myfile: 
        json.dump(books, myfile, indent=4) # ذخیرع لیست کتاب ها در فایل جیسان با فرمت زیبا

    df = pd.DataFrame(books)  #
    df = df.sort_values(by="name") # ایجاد و ذخیره فایل اکسل از لیست کتاب ها 
    df.to_excel("books.xlsx", index=False)#

    print("Book added successfully.") # چاپ پیام موفقیت

#######################################################

def delete_book():
    name = input("name of the book to delete :")
    try:
        with open("books.json" , "r")as myfile:
            books = json.load(myfile)
    except FileNotFoundError:
        return "no books have been registered"
            
    books = [book for book in books if book["name"].lower() != name.lower()]
    
    with open("books.json" , "w")as myfile:
        json.dump(books ,myfile,indent=4)
        print("the book got deleted .")
    
#######################################################

def draw_chart():
    try:
        with open("books.json" , "r")as myfile:
            books = json.load(myfile)
    except FileNotFoundError:
        return "books file not found"
    names = [book["name"] for book in books]
    counts = [book["count"] for book in books]
    
    plt.bar(names, counts, color="red")
    plt.xlabel("books")
    plt.ylabel("equity")
    plt.title("books equity chart")
    plt.xticks(rotation=45)
    plt.ylim(1, 500)
    plt.tight_layout()
    plt.show()
    
#######################################################

def show_user():
    try:
        with open("users.json", "r") as myfile:
            users = json.load(myfile)
    except FileNotFoundError:
        print(" No users have registered yet.")
        return

    if not users:
        return  " The user list is empty."

    print("Registered Users:")
    for username in users:
        print("-" + username)
        
#######################################################
        
def add_message_by_admin(message):
    try:
        with open("broadcast.json", "r") as myfile:
            data = json.load(myfile)
    except FileNotFoundError:
        data = []

    data.append({
        "message": message,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

    with open("broadcast.json", "w") as myfile:
        json.dump(data, myfile, indent=4)

    print("message sent")

#######################################################

def show_broadcast_messages():
    try:
        with open("broadcast.json", "r") as myfile:
            messages = json.load(myfile)
    except FileNotFoundError:
        return

    print("admins message :")
    for m in messages[-3:]:
        print(f"- {m['message']}  ({m['time']})")

#######################################################

def buy_book():
    books = list_book_sorted()
    if not books:
        return

    name = input("Enter book name to buy: ").strip().lower()

    for book in books:
        if book["name"].lower() == name:
            if book["count"] > 0:
                book["count"] -= 1
                print("Book purchased.")
            else:
                print("Out of stock.")
            break
    else:
        print("Book not found.")
        return
    
    with open("books.json", "w") as myfile:
        json.dump(books, myfile, indent=4)

    df = pd.DataFrame(books)
    df = df.sort_values(by="name")
    df.to_excel("books.xlsx", index=False)

#######################################################

def submit_ticket(username=None):
    if username is None:
        username = input("enter your username: ")
    message = input("write your message => ")
    try:
        with open("tickets.json", "r") as myfile:
            content = myfile.read().strip()
            tickets = json.loads(content) if content else {}
    except FileNotFoundError:
        tickets = {}

    if username not in tickets:
        tickets[username] = []

    tickets[username].append({
        "message": message,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

    with open("tickets.json", "w") as myfile:
        json.dump(tickets, myfile, indent=4)
    
    print("ticket sent to admin")

#######################################################

def delete_account():
    username = input("enter your username : ")
    password = input("enter your password : ")

    try:
        with open("users.json" , "r")as myfile:
            users = json.load(myfile)
    except FileNotFoundError:
        return "no user exist "
    if username in users and users[username] == password:
        users.pop(username)
        with open ("users.json" , "w") as myfile :
            json.dump(users,myfile,indent=4)
            print("account deleted successfully .")
    else:
        print("username or password incorrect .")
        
#######################################################

def suggest_book():
    try:
        with open("books.json", "r") as myfile:
            content = myfile.read().strip()
            if content:
                 books = json.loads(content)
            else:
                 books = []
    except FileNotFoundError:
        print("Book list not found.")
        return

    if not books:
        print("No books available to suggest.")
        return

    suggested = random.choice(books)
    print(f"Suggested book to read: \"{suggested['name']}\" by {suggested['author']}")

#######################################################

def show_books_with_multiple_chapters():
    with open("books.json", "r") as myfile:
        books = json.load(myfile)

    for book in books:
        chapters = book.get("chapters", "")
        matches = re.findall("chapter", chapters.lower())
        if len(matches) > 1:
            print(book["name"], "has", len(matches), "chapters")

######################################################

def filter_books_by_count():
    with open("books.json", "r") as myfile:
        books = json.load(myfile)

    min_count = int(input("Enter minimum quantity: "))

    for book in books:
        if book["count"] >= min_count:
            print(book["name"], "-", book["count"])

######################################################

def list_book_sorted():
    try:
        df = pd.read_excel("books.xlsx")
    except FileNotFoundError:
        print("books.xlsx not found .")
        return []
    
    df = df.sort_values(by="name")
    print("\navilable books :")
    for i, i1 in df.iterrows():
        print(f"{i1['name']} by {i1['author']}  -gener {i1['genre']} - quanity {i1['count']} - chapters {i1['chapters']}")
    return df.to_dict(orient="records")

#######################################################

def pin_book():
    name = input("Enter book name to pin: ")

    with open("books.json", "r") as myfile:
        books = json.load(myfile)

    for book in books:
        if book["name"].lower() == name.lower():
            book["pinned"] = True

    with open("books.json", "w") as myfile:
        json.dump(books, myfile, indent=4)

    print("Book pinned.")

########################################################

def save_books_to_excel():
    with open("books.json", "r") as myfile:
        books = json.load(myfile)

    df = pd.DataFrame(books)
    df.to_excel("books.xlsx", index=False)
    print("Saved to books.xlsx")

###########################################################

def show_all_tickets():
    if not os.path.exists("tickets.json"):
        print("No tickets found.")
        return

    with open("tickets.json", "r") as myfile:
        content = myfile.read().strip()
        tickets = json.loads(content) if content else {}

    if not tickets:
        print("No tickets to display.")
        return

    print("\n--- All User Tickets ---")
    for username, msgs in tickets.items():
        print(f"\nUser: {username}")
        for msg in msgs:
            print(f"  - {msg['message']}  ({msg['time']})")
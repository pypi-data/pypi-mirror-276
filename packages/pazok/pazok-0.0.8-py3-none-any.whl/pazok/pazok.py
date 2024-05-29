import os
try:
    import requests
    import argparse
    import json
    import locale
    import threading
    import re
    import shlex
    import random
    from collections import OrderedDict
    from urllib.parse import unquote, urlparse
    import pyperclip
    from rich.console import Console
    from rich.syntax import Syntax
    from PIL import Image
    from fake_useragent import UserAgent
    from colorama import init, Fore, Back, Style
    from asciimatics.renderers import ImageFile
except:
    os.system("pip install argparse")
    os.system("pip install json")
    os.system("pip install locale")
    os.system("pip install re")
    os.system("pip install shlex")
    os.system("pip install collections")
    os.system("pip install urllib")
    os.system("pip install pyperclip")
    os.system("pip install rich")
    os.system("pip install Pillow")
    os.system("pip install OneClick")
    os.system("pip install fake-useragent")
    os.system("pip install halo")
    os.system("pip install python-cfonts")
    os.system("pip install pyTelegramBotAPI")
    os.system("pip install colorama")
    os.system("pip install requests")
    os.system("pip install threading")
    os.system("pip install random")
    os.system("pip install time")
    os.system("pip install asciimatics")

#- - - - - - - - - - - - - - -- - - - - - -- - - - - #
#لوكو
def logo():
    o = "\u001b[38;5;208m"  # برتقالي
    e = "\u001b[38;5;242m"  # رمادي داكن
    logo=f"""
\033[1;97m        
\u001b[38;5;242m
    
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣤⣤⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣶⣦⣤⣤⣀⡀⠀⠀⠀⠀⠀        
            ⠀⠀⠀⠀⠀⠀⣠⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣄⡀⠀        
            ⠀⠀⠀⠀⣠⣾⣿⡿⠟⠛⠉⠁⠀⠀⡀⠀⠀⢀⡈⠉⠛⠻⠿⣿⣿⣿⣦⣉⣽⣿⣿⣿⣿⣿⣿⣆        
            ⠀⠀⠀⣼⣿⠟⠁⢀⣠⠔⢀⣴⡾⠋⣠⣾⣿⣿⣿⣿⣿⣶⣄⠀⠙⠛⠿⠿⠿⠟⠛⠛⢿⣿⣿⠛        
            ⠀⠀⣼⡟⠁⢀⣴⣿⠃⢰⣿⣿⡇⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⣄⣀⣀⣀⠀⠀⢀⡾⡿⠏⠀        
            ⠀⠀⡿⠀⣰⣿⣿⡏⠀⢸⣿⣿⣇⠀⠹⣿⣿⣿⣿⣿⣿⣿⡏⢿⣿⣏⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀        
            ⠀⢸⠃⢰⣿⣿⣿⣿⡀⠘⢿⣿⣿⣧⣀⠀⠙⠿⣿⣿⣿⣿⡇⠈⢻⣿⣇⢀⣄⡄⠀⠀⠀⠀⠀⠀        
            ⠀⠈⠀⢸⣿⣿⣿⣿⣷⣄⠈⠻⢿⣿⣿⣷⣦⣀⠈⠙⢿⣿⣿⡄⠀⠙⠻⠿⠿⠁⠀⠀⠀⠀⠀⠀        
            ⠀⠀⠀⠀⢻⣿⣿⣿⣿⣿⣷⣄⠀⠙⠻⢿⣿⣿⣿⣦⡀⠹⣿⣿⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀            
            ⠀⠀⠀⠀⠈⠻⣿⣿⣿⣿⣿⣿⣿⣦⣄⠀⠙⠻⣿⣿⣿⢀⣿⣿⣿⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀        
            ⠀⠀⠀⠀⠀⠀⠈⠻⣿⣿⣿⣿⣿⣿⣿⣿⣶⣄⠀⠙⣿⣾⣿⣿⣿⡿⣧⡀⠀⠀⠀⠀⠀⠀⠀⠀        
            ⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣦⠈⢿⣿⣿⣿⣿⣦⣄⠀⠀⠀⠀⠀⠀⠀⠀        
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠛⠿⣿⣿⣿⣿⣿⣿⣷⠘⣿⣿⣿⣿⡿⣿⣇⠀⠀⠀⠀⠀⠀⠀            
            ⠀⠀⠀⠀⠀⠀⠀ ⠀ ⠀⠀⠀{o}⣶⣶{e}⠀⠈⠙⠿⣿⣿⣿⡿⣸⣿⣿⣿⣿⣿⣶⣍⡀⠀⠀⠀⠀⠀⠀        
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀  {o}⣶⣿⣿⣶{e}⠀⠀⠀⠈⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⢿⡇⠀⠀⠀⠀⠀⠀        
            ⠀⠀⠀⣀⣀⠀⠀⢀⣀⡀⠉⣉⣉⠉⣀⣀⠀⠀⠀⠀⠙⢿⣿⣿⣿⣿⣿⣿⣷⣦⠀⠀⠀⠀⠀⠀        
            ⠀⠀⠀⣿⣿⠀⠀⢸⣿⡇⠐⣿⣿⠀⣿⣿⠀⠀⠀⠀⠀⠀⠻⣿⣿⣿⣿⣿⣝⠏⠀⠀⠀⠀⠀⠀        
            ⠀⠀⠀⣿⣿⣶⣶⣾⣿⣷⣾⣿⣿⣶⣿⣿⠀⠀⠀⠀⠀⢠⠀⢻⣿⣿⣿⡿⣿⠇⠀⠀⠀⠀⠀⠀        
            ⠀⢀⣀⣿⣿⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠀⠀⠀⠀⢀⣿⡇⢸⣿⣿⣿⣷⠌⠀⠀⠀⠀⠀⠀⠀        
            ⢠⣿⣿⣿⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣿⣿⡇⢸⣿⣿⡯⠁⠀⠀⠀⠀⠀⠀⠀⠀        
            ⠀⠀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣿⣿⣿⣿⢁⣿⡿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀        
            ⠀⠀⠀⠙⠲⣤⣤⣀⣀⣀⣀⣀⣠⣤⣴⣾⣿⣿⣿⣿⣿⠃⠚⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀        
            ⠀⠀⠀⠀⠀⠀⠈⠙⠛⠛⠿⠿⠿⠿⠿⠿⠟⠛⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀        
              
"""
    
    text2 = 50 * "_"
    terminal_size = os.get_terminal_size()
    max_width = terminal_size.columns - 1
    padding_width2 = (max_width - len(text2)) // 2
    centered_text2 = " " * padding_width2 + text2 + " " * padding_width2
    
    init(autoreset=True)
    custom_color = "\u001b[38;5;208m"
    
    def center_text(text):
        terminal_width = os.get_terminal_size().columns
        padding = (terminal_width - len(text)) // 2
        print(" " * padding, end='')
        for char in text:
            print(custom_color + Back.BLACK + Style.BRIGHT + char, end='', flush=True)
            time.sleep(0.02)

    print(logo)
    center_text("↝ Tele: b_azok | Insta: b_azok | tik: zquy ↜ ")
    print()
    print("\u001b[38;5;242m" + centered_text2)
    print("\u001b[38;5;15m")
    print(e)



#- - - - - - - - - - - - - - -- - - - - - -- - - - - #



#مهم
def love():
    print("- I love Mariam")





#- - - - - - - - - - - - - - -- - - - - - -- - - - - #

#دالة تلاشي النص
def tl(text=None, timg=None, center=None):
    if timg is None or center is None or text is None:
        raise ValueError("الرجاء تقديم نص ووقت وقيمة منطقية (True/False)")
    def b_azok_print(text):
        i = 232
        while i <= 255:
            b = f"\u001b[38;5;{i}m"
            p = '\x1b[1m'
            terminal_size = os.get_terminal_size()
            max_width = terminal_size.columns - 1
            if center:
                padding_width = (max_width - len(text)) // 2
                centered_text = " " * padding_width + text + " " * padding_width
            else:
                centered_text = text
            print(p + b + centered_text, end='\r')
            time.sleep(timg)
            i += 1
    b_azok_print(text)



#pazok.tl("hello",0.02,True)

#- - - - - - - - - - - - - - -- - - - - - -- - - - - #
#انشاء يوزرات

def user_ran(pattern=None):
    pattern = str(pattern)  
    username = ''
    last_pazoo_2 = ''
    
    for char in pattern:
        if char == '1':
            random_char = random.choice('abcdefghijklmnopqrstuvwxyz0123456789')
            username += random_char
        elif char == '2':
            if not last_pazoo_2:
                last_pazoo_2 = random.choice('abcdefghijklmnopqrstuvwxyz0123456789')
            username += last_pazoo_2
        elif char == '3':
            b_az_rand = random.choice(['.', '_'])
            username += b_az_rand
        elif char == '4':
            random_digit = random.choice('0123456789')
            username += random_digit
        else:
            username += char
    return username.strip()

    
    
#jj=pazok.user_ran("111_1")
#print(jj)
                                
                                
#- - - - - - - - - - - - - - - - - - - - -- - - - - #

# دالة الخيوط
        
def run_program():
    pass

def sb(func, num_threads):
    if not func or not num_threads:
        raise ValueError("يرجى تمرير قيم لكل من اسم الداله وعدد الخيوط")
        
    num_threads = int(num_threads)
    threads = []
    for _ in range(num_threads):
        t = threading.Thread(target=func)
        threads.append(t)
    for t in threads:
        t.start()
    for t in threads:
        t.join()


#def txt():
    

#pazok.sb(اسم الداله, عدد الخيوط)


#- - - - - - - - - - - - - - -- - - - - - -- - - - - #

#ارسال تلي حديث

def tele_ms(token, id, txt=None, file=None, img=None, buttons=None):
    if not token or not id or txt is None:
        raise ValueError("يرجى اضافة توكن وايدي ونص على الاقل")
    
    import telebot
    from telebot import types
    import requests
    import os

    bot = telebot.TeleBot(token)
    keyboard = types.InlineKeyboardMarkup()
    if buttons:
        for i in range(0, len(buttons), 2):
            button_name = buttons[i]
            button_url = buttons[i + 1]
            button = types.InlineKeyboardButton(button_name, url=button_url)
            keyboard.add(button)

    def download_file_from_url(url):
        file_name = url.split('/')[-1]
        response = requests.get(url)
        with open(file_name, 'wb') as f:
            f.write(response.content)
        return file_name

    if file or img:
        if img:
            if img.startswith('http'):
                bot.send_photo(id, photo=img, caption=txt, parse_mode='Markdown', reply_markup=keyboard)
            else:
                bot.send_photo(id, open(img, 'rb'), caption=txt, parse_mode='MarkdownV2', reply_markup=keyboard)
        
        if file:
            if file.startswith('http'):
                file_path = download_file_from_url(file)
                bot.send_document(id, open(file_path, 'rb'), caption=txt, parse_mode='MarkdownV2', reply_markup=keyboard)
                os.remove(file_path)
            else:
                bot.send_document(id, open(file, 'rb'), caption=txt, parse_mode='MarkdownV2', reply_markup=keyboard)

    elif txt:
        bot.send_message(id, txt, parse_mode='MarkdownV2', reply_markup=keyboard)



#توكن
#token=""
#ايدي
#id=""

#يستقبل جميع تنسيقات النص
#msg="hello"

#يستقبل رابط او مسار للملف
#fil=""

#يستقبل رابط او مسار للصوره
#imgs=""

#ازرار يستقبل مفرد وقائمة ازرار
#buttons="name button","URL button"

#لا تستقبل ارسال صوره وملف بنفس الوقت
#pazok.tele_ms(token,id,txt=msg,img=imgs,buttons=button)


#- - - - - - - - - - - - - - -- - - - - - -- - - - - #
#دالة طلب توكن وايدي مره وحده

def info_bot():
    try:
        import time, os
        from colorama import init, Fore, Back, Style
        from cfonts import render
    except ImportError:
        os.system('pip install colorama')
        os.system('pip install cfonts')

    b = "\u001b[38;5;14m"  # سمائي
    m = "\u001b[38;5;15m"  # ابيض
    F = '\033[2;32m'  # أخضر
    Z = '\033[1;31m'  # أحمر
    ee = "\033[0;90m"  # رمادي الداكن
    C = "\033[1;97m"  # أبيض
    p = '\x1b[1m'  # عريض
    X = '\033[1;33m'  # أصفر
    B = '\033[2;36m'  # أزرق
    E = "\u001b[38;5;8m"  # رمادي فاتح
    o = "\u001b[38;5;208m"  # برتقالي
    p = '\x1b[1m'  # عريض

    sev_amg=f"""
        
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⣿⣿⣿⣿⣿⣿⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣤⣤⣤⣤⣤⣼⣿⣿⣿⣿⣿⣿⣿⣧⣤⣤⣤⣤⣤⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠛⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠛⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣿⣿⣿⣿⣿⣿⣿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⢸⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⣿⣿⣿⡿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⡇⠀
        ⠀⢸⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⡇⠀
        ⠀⢸⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⡇⠀
        ⠀⢸⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⡇⠀
        ⠀⢸⣿⣿⣿⣿⣿⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣿⣿⣿⣿⣿⡇⠀
        ⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀
        ⠀⠀⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠁⠀
        
         
{E}             𝗜𝗙 𝗬𝗢𝗨 𝗧𝗬𝗣𝗘 𝗬, 𝗜𝗡𝗙𝗢 𝗦𝗔𝗩𝗘𝗗 𝗙𝗢𝗥 𝗡𝗘𝗫𝗧 𝗧𝗜𝗠𝗘

"""
    
    try:
        with open('.bot_info.txt', 'r') as file:
            lines = file.readlines()
            token = lines[0].strip()
            id = lines[1].strip()
    except FileNotFoundError:
        b_azokatext = """
\u001b[38;5;15m        
         ______   ___   __  _    ___  ____  
        |      | /   \ |  |/ ]  /  _]|    \ 
        |      ||     ||  ' /  /  [_ |  _  |
        |_|  |_||  O  ||    \ |    _]|  |  |
          |  |  |     ||     \|   [_ |  |  |
          |  |  |     ||  .  ||     ||  |  |
          |__|   \___/ |__|\_||_____||__|__|
          
                                                            
        """
        print(b_azokatext)
        token = input(f" - {b}Enter Token : {ee}")
        os.system('clear')

        
        b_azokatext ="""
\u001b[38;5;15m        
           _____ _           _     _____ _____  
          / ____| |         | |   |_   _|  __ \ 
         | |    | |__   __ _| |_    | | | |  | |
         | |    | '_ \ / _` | __|   | | | |  | |
         | |____| | | | (_| | |_   _| |_| |__| |
          \_____|_| |_|\__,_|\__| |_____|_____/ 
                                                
                                                
        
        """
        print(b_azokatext)
        id = input(f" - {b}Enter ID : {ee}")
        os.system('clear')

        print(sev_amg)
        save_data = input(f"{ee}-{o} 𝗗𝗢 𝗬𝗢𝗨 𝗪𝗜𝗦𝗛 𝗧𝗢 𝗦𝗔𝗩𝗘 𝗥𝗘𝗚𝗜𝗦𝗧𝗥𝗔𝗧𝗜𝗢𝗡 𝗜𝗡𝗙𝗢   {E} ({F}Y{ee}/{Z}N{E}){o}:{ee} ")
        if save_data.upper() == "Y":
            os.system('clear')
            with open('.bot_info.txt', 'w') as file:
                file.write(f"{token}\n{id}")
        elif save_data.upper() == "N":
            os.system('clear')
            pass
        else:
            exit(f"{Z}Invalid input. Please enter 'Y' or 'N'.")

    return token, id



#token, id = pazok.info_bot()


#حذف بيانات بوت
def info_bot_dlet():
    start_path = '/storage/emulated/0'
    for dirpath, dirnames, filenames in os.walk(start_path):
        if '.bot_info.txt' in filenames:
            file_path = os.path.join(dirpath, '.bot_info.txt')
            os.remove(file_path)
            
#pazok.info_bot_dlet()



#- - - - - - - - - - - - - - -- - - - - - -- - - - - #

#الطباعه مع اشكال مكتبة rich

import time
from rich.console import Console

def pazok_rich(text, spinner, duration):
    console = Console()
    spinner_instance = console.status(text, spinner=spinner)
    spinner_instance.start()
    time.sleep(duration)
    spinner_instance.stop()

#pazok.pazok_rich("النص المطلوب", "النمط", الوقت)


#اسماء الانماط
def name_rich():
    rich_list = [
        "arrow",
        "christmas",
        "circle",
        "clock",
        "hearts",
        "moon",
        "pong",
        "runner",
        "star",
        "weather"
    ]

    for index, pattern in enumerate(rich_list, start=1):
        print(f"{index}. {pattern}")
        
#print(pazok.name_rich())

#- - - - - - - - - - - - - - -- - - - - - -- - - - - #

#الطباعه مع اشكال مكتبة halo

from halo import Halo
import time


def pazok_halo(text, spinner, duration):
    spinner_instance = Halo(text=text, spinner=spinner)
    spinner_instance.start()
    time.sleep(duration)
    spinner_instance.stop_and_persist(symbol='', text='')
    print(' ' * len(text), end='\r')
    return None

#pazok.pazok_halo("النص المطلوب", "النمط", الوقت)


#اسماء الانماط
def name_halo():
    halo_list = [
        "dots",
        "dots2",
        "dots3",
        "dots4",
        "dots5",
        "dots6",
        "dots7",
        "dots8",
        "dots9",
        "dots10",
        "dots11",
        "dots12",
        "line",
        "line2",
        "pipe",
        "simpleDots",
        "simpleDotsScrolling",
        "star",
        "star2",
        "flip",
        "hamburger",
        "growVertical",
        "growHorizontal",
        "balloon",
        "balloon2",
        "noise",
        "bounce",
        "boxBounce",
        "boxBounce2",
        "triangle",
        "arc",
        "circle",
        "square",
        "circleQuarters",
        "circleHalves",
        "squish",
        "toggle",
        "toggle2",
        "toggle3",
        "toggle4",
        "toggle5",
        "toggle6",
        "toggle7",
        "toggle8",
        "toggle9",
        "toggle10",
        "toggle11",
        "toggle12",
        "toggle13",
        "arrow",
        "arrow2",
        "arrow3",
        "bouncingBar",
        "bouncingBall",
        "smiley",
        "monkey",
        "hearts",
        "clock",
        "earth",
        "moon",
        "runner",
        "pong",
        "shark",
        "dqpb"
    ]

    for index, pattern in enumerate(halo_list, start=1):
        print(f"{index}. {pattern}")

#print(pazok.name_halo())


#- - - - - - - - - - - - - - -- - - - - - -- - - - - #

#تخويل الصور الى نقاط

def picture(image_path, height=None, style=None):
    
    from PIL import Image, ImageOps
    from picharsso import new_drawer
    from asciimatics.renderers import ImageFile
    import io
    
    try:
        image = Image.open(image_path)
        if image.mode != "RGB":
            image = image.convert("RGB")
        inverted_image = ImageOps.invert(image)
        
        if style == 1:
            drawer = new_drawer("braille", height=height)
            return drawer(inverted_image)
        
        elif style == 2:
            with io.BytesIO() as output:
                inverted_image.save(output, format="PNG")
                output.seek(0)
                renderer = ImageFile(output, height=height)
                ascii_art = str(renderer)
            return ascii_art    
        else:
            raise ValueError("النمط غير مدعوم. يرجى اختيار 1 أو 2.")   
    except FileNotFoundError:
        print("المسار غير صحيح:", image_path)
    except Exception as e:
        print("حدث خطأ:", e)


#x="/storage/emulated/0/DCIM/100PINT/المنشورات/dbb76dbc7436ebe6defa7cd206103780.jpg"
#z=30

#jj=pazok.picture(x,z)
#print(jj)


#- - - - - - - - - - - - - - -- - - - - - -- - - - - #
#التحديث:

#يوزر ايجنت

def agnt():
    from fake_useragent import UserAgent
    ua = UserAgent()
    return str(ua.chrome)

#pazok.agnt()

#يوزر ايجنت انستا
def agnt_in():
    from OneClick import Hunter
    agent = Hunter.Services()
    return str(agent)


#- - - - - - - - - - - - - - -- - - - - - -- - - - - #

#اللوان
colors = ['o', 'b', 'm', 'F', 'Z', 'e', 'C', 'p', 'X', 'j', 'E']
o = "\u001b[38;5;208m" 
b = "\u001b[38;5;14m"
m = "\u001b[38;5;15m"
F = '\033[2;32m'
Z = '\033[1;31m'
e = "\033[0;90m"
C = "\033[1;97m"
p = '\x1b[1m'
X = '\033[1;33m'
j= "\u001b[38;5;200m" 
E = "\u001b[38;5;8m"
__all__ = colors

#طباعة اسماء الاللوان
def name_clo():
    colors_text = """
    
o = برتقالي
b = أزرق
m = أبيض
F = أخضر غامق
Z = أحمر فاتح
e = رمادي غامق
C = أبيض قوي
p = خط عريض
X = أصفر
j = وردي
E = رمادي فاتح

"""
    return colors_text





#- - - - - - - - - - - - - - -- - - - - - -- - - - - #
#سليب
def sleep(seconds=None):
    import random
    if seconds is None:
        seconds = random.uniform(0.5, 1)
    time.sleep(seconds)
    return seconds

#pazok.sleep()


#- - - - - - - - - - - - - - -- - - - - - -- - - - - #
#يوزرات من ملف


def user_file(file_name, tr_fa_paz):
    if not file_name:
        raise ValueError("يرجى تمرير اسم الملف أو مساره")
    
    file_path = os.path.join(os.getcwd(), file_name)
    try:
        if os.path.getsize(file_path) == 0:
            print("Error: The text file is empty")
            return None
                
        with open(file_path, 'r+') as file:
            data = file.readlines()
            if not data:
                print("Error: The text file is empty")
                return None

            first_line = data[0].strip()
            username = first_line.split("@")[0] if "@" in first_line else first_line

            if tr_fa_paz:
                data = data[1:]
            else:
                data = data[1:]
                data.append(first_line + '\n')
            data = [line for line in data if line.strip()]

            file.seek(0)
            file.writelines(data)
            file.truncate()
            
            return username
    except FileNotFoundError:
        print("File not found error")
        return None
    except Exception as e:
        print("حدث خطأ: ", e)
        return None
        

#pazok.user_file('bazok.txt', True)



#- - - - - - - - - - - - - - -- - - - - - -- - - - - #
#طباعة عدد سطور اللسته
def file_np(file_path):
    if not file_path:
        raise ValueError("يرجى تمرير اسم الملف او مساره")
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            return len(lines)
    except FileNotFoundError:
        print("الملف غير موجود")
        return 0

#print(pazok.file_np("user.py"))



#- - - - - - - - - - - - - - -- - - - - - -- - - - - #
#كوكيز انستا
class InstagramSession:    
    def __init__(self, csrftoken, ds_user_id, rur, sessionid):
        self.csrftoken = csrftoken
        self.ds_user_id = ds_user_id
        self.rur = rur
        self.sessionid = sessionid

def log_in(username, password):
    if not username or not password:
        raise ValueError("يرجى تمرير قيم لاسم المستخدم وكلمة المرور")
        
    import requests
    from fake_useragent import UserAgent

    ua = UserAgent()
    agnt = str(ua.getChrome)

    url = 'https://www.instagram.com/accounts/login/ajax/'

    headers = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'ar,en-US;q=0.9,en;q=0.8',
        'content-length': '275',
        'content-type': 'application/x-www-form-urlencoded',
        'cookie': 'csrftoken=DqBQgbH1p7xEAaettRA0nmApvVJTi1mR; ig_did=C3F0FA00-E82D-41C4-99E9-19345C41EEF2; mid=X8DW0gALAAEmlgpqxmIc4sSTEXE3; ig_nrcb=1',
        'origin': 'https://www.instagram.com',
        'referer': 'https://www.instagram.com/',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': agnt,
        'x-csrftoken': 'DqBQgbH1p7xEAaettRA0nmApvVJTi1mR',
        'x-ig-app-id': '936619743392459',
        'x-ig-www-claim': '0',
        'x-instagram-ajax': 'bc3d5af829ea',
        'x-requested-with': 'XMLHttpRequest'
    }

    data = {
        'username': username,
        'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:1589682409:{password}',
        'queryParams': '{}',
        'optIntoOneTap': 'false'
    }

    response = requests.post(url, headers=headers, data=data)
    cookies = None
    if response.status_code == 200:
        cookies = response.cookies.get_dict()
        csrftoken = cookies.get("csrftoken")
        ds_user_id = cookies.get("ds_user_id")
        rur = cookies.get("rur")
        sessionid = cookies.get("sessionid")
        return InstagramSession(csrftoken, ds_user_id, rur, sessionid)
    else:
        return None

#username = "jdjdjuuuudjjdk"
#password = "mmkkoopp"

#jj=pazok.log_in(username, password)
#print(jj.sessionid)
#print(jj.csrftoken)
#print(jj.rur)
#print(jj.ds_user_id)

#- - - - - - - - - - - - - - -- - - - - - -- - - - - #
#تحويل الاستجابه الى جيسون

import json
def json_req(response):
    if not response:
        raise ValueError("يرجى تمرير اسم المتغير الذي يحمل قيمة الاستجابه")
    try:
        json_response = response.json()
    except AttributeError:
        json_response = json.loads(response)
    return json.dumps(json_response, indent=4)

#print(pazok.json_req(rr))

#- - - - - - - - - - - - - - -- - - - - - -- - - - - #
#تحويل امرcURL الى طلب

import argparse
import json
import locale
import re
import shlex
from collections import OrderedDict
from urllib.parse import unquote, urlparse
import pyperclip
from rich.console import Console
from rich.syntax import Syntax


def prettier_print(code: str):
    from os import get_terminal_size
    syntax = Syntax(code, "python", theme="monokai", line_numbers=True)
    console = Console()
    console_width = int((get_terminal_size()[0] - 36) / 2)
    console.print("=" * console_width +
                  "[bold magenta] Python Requests Code Preview Start [/]" +
                  "=" * console_width,
                  justify='center')
    console.print(syntax)
    console.print("=" * console_width +
                  "[bold magenta]  Python Requests Code Preview End  [/]" +
                  "=" * console_width,
                  justify='center')


def parse_content_type(content_type: str):
    parts = content_type.split(';', 1)
    tuparts = parts[0].split('/', 1)
    if len(tuparts) != 2:
        return None
    dparts = OrderedDict()
    if len(parts) == 2:
        for i in parts[1].split(";"):
            c = i.split("=", 1)
            if len(c) == 2:
                dparts[c[0].strip()] = c[1].strip()
    return tuparts[0].lower(), tuparts[1].lower(), dparts


def format_multi(the_multi_list, indent=4):
    return 'MultipartEncoder(\n' + " " * indent + 'fields=[\n' + " " * indent * 2 + (
        ",\n" + " " * indent * 2).join(map(str, the_multi_list)) + '\n])'


def parse_multi(content_type, the_data):
    boundary = b''
    if content_type:
        ct = parse_content_type(content_type)
        if not ct:
            return [('no content-type')]
        try:
            boundary = ct[2]["boundary"].encode("ascii")
        except (KeyError, UnicodeError):
            return [('no boundary')]
    if boundary:
        result = []
        for i in the_data.split(b"--" + boundary):
            p = i.replace(b'\\x0d', b'\r')
            p = p.replace(b'\\x0a', b'\n')
            p = p.replace(b'\\n', b'\n')
            p = p.replace(b'\\r', b'\r')
            parts = p.splitlines()
            # print(parts)
            if len(parts) > 1 and parts[0][0:2] != b"--":
                if len(parts) > 4:
                    tmp_value = {}
                    key, tmp_value['filename'] = re.findall(
                        br'\bname="([^"]+)"[^"]*filename="([^"]*)"',
                        parts[1])[0]
                    tmp_value['content'] = b"".join(
                        parts[3 + parts[2:].index(b""):])
                    tmp_value['content_type'] = parts[2]
                    value = (tmp_value['filename'].decode(),
                             tmp_value['content'].decode(),
                             tmp_value['content_type'].decode())
                else:
                    key = re.findall(br'\bname="([^"]+)"', parts[1])[0]
                    value = (b"".join(parts[3 +
                                            parts[2:].index(b""):])).decode()
                result.append((key.decode(), value))
        return result


def parse_args(curl_cmd):
    parser = argparse.ArgumentParser()
    parser.add_argument('command')
    parser.add_argument('url')
    parser.add_argument('-d', '--data')
    parser.add_argument('-b', '--cookie', default=None)
    parser.add_argument('--data-binary',
                        '--data-raw',
                        '--data-ascii',
                        default=None)
    parser.add_argument('-X', default='')
    parser.add_argument('-F', '--form', default=None)
    parser.add_argument('-H', '--header', action='append', default=[])
    parser.add_argument('-A', '--user-agent', default='')
    parser.add_argument('--compressed', action='store_true')
    parser.add_argument('-k', '--insecure', action='store_true')
    parser.add_argument('-I', '--head', action='store_true')
    parser.add_argument('-G', '--get', action='store_true')
    parser.add_argument('--user', '-u', default=())
    parser.add_argument('-i', '--include', action='store_true')
    parser.add_argument('-s', '--silent', action='store_true')
    cmd_set = shlex.split(curl_cmd)
    arguments = parser.parse_args(cmd_set)
    return arguments


def prettier_dict(the_dict, indent=4):
    if not the_dict:
        return "{}"
    return ("\n" + " " * indent).join(
        json.dumps(the_dict,
                   ensure_ascii=False,
                   sort_keys=True,
                   indent=indent,
                   separators=(',', ': ')).splitlines())


def prettier_tuple(the_tuple, indent=4):
    if not the_tuple:
        return "()"
    return '(\n' + " " * indent + ("," + "\n" + " " * indent).join(
        str(i) for i in the_tuple) + ',\n)'


def quotestr(x):
    return f"'{x}'"


def prettier_dict_string(the_dict, indent=4):
    if not the_dict:
        return "{}"
    return '{\n' + " " * indent + ("," + "\n" + " " * indent).join(
        f"{quotestr(x) if isinstance(x,str) else str(x)}:{quotestr(y) if isinstance(y,str) else str(y)}"
        for x, y in the_dict.items()) + ',\n}'


def curl_replace(curl_cmd):
    curl_replace = [(r'\\\r|\\\n|\r|\n', ''), (' -XPOST', ' -X POST'),
                    (' -XGET', ' -X GET'), (' -XPUT', ' -X PUT'),
                    (' -XPATCH', ' -X PATCH'), (' -XDELETE', ' -X DELETE'),
                    (' -Xnull', ''), (' \$', ' ')]
    tmp_curl_cmd = curl_cmd
    for pattern in curl_replace:
        tmp_curl_cmd = re.sub(pattern[0], pattern[1], tmp_curl_cmd)
    return tmp_curl_cmd.strip()


class parseCurlCommand:
    def __init__(self, curl_cmd):
        self.curl_cmd = curl_replace(curl_cmd)
        self.arguments = parse_args(self.curl_cmd)
        self.method = 'get'
        post_data = self.arguments.data or self.arguments.data_binary
        self.urlparse = urlparse(self.arguments.url)
        self.url = "{}://{}{}".format(self.urlparse.scheme,
                                      self.urlparse.netloc, self.urlparse.path)
        self.cookies = None
        if self.urlparse.query:
            self.params = tuple(
                re.findall(r'([^=&]*)=([^&]*)', unquote(self.urlparse.query)))
        else:
            self.params = ()
        headers = self.arguments.header
        cookie_string = ''
        content_type = ''
        if headers:
            self.headers = dict(
                [tuple(header.split(': ', 1)) for header in headers])
            cookie_string = self.headers.get('cookie') or self.headers.get(
                'Cookie')
            if 'cookie' in self.headers:
                self.headers.pop('cookie')
            if 'Cookie' in self.headers:
                self.headers.pop('Cookie')
            self.content_type = self.headers.get(
                'Content-Type') or self.headers.get(
                    'content-type') or self.headers.get('Content-type')
        else:
            self.headers = {}
        if self.arguments.cookie:
            cookie_string = self.arguments.cookie
        if post_data and not self.arguments.get:
            self.method = 'post'
            if "multipart/form-data" in self.content_type.lower():
                self.data = parse_multi(
                    self.content_type,
                    unquote(post_data.strip('$')).encode('raw_unicode_escape'))
            elif "application/json" in self.content_type.lower():
                self.data = json.loads(post_data)
            else:
                self.data = dict(
                    re.findall(r'([^=&]*)=([^&]*)', unquote(post_data)))
        elif post_data:
            self.params = tuple(
                re.findall(r'([^=&]*)=([^&]*)', unquote(post_data)))
            self.data = {}
        else:
            self.data = {}
        if self.arguments.X:
            self.method = self.arguments.X.lower()
        if cookie_string:
            self.cookies = {}
            for cookie in re.findall(r'([^=\s;]*)=([^;]*)', cookie_string):
                if cookie[0] not in self.cookies:
                    self.cookies[cookie[0]] = cookie[1]
        if self.arguments.insecure:
            self.insecure = True
        else:
            self.insecure = False

def cURL(filestring, b_azok_path=''):
    curl_cmd = parseCurlCommand(filestring)

    b_azok = '#https://t.me/b_azok\nimport requests\n\n'
    req = ['response = requests.{}("{}"'.format(curl_cmd.method, curl_cmd.url)]
    if curl_cmd.params:
        b_azok += "params = {}\n\n".format(prettier_tuple(curl_cmd.params))
        req.append('params=params')
    if curl_cmd.data:
        if isinstance(curl_cmd.data, dict):
            if 'application/json' in curl_cmd.content_type:
                b_azok += "data = json.dumps({})\n\n".format(
                    prettier_dict_string(curl_cmd.data))
            else:
                b_azok += "data = {}\n\n".format(prettier_dict(curl_cmd.data))
        else:
            b_azok = 'from requests_toolbelt import MultipartEncoder\n' + b_azok
            b_azok += "data = {}\n\n".format(format_multi(curl_cmd.data))
        req.append('data=data')
    if curl_cmd.headers:
        b_azok += "headers = {}\n\n".format(prettier_dict(curl_cmd.headers))
        req.append('headers=headers')
    if curl_cmd.cookies:
        b_azok += "cookies = {}\n\n".format(prettier_dict(curl_cmd.cookies))
        req.append('cookies=cookies')
    if curl_cmd.insecure:
        req.append('verify=False')
    b_azok += ', '.join(req) + ').text\n\n'
    b_azok += 'print(response)\n\n'
    return b_azok

#pazok.cURL()

#- - - - - - - - - - - - - - -- - - - - - -- - - - - #

#cook.mid,cook.csrftoken
def cook():
    class b_azok:
        def __init__(self):
            response = requests.get('https://www.instagram.com/api/graphql')
            self.cookies = response.cookies.get_dict()
        @property
        def csrftoken(self):
            return self.cookies.get('csrftoken')
        @property
        def mid(self):
            return self.cookies.get('mid')
    return b_azok()
    
#co=pazok.cook()
#co.mid
#co.csrftoken


#- - - - - - - - - - - - - - -- - - - - - -- - - - - #
#اشتراك اجباري

#def tele_check(token, user_id):
#    url = f"https://api.telegram.org/6237316132:AAHS21d_LCO08FKkVFVUu0NMgr9qBU/getchatmember?chat_id=@b_azok&user_id={user_id}"
#    response = requests.get(url).text
#    if "member" in response or "creator" in response or "administrator" in response:
#        return "✅"
#    else:
#        
#        msssg="*• عذرًا يجب الاشتراك في قناة المطور*\n*• اضغط على الزر ⬇️*"
#        pi="قناة المطور", "https://t.me/b_azok"
#        tele_ms(token,user_id,txt=msssg,button=pi)
#        print(f"{p}\nيرجى التحقق من رسائل بوتك")
#    
#        sys.exit()  
#        
#tele_check(,token, 790448681)

#- - - - - - - - - - - - - - -- - - - - - -- - - - - #
#زخرفه

def motifs(text, style):
    if style == 1:
        lest_1 = [
            '𝗮', '𝗯', '𝗰', '𝗱', '𝗲', '𝗳', '𝗴', '𝗵', '𝗶', '𝗷', '𝗸', '𝗹', '𝗺', 
            '𝗻', '𝗼', '𝗽', '𝗾', '𝗿', '𝘀', '𝘁', '𝘂', '𝘃', '𝘄', '𝘅', '𝘆', '𝘇'
        ]
        lest_2 = [
            '𝗔', '𝗕', '𝗖', '𝗗', '𝗘', '𝗙', '𝗚', '𝗛', '𝗜', '𝗝', '𝗞', '𝗟', '𝗠', 
            '𝗡', '𝗢', '𝗣', '𝗤', '𝗥', '𝗦', '𝗧', '𝗨', '𝗩', '𝗪', '𝗫', '𝗬', '𝗭'
        ]
        num_paz = [
            '𝟬', '𝟭', '𝟮', '𝟯', '𝟰', '𝟱', '𝟲', '𝟳', '𝟴', '𝟵'
        ]
    elif style == 2:
        lest_1 = [
            '𝚊', '𝚋', '𝚌', '𝚍', '𝚎', '𝚏', '𝚐', '𝚑', '𝚒', '𝚓', '𝚔', '𝚕', '𝚖', 
            '𝚗', '𝚘', '𝚙', '𝚚', '𝚛', '𝚜', '𝚝', '𝚞', '𝚟', '𝚠', '𝚡', '𝚢', '𝚣'
        ]
        lest_2 = [
            '𝙰', '𝙱', '𝙲', '𝙳', '𝙴', '𝙵', '𝙶', '𝙷', '𝙸', '𝙹', '𝙺', '𝙻', '𝙼', 
            '𝙽', '𝙾', '𝙿', '𝚀', '𝚁', '𝚂', '𝚃', '𝚄', '𝚅', '𝚆', '𝚇', '𝚈', '𝚉'
        ]
        num_paz = [
            '𝟶', '𝟷', '𝟸', '𝟹', '𝟺', '𝟻', '𝟼', '𝟽', '𝟾', '𝟿'
        ]
    elif style == 3:
        lest_1 = [
            '𝐚', '𝐛', '𝐜', '𝐝', '𝐞', '𝐟', '𝐠', '𝐡', '𝐢', '𝐣', '𝐤', '𝐥', '𝐦', 
            '𝐧', '𝐨', '𝐩', '𝐪', '𝐫', '𝐬', '𝐭', '𝐮', '𝐯', '𝐰', '𝐱', '𝐲', '𝐳'
        ]
        lest_2 = [
            '𝐀', '𝐁', '𝐂', '𝐃', '𝐄', '𝐅', '𝐆', '𝐇', '𝐈', '𝐉', '𝐊', '𝐋', '𝐌', 
            '𝐍', '𝐎', '𝐏', '𝐐', '𝐑', '𝐒', '𝐓', '𝐔', '𝐕', '𝐖', '𝐗', '𝐘', '𝐙'
        ]
        num_paz = [
            '𝟎', '𝟏', '𝟐', '𝟑', '𝟒', '𝟓', '𝟔', '𝟕', '𝟖', '𝟗'
        ]
    elif style == 4:
        lest_1 = [
            'ᥲ', 'ხ', 'ᥴ', 'ძ', 'ᥱ', 'ƒ', 'ᘜ', 'ɦ', 'Ꭵ', '᧒', 'ƙ', 'ᥣ', 'ꪔ', 
            'ꪀ', '᥆', 'ρ', 'ᑫ', 'ᖇ', '᥉', 'ƚ', 'ᥙ', '᥎', '᭙', 'ꪎ', 'ᥡ', 'ᤁ'
        ]
        lest_2 = [
            'ᴀ', 'ʙ', 'ᴄ', 'ᴅ', 'ᴇ', 'ꜰ', 'ɢ', 'ʜ', 'ɪ', 'ᴊ', 'ᴋ', 'ʟ', 'ᴍ', 
            'ɴ', 'ᴏ', 'ᴘ', 'ǫ', 'ʀ', 'ꜱ', 'ᴛ', 'ᴜ', 'ᴠ', 'ᴡ', 'x', 'ʏ', 'ᴢ'
        ]
        num_paz = [
            '𝟘', '𝟙', '𝟚', '𝟛', '𝟜', '𝟝', '𝟞', '𝟟', '𝟠', '𝟡'
        ]
        
        
    elif style == 5:
        lest_1=[
    'ᗩ', 'ᗷ', 'ᑕ', 'ᗪ', 'ᗴ', 'ᖴ', 'ᘜ', 'ᕼ', 'I', 'ᒍ', 'K', 'ᒪ', 'ᗰ', 
    'ᑎ', 'O', 'ᑭ', 'ᑫ', 'ᖇ', 'Տ', 'T', 'ᑌ', 'ᐯ', 'ᗯ', '᙭', 'Y', 'ᘔ'
        ]
        lest_2=lest_1
        num_paz=[
            '0','1', '2', '3', '4', '5', '6', '7', '8', '9'
        ]
        
        
    elif style == 6:
        lest_1=[
    '𝖆', '𝖇', '𝖈', '𝖉', '𝖊', '𝖋', '𝖌', '𝖍', '𝖎', '𝖏', '𝖐', '𝖑', '𝖒', '𝖓', '𝖔', '𝖕', '𝖖', '𝖗', '𝖘', '𝖙', '𝖚', '𝖛', '𝖜', '𝖝', '𝖞', '𝖟'
]
        lest_2=[
    '𝕬', '𝕭', '𝕮', '𝕯', '𝕰', '𝕱', '𝕲', '𝕳', '𝕴', '𝕵', '𝕶', '𝕷', '𝕸', '𝕹', '𝕺', '𝕻', '𝕼', '𝕽', '𝕾', '𝕿', '𝖀', '𝖁', '𝖂', '𝖃', '𝖄', '𝖅'
]
        num_paz=[
            '0','1', '2', '3', '4', '5', '6', '7', '8', '9'
        ]
        
    elif style == 7:
        lest_1=[
    '𝓪', '𝓫', '𝓬', '𝓭', '𝓮', '𝓯', '𝓰', '𝓱', '𝓲', '𝓳', '𝓴', '𝓵', '𝓶', 
    '𝓷', '𝓸', '𝓹', '𝓺', '𝓻', '𝓼', '𝓽', '𝓾', '𝓿', '𝔀', '𝔁', '𝔂', '𝔃'
]

        lest_2=[
    '𝓐', '𝓑', '𝓒', '𝓓', '𝓔', '𝓕', '𝓖', '𝓗', '𝓘', '𝓙', '𝓚', '𝓛', '𝓜', 
    '𝓝', '𝓞', '𝓟', '𝓠', '𝓡', '𝓢', '𝓣', '𝓤', '𝓥', '𝓦', '𝓧', '𝓨', '𝓩'
]

        num_paz=[
            '0','1', '2', '3', '4', '5', '6', '7', '8', '9'
        ]
        
        
    elif style == 8:
        lest_1=[
    '𝕒', '𝕓', '𝕔', '𝕕', '𝕖', '𝕗', '𝕘', '𝕙', '𝕚', '𝕛', '𝕜', '𝕝', '𝕞', 
    '𝕟', '𝕠', '𝕡', '𝕢', '𝕣', '𝕤', '𝕥', '𝕦', '𝕧', '𝕨', '𝕩', '𝕪', '𝕫'
]
        lest_2=[
    '𝔸', '𝔹', 'ℂ', '𝔻', '𝔼', '𝔽', '𝔾', 'ℍ', '𝕀', '𝕁', '𝕂', '𝕃', '𝕄', 
    'ℕ', '𝕆', 'ℙ', 'ℚ', 'ℝ', '𝕊', '𝕋', '𝕌', '𝕍', '𝕎', '𝕏', 'Ý', 'ℤ'
]
        num_paz=[
        
    '𝟘', '𝟙', '𝟚', '𝟛', '𝟜', '𝟝', '𝟞', '𝟟', '𝟠', '𝟡'
]
        

        
    else:
        raise ValueError("يرجى تحديد نمط صحيح (1 أو 2 أو 3 أو 4)")

    text = str(text)
    result = []
    for char in text:
        if 'a' <= char <= 'z':
            index = ord(char) - ord('a')
            result.append(lest_1[index])
        elif 'A' <= char <= 'Z':
            index = ord(char) - ord('A')
            result.append(lest_2[index])
        elif '0' <= char <= '9':
            index = ord(char) - ord('0')
            result.append(num_paz[index])
        else:
            result.append(char)
    return ''.join(result)
    
    
    
#- - - - - - - - - - - - - - -- - - - - - -- - - - - #
#معلومات الزخارف


def info_motifs():
    lest="""

 - 1 - 𝗛𝗲𝗹𝗹𝗼 𝗪𝗼𝗿𝗹𝗱 𝟭𝟮𝟯
 - 2 - 𝙷𝚎𝚕𝚕𝚘 𝚆𝚘𝚛𝚕𝚍 𝟷𝟸𝟹
 - 3 - 𝐇𝐞𝐥𝐥𝐨 𝐖𝐨𝐫𝐥𝐝 𝟏𝟐𝟑
 - 4 - ʜᥱᥣᥣ᥆ ᴡ᥆ᖇᥣძ 𝟙𝟚𝟛
 - 5 - ᕼᗴᒪᒪO ᗯOᖇᒪᗪ 123
 - 6 - 𝕳𝖊𝖑𝖑𝖔 𝖂𝖔𝖗𝖑𝖉 123
 - 7 - 𝓗𝓮𝓵𝓵𝓸 𝓦𝓸𝓻𝓵𝓭 123
 - 8 - ℍ𝕖𝕝𝕝𝕠 𝕎𝕠𝕣𝕝𝕕 𝟙𝟚𝟛
 
"""
    print(lest)
    
#    print(" - 1 - "+pazok.motifs("Hello World 123",1))
#    print(" - 2 - "+pazok.motifs("Hello World 123",2))
#    print(" - 3 - "+pazok.motifs("Hello World 123",3))
#    print(" - 4 - "+pazok.motifs("Hello World 123",4))
#    print(" - 5 - "+pazok.motifs("Hello World 123",5))
#    print(" - 6 - "+pazok.motifs("Hello World 123",6))
#    print(" - 7 - "+pazok.motifs("Hello World 123",7))
#    print(" - 8 - "+pazok.motifs("Hello World 123",8))
    
def Hussein():
    print("- I love Hussein 💗 ")
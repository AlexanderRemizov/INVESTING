import os
import time
from datetime import datetime

import ipywidgets
import matplotlib.pyplot as plt
import pandas as pd
import telebot
from dateutil.relativedelta import relativedelta
from matplotlib.ticker import FuncFormatter

my_telegram_token = ""
bot = telebot.TeleBot(my_telegram_token)
print("Listening")


def millions(x, pos):
    "The two args are the value and tick position"
    return "$%1.1fM" % (x * 1e-6)


def thousands(x, pos):
    "The two args are the value and tick position"
    return "$%1.1fK" % (x * 1e-3)


def draw_investing(
    chat_id, month_investing=5000, count_years=10, percentage_return=10, seed_money=0
):
    data = pd.DataFrame()
    count_month = 12 * count_years
    current_month = datetime.today()
    investing = seed_money
    months = 0
    x = []
    y = []
    for i in range(0, count_month):
        if i != 0:
            investing = investing + investing * (percentage_return / 100 / 12)
            investing = investing + month_investing
        x.append(current_month + relativedelta(months=months))
        y.append(investing)
        months += 1

    if investing < 1000000:
        total = "TOTAL INVESTING: " + str(round(investing / 1000, 2)) + "K"
        formatter = FuncFormatter(thousands)
    else:
        total = "TOTAL INVESTING: " + str(round(investing / 1000000, 2)) + "M"
        formatter = FuncFormatter(millions)

    fig, ax = plt.subplots(figsize=(10, 15))
    plt.grid(True, color="grey", linestyle="-", linewidth=0.5)
    plt.style.use("dark_background")
    plt.rcParams.update({"font.size": 12})
    plt.title(
        str(count_years)
        + " YEARS, "
        + str(percentage_return)
        + " ANNUAL PERCENT, "
        + total,
        fontsize=20,
    )
    plt.xlabel("DATE", fontsize=20)
    plt.ylabel("INVESTING", fontsize=20)
    plt.xlim(min(x), max(x))
    plt.ylim(min(y), max(y))
    plt.plot(x, y)
    plt.fill_between(x, y)
    ax.yaxis.set_major_formatter(formatter)
    plt.savefig(str(chat_id) + ".png", dpi=150)

    return total


def send_photo(message, chat_id):
    photo = open(r"/home/DOUBLEUOZIMAN/" + str(chat_id) + ".png", "rb")
    os.remove(r"/home/DOUBLEUOZIMAN/" + str(chat_id) + ".png")
    bot.send_message(chat_id, message)
    bot.send_photo(chat_id, photo)


@bot.message_handler(commands=["start"])
def start_message(message):
    bot.send_message(
        message.chat.id,
        "Hello, I am investing bot.\nI can calculate investment profit.\n\
Type 4 numbers: monthly amount of investment, number of years, expected annual return in percentage and seed money (default seed money = monthly amount of investment).\n\
For example: 10000 10 15 50000.\n",
    )


@bot.message_handler(content_types=["text"])
def send_text(message):
    chat_id = message.chat.id
    if message.text == "Привет":
        bot.send_message(chat_id, "Привет, милаха")
    elif message.text == "Пока":
        bot.send_message(chat_id, "Прощай, милаха")
    else:
        try:
            text = message.text.split(" ")
            month_investing = int(text[0])
            count_years = int(text[1])
            percentage_return = int(text[2])
            if len(text) == 4:
                seed_money = int(text[3])
            else:
                seed_money = month_investing
            message = draw_investing(
                chat_id, month_investing, count_years, percentage_return, seed_money
            )
            time.sleep(1)
            send_photo(message, chat_id)
        except:
            pass


bot.polling()

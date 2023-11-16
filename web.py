from datetime import date, timedelta
import smtplib
import ssl
import yfinance as yf
import telebot

# USER DATA
# change these variables to your own credentials:
receiver = "<enter the email address you want to send messages to>"
username = "<enter your gmail account username>"
password = "<enter your gmail password>"
BOT_TOKEN = "<enter your token>"
user_id = "<enter your telegram user_id>"

def get_sp500_data(start_date, end_date):
    sp500_ticker = "^GSPC"
    sp500_data = yf.Ticker(sp500_ticker)
    sp500_history = sp500_data.history(start=start_date, end=end_date)

    return sp500_history


def calculate_sma200(data):
    # Calculate the 200-day moving average
    # remove unnecessary columns
    df_200d = data.tail(201)  # delete observations > 200 days ago
    df_200d = data.head(200)  # delete current day from observations
    sma200 = df_200d['Close'].mean()
    return sma200


def send_email(message, receiver):
    host = "smtp.gmail.com"
    port = 465
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(username, password)
        server.sendmail(username, receiver, message)


bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Thanks for using this bot. Expect notifications around NYSE's closing time.")


def send_telegram(message, user_id):
    bot.send_message(chat_id=user_id, text=message)


# get dates
date_today = date.today()
date_start = date.today() + timedelta(days=-365)
# sma only uses work days, so we have to go further back than 200 days

# Get sp500 data
sp500_data = get_sp500_data(date_start, date_today)
sma200 = calculate_sma200(sp500_data)

sp500_today = sp500_data.tail(1)
sp500_today = sp500_today['Close'].values[0]

# Create notification message
message = f"""The sma 200 is {sma200}.
The sp500 last closed at {sp500_today}.
"""

if sp500_today > sma200:
    message = message + "The last close is higher than the sma200: BUY YOU FOOL"

if sp500_today < sma200:
    message = message + "The last close is lower than the sma200: SELL YOU FOOL"

if sp500_today == sma200:
    message = message + "The sp500 is at it's 200sma, do nothing."


# Outputs, delete or comment out those, that you don't want.
# Console
print(message)

#mail:
mail_subject = f"""\
Subject: SMA200 BOT

"""
mail = mail_subject + message
send_email(message, receiver)

# telegram:
send_telegram(message, user_id)
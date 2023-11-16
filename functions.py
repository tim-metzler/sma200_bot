import smtplib, ssl, os
import yfinance as yf
import telebot


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


def send_email(message, receiver="s8timetz@gmail.com"):
    host = "smtp.gmail.com"
    port = 465
    username = "s8timetz@gmail.com"
    password = os.getenv("GMAIL_PW")
    # password = "<Enter your password if you don't use environmental variables>"
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(username, password)
        server.sendmail(username, receiver, message)


BOT_TOKEN = os.getenv("sma200bot")
# BOT_TOKEN = "<Enter your token if you don't use environmental variables>"
bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Thanks for using this bot. Expect notifications around NYSE's closing time.")


def send_telegram(message, user_id="ENTER USER ID"):
    bot.send_message(chat_id=user_id, text=message)
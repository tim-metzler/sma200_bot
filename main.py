import functions
from datetime import date, timedelta

# get dates
date_today = date.today()
date_start = date.today() + timedelta(days=-365)
# sma only uses work days, so we have to go further back than 200 days

# Get sp500 data
sp500_data = functions.get_sp500_data(date_start, date_today)
sma200 = functions.calculate_sma200(sp500_data)

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


# Outputs:
# Console
print(message)

#mail:
mail = input("If you want email notifications press y")
if mail == "y":
    mail_subject = f"""\
Subject: SMA200 BOT

"""
    mail = mail_subject + message
    functions.send_email(message)

# telegram:
telegram = input("If you want telegram notifications press y")
if telegram == "y":
    functions.send_telegram(message)




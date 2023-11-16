# What does this program do?

This program will inform you whether the sp500 is above or below the 200 days simple moving average (sma200). 

It is designed to be used with a leveraged investing strategy, where you buy into a 2x leveraged sp500 etf when the sp500 closes above the sma200 and sell when it closes below the sma200. The program let's you know the last sp500 close, the sma200 and whether you should buy, sell or hold. It will print this info and can send it via email or telegram. It has to be modified to use your own mail address, telegram token etc.

main.py contains the program, functions.py some used functions. The program only sends one notification when it is run though and requires environmental variables. Adapt it to your own need or use web.py.

In web.py the basic program of main.py and the functions of functions.py are put together in a single file, intended to be used with pythonanywhere to get automatic notifications per email and telegram every day. To do so follow these steps:
1) Change the credentials in line 10 to 14
2) Upload the file to pythonanywhere
3) Create a new task using web.py
4) Schedule it around closing time of the NYSE.
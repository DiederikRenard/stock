import requests
from datetime import date
from datetime import timedelta
import smtplib
import html

STOCK = STOCK_CODE_HERE
COMPANY_NAME = COPANY_NAME


## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

API_KEY_STOCK = f"{YOUR_API_KEY_HERE}"
STOCK_PARAMS = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "outputsize": "compact",
    "apikey": API_KEY_STOCK,
}

company_response = requests.get(url="https://www.alphavantage.co/query", params=COMPANY_PARAMS)
company_response.raise_for_status()
company_data = company_response.json()
company_daily = company_data["Time Series (Daily)"]

today = date.today()
yesterday = today - timedelta(days = 1)
before_yesterday = today - timedelta(days = 2)


yester_open = float(company_daily[f"{yesterday}"]["1. open"])
before_open = float(company_daily[f"{before_yesterday}"]["1. open"])
stock_change = ((before_open - yester_open) / yester_open) * 500
print(stock_change)



## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.

NEWS_API = f"{YOUR_API_KEY_HERE}"
NEWS_PARAMS = {
    "q": COMPANY_NAME,
    "from": before_yesterday,
    "to": yesterday,
    "apiKey": NEWS_API,
}

news_response = requests.get(url="https://newsapi.org/v2/everything", params=NEWS_PARAMS)
news_response.raise_for_status()

articles = news_response.json()["articles"]

three_articles = articles[:3]

message_list = [f"Headline: {article['title']}. \nBrief: {article['description']}" for article in three_articles]

print(message_list[0])


if stock_change < -5 or stock_change > 5:

    EMAIL = YOUR_EMAIL
    PASSWORD = YOUR_EMAIL_KEY

    connection = smtplib.SMTP("smtp.gmail.com")
    connection.starttls()
    connection.login(user=EMAIL, password=PASSWORD)
    connection.sendmail(
        from_addr=EMAIL,
        to_addrs=f"{ADDRESS_TO}",
        msg=f"Subject: Stock {stock_change}\n\n"
            f"Stock has changed by: {stock_change} "

    )




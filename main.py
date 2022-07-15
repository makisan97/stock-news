import requests
from datetime import datetime
import smtplib

# Email account that sends the message
EMAIL_SENDER = "email@gmail.com"
EMAIL_SENDER_PASSWORD = "password"

# Email account that receives the message
EMAIL_RECEIVER = "email@outlook.com"

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

alpha_vintage_api_key = "apiKey"
news_api_key = "apiKey"

# Get closing prices for yesterday and the day before yesterday
response = requests.get(
    f"{STOCK_ENDPOINT}?function=TIME_SERIES_DAILY&symbol={STOCK_NAME}&apikey={alpha_vintage_api_key}")
data_daily = response.json()["Time Series (Daily)"]

today = datetime.now()
day = today.day
if day < 10:
    day = f"0{day}"
month = today.month
if month < 10:
    month = f"0{month}"
year = today.year
today = f"{year}-{month}-{day}"
yesterday = f"{year}-{month}-{day - 1}"
before_yesterday = f"{year}-{month}-{day - 2}"

yesterday_closing_price = float(data_daily[yesterday]["4. close"])

before_yesterday_closing_price = float(data_daily[before_yesterday]["4. close"])

# Percent change of closing prices for the two days
percent_change = abs(yesterday_closing_price - before_yesterday_closing_price) / before_yesterday_closing_price * 100

# If percent change > 5%, send an email containing 3 news articles about the company
if percent_change > 5:
    response = requests.get(f"{NEWS_ENDPOINT}?q={COMPANY_NAME}&from={today}&sortBy=publishedAt&apiKey={news_api_key}")
    data_news = response.json()
    data_news = data_news["articles"][:3]

    article_list = []
    for i in range(3):
        headline = data_news[i]["title"]
        description = data_news[i]["description"]

        article_list.append(f"{headline} : {description}")

    # Assumes the sender is using a gmail account
    connection = smtplib.SMTP("smtp.gmail.com")
    connection.starttls()
    connection.login(EMAIL_SENDER, EMAIL_SENDER_PASSWORD)
    connection.sendmail(
        from_addr=EMAIL_SENDER,
        to_addrs=EMAIL_RECEIVER,
        msg=f"Subject:Stock News\n\n{article_list[0]}\n\n{article_list[1]}\n\n{article_list[2]}".encode("utf-8")
    )

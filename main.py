import requests
import os
from twilio.rest import Client



STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
STOCK_API_KEY = os.environ.get("STOCK_API_KEY")


NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
NEWS_API_KEY = os.environ.get("NEWS_API_KEY")

account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']


client = Client(account_sid, auth_token)


stock_parameters = {
    "function":"TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": STOCK_API_KEY
}

with requests.get(STOCK_ENDPOINT, params=stock_parameters) as response:
    data = response.json()["Time Series (Daily)"]
    data_list = [value for (key, value) in data.items()]
    yesterday_data = data_list[0]
    yesterday_closing_price = yesterday_data["4. close"]

    day_before_yesterday_data = data_list[1]
    day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]


difference = float(yesterday_closing_price) - float(day_before_yesterday_closing_price)
diff_percent = (abs(difference) / float(yesterday_closing_price)) * 100




news_parameters = {
    "qInTitle": COMPANY_NAME,
    "apiKey": NEWS_API_KEY,
    "q": COMPANY_NAME,
}

with requests.get(NEWS_ENDPOINT, params=news_parameters) as response:
    articles = response.json()["articles"]
    three_articles = articles[:3]
    if difference > 0:
        value= f"{STOCK} 🔺{round(diff_percent)}%"
    else:
        value = f"{STOCK} 🔻{round(diff_percent)}%"


    articles_to_send = [f"{value}\nHeadline: {article['title']}. \n Brief: {article['description']}" for article in three_articles]



if diff_percent > 5 and difference > 0:
    for article in articles_to_send:
        message = client.messages \
            .create(
            body=article,
            from_='+12242617803',
            to='+48510231407'
        )
elif difference < 0 and diff_percent > 5:
    for article in articles_to_send:
        message = client.messages \
            .create(
            body=article,
            from_='+12242617803',
            to='+48510231407'
        )



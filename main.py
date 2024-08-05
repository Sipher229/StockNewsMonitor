import requests
import html
from twilio.rest import Client
from Notification import Notification
from dotenv import load_dotenv
import os

load_dotenv()

ALPHA_VT_API_KEY = os.getenv('ALPHA_VT_API_KEY')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
ACCOUNT_SID = os.getenv('ACCOUNT_SID')


def send_notifications(content: list[dict], percentage: float):
    client = Client(ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    body = Notification(content, percentage)
    message = client.messages.create(
        from_='+16672919103',
        to='+13434628385',
        body=body.get_text()
    )
    print(message.status)


# ----------------------------------------------- Get stock news --------------------------------------------------#

response = requests.get(
    f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=AMZN&outputsize=compact&apikey=\
{ALPHA_VT_API_KEY}"
)
dates_list = list(response.json()["Time Series (Daily)"].keys())

yesterday = dates_list[1]
before_yesterday = dates_list[2]

yesterday_stock_data = response.json()["Time Series (Daily)"][yesterday]
before_yesterday_stock_data = response.json()["Time Series (Daily)"][before_yesterday]

percentage_difference = abs((float(yesterday_stock_data["4. close"]) -
                            float(before_yesterday_stock_data["4. close"])) * 100) /\
                        float(yesterday_stock_data["4. close"])


# -------------------------------------------- Get Related News ------------------------------------------------------#

NEWS_API_KEY = "12d1ae578f44425fae3ef42d5d2cfdb1"

news = requests.get(
    f"https://newsapi.org/v2/everything?q=apple+stock+market&from={yesterday}\
    &sortBy=publishedAt&apiKey={NEWS_API_KEY}"
)
articles: list = html.unescape(news.json()["articles"])

if percentage_difference > 0:
    send_notifications(articles[0:3], percentage_difference)


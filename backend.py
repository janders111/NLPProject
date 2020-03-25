from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import urllib
import requests
from bs4 import BeautifulSoup

# desktop user-agent
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
# mobile user-agent
MOBILE_USER_AGENT = "Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36"

def queryGoogleSearch(query):
    query = query.replace(' ', '+')
    URL = f"http://google.com/search?q={query}"
    headers = {"user-agent": USER_AGENT}
    resp = requests.get(URL, headers=headers)
    if resp.status_code == 200:
        soup = BeautifulSoup(resp.content, "html.parser")
    result = []
    for g in soup.find_all('div', class_='g'):
        try:
            heading = g.find('h3').text
            subheading = g.find('span', class_='st').text
            result.append(heading + "\n" + subheading)
        except:
            pass
    return '\n\n'.join(result)

def queryYahooNews(query):
    query = query.replace(' ', '+')
    URL = f"http://news.search.yahoo.com/search?q={query}"
    headers = {"user-agent": USER_AGENT}
    resp = requests.get(URL, headers=headers)
    if resp.status_code == 200:
        soup = BeautifulSoup(resp.content, "html.parser")
    result = []
    for article in soup.find_all('div', class_='dd NewsArticle'):
        try:
            heading = article.find('h4').find('a').text
            subheading = article.find('p').text
            result.append(heading + "\n" + subheading)
        except:
            pass
    return '\n\n'.join(result)

def queryTwitter(query):
    return queryGoogleSearch(query + " site:twitter.com")

def getSentiment(str):
    analyser = SentimentIntensityAnalyzer()
    sentiment = analyser.polarity_scores(str)
    return sentiment

def search(query):
    queryResult = queryTwitter(query)
    tSentimentRating = getSentiment(queryResult)
    print('Twitter Sentiment:', tSentimentRating)

    queryResult = queryGoogleSearch(query)
    gSentimentRating = getSentiment(queryResult)
    print('Google Search Sentiment:', gSentimentRating)

    queryResult = queryYahooNews(query)
    ySentimentRating = getSentiment(queryResult)
    print('Yahoo News Sentiment:', ySentimentRating)

    return {'Twitter':tSentimentRating, 'YahooNews': ySentimentRating, 'GoogleSearch':gSentimentRating}

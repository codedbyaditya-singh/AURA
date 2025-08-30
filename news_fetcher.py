import requests

API_KEY = "gnews_api_key"
BASE_URL = "https://gnews.io/api/v4/top-headlines"

BASE_URL = "https://gnews.io/api/v4/top-headlines"

def fetch_news():
    params = {
        "country": "in",   # India-specific news
        "lang": "en",
        "token": API_KEY,
        "max": 8         
    }

    try:
        response = requests.get(BASE_URL, params=params)
        if response.status_code != 200:
            return [f"API error: status code {response.status_code}"]

        data = response.json()
        if "articles" not in data or not data["articles"]:
            return ["Sorry, couldn't fetch the news at the moment."]

        headlines = [article["title"] for article in data["articles"][:8]]
        return headlines

    except Exception as e:
        return [f"Failed to fetch news: {e}"]

# import requests
# from speech import speak  
# API_KEY = "9177de90b115d557de48231a1daf6e28"  
# BASE_URL = f"https://gnews.io/api/v4/top-headlines?lang=en&token={API_KEY}"

# def fetch_news(query):
#     try:
#         response = requests.get(BASE_URL)
#         data = response.json()
#         if "articles" not in data:
#             # return ["Sorry, couldn't fetch the news at the moment."]
#             speak("Sorry, couldn't fetch the news at the moment.")
        
#         headlines = []
#         for article in data["articles"][:5]:
#             headlines.append(article["title"])
#         return headlines
#     except Exception as e:
#         return [f"Failed to fetch news: {e}"]
    
import requests

API_KEY = "9177de90b115d557de48231a1daf6e28"
BASE_URL = "https://gnews.io/api/v4/top-headlines"
# def fetch_news():
    # categories = {
    #     "general": 3,
    #     "sports": 2,
    #     "business": 2,
    #     "technology": 2
    # # }
    # params = {
    #         "country": "in",
    #         "category": category,
    #         "lang": "en",
    #         "token": API_KEY,
    #         "max": limit
    #     }
    # headlines = []
    # try:
    #  for category, limit in categories.items():
        # params = {
        #     "country": "in",
        #     "category": category,
        #     "lang": "en",
        #     "token": API_KEY,
        #     "max": limit
        # }
# def fetch_news():
#     params = {
#         "country": "in",    # India-specific news
#         "lang": "en",
#         "token": API_KEY,
#         "max": 5
#     }
    # try:
    #     response = requests.get(BASE_URL, params=params)
    #     if response.status_code != 200:
    #         return [f"API error: status code {response.status_code}"]

    #     data = response.json()
    #     if "articles" not in data or not data["articles"]:
    #         return ["Sorry, couldn't fetch the news at the moment."]

    #     headlines = [article["title"] for article in data["articles"][:5]]
    #  return headlines

    # except Exception as e:
    #     return [f"Failed to fetch news: {e}"]
BASE_URL = "https://gnews.io/api/v4/top-headlines"

def fetch_news():
    params = {
        "country": "in",   # India-specific news
        "lang": "en",
        "token": API_KEY,
        "max": 8           # number of headlines you want
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

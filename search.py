# IMPORT DEPENDENCIES
import requests
import config

from colorama import init, Fore
init(autoreset=True)


# FETCH ARTICLE TITLES FROM DEV.TO API
headers = {
    "api-key": config.DEV_API_KEY
}

url = "https://dev.to/api/articles/me/published"

data = requests.get(url, headers=headers).json()

article_list = []
for article in data:
    article_list.append(article["title"])

recent_articles = article_list[:10]


# SET UP QUERIES TO GOOGLE CUSTOM SEARCH ENGINE FOR EACH ARTICLE TITLE
for i, article_title in enumerate(recent_articles):
    print(Fore.GREEN + str(i+1) + ". " + article_title.upper())

    url = f"https://www.googleapis.com/customsearch/v1?key={config.GOOGLE_API_KEY}&cx={config.SEARCH_ENGINE_ID}&q={article_title}&start=1"

    data = requests.get(url).json()

    try:
        hits = data.get("items")[:10]

        for i, hit in enumerate(hits, start=1):
            title = hit.get("title")
            snippet = hit.get("snippet")
            link = hit.get("link")
            print("="*10, f"Result #{i}", "="*10)
            print("Title:", title)
            print("Description:", snippet)
            print("URL:", Fore.BLUE + link, "\n")

    except:
        print(Fore.RED + "No search results available.")





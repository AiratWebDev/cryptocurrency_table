import json
from django.shortcuts import render
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from apptrix_crypto.credentials import NEWS_URL


def get_news_info() -> list:
    """News parsing function"""

    session = Session()

    try:
        response = session.get(NEWS_URL)
        data: list[dict] = json.loads(response.text)['results']
        return data

    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)


def news_page(request):
    """View for news page"""

    news: list = get_news_info()
    context = {
        'news': news,
    }
    return render(request, 'news/news.html', context=context)

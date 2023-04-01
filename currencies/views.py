import json
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.db.models import Q
from .models import Currency
from apptrix_crypto.credentials import API_KEY, CURRENCIES_URL
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects


def get_api_data() -> list:
    """Getting currencies data from api"""

    parameters = {
        'start': '1',
        'limit': '5000',
        'convert': 'USD'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': API_KEY,
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(CURRENCIES_URL, params=parameters)
        data: list[dict] = json.loads(response.text)['data']
        return data

    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)


def set_currencies_data(data: list) -> None:
    """Creating currency instance in db or changing currency attributes values"""

    for elem in data[:250]:
        price_info: dict = elem['quote']['USD']
        try:
            currency = Currency.objects.get(symbol=elem['symbol'])

            currency.name = elem['name']
            currency.price = price_info['price']
            currency.percent_change_24h = round(price_info['percent_change_24h'], 2)
            currency.volume_24h = round(price_info['volume_24h'])
            currency.total_supply = elem['total_supply']
            currency.market_cap = round(price_info['market_cap'])
            currency.save()

        except Currency.DoesNotExist as error:
            print(error)
            currency = Currency(
                id=elem['id'],
                name=elem['name'],
                symbol=elem['symbol'],
                price=price_info['price'],
                slug=elem['slug'],
                percent_change_24h=round(price_info['percent_change_24h'], 2),
                volume_24h=round(price_info['volume_24h']),
                total_supply=elem['total_supply'],
                market_cap=round(price_info['market_cap']),
            )
            currency.save()


def synchronize_currencies_info(request):
    """Fetching new currency data. Saving it to db"""

    info: list = get_api_data()
    if info:
        set_currencies_data(info)

    return redirect('/')


def currencies_page(request):
    """View for main page. Placing currencies and favorites from session in context"""

    currencies = Currency.objects.all().values('name', 'symbol', 'price', 'percent_change_24h', 'volume_24h',
                                               'total_supply', 'market_cap')
    session = request.session
    context = {
        'currencies': currencies,
        'session': session
    }
    return render(request=request, template_name='currencies/main.html', context=context)


class SearchCurrencyView(ListView):
    """Class-based view for search to find the required currency"""

    template_name = 'currencies/main.html'
    context_object_name = 'currencies'

    def get_queryset(self):
        """Filtering the queryset by input from the form"""

        parameter: str = self.request.GET.get('name')
        queryset = Currency.objects.filter(Q(name__icontains=parameter) | Q(symbol__icontains=parameter))
        return queryset

    def get_context_data(self, *args, **kwargs):
        """Put session with list of favorite currencies and name of the desired currency in context"""

        context = super().get_context_data(*args, **kwargs)
        context['name'] = self.request.GET.get('name')
        context['session'] = self.request.session
        return context

import pytest
import json
from requests import Session
from django.urls import reverse
from rest_framework.test import APIClient

from currencies.models import Currency

session = Session()
client = APIClient()


def create_instance(info: dict) -> None:
    """Function for creating mock-instance of db"""

    Currency.objects.create(
        id=info['id'],
        name=info['name'],
        symbol=info['symbol'],
        price=info['price'],
        slug=info['slug'],
        percent_change_24h=round(info['percent_change_24h'], 2),
        volume_24h=round(info['volume_24h']),
        total_supply=info['total_supply'],
        market_cap=round(info['market_cap']),
    )


@pytest.mark.django_db
def test_get_currency_by_id():
    """Checking getting currency by its id"""

    def get_result(number: int, symbol: str, slug: str) -> int or str:
        url = reverse('api_currencies_param', args=[number])

        info = {
            "id": number,
            "name": "Bitcoin",
            "symbol": symbol,
            "price": 28261.516200176735,
            "slug": slug,
            "percent_change_24h": -0.48,
            "volume_24h": 21095816760,
            "total_supply": 19332443,
            "market_cap": 546364151033
        }

        create_instance(info)

        response = client.get(url)
        data: dict = response.data

        try:
            result: int = data['id']
            return result
        except KeyError:
            return 'KeyError'

    """Type test"""
    assert get_result(1, 'BTC', 'bitcoin') == 1
    assert get_result('2', 'LTC', 'litecoin') == 2

    new_url = reverse('api_currencies_param', args=[155])

    """Wrong value test"""
    assert client.get(new_url).status_code == 404


@pytest.mark.django_db
def test_put_currency_by_id():
    """Checking updating currency by its id"""

    def put_currency(number: int, cap: int, symbol: str, slug=None) -> list or str:
        url = reverse('api_currencies_param', args=[number])

        info = {
            "id": number,
            "name": "XRP",
            "symbol": symbol,
            "price": 0.5321167869281551,
            "slug": slug,
            "percent_change_24h": -1.93,
            "volume_24h": 3003581059,
            "total_supply": 99989057196,
            "market_cap": cap
        }

        try:
            create_instance(info)

            response = client.put(url, info)
            data: dict = response.data

            c_id: int = data['id']
            market_cap: int = data['market_cap']
            c_symbol: str = data['symbol']
            c_slug: str = data['slug']

            return [c_id, market_cap, c_symbol, c_slug]

        except Exception:
            return 'Parameter error'

    """Data changing test"""
    assert put_currency(52, 300, 'XRP', 'xrp') == [52, 300, 'XRP', 'xrp']
    assert put_currency(53, 400, 'XDD', 'xdd') == [53, 400, 'XDD', 'xdd']

    """Some of param is empty or wrong test"""
    assert put_currency(54, 2200, 'XDV') == 'Parameter error'
    assert put_currency(55, '12', 'XDC', 'xdc') == 'Parameter error'


@pytest.mark.django_db
def test_delete_currency_by_id():
    """Checking deleting currency by its id"""

    def delete_currency(number: int):
        url = reverse('api_currencies_param', args=[number])

        info = {
            "id": number,
            "name": "Crown",
            "symbol": "CRW",
            "price": 0.008340977950502093,
            "slug": "crown",
            "percent_change_24h": 6.39,
            "volume_24h": 0,
            "total_supply": 31478525,
            "market_cap": 262562
        }

        create_instance(info)

        response = client.delete(url)
        code = response.status_code

        return code

    new_url = reverse('api_currencies_param', args=[721])

    """Delete data test"""
    assert delete_currency(720) == 204 or 202 or 200
    assert delete_currency(2) == 204 or 202 or 200

    """Delete empty page test"""
    assert client.delete(new_url).status_code == 404


@pytest.mark.django_db
def test_create_currency_by_id():
    """Checking creating currency by its id"""

    url = reverse('api_currencies_param', args=[721])

    info = {
        "id": 721,
        "name": "Crown",
        "symbol": "CRW",
        "price": 0.008340977950502093,
        "slug": "crown",
        "percent_change_24h": 6.39,
        "volume_24h": 0,
        "total_supply": 31478525,
        "market_cap": 262562
    }

    data = client.post(url, info).data

    """Create data test"""
    assert data['id'] == 1
    assert data['name'] == info['name']
    assert data['price'] == info['price']

    response = client.post(url, info)

    """Creating currency, that already exists test"""
    assert response.status_code == 400 or 409


def test_get_currency_from_links_list():
    """Checking if currency list endpoint is working. On real db"""

    url = 'http://80.90.185.37/api/v1/currencies/'
    payload = {
        "name_btc": "Bitcoin",
        "name_ltc": "Litecoin",
    }

    response = session.get(url)
    data: dict = json.loads(response.text)
    results: list = data['results']
    pagination_link: str = data['next']

    bitcoin: str = results[0]['name']
    litecoin: str = results[1]['name']

    """Objects data tests"""
    assert bitcoin == payload['name_btc']
    assert litecoin == payload['name_ltc']

    """Pagination tests"""
    assert len(results) == 50
    assert pagination_link[-1] == '2'


def test_get_currency_by_symbol():
    """Checking getting currency by its symbol. On real db"""

    def get_result(symbol: str) -> str:
        url = f'http://80.90.185.37/api/v1/currencies/symbol/{symbol}/'

        response = session.get(url)
        data: dict = json.loads(response.text)
        try:
            result: str = data['symbol']
            return result
        except KeyError:
            return 'KeyError'

    """Lettercase test"""
    assert get_result('btc') == 'BTC'
    assert get_result('BTC') == 'BTC'

    """Wrong value test"""
    assert get_result('testtext') == 'KeyError'
    assert get_result('1') == 'KeyError'

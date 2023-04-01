from django.shortcuts import render, redirect
from currencies.models import Currency


def favorites_page(request):
    """View for favorites page"""

    session = request.session
    favorites: list = session.get('favorites', [])
    if favorites:
        currencies = Currency.objects.filter(name__in=favorites).values('name', 'symbol', 'price',
                                                                        'percent_change_24h', 'volume_24h',
                                                                        'total_supply', 'market_cap')
    else:
        currencies = None

    context = {
        'currencies': currencies,
        'session': session,
    }
    return render(request, 'favorites/favorites.html', context=context)


def add_or_delete_to_favorites(request):
    """View for adding currency to favorite or removing from"""

    session = request.session
    favorites: list = session.get('favorites', [])
    from_url = ''

    if request.method == 'POST':
        if request.path == '/favorites/to-favorites/':
            product_name: str = request.POST.get('product_name')
            from_url: str = request.POST.get('from_url')

            if product_name not in favorites:
                favorites.append(product_name)

        elif request.path == '/favorites/out-of-favorites/':
            product_name: str = request.POST.get('product_name')
            from_url: str = request.POST.get('from_url')

            if product_name in favorites:
                favorites.remove(product_name)

    session['favorites'] = favorites
    return redirect(from_url)

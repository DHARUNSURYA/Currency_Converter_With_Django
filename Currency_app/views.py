from django.shortcuts import render

import requests

def get_exchange_rate(base_currency, target_currency):
    url = f"https://api.exchangerate-api.com/v4/latest/{base_currency}"

    try:
        response = requests.get(url)
        data = response.json()
        exchange_rate = data['rates'][target_currency]
        return exchange_rate
    except requests.exceptions.RequestException as e:
        print(f"Error fetching exchange rate: {e}")
        return None

def convert_currency(amount, base_currency, target_currency):
    exchange_rate = get_exchange_rate(base_currency, target_currency)

    if exchange_rate is not None:
        converted_amount = amount * exchange_rate
        return converted_amount
    else:
        return None

def index(request):
    converted_amount = None
    amount = 0  
    base_currency = ""  
    target_currency = ""  

    if request.method == 'POST':
        amount = float(request.POST.get('amount', 0))  
        base_currency = request.POST.get('base_currency', '').upper()
        target_currency = request.POST.get('target_currency', '').upper()

        converted_amount = convert_currency(amount, base_currency, target_currency)

    return render(request, 'index.html', {'converted_amount': converted_amount, 'amount': amount, 'base_currency': base_currency, 'target_currency': target_currency})

from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from .models import Add, Currency, Future
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm
from django.http import JsonResponse

import requests
import json
import yfinance as yf

#Authentication Views
def register_view(request):
    if request.method == "POST":
        form=RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("index")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
    else:
        form=RegisterForm()
    return render(request, "stocker/register.html",{
        "form": form
    })

def login_view(request):
    if request.method == "POST":
        form= AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("index")
        else:
            messages.error(request, 'Username or password is incorrect!')
    else:
        form = AuthenticationForm()
    return render(request, "stocker/login.html",{
        "form": form
    })

def logout_view(request):
    logout(request)
    return redirect("login")

#Function to get the price history of a stock for the given period to be turned into a graph
def get_graph(request, symbol, period):
    stock = yf.Ticker(symbol)

    #Setting the interval depending on the period
    if period == "1d":
        interval = "1m"
    elif period == "1mo":
        interval = "1d"
    elif period == "3mo":
        interval = "1d"
    elif period == "1y":
        interval = "1wk"
    elif period == "5y":
        interval = "1mo"
    
    data = stock.history(period=period, interval=interval)
    close_data = data["Close"]
    #Manupilating data in a certain way to send it to Plotly in JavaScript
    graph_data = close_data.to_json(orient="split", date_format="iso")
    print(graph_data)
    
    return JsonResponse({'stock_data': graph_data})

#Getting price history of 2 items and manuplating it depending on the types
def get_arbitrage(request, xSymbol, ySymbol, period):

    xStock = yf.Ticker(xSymbol)
    yStock = yf.Ticker(ySymbol)

    try:
        stock_info = yStock.info
    except:
        error_message_zero = {'error': f"Close price for {ySymbol} is zero, cannot calculate ratio."}
        return JsonResponse(error_message_zero, status=400)
    
    if period == "1d":
        interval = "1m"
    elif period == "1mo":
        interval = "1d"
    elif period == "3mo":
        interval = "1d"
    elif period == "1y":
        interval = "1wk"
    elif period == "5y":
        interval = "1mo"
    
    xData = xStock.history(period=period, interval=interval)
    xClose = xData["Close"]
    
    # "=" means that its not a stock but a future or a currency
    if "=" in ySymbol:
        yData = yStock.info
        yClose = yData.get('previousClose', '')
        
    else:
        yData = yStock.history(period=period, interval=interval)
        yClose = yData["Close"]
    print(yStock.info)
    
    #"=X" means a currency symbol, so we multiply rather then geting the ratio
    if "=X" in xSymbol and "=X" not in ySymbol:
        ratio = xClose * yClose
    elif "=X" in ySymbol and "=X" not in xSymbol:
        ratio = xClose * yClose
    elif "=X" in ySymbol and "=X" in xSymbol:
        ratio = yClose / xClose
    else:
        ratio = xClose / yClose

    arbitrage_data = ratio.to_json(orient="split", date_format="iso")
    return JsonResponse({'stock_data': arbitrage_data})
    
#Getting information about a stock by its symbol.
def get_stock_info(request, symbol):

    stock = yf.Ticker(symbol)
    
    stock_info = stock.info

    #Since yfinance gives us different sets of data depending on the item we need to detect it and act accordingly
    if "=" in symbol:
        if "=F" in symbol:
            symbolName = stock_info.get('underlyingSymbol', '')
            name = stock_info.get('shortName', '').split()[0]
        else:
            symbolName = stock_info.get('symbol', '')
            name = stock_info.get('shortName', '')
             
        
        stock_data = {
            'symbol': symbolName,
            'name': name,
            'previous': stock_info.get('previousClose', ''),
            'price': stock_info.get('previousClose', 0),
            'open': stock_info.get('open', ''),
            'dayLow': stock_info.get('dayLow', ''),
            'dayHigh': stock_info.get('dayHigh', ''),
            'fiftyDayAverage': stock_info.get('fiftyDayAverage', ''),
        }
    else:
        previous_close = stock_info.get('previousClose')
        current_price = stock_info.get('currentPrice')
        if current_price > previous_close:
            indicator = 'up'
        elif current_price < previous_close:
            indicator = 'down'
        else:
            indicator = 'unch'
        stock_data = {
            'symbol': stock_info.get('symbol', ''),
            'name': stock_info.get('shortName', ''),
            'price': stock_info.get('currentPrice', 0), 
            'indicator': indicator,
            'previous': previous_close,
            'dayHigh': stock_info.get('dayHigh', 0),
            'dayLow': stock_info.get('dayLow', 0), 
            'targetHighPrice': stock_info.get('targetHighPrice', 0), 
            'fiftyDayAverage': stock_info.get('fiftyDayAverage', 0), 
            'volume': stock_info.get('volume', 0), 
            'averageVolume': stock_info.get('averageVolume', 0), 
            'marketCap': stock_info.get('marketCap', 0), 
            'totalRevenue': stock_info.get('totalRevenue', 0), 
            'operatingCashflow': stock_info.get('operatingCashflow', 0), 
            
        }
        
    
    return JsonResponse(stock_data)
    

#Index  
def index_view(request):
    user = request.user


    return render(request, 'stocker/index.html',{
        'user': user,
        
    })

#Add or remove a stock from portfolio.
@login_required(login_url='login')
def add_stock(request):
    if request.method == 'POST':
        user = User.objects.get(pk= request.user.id)
        data = json.loads(request.body.decode('utf-8'))
        stock = data.get('symbol')
        action = data.get('action')
        if action == 'Add':
            add = Add(user=user, stock=stock)
            add.save()
            message={'message':'Stock added to portfolio.'}
            
        else:
            remove = Add.objects.filter(user=user, stock=stock)
            remove.delete()
            message={'message':'Stock removed from portfolio.'}

    return JsonResponse(message, status=200)

#Gets the requested index.
def get_index(request, index):
    if index == "nasdaq":
        response_data = get_nasdaq()
    elif index == "currencies":
        response_data = get_currencies()
    elif index == "futures":
        response_data = get_futures()
    return JsonResponse(response_data)

#Get Nasdaq components.
def get_nasdaq():
    #Web scraping for components data, also includes price and company name so its very suitable for a fast default page
    headers = {"User-Agent": "Mozilla/5.0"}
    res=requests.get("https://api.nasdaq.com/api/quote/list-type/nasdaq100",headers=headers)
    main_data=res.json()['data']['data']['rows']
    data =[]
    stocks = {'stocks': data}
 
    for item in main_data:
        data.append({
            "symbol": item["symbol"],
            "companyName": item["companyName"],
            "lastSalePrice": item["lastSalePrice"],
            "deltaIndicator": item["deltaIndicator"]
        })
 
    return stocks

#Get list of currencies from models and create a ticker object for each of them
def get_currencies():

    currency_list = Currency.objects.all()
    data =[]
    stocks = {'stocks': data}
 
    for currency in currency_list:
        item_ticker = yf.Ticker(str(currency))
        item = item_ticker.info
        data.append({
            "symbol": item["symbol"],
            "companyName": item["shortName"],
            "lastSalePrice": item["previousClose"]
        })
    return stocks

#Get list of futures from models and create a ticker object for each of them
def get_futures():

    future_list = Future.objects.all()

    data =[]
    stocks = {'stocks': data}
 
    for future in future_list:
        item_ticker = yf.Ticker(str(future))
        item = item_ticker.info
        data.append({
            "symbol": item["underlyingSymbol"],
            "companyName": item["shortName"].split()[0],
            "lastSalePrice": item["previousClose"]
        })
    return stocks

#Get portfolio of the user from models and create a ticker object for each of them
@login_required(login_url='login')
def get_portfolio(request):
    user= request.user
    add_objects = Add.objects.filter(user= user.id)
    data = []
    for i in add_objects:
        data.append(str(i.stock))
    

    return JsonResponse(data, safe=False)



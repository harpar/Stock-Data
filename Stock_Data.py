# Harshil Parikh

# Nov 28th, 2016

import urllib.request
import json
import time
from tkinter import *
import collections

#ONLY SUPPORT NASDAQ FOR GRAPH CURRENTLY

#Graph data provided by Bloomberg and Stock Info provided by Yahoo Inc.
tckr = input("What stock in NASDAQ price would you like? (TICKER): ")

#tckr = "AAPL"

stockinfotags = ["Price", "Open", "Ask", "Bid", "Day Range", "Volume", "Previous Close", "52-Week Range", "P/E Ratio", "EPS", "Market Cap", "Float Shares", "Price/Sales", "Dividend Share", "Dividend Yield"]

stockChartURL = "http://www.bloomberg.com/markets/chart/data/1D/" + tckr + ":US"
#INFO ORDER: PRICE(l1), OPEN(o), ASK(a), BID(b), DAY RANGE(m), VOLUME(v), PREVIOUS CLOSE(p), 52-WEEK RANGE(w), P/E RATIO(r), EARNINGS/SHARE(e), MARKET CAP(j1), FLOAT SHARES(f6), PRICE/SALES(p5), DIVIDED SHARE(d), DIVIDEND YIELD(y)
stockInfoURL = "http://finance.yahoo.com/d/quotes.csv?s=" + tckr + "&f=l1oabmvpwrej1f6p5dy"

# Getting Stock chart data and info
charthtml = urllib.request.urlopen(stockChartURL)
stockhtml = urllib.request.urlopen(stockInfoURL)

charttext = charthtml.read()
stocktext = stockhtml.read()

chartstr = charttext.decode("utf-8")
stockstr = stocktext.decode("utf-8")

# Manipulating data
chartdata = json.loads(chartstr)

stockstr = stockstr.replace(" ", "")
stockstr = stockstr.replace (",", " ")
stockstr = stockstr.replace('"', "")

stockarr = stockstr.split()

stockdata = collections.OrderedDict()
for tag in stockinfotags:
    stockdata[tag] = stockarr[stockinfotags.index(tag)]

# chartdata and stockdata are both dictionaries ready to be represented to the user
#for key, value in stockdata.items():
#   print(key + ": " + value)

#print(stockdata)
#print(chartdata)

def chartDataTimestampCheckpoints():
    times = []
    for x in chartdata['data_values']:
       epochTimeEST = x[0] + 18000000
       formatTime = time.strftime('%Y-%m-%d %H:%M', time.localtime(epochTimeEST/1000))
       times.append(formatTime)
    return times

def chartDataPriceCheckPoints():
    prices = []
    for x in chartdata['data_values']:
        prices.append(x[1])
    return prices

def getChartLowerBound():
    return stockdata['Open']

def getChartUpperBound(prices):
    return max(prices)

def drawGraph(xOrigin, yOrigin, xDist, yDist):
    marketMin = 390
    
    timestamp = chartDataTimestampCheckpoints()
    prices = chartDataPriceCheckPoints()
    

root = Tk()

width = root.winfo_screenwidth()/2
height = root.winfo_screenheight()/2

widthGraphIncrement = width + height - (width/2) + 200

labelSize = 100
counter = 0
counter2 = 0

canvas = Canvas(root, width=widthGraphIncrement, height=height)
canvas.pack()


for key in stockdata:
    keyLabel = Label(root, text = key, bg="SKYBLUE")
    x = (width/6 - labelSize) / 2 + (width/6) * counter + counter*widthGraphIncrement/50 + 10
    y = (height/10) + (height/10)*counter2*2 - 25
    keyLabel.place(x=x, y=y)
    counter += 1
    counter2 += 1
    if counter % 3 == 0:
        counter = 0
    if counter2 % 5 == 0:
        counter2 = 0

for value in stockdata.values():
    valueLabel = Label(root, text = value)
    x = (width/6 - labelSize) / 2 + (width/6) * counter + counter*widthGraphIncrement/50 + 10
    y = (height/10) + (height/10)*counter2*2
    valueLabel.place(x=x, y=y)
    counter += 1
    counter2 += 1
    if counter % 3 == 0:
        counter = 0
    if counter2 % 5 == 0:
        counter2 = 0
    
canvas.create_line(widthGraphIncrement/2, 25, widthGraphIncrement/2, height-25)
canvas.create_line(widthGraphIncrement/2, height-25, widthGraphIncrement-10, height-25)

drawGraph(widthGraphIncrement/2, height-25, widthGraphIncrement-10-widthGraphIncrement/2, height-50)

mainloop()



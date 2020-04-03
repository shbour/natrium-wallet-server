import redis, json, time, sys, requests

#rblocks = redis.StrictRedis(host='localhost', port=6379, db=0)
#rwork = redis.StrictRedis(host='localhost', port=6379, db=1)
rdata = redis.StrictRedis(host='localhost', port=6379, db=2)

currency_list = [ "ARS", "AUD", "BRL", "BTC", "CAD", "CHF", "CLP", "CNY", "CZK", "DKK", "EUR", "GBP", "HKD", "HUF", "IDR", "ILS", "INR", "JPY", "KRW", "MXN", "MYR", "NOK", "NZD", "PHP", "PKR", "PLN", "RUB", "SEK", "SGD", "THB", "TRY", "TWD", "USD", "ZAR", "SAR", "AED", "KWD" ]

coingecko_url='https://api.coingecko.com/api/v3/coins/spectresecuritycoin?localization=false&tickers=false&market_data=true&community_data=false&developer_data=false&sparkline=false'

def coingecko():
	response = requests.get(url=coingecko_url).json()
	if 'market_data' not in response:
		return
	for currency in currency_list:
		try:
			data_name = currency.lower()
			price_currency = response['market_data']['current_price'][data_name]
			print(rdata.hset("prices", "coingecko:xspc-"+data_name, price_currency),"Coingecko XSPC-"+currency, price_currency)
		except Exception:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			print('exception',exc_type, exc_obj, exc_tb.tb_lineno)
			print("Failed to get price for XSPC-"+currency.upper()+" Error")
	# Convert to VES
	usdprice = float(rdata.hget("prices", "coingecko:xspc-usd").decode('utf-8'))
	print(rdata.hset("prices", "coingecko:lastupdate",int(time.time())),int(time.time()))

coingecko()

print("Coingecko XSPC-USD:", rdata.hget("prices", "coingecko:xspc-usd").decode('utf-8'))
print("Coingecko XSPC-BTC:", rdata.hget("prices", "coingecko:xspc-btc").decode('utf-8'))
print("Last Update:          ", rdata.hget("prices", "coingecko:lastupdate").decode('utf-8'))


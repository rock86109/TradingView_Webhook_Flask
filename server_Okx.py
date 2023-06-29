from flask import Flask, request, abort
import ccxt

## Remember to set account mode! Not avaible for simple mode.


app = Flask(__name__)

# OKX API pair
api_key = ''
api_secret = ''
okx_password = ''

passwordList = ["monadanny", "mayigetyournumber?"]
# client = Client(api_key, api_secret)

ex_future = ccxt.okx({
    'apiKey': api_key,
    'secret': api_secret,
    'password': okx_password,
    'enableRateLimit': True,
    'options': { 'defaultType': 'swap'} # ←-------------- quotes and 'future'
})

@app.route("/webhook", methods=["POST"])
def webhook():
    if request.method == "POST":
        try:
            signal = request.json # TradingView Alert Message
            # print(signal)
            if signal["password"] not in passwordList:
                return "Password Not In The List!!"

            prev_side = signal["log"].split("/")[0]
            curr_side = signal["log"].split("/")[1]
            qty = signal["qty"] if "qty" in signal.keys() else 1
            symbol = signal["pair"] # "ETH-USDT-SWAP"
            print(prev_side, curr_side, qty, symbol, end=" || ")

            ## check current position
            coinInfo = ex_future.fetch_position(symbol) ## could be None
            positionAmt = float(coinInfo["info"]["pos"]) if coinInfo else 0

            # place order
            if curr_side == "long":
                if positionAmt == 0:
                    ex_future.create_market_buy_order(symbol=symbol, amount=qty)
                elif positionAmt < 0:
                    ex_future.create_market_buy_order(symbol=symbol, amount=qty-positionAmt)
                else: ## amount already > 0
                    pass
            elif curr_side == "short":
                if positionAmt == 0:
                    ex_future.create_market_sell_order(symbol=symbol, amount=qty)
                elif positionAmt > 0:
                    ex_future.create_market_buy_order(symbol=symbol, amount=qty+positionAmt)
                else: ## amount already < 0
                    pass
            elif curr_side == "flat":
                if positionAmt > 0:
                    ex_future.create_market_sell_order(symbol=symbol, amount=qty)
                elif positionAmt < 0:
                    ex_future.create_market_buy_order(symbol=symbol, amount=qty)
                else: ## amount already == 0
                    pass
            else:
                print("Not long/short/flat", end=" || ")
            print("")
            return "success", 200
        except Exception as e:
            return e
    else:
        abort(400)

@app.route("/", methods=["GET"])
def getTest():
    if request.method == "GET":
        print("request.json")
        return "success", 200
    else:
        abort(400)

if __name__ == '__main__':
    app.run(port=5001)


from flask import Flask, request, abort
from binance.client import Client

app = Flask(__name__)

api_key = ''
api_secret = ''
qty = 0.005
client = Client(api_key, api_secret)

@app.route("/webhook", methods=["POST"])
def webhook():
    if request.method == "POST":
        signal = request.json
        prev_side = signal["log"].split("/")[0]
        curr_side = signal["log"].split("/")[1]
        pair = signal["log"].split("/")[2]
        print(prev_side, curr_side, pair, end=" || ")

        ## check current position
        coinInfo = client.futures_position_information(symbol=pair)[0]
        symbol = coinInfo["symbol"]
        positionAmt = float(coinInfo["positionAmt"])

        # place order
        if curr_side == "long":
            if positionAmt == 0:
                client.futures_create_order(symbol=symbol, side="BUY", type="MARKET", quantity=qty)
            elif positionAmt < 0:
                client.futures_create_order(symbol=symbol, side="BUY", type="MARKET", quantity=qty-positionAmt)
            else: ## amount already > 0
                pass
        elif curr_side == "short":
            if positionAmt == 0:
                client.futures_create_order(symbol=symbol, side="SELL", type="MARKET", quantity=qty)
            elif positionAmt > 0:
                client.futures_create_order(symbol=symbol, side="SELL", type="MARKET", quantity=qty+positionAmt)
            else: ## amount already > 0
                pass
        elif curr_side == "flat":
            if positionAmt > 0:
                client.futures_create_order(symbol=symbol, side="SELL", type="MARKET", quantity=positionAmt)
            elif positionAmt < 0:
                client.futures_create_order(symbol=symbol, side="BUY", type="MARKET", quantity=positionAmt)
            else: ## amount already > 0
                pass
        else:
            print("Not long/short/flat", end=" || ")
        print("")
        return "success", 200
    else:
        abort(400)

# @app.route("/getTest", methods=["GET"])
# def getTest():
#     if request.method == "GET":
#         print("request.json")
#         return "success", 200
#     else:
#         abort(400)

if __name__ == '__main__':
    app.run(port=5001)


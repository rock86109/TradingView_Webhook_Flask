import requests
import json

webhook_url = "https://3cdf-203-163-199-36.jp.ngrok.io/webhook"

data = {"K": "value"}

requests.post(webhook_url, data=json.dumps(data), headers={'Content-Type':'application/json'})

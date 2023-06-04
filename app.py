from flask import Flask,request,jsonify
import requests

app = Flask(__name__)


@app.route('/',methods=['POST'])
def index():
    data = request.get_json()
    source_currency = data['queryResult']['parameters']['unit-currency']['currency']
    amount = data['queryResult']['parameters']['unit-currency']['amount']
    target_currency = data['queryResult']['parameters']['currency-name']


    conver_rate = get_conversion_factor(source_currency,target_currency)
    final_amount = amount * conver_rate

    final_amount = round(final_amount,2)

    response_chat = {
        'fulfillmentText':"{} {} is {} {}".format(amount,source_currency,final_amount,target_currency)
    }
    print(response_chat)

    return jsonify(response_chat)


def get_conversion_factor(source,target):
    url = "https://v6.exchangerate-api.com/v6/1db6ed1a785f19a422039a59/pair/{}/{}".format(source,target)

    response = requests.get(url)
    response = response.json()
    return response['conversion_rate']


if __name__ == '__main__':
    app.run(debug=True)
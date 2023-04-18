import requests
import xmltodict
from flask import Flask, jsonify, request, abort
from datetime import datetime

app = Flask(__name__)


@app.route("/GetValuteCources", methods=['POST'])
def get_valutes():
    x = request.get_json(force=True)
    request_data = request.get_json()

    try:
        date = request_data['date']
    except:
        date = datetime.now().strftime('%d/%m/%Y')

    try:
        x = datetime.strptime(date, '%d/%m/%Y')
    except:
        abort(400, 'Некорректный формат даты')
    try:
        address = request_data['address']
    except:
        abort(400, 'Адрес не передан')

    currencyCodes = request_data['currencyCodes']

    if x > datetime.now():
        abort(400, 'Дата больше сегодняшней')
    try:
        response = requests.get('{}?date_req={}'.format(address, date))
        content = response.content
        dict_content = xmltodict.parse(content)
        valutes_list = dict_content['ValCurs']['Valute']
        list_result = []
        for x in valutes_list:
            if x['CharCode'] in currencyCodes:
                float_value = float(x['Value'].replace(',', '.'))
                float_nominal = float(x['Nominal'].replace(',', '.'))
                course = float_value / float_nominal
                currency_info = {'charCode': x['CharCode'], 'course': course}
                list_result.append(currency_info)
        response_dict = {'response': list_result}
        response_json = jsonify(response_dict)
        return response_json
    except Exception as err:
        abort(500, 'Внутренняя ошибка сервиса: ' + err)


#app.run()

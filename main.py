from datetime import datetime

import requests
import xmltodict
from flask import Flask, jsonify, request, abort
from datetime import datetime

app = Flask(__name__)
@app.get("/GetValuteCources")
def get_valutes():
    date = request.args.get('date')
    try:
        x = datetime.strptime(date, '%d/%m/%Y')
    except:
        abort(400, 'Некорректный формат даты')
    if x > datetime.now():
        abort(400, 'Дата больше сегодняшней')
    try:
        response = requests.get('http://www.cbr.ru/scripts/XML_daily.asp?date_req={}'.format(date))
        content = response.content
        dict_content = xmltodict.parse(content)
        valutes_list = dict_content['ValCurs']['Valute']
        list_result = []
        for x in valutes_list:
            if x['CharCode'] in ['CNY', 'EUR', 'USD']:
                float_value = float(x['Value'].replace(',', '.'))
                float_nominal = float(x['Nominal'].replace(',', '.'))
                course = float_nominal / float_value
                currency_info = {'charCode': x['CharCode'], 'course': course}
                list_result.append(currency_info)
        response_dict = {'response': list_result}
        response_json = jsonify(response_dict)
        return response_json
    except Exception as err:
        abort(500, 'Внутренняя ошибка сервиса: '+ err)
app.run()
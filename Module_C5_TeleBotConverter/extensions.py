import requests
import json

from config import exchanges


class APIException(Exception):
    ...

class Converter:
    @staticmethod
    def get_price(base, sym, amount):
        try:
            base_key = exchanges[base.lower()]
        except KeyError:
            return APIException(f'Валюта {base} не найдена')

        try:
            sym_key = exchanges[sym.lower()]
        except KeyError:
            return APIException(f'Валюта {sym} не найдена')

        if base_key == sym_key:
            raise APIException(f'Невозможно перевести одинаковые валюты {base_key} в {sym_key}')

        try:
            amount = float(amount.replace(',', '.'))
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}')



        url = f"https://api.apilayer.com/exchangerates_data/convert?to={sym_key}&from={base_key}&amount={amount}"

        payload = {}
        headers = {"apikey": "efR44todFp5VFi9hhvl3r8MOq8K6xdPP"}

        response = requests.request("GET", url, headers=headers, data=payload)
        result = json.loads(response.content)
        new_price = result.get('result')
        return round(new_price, 2)


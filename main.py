from database_management.my_orm_base import DatabaseControl
from flask import Flask, request
import logging
import json


app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
db_control = DatabaseControl("database_management/money_database.db")


@app.route('/post', methods=['POST'])
def main():
    logging.info(f'Request: {request.json!r}')
    input_js = request.json
    cats = ["еда", "налоги", "развлечения", "одежда", "транспорт", "услуги",
            "другое"]
    input_text = input_js["request"]["command"]
    out = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }
    spending = 'потратил' in input_text
    cat = ""
    summa = 0
    user = input_js['session']['user_id']
    db_control.set_user(user)
    for string in input_text.split(" "):
        if string in cats:
            cat = string
        else:
            try:
                summa = int(string)

            except ValueError:
                pass

    if cat and summa:
        if spending:
            out["response"]["text"] =  \
                f"Хорошо, записала в категорию: {cat}, {summa} рублей"
            db_control.add_spending(summa, category=cat)
        else:
            out['response']['text'] = f'Поздравляю ' \
                                      f'с заработком: аж {summa} руб.'
            db_control.add_earning(summa)

    else:
        out["response"][
            "text"] = f"Я не расслышала, можете повторить."

    return json.dumps(out)


if __name__ == '__main__':
    app.run(port=5000, host='127.0.0.1')

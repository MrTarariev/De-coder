from database_management.my_orm_base import DatabaseControl
from flask import Flask, request
import logging
import json


app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
sessionStorage = {}
db_control = DatabaseControl("database_management/money_database.db")


@app.route('/post', methods=['POST'])
def main():
    logging.info(f'Request: {request.json!r}')

    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }
    handle_dialog(request.json, response)

    command = request.json['request']['command'].split()
    categories = [
        'еду',
        'налоги',
        'развлечения',
        'одежду',
        'транспорт',
        'услуги'
    ]
    summa = 0
    category = None
    spending = False
    asking = False
    date = None
    date_dict = {'day': None, 'month': None, 'year': None}
    previous_word = None
    db_control.set_user(request.json['session']
                        ['application']['application_id'])
    for word in command:
        try:
            if previous_word == 'за':
                date_dict['year'] = int(word)
            else:
                summa = int(word)
        except ValueError:
            if 'потратил' in word or 'расходы' in word:
                spending = True
            elif word == 'Сколько' or word == 'расходы' or word == 'доходы':
                asking = True
            elif word in categories:
                category = categories.index(word) + 1
            elif len(word.split('.')) != 1:
                date = word.split('.')
                if len(date) == 3:
                    date_dict['day'], date_dict['month'], date_dict['year'] = \
                        date[0], date[1], date[2]
                elif len(date) == 2:
                    if len(date[-1]) > 2:
                        date_dict['month'], date_dict['year'] = date[0], date[1]
            previous_word = word
    if not summa:
        response['response']['text'] = 'Извините, я вас не поняла.'
    else:
        if not asking:
            if spending:
                if not category or category not in categories:
                    category = 7
                else:
                    category = categories.index(category) + 1
                db_control.add_spending(summa, category=category)
            else:
                db_control.add_earning(summa)
            response['response']['text'] = 'Хорошо, записала'
        else:
            if spending:
                if not category:
                    if not date:
                        summa = db_control.get_spending()
                    else:
                        summa = db_control.get_spending(
                            day=date_dict['day'],
                            month=date_dict['month'],
                            year=date_dict['year']
                        )
                else:
                    category = db_control.get_category(category)
                    if not date:
                        summa = db_control.get_spending(category=category)
                    else:
                        summa = db_control.get_spending(
                            category=category,
                            day=date_dict['day'],
                            month=date_dict['month'],
                            year=date_dict['year']
                        )
                response['text'] = f'По моим данным, вы потратили {summa} руб.'
            else:
                if not date:
                    summa = db_control.get_earnings()
                else:
                    summa = db_control.get_earnings(day=date_dict['day'],
                                                    month=date_dict['month'],
                                                    year=date_dict['year'])
                response['text'] = f'По моим данным, вы заработали {summa} руб.'

    logging.info(f'Response:  {response!r}')

    return json.dumps(response)


def handle_dialog(req, res):
    user_id = req['session']['application']['application_id']

    if req['session']['new']:

        sessionStorage[user_id] = {
            'suggests': [
                "Потратился",
                "Заработал",
                "Мои расходы",
                "Мои доходы",
                "Не хочу"
            ]
        }
        res['response']['text'] = 'Привет! Давайте обсудим ваш бюджет!'
        res['response']['buttons'] = get_suggests(user_id)
        return

    if req['request']['original_utterance'].lower() in [
        'Не хочу',
        'Отстань',
        'Не буду'
    ]:
        res['response']['text'] = f'Поняла, до встречи'
        res['response']['end_session'] = True
        return


def get_suggests(user_id):
    session = sessionStorage[user_id]

    suggests = [
        {'title': suggest, 'hide': True}
        for suggest in session['suggests'][:2]
    ]
    session['suggests'] = session['suggests'][1:]

    sessionStorage[user_id] = session

    return suggests


if __name__ == '__main__':
    app.run(port=5000, host='127.0.0.1')

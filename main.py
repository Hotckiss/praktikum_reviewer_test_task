import datetime as dt


class Record:
    # В конструкторе проверяется отсутствие даты через None, поэтому правильнее сделать дефлотом именно его.
    def __init__(self, amount, comment, date=''):
        # Имена приватных полей правильнее называть с нижнего подчеркивания: self._amount = amount.
        # Это касается и всех остальных полей далее по коду
        self.amount = amount
        
        # Немного лучше инвертировать условие if, избавляясь от отрицания:
        # dt.datetime.strptime(date, '%d.%m.%Y').date() if date else dt.datetime.now().date()
        self.date = (
            dt.datetime.now().date() if
            not
            date else dt.datetime.strptime(date, '%d.%m.%Y').date())
        self.comment = comment


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today_stats = 0
        # Переменные правильно именовать с маленьких букв, например record
        for Record in self.records:
            # часто используем dt.datetime.now().date(), стоит выделить в отдельную переменную или метод класса.
            # можно пометить его как @property:
            # @property
            # def current_date(self):
            #     return dt.datetime.now().date()
            if Record.date == dt.datetime.now().date():
                # Можно today_stats += Record.amount
                today_stats = today_stats + Record.amount
                
        # Еще в качестве варианта вместо цикла с условием можно также использовать встроенные функции:
        # return sum(map(lambda rec: rec.amount, filter(lambda rec: rec.data == self.current_date)))         
        return today_stats

    def get_week_stats(self):
        week_stats = 0
        # Если есть property, то заменить на него, иначе ОК
        today = dt.datetime.now().date()
        for record in self.records:
            # if 0 <= (today - record.date).days < 7:
            if (
                (today - record.date).days < 7 and
                (today - record.date).days >= 0
            ):
                week_stats += record.amount
        return week_stats


class CaloriesCalculator(Calculator):
    # В данном случае правильнее написать комментарий к функции сверху по стандартам
    # """Получает остаток калорий на сегодня."""
    def get_calories_remained(self):  # Получает остаток калорий на сегодня
        # Переменные следует называть понятными именами, например remaining_calories_limit
        x = self.limit - self.get_today_stats()
        if x > 0:
            # \ не нужен
            return f'Сегодня можно съесть что-нибудь' \
                   f' ещё, но с общей калорийностью не более {x} кКал'
        # Не ошибка, но необязательно: при первом условии функция и так завершится.
        else:
            # Скобки излишни
            return('Хватит есть!')


class CashCalculator(Calculator):
    # Оптимистичный курс ). Можно просто 60.0.
    USD_RATE = float(60)  # Курс доллар США.
    EURO_RATE = float(70)  # Курс Евро.

    # Аргументы с валютами не нужны по заданию. Но вообще если они будут, то буквы в них допускаются только строчные.
    def get_today_cash_remained(self, currency,
                                USD_RATE=USD_RATE, EURO_RATE=EURO_RATE):
        # Я бы дефолтом считал рубли и вместо второго elif делал else.
        # Либо же делал отдельный if с рублями, а в else бросал InvalidArgument. 
        # Тогда инициализация currency_type точно состоится и не нужна заранее.
        currency_type = currency
        cash_remained = self.limit - self.get_today_stats()
        
        # Логику по определению типа валюты и ее курса можно выделить в отдельный метод.
        if currency == 'usd':
            cash_remained /= USD_RATE
            currency_type = 'USD'
        # Неконсистентно. Лучше currency.
        elif currency_type == 'eur':
            cash_remained /= EURO_RATE
            currency_type = 'Euro'
        elif currency_type == 'rub':
            # Ошибка, строго говоря нужно cash_remained /= 1.0, но тогда эта строка не имеет смысла и не нужна.
            cash_remained == 1.00
            currency_type = 'руб'
            
        # Я бы добавил перевод строки на месте этого комментария
        if cash_remained > 0:
            # Можно в 1 строку и без скобок
            return (
                # Лучше посчитать округленное значение вне строки.
                f'На сегодня осталось {round(cash_remained, 2)} '
                # Можно все разместить в предыдущей строке 
                f'{currency_type}'
            )
        elif cash_remained == 0:
            return 'Денег нет, держись'
        # можно без else, только я бы вынес из if-ов самый простой случай с == 0
        elif cash_remained < 0:
            # Для консистентности лучше тоже f-строки использовать.
            return 'Денег нет, держись:' \
                   ' твой долг - {0:.2f} {1}'.format(-cash_remained,
                                                     currency_type)

    # Просто вызов метода предка, прописывать явно не нужно.
    def get_week_stats(self):
        # Пропущен return
        super().get_week_stats()

# -*- coding: utf-8 -*-
from datetime import timedelta, date
import re
import random


class Dates():

    def get_today():
        result = date.today()
        return result

    def get_next_date():
        result = date.today() + timedelta(days=1)
        return result

    def get_next_month():
        result = date.today() + timedelta(days=30)
        return result


class TextFormat():

    def remove_html(text):
        if text is None:
            return ''
        regex = re.compile('<[^>]+>')
        return re.sub(regex, '', text)


class RandomDigits():

    def four_digits():
        data = random.randint(1000, 9999)
        return str(data)

    def six_digits():
        data = random.randint(100000, 999999)
        return str(data)

# -*- coding: utf-8 -*-
__author__ = 'Yongheng'
import sqlite3
import random

class GoPlayer:
    def __init__(self, name_cn):
        conn = sqlite3.connect('Gorating.db')
        c = conn.cursor()
        row = c.execute("select rank, country, rating from GoRatings where name_cn=(?)", (name_cn,))
        conn.commit()
        attr = row.fetchone()
        conn.close()
        self.major_win = 0
        self.major_play = 0
        self.out = False
        self.win = 0
        self.lose = 0
        self.play = 0
        if attr is None:
            self.name = name_cn
            self.rating = 3000
            self.rank = 500
            self.country = u'cn'
        else:
            self.name = name_cn
            self.country = attr[1]
            self.rating = attr[2]
            self.rank = attr[0]

    def __cmp__(self, other):
        return cmp(self.rating, other.rating)

    def win_percent(self, other):
        diff = float((other.rating - self.rating)/400.0)
        return float(1/(1 + 10**diff))

    def match(self, other):
        win_rate = self.win_percent(other)
        luck_value = random.random()
        if luck_value < win_rate:
            self.win += 1
            self.play += 1
            other.lose += 1
            other.play += 1
            flag = u'win'
        else:
            self.lose += 1
            self.play += 1
            other.win += 1
            other.play += 1
            flag = u'lose'
        return flag, luck_value, win_rate

# -*- coding:utf-8 -*-

__author__ = 'Yongheng'

import urllib2
import re
import sqlite3
import os.path

class GoRating:
    def __init__(self):
        self.base_url = 'https://www.goratings.org/'
        self.proxy_url = '87.254.212.121:8080'
        self.proxy_enabled = True
        self.db_name = 'Gorating.db'
        self.rating_table = 'Gorating'
        self.result_table = 'Result'

    def get_page(self, url):
        try:
            if self.proxy_enabled:
                proxy_support = urllib2.ProxyHandler({'https': self.proxy_url})
                opener = urllib2.build_opener(proxy_support)
                urllib2.install_opener(opener)
            content = urllib2.urlopen(url).read()
            return content.decode('UTF-8')

        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                print u"connect failed: ", e.reason
                return None

    def get_page_content(self, page_content, page_type):

        main_pattern = re.compile('</tr><tr><td class="r">(.*?)</td><td><a href="(.*?)">(.*?)</a></td><td class="c">' +
                             '<span style=".*?">(.*?)</span></td>' +
                             '<td class="c"><img src=".*?" style=".*?" alt="(.*?)" />' +
                             '</td><td>(\d{4})</td>', re.S)
        person_pattern = re.compile('<th class="r">Chinese Name</th><td>(.*?)</td>', re.S)
        result_pattern = re.compile('<tr><td>(.*?)</td><td>(\d{4})</td>\n<td>(White|Black)</td>\n<td>(.*?)</td>\n' +
                                    '<td><a href=".*?">(.*?)</a></td>\n<td>(\d{4})</td>\n' +
                                    '<td class="c"><span style=".*?">(.*?)</span></td>', re.S)
        items = []
        if page_type == 'main':
            items = re.findall(main_pattern, page_content)
        elif page_type == 'person':
            items = re.findall(person_pattern, page_content)
        elif page_type == 'result':
            items = re.findall(result_pattern, page_content)
        return items

    def store_to_db(self, items):
        if not os.path.isfile(self.db_name):
            self.prepare_db()
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute('DELETE from GoRatings')
        for item in items:
            gender = ''
            if item[3] == u'\u2642':
                gender = 'Male'
            elif item[3] == u'\u2640':
                gender = 'Female'

            c.execute("INSERT INTO GoRatings VALUES (?, ?, ?, ?, ?, ?)", (int(item[0]), item[2], item[6], gender, item[4], int(item[5])))
        conn.commit()
        for row in c.execute('SELECT * from GoRatings'):
            print row
        print c.execute('SELECT COUNT(*) from GoRatings')
        conn.close()

    def prepare_db(self):
        if os.path.isfile(self.db_name):
            return
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()

        c.execute('''CREATE TABLE GoRatings
             (rank integer, name_en text, name_cn text, gender text, country text, rating integer)''')

        c.execute("CREATE UNIQUE INDEX IF NOT EXISTS name_en ON GoRatings (name_en)")

        c.execute('''CREATE TABLE TotalResult
             (name_cn text, time text, self_rating integer, white_black text, result text
              opponent_cn_name text, opponent_rating integer)''')

        conn.commit()
        conn.close()

    def start(self):
        print 'load GoRatings'
        items = self.get_page_content(self.get_page(self.base_url), 'main')

        full_items = []
        for item in items:
            result = self.get_page(self.base_url + item[1][1:])
            name_cn = self.get_page_content(result, 'person')
            full_item = list(item)
            full_item.extend(name_cn)
            print full_item
            full_items.append(full_item)
        self.prepare_db()
        self.store_to_db(full_items)

        #person_page = self.get_page(self.base_url + items[1][1][1:])
        #results = self.get_page_content(person_page, 'result')
        #for result in results:
            #print result[0], result[1], result[2], result[3], result[4], result[5].decode('UTF-8')

spider = GoRating()
spider.start()

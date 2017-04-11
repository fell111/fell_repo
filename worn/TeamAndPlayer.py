# -*- coding: utf-8 -*-
__author__ = 'Yongheng'

from GoPlayer import GoPlayer
import random


team1 = ['苏泊尔杭州队', '朴廷桓', '连笑', '李钦诚', '邬光亚', '谢科', '陈玉侬']
team2 = ['厦门国旅联合队','柯洁', '姜东润', '牛雨田', '范胤', '蒋其润', '陈豪鑫']
team3 = ['中信北京队', '陈耀烨', '柁嘉熹', '钟文靖', '韩一洲', '申旻埈', '伊凌涛']
team4 = ['重庆地产队', '古力', '檀啸', '李轩豪', '杨鼎新', '一力辽', '韩晗']
team5 = ['民生银行北京队', '时越', '彭立尧', '陶欣然', '许嘉阳', '金志锡', '沈沛然']
team6 = ['江西新晶钛业队', '李东勋', '辜梓豪', '孙腾宇', '杨楷文', '胡跃峰', '丁世雄']
team7 = ['成都园丁控股队', '党毅飞', '古灵益', '廖元赫', '马逸超', '崔哲瀚', '彭荃']
team8 = ['辽宁觉华岛队', '孟泰龄', '唐韦星', '谢尔豪', '王泽锦', '陈正勋', '张英挺']
team9 = ['华泰证券江苏队', '芈昱廷', '黄云嵩', '童梦成', '赵晨宇', '屠晓宇', '陈翰祺']
team10 = ['山东景芝酒业队', '周睿羊', '江维杰', '范廷钰', '陈梓健', '黄昕', '侯靖哲']
team11 = ['杭州云林决破队', '申真谞', '谢赫', '丁浩', '夏晨琨', '李铭', '李翔宇']
team12 = ['上海建桥学院队', '常昊', '范蕴若', '李维清', '李喆', '安成浚', '胡耀宇']
team13 = ['广东东湖棋院队', '朴永训', '王昊洋', '安冬旭', '戎毅', '王硕', '蔡竞']
team14 = ['河南队', '李世石', '刘星', '张立', '廖行文', '陈贤', '刘曦']


class GoTeam:
    def __init__(self, team):
        self.score = 0
        self.win = 0
        self.major_win = 0
        self.major_lose = 0
        self.lose = 0
        self.win_set = 0
        self.team_name = team[0].decode('UTF-8')
        self.team_players = []
        for i in range(1, 7):
            player = GoPlayer(team[i].decode('UTF-8'))
            self.team_players.append(player)
        self.team_players.sort()
        self.team_players.reverse()
        self.vs_setting = []

    def avg_rating(self, number):
        total_rating = 0
        for i in range(0, number):
            total_rating += self.team_players[i].rating
        return int(total_rating/number)

    def __cmp__(self, other):
        return cmp(self.avg_rating(4), other.avg_rating(4))

    def arrange_vs(self):
        del self.vs_setting[:]
        temp_list = []
        for player in self.team_players:
            if player.country != u'cn':
                roll = random.random()
                if roll < 0.5:
                    player.out = True
                    continue
            temp_list.append(player)
        temp_list = temp_list[:4]
        self.vs_setting.append(temp_list.pop(0))
        random.shuffle(temp_list)
        self.vs_setting.extend(temp_list)

    def vs_result(self, other):
        print self.team_name + ' vs ' + other.team_name
        person_results = []
        for i in range(0, 4):
            result = self.vs_setting[i].match(other.vs_setting[i])
            if result[0] == u'win':
                person_results.append(1)
            else:
                person_results.append(0)
            print self.vs_setting[i].name + ' ' + result[0] + ' ' + other.vs_setting[i].name + ' '\
                  + str(result[1]) + ' ' + str(result[2])

        self.vs_setting[0].major_play += 1
        other.vs_setting[0].major_play += 1
        if person_results[0] == 1:
            self.vs_setting[0].major_win += 1
        else:
            other.vs_setting[0].major_win += 1
        single_score = sum(person_results)
        self.win_set += single_score
        other.win_set += (4 - single_score)
        if single_score > 2:
            self.score += 3
            self.win += 1
            other.lose += 1
            team_result = u'胜'
        elif single_score == 2:
            if person_results[0] == 1:
                self.score += 2
                self.major_win += 1
                other.score += 1
                other.major_lose += 1
                team_result = u'主将胜'
            else:
                self.score += 1
                other.score += 2
                self.major_lose += 1
                other.major_win += 1
                team_result = u'主将负'
        else:
            other.score += 3
            self.lose += 1
            other.win += 1
            team_result = u'负'
        print self.team_name + ' ' + team_result + ' ' + other.team_name
        print ''


Teams = [team1, team2, team3, team4, team5, team6, team7,
         team8, team9, team10, team11, team12, team13, team14]

all_teams = []
for team in Teams:
    all_teams.append(GoTeam(team))
all_teams.sort()
all_teams.reverse()

print 'initial all teams and players'
print 'team name, average elo, player1, player2, player3, player4'
for team_info in all_teams:
    team_info.arrange_vs()
    print team_info.team_name.encode('UTF-8'), team_info.avg_rating(4), team_info.team_players[0].name, team_info.team_players[1].name, \
        team_info.team_players[2].name, team_info.team_players[3].name
















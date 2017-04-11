# -*- coding:utf-8 -*-
__author__ = 'Yongheng'
import operator
import TeamAndPlayer
from TeamAndPlayer import GoTeam


class GoLeague:
    def __init__(self, all_teams):
        self.teams = []
        for team in all_teams:
            self.teams.append(team)
        self.team_seq = []

    def fixture(self, teams):
        if len(self.teams) % 2:
            self.teams.append('Day off')

        rotation = list(teams)

        fixtures = []
        for i in range(0, len(teams) - 1):
            fixtures.append(rotation)
            rotation = [rotation[0]] + [rotation[-1]] + rotation[1:-1]

        return fixtures

    def double_loop_match(self, teams, matches):
        for f in matches:
            zip(*[iter(f)]*2)

        reverse_teams = [list(x) for x in zip(teams[1::2], teams[::2])]
        reverse_teams = reduce(operator.add, reverse_teams)

        return self.fixture(reverse_teams)

    def total_match(self, teams):
        total_list = []
        first_half = self.fixture(teams)
        second_half = self.double_loop_match(teams, first_half)
        first_half.extend(second_half)
        for league_round in first_half:
            total_list.append(zip(*[iter(league_round)] * 2))
        return total_list

    def team_standing(self):
        self.team_seq = sorted(self.teams, key=lambda team: team.score, reverse=True)

    def print_seq(self):
        print '排名 队伍 积分 胜局 胜 主将胜 主将负 负'
        for i in range(1, len(self.team_seq) + 1):
            print str(i) + ', ' + self.team_seq[i - 1].team_name + ', ' + str(self.team_seq[i - 1].score)\
                  + ', ' + str(self.team_seq[i - 1].win_set) + ', ' + str(self.team_seq[i - 1].win) + ', '\
                  + str(self.team_seq[i - 1].major_win) + ', ' + str(self.team_seq[i - 1].major_lose) + ', '\
                  + str(self.team_seq[i - 1].lose)

    def person_standing(self):
        return

ChineseLeague = GoLeague(TeamAndPlayer.all_teams)
total_round = ChineseLeague.total_match(ChineseLeague.teams)
ChineseLeague.team_standing()

for rounds in total_round:
    print 'Begin new round'
    for match in rounds:
        match[0].arrange_vs()
        match[1].arrange_vs()
        match[0].vs_result(match[1])

    ChineseLeague.team_standing()
    ChineseLeague.print_seq()
    print '*******************************************************'

all_players = []
for team in ChineseLeague.teams:
    for player in team.team_players:
        all_players.append(player)


print '#############################################################'
print '姓名 胜 负 主将场次 主将胜'
player_seq = sorted(all_players, key=lambda player: player.win, reverse=True)
for i in range(1, len(player_seq) + 1):
    print str(i) + ', ' + player_seq[i - 1].name + ', ' + str(player_seq[i - 1].win) + ', '\
          + str(player_seq[i - 1].lose) + ', ' + str(player_seq[i - 1].major_play)\
          + ', ' + str(player_seq[i - 1].major_win)

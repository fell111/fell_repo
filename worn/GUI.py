#!/usr/bin/python
# -*- coding: UTF-8 -*-
import MatchesSet
import ttk
from Tkinter import *


class MainForm:
    def __init__(self, league_info):
        self.player_click_reverse = False
        self.team_click_reverse = False
        self.root1 = Tk()
        self.root2 = Tk()
        self.frame_1 = self.team_standing_frame(league_info)
        self.frame_2 = self.player_standing_frame(league_info)
        self.root1.mainloop()
        self.root2.mainloop()
        self.league_info = league_info

    def team_standing_frame(self, league_info):
        frame = Frame(self.root1)
        self.root1.title('队伍排名')
        self.root1.resizable(False, False)
        tree = ttk.Treeview(self.root1, height=len(league_info.team_seq), show="headings", columns=('排名', '队伍', '积分', '胜盘', '胜', '主将胜', '主将负', '负'))
        tree.column('排名', width=50, anchor='center')
        tree.column('队伍', width=150, anchor='center')
        tree.column('积分', width=50, anchor='center')
        tree.column('胜盘', width=50, anchor='center')
        tree.column('胜', width=50, anchor='center')
        tree.column('主将胜', width=50, anchor='center')
        tree.column('主将负', width=50, anchor='center')
        tree.column('负', width=50, anchor='center')
        tree.heading('排名', text='排名')
        tree.heading('队伍', text='队伍')
        tree.heading('积分', text='积分')
        tree.heading('胜盘', text='胜盘')
        tree.heading('胜', text='胜')
        tree.heading('主将胜', text='主将胜')
        tree.heading('主将负', text='主将负')
        tree.heading('负', text='负')

        vbar = ttk.Scrollbar(frame, orient=VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=vbar.set)
        tree.grid(row=1, column=0, sticky=NSEW)
        vbar.grid(row=0, column=1, sticky=NS)
        self.team_tree = tree
        for i in range(1, len(league_info.team_seq) + 1):
            tree.insert('', i, values=(str(i), league_info.team_seq[i-1].team_name, str(league_info.team_seq[i-1].score),
                                       str(league_info.team_seq[i-1].win_set), str(league_info.team_seq[i-1].win),
                                       str(league_info.team_seq[i-1].major_win), str(league_info.team_seq[i-1].major_lose),
                                       str(league_info.team_seq[i-1].lose)))
        tree.bind("<Button-1>", self.on_click_team)

        # manage location
        self.root1.update()
        cur_width = self.root1.winfo_reqwidth()
        cur_height = self.root1.winfo_reqheight()
        self.team_tree_width = cur_width
        self.team_tree_height = cur_height
        scn_width, scn_height = self.root1.maxsize()  # get screen width and height
        tmpcnf = '%dx%d+%d+%d' % (cur_width, cur_height, (scn_width - cur_width) / 6, (scn_height - cur_height) / 3)
        self.root1.geometry(tmpcnf)

    def player_standing_frame(self, league_info):
        frame = Frame(self.root2)
        self.root2.title('棋手排名')
        self.root1.resizable(False, False)
        columns = ('排名', '棋手', '胜', '负', '主将场次', '主将胜', '总胜率', '主将胜率')
        tree = ttk.Treeview(self.root2, height=20, show="headings", columns=columns)
        tree.column('排名', width=50, anchor='center')
        tree.column('棋手', width=80, anchor='center')
        tree.column('胜', width=50, anchor='center')
        tree.column('负', width=50, anchor='center')
        tree.column('主将场次', width=60, anchor='center')
        tree.column('主将胜', width=60, anchor='center')
        tree.column('总胜率', width=60, anchor='center')
        tree.column('主将胜率', width=60, anchor='center')
        tree.heading('排名', text='排名')
        tree.heading('棋手', text='棋手')
        tree.heading('胜', text='胜')
        tree.heading('负', text='负')
        tree.heading('主将场次', text='主将场次')
        tree.heading('主将胜', text='主将胜')
        tree.heading('总胜率', text='总胜率')
        tree.heading('主将胜率', text='主将胜率')

        tree.bind("<Button-1>", self.on_click_player)
        vbar = ttk.Scrollbar(frame, orient=VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=vbar.set)
        tree.grid(row=1, column=0, sticky=NSEW)
        vbar.grid(row=0, column=1, sticky=NS)

        all_players = []
        for team in league_info.teams:
            for player in team.team_players:
                all_players.append(player)

        all_players = sorted(all_players, key=lambda player: player.win, reverse=True)
        for i in range(1, len(all_players) + 1):
            if all_players[i-1].play == 0:
                win_rate = 0.0
            else:
                win_rate = float(all_players[i-1].win)/all_players[i-1].play
            if all_players[i-1].major_play == 0:
                major_win_rate = 0.0
            else:
                major_win_rate = float(all_players[i-1].major_win)/all_players[i-1].major_play
            tree.insert('', i, values=(str(i), all_players[i-1].name, str(all_players[i-1].win),
                                       str(all_players[i-1].lose), str(all_players[i-1].major_play),
                                       str(all_players[i-1].major_win), str("%.2f"%win_rate),
                                       str("%.2f"%major_win_rate)))
        self.player_tree = tree
        self.root2.update()
        cur_width = self.root2.winfo_reqwidth()
        cur_height = self.root2.winfo_reqheight()

        scn_width, scn_height = self.root2.maxsize()  # get screen width and height
        tmpcnf = '%dx%d+%d+%d' % (cur_width, cur_height, (scn_width - self.team_tree_width) / 4 + self.team_tree_width,
                                  (scn_height - self.team_tree_height) / 3)
        self.root2.geometry(tmpcnf)

    def on_click_player(self, event):
        region = self.player_tree.identify("region", event.x, event.y)
        column = self.player_tree.identify_column(event.x)
        if region == 'heading' and column in ['#1', '#3', '#4', '#5', '#6', '#7', '#8']:
            self.treeview_sort_column(self.player_tree, column, self.player_click_reverse)
            self.player_click_reverse = not self.player_click_reverse

    def on_click_team(self, event):
        region = self.team_tree.identify("region", event.x, event.y)
        column = self.team_tree.identify_column(event.x)
        if region == 'heading' and column in ['#1', '#3', '#4', '#5', '#6', '#7', '#8']:
            self.treeview_sort_column(self.team_tree, column, self.team_click_reverse)
            self.team_click_reverse = not self.team_click_reverse

    def treeview_sort_column(self, tv, col, reverse):
        l = [(tv.set(k, col), k) for k in tv.get_children('')]
        sort_l = sorted(l, key=lambda win: float(win[0]), reverse=reverse)
        # rearrange items in sorted positions
        for index, (val, k) in enumerate(sort_l):
            tv.move(k, '', index)

        # reverse sort next time
        # tv.heading(col, command=lambda: self.treeview_sort_column(tv, col, not reverse))

if __name__ == "__main__":
    app = MainForm(MatchesSet.ChineseLeague)





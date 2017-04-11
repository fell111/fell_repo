#!/usr/bin/python
# -*- coding: UTF-8 -*-
import MatchesSet
import Tkinter


class Display(Tkinter.Tk):
    def __init__(self, player_list):
        Tkinter.Tk.__init__(self)
        t = SimpleTable(self, len(player_list)+1, 5)
        t.pack(side="top", fill="x")
        t.set(0,0,u'棋手')
        t.set(0,1,u'胜')
        t.set(0,1,u'负')
        t.set(0,2,u'主将胜')
        t.set(0,2,u'rating')


class SimpleTable(Tkinter.Frame):
    def __init__(self, parent, rows, columns):
        # use black background so it "peeks through" to
        # form grid lines
        Tkinter.Frame.__init__(self, parent, background="black")
        self._widgets = []
        for row in range(rows):
            current_row = []
            for column in range(columns):
                label = Tkinter.Label(self, text="%s/%s" % (row, column),
                                 borderwidth=0, width=10)
                label.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
                current_row.append(label)
            self._widgets.append(current_row)

        for column in range(columns):
            self.grid_columnconfigure(column, weight=1)

    def set(self, row, column, value):
        widget = self._widgets[row][column]
        widget.configure(text=value)

if __name__ == "__main__":
    app = Display(MatchesSet.player_seq)
    app.mainloop()




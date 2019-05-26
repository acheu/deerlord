#Deer Lord Auto-Narrator

from ttk import Notebook
import Tkinter as tk
import os
import time

frameID = [0,1,2]  # Global id list for the tab frame IDs
playerList = []  # List of Player(class) that contains player info including score
gmObj = []  # Main Game Object

class frame_make(tk.Frame):
    def __init__(self, parent):
        # Frame.__init__(self, parent, background="white")
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.initUI()
    def initUI(self):
        self.parent.title("Deer Lord Narrator")
        self.pack(fill=tk.BOTH, expand=1)

class gamerules():
    """ Gamerules class. There should only be 1 gamerules object per game
    """
    def __init__(self):
        self.player_first = []
        self.player_second= []
        self.player_third = []
        self.timer_curr = 5  # Current countdown timer
        self.timer_turn = 5  # Turn time alotted, minutes
        self.turn_order = []
        self.turn_rule = 1
        self.turn_curr = 1

    def set_turnorder(self):
        """
        Turn Rule (TR):
        1: Clock Wise (left to Right of PlayerList starting first)
        2: CCW (right to left of Player List starting end)
        3: Shuffle (Player List but in a shuffled order)
        4: Random (Total random order meaning a player may have multiple turns per round)
            a seed will be used
        """
        plen = len(playerList)
        print("Player #: " + plen)
        print(self.turn_rule)
        
        if self.turn_rule == 1:  #CW
            self.turn_order = range(0, plen)
        elif self.turn_rule == 2:  #CCW
            self.turn_order = range(plen, 0, -1)
        elif self.turn_rule == 3:  #Shuffle
            rngord = range(0,plen)
            self.turn_order = shuffle(rngord)
        else:  #Random, Assume TR4 as efault
            print('Random not implemented')
            self.turn_order = range(0, plen)
        print(self.turn_order)

class player():
    """ Class that creates and manages the Player Profile
        This includes fields:
            Name, Score    
    """
    def __init__(self):
        name = ""
        score = 0
    def set_name(self,newname):

        self.name = newname
    def set_score(self,newscore):
        self.score = int(newscore)


def main():
    root = tk.Tk()
    root.geometry("620x400")
    #FIX ME: should I fix this so it's arbitrary full screen intsead of fixed?
    app = frame_make(root)
    menubar = tk.Menu(root)
    filemenu = tk.Menu(menubar, tearoff=0)
    background_image=tk.PhotoImage('deerlord_background.png')
    background_label = tk.Label(root, image=background_image)
    background_label.place(x=0,y=0, relwidth=1, relheight=1)
    #menubar.add_cascade(label='File', menu=filemenu)
    root.config(menu=menubar)
    note = Notebook(root)
    ##------------------------Setup Tab1, Players
    frameID[0] = tk.Frame(note)
    note.add(frameID[0], text='Players')
    refresh_playertab(note)
    ##------------------------Setup Tab2, Score and Narrator
    frameID[1] = tk.Frame(note)
    note.add(frameID[1], text='Game')
    refresh_gametab(note)
    ##------------------------Setup Tab3, Settings
    frameID[2] = tk.Frame(note)
    note.add(frameID[2], text='Settings')
    refresh_settingstab(note)
    #-------------------------End Tab Setup
    note.pack(fill=tk.BOTH,expand=True, side=tk.LEFT)
    #note.pack(fill=tk.X, side=tk.TOP)

    while True:
        root.update_idletasks()
        root.update()
        #Detect update player/rules flag
        time.sleep(.1)

    #FIXME: If you press the X button it throws an errro bc it can't update anymore,
        # I don't want to suprress the error
    #root.mainloop()
    # PAST THIS POINT, THE USER HAS PRESSED THE "X" CLOSE
    # BUTTON ON THE WINDOW, invoking root.destroy

def refresh_playertab(note):
    lastrow = len(playerList)+2
    # +2 accounts for last row of add layer widget and first row
    # of the Name/Score column headers
    for widget in frameID[0].winfo_children():  # Removes all the prior names and scores
        widget.destroy()
    
    tk.Label(frameID[0], text='Player').grid(row=1,
                                             column=0,
                                             sticky='n')
    tk.Label(frameID[0], text='Score').grid(row=1,
                                            column=1,
                                            sticky='n')
    tk.Label(frameID[0], text='Delete').grid(row=1,
                                            column=2,
                                            sticky='n')
    
    for itt in range(len(playerList)):
        ne = tk.Label(frameID[0], text=playerList[itt].name)
        ne.grid(row=itt+2, column=0, sticky='w')
        nf = tk.Label(frameID[0], text=playerList[itt].score)
        nf.grid(row=itt+2, column=1, sticky='w')
        fnc_deleteplayer = lambda com: lambda: removeplayer(com)
        ng = tk.Button(frameID[0], text='X',
                       command=fnc_deleteplayer(note))
        ng.grid(row=itt+2, column=2, sticky='n')
    
    txtid_name = tk.Entry(frameID[0])
    txtid_score = tk.Entry(frameID[0])
    
    txtid_name.grid(row=lastrow,column=0, sticky='w')
    txtid_score.grid(row=lastrow, column=1, stick='w')
    txtid_name.insert(0,'Name')
    txtid_score.insert(0,'0')
    fnc_addplayer = lambda com, j, k: lambda: addplayer(com, j, k)
    bt_addpl = tk.Button(frameID[0],
                         text='Add Player',
                         command=fnc_addplayer(txtid_name,txtid_score, note)).grid(row=lastrow, column=2, stick='w')

def refresh_gametab(note):
    """ This is frameID[1], the Game Tab

    """
    tk.Label(frameID[1], text=gmObj.timer_curr).grid(row=1, column=0, sticky='w')
    
def refresh_settingstab(note):
    """ This is frameID[2], the settings tab

    """
    tk.Label(frameID[2], text='Win Points:').grid(row=1, column=0, sticky='w')
    tk.Label(frameID[2], text='Order:').grid(row=2, column=0, sticky='w')
    tk.Label(frameID[2], text='Timer:').grid(row=3, column=0, sticky='w')
    
    
def removeplayer(note):
    print('this don''t do nothing yet')

def addplayer(txt_name, txt_score, note):
    name = txt_name.get()
    score = txt_score.get()
    newplayer = player()
    newplayer.set_name(name)
    newplayer.set_score(score)
    playerList.append(newplayer)
    refresh_playertab(note)

if __name__ == '__main__':
    gmObj = gamerules()  # Creates the Game Object
    main()



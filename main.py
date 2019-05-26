#Deer Lord Auto-Narrator

from ttk import Notebook
import Tkinter as tk
import os

frameID = [0,1,2]  # Global id list for the tab frame IDs
playerList = []  # List of Player(class) that contains player info including score 
turnOrder = []  # Turnorder in which the narrator will choose from Player List

class frame_make(tk.Frame):
    def __init__(self, parent):
        # Frame.__init__(self, parent, background="white")
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.initUI()
    def initUI(self):
        self.parent.title("Deer Lord Narrator")
        self.pack(fill=tk.BOTH, expand=1)

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

    root.mainloop()
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
    #frameID.append(tk.Frame(note))
    a = 1
    
def refresh_settingstab(note):
    a = 1

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
    main()



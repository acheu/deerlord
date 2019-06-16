#Deer Lord Auto-Narrator

from ttk import Notebook
import Tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from numpy import random as nprnd
from pygame import mixer
import os, sys, math
import random
import time



frameID = [0,1,2]  # Global id list for the tab frame IDs
playerList = []  # List of Player(class) that contains player info including score
gmObj = []  # Main Game Object
__location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))
background_image = __location__ + '/deerlord_background.png'
seff1 = __location__ + '/sleighbell1.mp3'
seff2 = __location__ + '/jiyt.mp3'

# Initialization parameters of the pygame.mixer
#FREQ = 48000
#BITSIZE = -16
#CHANNELS = 1
#BUFFER = 4096

class gamerules():
    """ Gamerules class. There should only be 1 gamerules object per game
    """
    def __init__(self):        
        self.player_first = []
        self.player_second= []
        self.player_third = []
        self.player_curr = []
        self.timer_curr = 300  # Current countdown timer
        self.timer_currform = ''
        self.timer_turn = 300  # Turn time alotted, seconds
        self.turn_order = []  # Lists playerList reference in order of turns
        self.turn_rule = 1  #what kind of order the playerList will cycle through
        self.turn_curr = 0  # Current playerList Turn referenced to turn_order
        self.turn_count = 0  # When the game starts, set to turn 1. Turn 0 before game starts
        self.winpoints = 10  # Amount of points to win
        self.flag_players = True
        self.flag_pause = False
        self.rootobj = []
        

    def get_turnrule(self, spec):
        modes = []
        if spec == 0:
            modes = [
                ("Clockwise", 1),
                ("Counter-CW", 2),
                ("Shuffle", 3),
                ("Random", 4),
            ]
        else:
            modes = self.turn_rule
        return modes


    def time_formatted(self):
        """
        Returns as a String the formatted time to MM:SS from the
        current seconds in obj.timer_curr
        """
        t_cursec = self.timer_curr.get()
        t_min = t_cursec/60
        t_sec = t_cursec-t_min*60
        t_form = ''
        if t_sec >= 10:
            t_form = str(t_min) + ':' + str(t_sec)
        else:
            t_form = str(t_min) + ':0' + str(t_sec)
        return t_form

    def start_game(self):
        self.turn_count = 1
        self.timer_curr.set(self.timer_turn.get())
        self.set_turnorder()
        self.timer()


    def timer(self):
        #sf = __location__ + "/sleighbells1.wav"
        if not self.flag_pause:
            if self.timer_curr.get() <= 0:
                self.timer_curr.set(self.timer_turn.get())
                __nextturn = (self.turn_curr.get()+1)%len(self.turn_order)
                self.turn_curr.set(__nextturn)
                self.turn_count = self.turn_count + 1  # Iterate turn counter
                playername = playerList[self.turn_curr.get()].name
                if playername == 'Jack':
                    playsound(seff2)
                else:
                    playsound(seff1)
            else:
                self.timer_curr.set(self.timer_curr.get() - 1)
        gmObj.rootobj.after(1000,self.timer)


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
        #print("Player #: " + str(plen))
        __rule = self.turn_rule.get()
        #print(__rule)

        if __rule == 1:  #CW
            self.turn_order = range(0, plen)
        elif __rule == 2:  #CCW
            self.turn_order = range(plen-1, -1, -1)
        elif __rule == 3:  #Shuffle
            rngord = range(0,plen)
            self.turn_order = random.sample(rngord,plen)
        else:  #Random, Assume Shuffle as default
            #print('Random not implemented')
            rngord = nprnd.randint(plen,size=500)
            self.turn_order = rngord
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

class FullScreenApp(object):
    def __init__(self, master, **kwargs):
        self.master=master
        pad=3
        self._geom='820x510+0+0'
        self.master.title('Deer Lord Narrator')
        master.geometry("{0}x{1}+0+0".format(
            master.winfo_screenwidth()-pad, master.winfo_screenheight()-pad))
        master.bind('<Escape>',self.toggle_geom)
        
    def toggle_geom(self,event):
        geom=self.master.winfo_geometry()
        print(geom,self._geom)
        self.master.geometry(self._geom)
        self._geom=geom

class frame_make(tk.Frame):
    def __init__(self, parent):
        # Frame.__init__(self, parent, background="white")
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.initUI()
    def initUI(self):
        self.parent.title("Deer Lord Narrator")
        self.pack(fill=tk.BOTH, expand=1)


def main():
    root = tk.Tk()
    #root.geometry("620x400")
    #app = frame_make(root)
    app = FullScreenApp(root)
    #mixer.init(FREQ, BITSIZE, CHANNELS, BUFFER)
    mixer.init()
    note = Notebook(root)
    gmObj.timer_curr = tk.IntVar()
    gmObj.timer_currform = tk.StringVar()
    gmObj.timer_turn = tk.IntVar()
    gmObj.turn_rule = tk.IntVar()
    gmObj.turn_curr = tk.IntVar()
    gmObj.player_first = tk.StringVar()
    gmObj.player_second = tk.StringVar()
    gmObj.player_third = tk.StringVar()
    gmObj.player_curr = tk.StringVar()
    gmObj.winpoints = tk.IntVar()
    

    gmObj.turn_curr.set(0)  # Starting player is the first one added
    gmObj.turn_rule.set(1)  # Default to Clockwise turn-rule
    gmObj.winpoints.set(10)  # Default winning points
    gmObj.player_curr.set('')
    gmObj.timer_turn.set(300)
    gmObj.rootobj = root
    ##------------------------Setup Tab1, Players
    frameID[0] = tk.Frame(note)
    note.add(frameID[0], text='Players')
    refresh_playertab(note)

    ##------------------------Setup Tab2, Score and Narrator
    frameID[1] = tk.Frame(note)
    note.add(frameID[1], text='Game')
    frameID[1].configure(background='black')
    
    #background_label.place(x=0,y=0, relwidth=1, relheight=1)
    setup_gametab(note)
    #refresh_gametab(note)
    ##------------------------Setup Tab3, Settings
    frameID[2] = tk.Frame(note)
    note.add(frameID[2], text='Settings')
    refresh_settingstab(note)
    #-------------------------End Tab Setup
    note.pack(fill=tk.BOTH,expand=True, side=tk.LEFT)
    #note.pack(fill=tk.X, side=tk.TOP)

    fnc_close = lambda com: lambda: on_closing(com)
    root.protocol("WM_DELETE_WINDOW", fnc_close(root))
    
    while True:
        try:
            root.update_idletasks()
            root.update()
            if gmObj.turn_count > 0:
                gmObj.player_curr.set(playerList[gmObj.turn_order[gmObj.turn_curr.get()]].name)
                refresh_gametab(note)
                #Detect update player/rules flag
        except:
            break

def resize_image(event):
    #FIXME: This is jank as hell, should redo to avoid globals
    global copy_backimage, background_label
    new_width = event.width
    new_height = event.height
    img_width = copy_backimage.size[0]
    img_height = copy_backimage.size[1]
    wpercent = new_width/float(img_width)
    hsize = int(float(img_height)*float(wpercent))
    image = copy_backimage.resize((new_width, hsize))
    #FIXME: Understand this resize algorithm and improve it
    
    #image = copy_backimage.resize((new_width, new_height))
    photo = ImageTk.PhotoImage(image)
    background_label.config(image = photo)
    background_label.image = photo #avoid garbage collection


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
                                            column=3,
                                            sticky='n')
    
    for itt in range(len(playerList)):
        ne = tk.Label(frameID[0], text=playerList[itt].name)
        ne.grid(row=itt+2, column=0, sticky='w')
        nf = tk.Label(frameID[0], textvariable=playerList[itt].score)
        nf.grid(row=itt+2, column=1, sticky='w')
        fnc_deleteplayer = lambda com, j: lambda: removeplayer(com, j)
        ng = tk.Button(frameID[0], text='X',
                       command=fnc_deleteplayer(note, itt))
        ng.grid(row=itt+2, column=3, sticky='n')
    
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

def start_button_press(arg):
    """
    Called to handle the Start Button press. Destroys the start button and starts the game
    """
    if len(playerList)>0:
        try:
            arg.destroy()
        except:
            print('No Button Object')
        gmObj.start_game()
    

def setup_gametab(note):
    global copy_backimage, background_label
    for widget in frameID[1].winfo_children():  # Removes all the prior names and scores
        widget.destroy()

    backimage = Image.open(background_image)
    copy_backimage = backimage.copy()
    photo= ImageTk.PhotoImage(backimage)
    
    background_label = tk.Label(frameID[1], image=photo)
    background_label.place(x=0,y=0, relwidth=1, relheight=1)
    background_label.image = photo
    
    #background_label.bind('<Configure>', resize_image)
    # Uncomment above to enable background image resizing
    
    
    st_button = []
    if gmObj.turn_count is 0:
        fnc_set = lambda: lambda: start_button_press(st_button)
        st_button = tk.Button(frameID[1], text='Start Game', command=fnc_set())
        st_button.grid(row=0,column=1)
    
    tkcounter = tk.Label(frameID[1], textvariable=gmObj.timer_currform)
    tkcounter.config(font=('Arial',44))
    tkcounter.grid(row=1, column=0, sticky='n', columnspan=10, padx=5, pady=5)
    tk.Label(frameID[1], text='Turn: ').grid(row=2, column = 0, sticky = 'w')
    tk.Label(frameID[1], textvariable=gmObj.player_curr).grid(row=2, column=1, sticky='w')
    #tk.Label(frameID[1], textvariable=gmObj.winpoints).grid(row=2,column=2, sticky='w')
    pl_offset = 4  # Row Offset
    fnc_pause = lambda almbda: toggle_pause()
    gmObj.rootobj.bind('p', fnc_pause)
    for itt in range(len(playerList)):
        i = tk.Label(frameID[1], text=playerList[itt].name)
        j = tk.Label(frameID[1], textvariable=playerList[itt].score)
        fnc_upscore = lambda com: lambda: playerList[com].score.set(playerList[com].score.get()+1)
        fnc_downscore = lambda com: lambda: playerList[com].score.set(playerList[com].score.get()-1)
        bup = tk.Button(frameID[1], text='^',
                        command=fnc_upscore(itt))
        bdwn = tk.Button(frameID[1], text='v',
                        command=fnc_downscore(itt))
        i.grid(row=pl_offset+itt, column=0, sticky='w')
        j.grid(row=pl_offset+itt, column=1, sticky='w')
        bup.grid(row=pl_offset+itt, column=2, sticky='w')
        bdwn.grid(row=pl_offset+itt, column=3, sticky='w')

def toggle_pause():
    print('Pause Toggle')
    gmObj.flag_pause = not gmObj.flag_pause
    if gmObj.flag_pause:
        messagebox.showinfo("Pause","Press OK then 'p' to unpause")
    return gmObj.flag_pause


def refresh_gametab(note):
    """ This is frameID[1], the Game Tab
    """
    __time = gmObj.time_formatted()
    gmObj.timer_currform.set(__time)
    #FIXME, I'm assumingthere's at least 1 player.
    #If needed and time, add handler for if the game started without players
    scores=[]
    for itt in range(len(playerList)):
        scores.append(playerList[itt].score)
    
    scores.sort(reverse=True)
    gmObj.player_first.set(scores[0])
    #gmObj.player_second.set(scores[1])
    #gmObj.player_third.set(scores[2])
    #FIXME this needs to be an array of player name sorted by score
    


def refresh_settingstab(note):
    """ This is frameID[2], the settings tab

    """
    gme_orders = gmObj.get_turnrule(0)  # Gets all legal Turn Rules
    gme_rle = gmObj.get_turnrule(1)  # Gets the current Turn Rule
    
    tk.Label(frameID[2], text='Win Points:').grid(row=1, column=0, sticky='w')
    tk.Label(frameID[2], text='Order:').grid(row=2, column=0, sticky='w')
    tk.Label(frameID[2], text='Turn Time:').grid(row=3, column=0, sticky='w')

    e1 = tk.Entry(frameID[2],textvariable=gmObj.winpoints)
    e2 = []
    v_rlf = []
    for txt, mode in gme_orders:
        if gme_rle == mode:
            v_rlf = 'sunken'
        else:
            v_rlf = 'raised'

        fnc_updateturn = lambda: lambda: gmObj.set_turnorder()
        #fnc_updateturn = lambda: lambda: gmObj.flag_players = True
        e2 = tk.Radiobutton(frameID[2], text = txt, value=mode, indicatoron=0,
                            relief=v_rlf, variable=gmObj.turn_rule,
                            command=fnc_updateturn())
        e2.grid(row=2,column=mode, stick='w')
    e3 = tk.Entry(frameID[2], textvariable=gmObj.timer_turn)
    
    e1.grid(row=1,column=1, stick='w')
    e3.grid(row=3,column=1, stick='w')


def removeplayer(note,itt):
    playerList.remove(playerList[itt])
    gmObj.set_turnorder()
    refresh_playertab(note)
    setup_gametab(note)
    

def addplayer(txt_name, txt_score, note):
    name = txt_name.get()
    score = txt_score.get()
    newplayer = player()
    newplayer.set_name(name)
    newplayer.score = tk.IntVar()
    newplayer.score.set(score)
    playerList.append(newplayer)
    gmObj.set_turnorder()
    refresh_playertab(note)
    setup_gametab(note)


def playsound(sf_loc):
    # play bell sound when a player changes
    #UNLESS the name is "Jack", in that case play a prerecorded voice shouting
    #"Jack, it's your turn"
    #os.system("mpg123 " + sf_loc)
    mixer.music.load(sf_loc)
    mixer.music.play()

def on_closing(root):
    try:
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            root.destroy()
    except:
        pass

if __name__ == '__main__':
    gmObj = gamerules()  # Creates the Game Object
    main()

#Deer Lord Auto-Narrator

from ttk import Notebook
import Tkinter as tk
import os

frameID = []

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
    root.geometry("620x400+150+150")
    #FIX ME: should I fix this so it's arbitrary full screen intstead of fixed?
    app = frame_make(root)
    menubar = tk.Menu(root)
    filemenu = tk.Menu(menubar, tearoff=0)
    background_image=tk.PhotoImage('deerlord_background.png')
    background_label = tk.Label(root, image=background_image)
    background_label.place(x=0,y=0, relwidth=1, relheight=1)
    #menubar.add_cascade(label='File', menu=filemenu)
    root.config(menu=menubar)
    note = Notebook(root)
    
    frameID.append(tk.Frame(note))
    note.add(frameID[0], text='Players')
    frameID.append(tk.Frame(note))
    note.add(frameID[1], text='Game')
    frameID.append(tk.Frame(note))
    note.add(frameID[2], text='Settings')
    note.pack(fill='both',expand=True)

    #refresh_tabs(note, fileloc, gameID)
    root.mainloop()
    # PAST THIS POINT, THE USER HAS PRESSED THE "X" CLOSE
    # BUTTON ON THE WINDOW, invoking root.destroy


if __name__ == '__main__':
    main()

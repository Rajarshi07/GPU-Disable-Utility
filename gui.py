from gfxutil import *
import tkinter as tk
from tkinter import messagebox

class DictLabel( tk.Frame ):
    # This class is a frame that prints a dictionary as a label.
    def __init__( self, parent, dict, colour=None ):
        tk.Frame.__init__( self, parent )
        rv=0
        self.klabels=[]
        self.vlabels=[]
        for k, v in dict.items():
            self.klabels.append( tk.Label( self, text = f"{k} :", anchor = "w", justify = "left", font = ( "Helvetica", 10, "bold" ), bg = colour ) )
            self.klabels[ rv ].grid( row = rv, column = 0, sticky = "nw" )
            self.vlabels.append( tk.Label( self, text = v, anchor = "w", justify = "left", font = ( "Helvetica", 10 ) ) )
            self.vlabels[ rv ].grid( row = rv, column = 1, sticky = "nw" )
            rv += 1
    
    def updatetext( self, dict, colour=None ):
        rv=0
        for k, v in dict.items():
            self.klabels[ rv ].config( text = f"{k} :", bg = colour )
            self.vlabels[ rv ].config( text = v )
            rv += 1


class FormattedRadio( tk.Frame ):
    # This class is a frame that enables a radio button to have a multiline formatted label.
    def __init__( self, parent, labels, variable, value, colour = None ):
        tk.Frame.__init__( self, parent )
        self.rbtn = tk.Radiobutton( self, variable = variable, value = value, width = 15, height = 10, indicatoron = 1, bg = "white" )
        self.rbtn.grid( row = 0, column = 0, sticky = "nw" )
        self.label = DictLabel( self, labels, colour )
        self.label.grid( row = 0, column = 1, sticky = "nw" )
    
    def labelupdate( self, dict, colour = None ):
        self.label.updatetext( dict, colour )


def on_closing( root ):
    if messagebox.askokcancel( " Exit", "Do you want to exit?" ):
        root.destroy()


def enable_btn_fn( displays, R, var ):
    enable( displays[ var.get() ][ "InstanceID" ] )
    R[ var.get() ].labelupdate( getDisplays()[ var.get() ], 'green')


def disable_btn_fn( displays, R, var ):
    disable(displays[ var.get() ][ "InstanceID" ])
    R[ var.get() ].labelupdate( getDisplays()[ var.get() ], 'red' )


if __name__ == '__main__':
    root = tk.Tk()
    root.title( "GPU Disable Utility" )
    root.protocol( "WM_DELETE_WINDOW", lambda : on_closing(root) )
    var = tk.IntVar()
    displays = getDisplays()
    R = []
    for i in range( len( displays ) ):
        colour = lambda : 'red' if displays[ i ][ "Status" ] == "Disabled" else 'green'
        R.append( FormattedRadio( root, labels = displays[ i ], variable = var, value = i, colour=colour() ) )
        R[ i ].pack( anchor = 'w' )
    buttonframe = tk.Frame( root )
    buttonframe.pack()
    enablebtn = tk.Button( buttonframe, text = "Enable", command = lambda : enable_btn_fn( displays, R, var ) )
    enablebtn.pack( side = tk.LEFT, anchor = tk.W )
    disablebtn = tk.Button( buttonframe, text = "Disable", command = lambda : disable_btn_fn( displays, R, var ) )
    disablebtn.pack( side = tk.LEFT, anchor = tk.W )
    root.mainloop()

# pyinstaller --uac-admin -w -F gui.py -n GPU_Utility
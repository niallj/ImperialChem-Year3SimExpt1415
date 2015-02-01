import Plot
#needed to build the button menu
from collections import OrderedDict

#Import Tk on any python version
import sys
if sys.version_info[0] < 3:
    import Tkinter as Tk
else:
    import tkinter as Tk

class MainWindow:
    class Button:
	def __init__(self, name, label, handler):
            self.name = name
            self.label = label
            self.handler = handler
            self.obj = None

    def __init__(self):
	#create the main window
        self.root = Tk.Tk()
        self.root.wm_title("PlotLAMMPS")

	#"matplotlib" frame contains the plot and the controls
        self.mpl_frame = Tk.Frame(self.root)
        self.mpl_obj = Plot.Plot(self.mpl_frame)

	#menu buttons
        self.control_frame = Tk.Frame(self.root)
        self.control_init()

        Tk.mainloop()

    def control_init(self):
        self.buttons = OrderedDict([
                ("load", self.Button("load", "Load", self._load)),
                ("unload", self.Button("unload", "Unload", self._unload)),
                ("manage", self.Button("manage", "Manage", self._manage)),
                ("quit", self.Button("quit", "Quit", self._quit)),
        ])

        import DatafileList
        self.file_list = DatafileList.DatafileList(master=self.control_frame, selectmode=Tk.SINGLE)
        self.file_list.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

        for name, button in self.buttons.iteritems():
                button.obj = Tk.Button(master=self.control_frame, text=button.label, command=button.handler)
                button.obj.pack(side=Tk.TOP, fill=Tk.BOTH)

        self.control_frame.pack(side=Tk.RIGHT, fill=Tk.Y)

    def _load(self):
        self.file_list.load()
        self.mpl_obj.replot(self.file_list.name2ds)
        return

    def _unload(self):
        self.file_list.unload()
        self.mpl_obj.replot(self.file_list.name2ds)
    
    def _manage(self):
        self.file_list.manage()
        self.mpl_obj.replot(self.file_list.name2ds)

    def _quit(self):
        self.root.quit()
        self.root.destroy()

if __name__ == "__main__":
    LMPP = MainWindow()

import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

#Import Tk on any python version
import sys
if sys.version_info[0] < 3:
    import Tkinter as Tk
else:
    import tkinter as Tk

class Plot:
    def __init__(self, frame):
        self.frame = frame
        self.figobj = Figure()
        self.ax = self.figobj.add_subplot(111)

        canvas = FigureCanvasTkAgg(self.figobj, master=self.frame)
        canvas.show()

        canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
        toolbar = NavigationToolbar2TkAgg(canvas, self.frame)
        toolbar.update()

        canvas._tkcanvas.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
        self.frame.pack(side=Tk.LEFT, fill=Tk.BOTH, expand=1)


    def replot(self, dataseries):
        self.ax.clear()

        xtitle = ""
        ytitle = ""

        for name,d in dataseries.items():
            xcol = d.columns.index(d.x_data)
            ycol = d.columns.index(d.y_data)
            xtitle = d.x_data
            ytitle = d.y_data
            l, = self.ax.plot(d.plotdata[:,xcol], d.plotdata[:,ycol], label=d.name)
            if hasattr(d, "color"):
                l.set_color(d.color)
            else:
                d.color = l.get_color()

        #display the last column titles as the axes titles
        self.ax.set_xlabel(xtitle)
        self.ax.set_ylabel(ytitle)

        handles, labels = self.ax.get_legend_handles_labels()
        self.ax.legend(handles, labels)
        self.figobj.canvas.draw()

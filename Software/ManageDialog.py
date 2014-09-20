import Dialog
import sys

if sys.version_info[0] < 3:
    import Tkinter as Tk
else:
    import tkinter as Tk

class ManageDialog(Dialog.Dialog):
	def __init__(self, parent, dataseries):
		self.ds = dataseries
		title = "Properties for plot: "+dataseries.name
		Dialog.Dialog.__init__(self, parent, title = title)

	def body(self, master):
		row = 0
		Tk.Label(master, text=self.ds.filetype).grid(row=row, columnspan=2)

		row += 1
		Tk.Label(master, text="Series name:").grid(row=row)
                self.ds_name_entry = Tk.Entry(master)
		self.ds_name_entry.insert(0, self.ds.name)
		self.ds_name_entry.grid(row=row,column=1)

		#if this is a LAMMPS log file, there might be different runs to show
		if self.ds.filetype.find("log file") and self.ds.runs > 0:
			row += 1
			Tk.Label(master, text="Display run #").grid(row=row)
			self.run_number = Tk.IntVar(master)
			self.run_number.set(self.ds.run)
			ds_run_number_opt = Tk.OptionMenu(master, self.run_number, *range(self.ds.runs+1)).grid(row=row, column=1)

		row += 1
		Tk.Label(master, text="X axis data:").grid(row=row)
		self.x_opt = Tk.StringVar(master)
		self.x_opt.set(self.ds.x_data)
		ds_x_axis_opt = Tk.OptionMenu(master, self.x_opt, *self.ds.columns).grid(row=row, column=1)

		row += 1
		Tk.Label(master, text="Y axis data:").grid(row=row)
		self.y_opt = Tk.StringVar(master)
		self.y_opt.set(self.ds.y_data)
		ds_y_axis_opt = Tk.OptionMenu(master, self.y_opt, *self.ds.columns).grid(row=row, column=1)

		return self.ds_name_entry #focus to e1

	def apply(self):
		self.ds.name = self.ds_name_entry.get()
		self.ds.x_data = self.x_opt.get()
		self.ds.y_data = self.y_opt.get()
		if hasattr(self, "run_number"):
			self.ds.change_run(self.run_number.get())

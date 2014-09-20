#Import Tk on any python version
import sys
import os.path
if sys.version_info[0] < 3:
    import Tkinter as Tk
else:
    import tkinter as Tk

class DatafileList(Tk.Listbox):
	name2ds = {}
	index2name = []
	def __init__(self, **kwargs):
		Tk.Listbox.__init__(self, **kwargs)

	def load(self):
            import tkFileDialog as tkfd
	    import tkSimpleDialog as tksd
            filename = tkfd.askopenfilename(parent=self)
            if filename:
		suggested_name = os.path.split(filename)[1]
                name = tksd.askstring("Select dataset name", "Enter a name for this dataset:", initialvalue=suggested_name)
		if name == None:
			return
		if name == "":
			import tkMessageBox
			tkMessageBox.showerror("Blank name", "Every data series must have a name.")
			return
		if name in self.name2ds.keys():
			import tkMessageBox
			tkMessageBox.showerror("Repeated Name", "Every data series must have a unique name, please try a different one.")
		else:
			import DataSeries
			self.name2ds[name] = DataSeries.DataSeries(name, filename)
			self.index2name.append(name)
			self.insert(Tk.END, name)
			self.manage(name)

	def unload(self):
            currentfile = self.curselection()
            if currentfile:
		del self.name2ds[self.get(currentfile)]
		self.index2name.pop(int(currentfile[0]))
                self.delete(currentfile)

	def manage(self, ds_name = None):
	    if not ds_name:
		    ds_name = self.getselected()
	    if ds_name:
                import ManageDialog
                ds = self.name2ds[ds_name]
		ManageDialog.ManageDialog(self, ds)
		#now update the listbox
		pos = self.index2name.index(ds_name)
		self.index2name[pos] = ds.name
		del self.name2ds[ds_name]
		self.name2ds[ds.name] = ds
		self.delete(pos)
		self.insert(pos, ds.name)

	def getselected(self):
            sel = self.curselection()
	    if sel:
                return self.get(sel)
	    else:
		return None


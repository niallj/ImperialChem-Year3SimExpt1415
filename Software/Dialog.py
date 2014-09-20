#a simple Tk Dialog class

import sys

if sys.version_info[0] < 3:
    import Tkinter as Tk
else:
    import tkinter as Tk

class Dialog(Tk.Toplevel):
    def __init__(self, parent, title = ""):
        #create the toplevel object
        Tk.Toplevel.__init__(self, parent)
        #make this window "transient"
        #such windows always overlap the main window, are hidden on minimise, etc.
        self.transient(parent)

        self.title(title)

        self.parent = parent
        self.result = None

        body = Tk.Frame(self)
        self.initial_focus = self.body(body)
        body.pack(padx=5, pady=5)

        self.buttonbox()

        #make this dialog modal
        self.grab_set()

        if not self.initial_focus:
            self.initial_focus = self

        #treat explicit closes as cancels
        self.protocol("WM_DELETE_WINDOW", self.cancel)

        #position us relative to the parent
        self.geometry("+{:d}+{:d}".format(parent.winfo_rootx()+50, parent.winfo_rooty()+50))

        #move the focus to whichever widget we want
        self.initial_focus.focus_set()

        self.wait_window(self)

    def body(self, master):
        #create dialog body
        #return whatever widget should have the initial focus
        #this should be overridden!
        pass

    def buttonbox(self):
        #adds a standard box button
        #override if you don't want them

        box = Tk.Frame(self)

        w = Tk.Button(box, text="OK", width=10, command=self.ok, default=Tk.ACTIVE)
        w.pack(side=Tk.LEFT, padx=5, pady=5)
        w = Tk.Button(box, text="Cancel", width=10, command=self.cancel)
        w.pack(side=Tk.LEFT, padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack()

    #standard button semantics
    def ok(self, event=None):
        if not self.validate():
            self.initial_focus.focus_set() #put focus back
            return

        self.withdraw()
        self.update_idletasks()

        self.apply()

        self.cancel()

    def cancel(self, event=None):
        #put focus back on parent
        self.parent.focus_set()
        self.destroy()

    def validate(self):
        return 1

    def apply(self):
        pass

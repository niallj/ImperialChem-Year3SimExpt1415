import os.path
import sys
from Tkinter import Tk
from tkFileDialog import askopenfilename
from tkFileDialog import asksaveasfilename

Tk().withdraw() #we don't want a full GUI, so don't show the root window
LAMMPS_log_filename = askopenfilename() #show the "open" dialog

base_filename = os.path.splitext(LAMMPS_log_filename)[0]
output_filename = base_filename + ".csv"

with open(LAMMPS_log_filename) as log:
    outfile = open(output_filename, "w")
    nlines = 0
    therm_output = False
    for line in log.readlines():
        if (nlines == 0 and line[0:6] != "LAMMPS"):
            print "Error! Not a LAMMPS log file!"
            sys.exit(1)
        nlines += 1

        if therm_output:
            if line[0:4] == "Loop":
                therm_output = False
                continue
            cols = line.strip().split()
            for c in cols:
                outfile.write("{},".format(c))
            outfile.write("\n")
        elif line[0:6] == "Memory":
            #next line is the output header
            therm_output = True


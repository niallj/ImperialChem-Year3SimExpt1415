import numpy as np

class DataSeries:
	def __init__(self, name, filename):
		self.name = name
		self.filename = filename

		#first check we can open the file
		f = open(filename)

		#find out what kind of file it is
		line1 = f.readline()
		if line1[0:6] == "LAMMPS":
			self.filetype = "LAMMPS log file"

			self.runs = -1
			self.run = -1
			self.all_columns = []
			col_headings_line = False
			log_data_lines = False

			self.all_plotdata = [None]
			self.plotrun = 0

			def line_start_match(line, snippet):
				return line[0:len(snippet)] == snippet

			for l in f.readlines():
				if line_start_match(l, "Memory usage per processor"):
					#then the next line will contain the column headings
					col_headings_line = True
					continue
				elif line_start_match(l, "Loop time"):
					#end of data section
					log_data_lines = False
                                elif line_start_match(l, "ERROR:"):
					#if an error occurs, stop reading
					return

				if col_headings_line:
					self.runs += 1
					self.all_columns.append(l.strip().split())
					col_headings_line = False
					log_data_lines = True
					continue
				
				if log_data_lines:
					if self.all_plotdata[self.runs] == None:
						self.all_plotdata[self.runs] = np.zeros((1,len(self.all_columns[self.runs])))
						self.all_plotdata.append(None)
					else:
						size = list(self.all_plotdata[self.runs].shape)
						size[0] += 1
						self.all_plotdata[self.runs].resize(size)

					self.all_plotdata[self.runs][-1,:] = map(float, l.strip().split())
			self.change_run(0) #show first run by default
		elif line1[0:18] == '# Spatial-averaged':
			self.filetype = "LAMMPS ave/spatial data file"
		else:
			self.filetype = "Unknown file type"

	def change_run(self, run):
		if run == self.run:
			pass

		if run > self.runs:
			run = 0

		self.run = run
		self.plotdata = self.all_plotdata[run]
		self.columns = self.all_columns[run]
		self.x_data = self.columns[0]
		self.y_data = self.columns[1]

#!C:\Users\zachc\AppData\Local\Programs\Python\Python36-32\python36.exe
#The above shebang tells the OS what program to open this script with (Python 3.6)

from tkinter import *							#Import tkinter, the base GUI classes
from tkinter import ttk							#Import ttk, the themed widgets from tkinter
from tkinter import filedialog					#Import the filedialog, which allows for the script to ask the user for files
import subprocess								#Used to run programs from this script
from subprocess import Popen					#More advanced program running
import json

newConfig = []									#This will be used to store the changes made to the config file (Which saves automatically)

#Start functions		
def Load():										#This function will load the config text file, parse it, and return the config
	with open("config.json", "r") as l:
		config =  json.load(l)
	return config
		
def Add(newPath, newAlias):										#Defines the function that adds items to the list of files and to the config
	c = {"alias": newAlias, "path": newPath}
	newConfig["files"].append(c)
	with open("config.json", "w") as j:		
		json.dump(newConfig, j)	
		
	scriptSelect["values"] = ParseFiles("alias")		#Sets the list of files in the drop-down menu to the config list
	
def Run():										#Defines the function that will launch the scripts
	p = Popen(path.get(), shell = True)	#Uses the Popen subprocess to launch the currently selected script. This needs to be tested more, but it works for batch and python files, as well as images and text.
	
def ParseFiles(arg):							#Parse the config file and return a list of the files in the config based on Alias or path. Should rename.
	parsed = []
	i = 0
	while i < len(newConfig["files"]):	#
		file = newConfig["files"][i][arg]
		parsed.append(file)
		i = i + 1
	return parsed
	
def UpdateSelected(event):
	path.set(newConfig["files"][scriptSelect.current()]["path"])
	
def AddWindow():
	def PickFile():
		winPath.set(filedialog.askopenfilename())
		win.lift()
	
	def Push():
		if winPath.get() != "":
			Add(winPath.get(), winAlias.get())
			win.destroy()
		else:
			pass
	
	win = Toplevel(root)
	win.title("Add Files And Scripts")
	winPath = StringVar()
	winAlias = StringVar()
	
	ttk.Label(win, text = "File:").grid(column = 1, row = 1, sticky = (N, W, E, S))
	fileEntry = ttk.Entry(win, width = 40, textvariable = winPath)
	fileEntry.grid(column = 2, row = 1, sticky = (N, W, E, S))
	ttk.Button(win, text = "Change File", command = PickFile).grid(column = 3, row = 1, sticky = (N, W, E, S))
	
	ttk.Label(win, text = "Name:").grid(column = 1, row = 2, sticky = (N, W, E, S))
	ttk.Entry(win, width = 40, textvariable = winAlias).grid(column = 2, row = 2, sticky = (N, W, E, S))
	
	ttk.Button(win, text = "Add script", command = Push).grid(column = 3, row = 3, sticky = (N, W, E, S))
	
newConfig = Load()								#Loads the config

#End functions

root = Tk()													#Create the GUI as root
root.title("Script Start")									#Change the window title
content = ttk.Frame(root)									#Create the frame everything will go on
content.grid(column = 0, row = 0, sticky = (N, W, E, S,))	#Add the frame to the grid

#Row one
ttk.Label(content, text = "Select Script").grid(column = 1, row = 1, sticky = (N, W, E, S))
scriptSelect = ttk.Combobox(content, width = 50)
scriptSelect["values"] = ParseFiles("alias")
scriptSelect.grid(column = 2, row = 1, sticky = (N, W, E, S))
path = StringVar()
path.set(newConfig["files"][scriptSelect.current()]["path"])
add = ttk.Button(content, text = "Add...", command = AddWindow)
add.grid(column = 3, row = 1, sticky = (N, W, E, S))


#Row Three
ttk.Label(content, text = "Current Script:").grid(column = 1, row = 3, sticky = (N, W, E, S))
ttk.Label(content, textvariable = path).grid(column = 2, row = 3, sticky = (N, W, E, S))
ttk.Button(content, text = "Run", command = Run).grid(column = 3, row = 3, sticky = (N, W, E, S))

scriptSelect.bind('<<ComboboxSelected>>', UpdateSelected)

root.mainloop()					#Start the main GUI loop
#Nothing on or after this line is run
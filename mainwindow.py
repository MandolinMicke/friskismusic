# -*- coding: utf-8 -*-
"""
Created on Fri Jul 27 14:42:13 2018

@author: Mikael
"""

from tkinter import *
import friskissongs as fsongs
import jympatypes as jtypes
import jympasong as jsong
import webbrowser
from win32api import GetSystemMetrics


class MainWindow():
	
	def __init__(self,master,songfile):
		self.songfile = songfile
		self.master = master
		self.width = GetSystemMetrics(0)
		self.height = GetSystemMetrics(1)
		if self.width > self.height:
			self.width = self.width*2/5
		else:
			self.width = self.width*2/3
		self.height = self.height*2/3
#		self.master.geometry(str(int(self.width)) + 'x' + str(int(self.height)))
		frame = Frame(self.master)
		
		
		self.fsongs = fsongs.friskissongs()
		self.fsongs.loadSongsFromYaml(songfile)
		self.master.title("Friskismusik")
		


		# bpm search critera
		
		bpmwin = LabelFrame(self.master, text="BPM sökning", padx=5, pady=3)
		bpmwin.pack(padx=10, pady=10)   

		lab = Label(bpmwin, text = "BPM" ,width=20,height=2)
		lab.grid(row=0,column=0)		
		self.bpm = Entry(bpmwin,width = 20)
		self.bpm.grid(row=1,column=0)	
		self.bpm.focus_set()
		        
		self.bpm.delete(0, END)
		self.bpm.insert(0, "0")


		lab = Label(bpmwin, text = "BPM tolerans" ,width=10,height=2)
		lab.grid(row=0,column=1)		
		
		self.bpmtol = Entry(bpmwin,width = 10)
		self.bpmtol.grid(row=1,column=1)		
		self.bpmtol.focus_set()
		        
		self.bpmtol.delete(0, END)
		self.bpmtol.insert(0, "5")
		
		self.showused = StringVar()
		check = Checkbutton(bpmwin,text = 'Visa använda', variable = self.showused)
		check.grid(row=0,column=2)	
		check.deselect()

		self.doublebpm = StringVar()
		check = Checkbutton(bpmwin,text = 'Visa Dubbla BPM', variable = self.doublebpm)
		check.grid(row=1,column=2)
		check.deselect()


		# artist seach 

		artistwin = LabelFrame(self.master, text="Sång preferenser", padx=5, pady=3)
		artistwin.pack(padx=10, pady=10)        

		lab = Label(artistwin, text = "Artist" ,width=10,height=2)
		lab.grid(row=0,column=0)		
		
		self.artist = Entry(artistwin,width = 30)
		self.artist.grid(row=1,column=0)
		self.artist.focus_set()
		        
		self.artist.delete(0, END)
		self.artist.insert(0, "")
		
		lab = Label(artistwin, text = "Song" ,width=10,height=2)
		lab.grid(row=0,column=1)		
		
		self.song = Entry(artistwin,width = 30)
		self.song.grid(row=1,column=1)		
		self.song.focus_set()
		        
		self.song.delete(0, END)
		self.song.insert(0, "")		
		
		# typer
		typewin = LabelFrame(self.master, text="Typ av musik", padx=5, pady=3)
		typewin.pack(padx=10, pady=10)        

		lab = Label(typewin, text = "Passar till" ,width=20,height=2)
		lab.grid(row=0,column=0)		
		
		self.fitsfor = StringVar()		
		self.fitsfor.set('Välj Block')
		fitsforlist = OptionMenu(typewin,self.fitsfor,*set(jtypes.blocktypes + ['Välj Block']))
		fitsforlist.grid(row=1,column=0)

		lab = Label(typewin, text = "Genre" ,width=20,height=2)
		lab.grid(row=0,column=1)		

		self.genre = StringVar()		
		self.genre.set('Välj Genre')
		genrelist = OptionMenu(typewin,self.genre,*set(jtypes.	genres + ['Välj Genre']))
		genrelist.grid(row=1,column=1)
		
		
		searchwindow = LabelFrame(self.master, text="Val", padx=1, pady=3)
		searchwindow.pack(padx=10, pady=10)
		
		Button(searchwindow, text="Sök", width=15,height = 2, command = self.search).grid(row=0,column=0)
		Button(searchwindow, text="Lägg till låt", width=15,height = 2, command = self.add_song).grid(row=0,column=1)
		Button(searchwindow, text="Stäng", width = 15, height = 2, command=frame.quit).grid(row=0, column=2)
	
	def add_song(self):
		editSong(self)
		
	def search(self):
		
		# create temporary vector of all songs				
		songsfound = [i for i in range(len(self.fsongs.allsongs))]		
		# set the BPM tolarance
		self.fsongs.tolerance = int(self.bpmtol.get())
		# search for used or not
		if self.showused.get() != "1":
			notusedindex = self.fsongs.isNotUsed(False)
			songsfound = self.comparenumvec(songsfound,notusedindex)
		
		# check artists and songs
		artistindex = self.fsongs.findArtist(self.artist.get(),False)
		songsfound = self.comparenumvec(songsfound,artistindex)
		songindex = self.fsongs.findSong(self.song.get(),False)
		songsfound = self.comparenumvec(songsfound,songindex)		
		
		# search for BPM
		bpmindex = self.fsongs.findBPM(int(self.bpm.get()),self.doublebpm.get() is "1",False)		
		songsfound = self.comparenumvec(songsfound,bpmindex)
		
		# find fits for
		if self.fitsfor.get() != 'Välj Block':
			fitindex = self.fsongs.findFitsFor(self.fitsfor.get() ,False)
			songsfound = self.comparenumvec(songsfound,fitindex)
		# find genre
		if self.genre.get() != 'Välj Genre':
			genreindex = self.fsongs.findGenre(self.genre.get() ,False)
			songsfound = self.comparenumvec(songsfound,genreindex)
		

			
		resultWindow(self,songsfound)
		

	def comparenumvec(self,refvec,newvec):
		retvec = []
		for i in refvec:
			if i in newvec:
				retvec.append(i)
		return retvec



class editSong:
	def __init__(self,masterwin,songindex = -1):
		if songindex == -1:
			self.new = True
		else:
			self.new = False
		self.songindex = songindex
		self.masterwin = masterwin
		self.t = Toplevel(masterwin.master)
		self.t.wm_title('Lägg till ny låt')
		self.t.pack_propagate(0)
		
		lab = Label(self.t, text = "Artist" ,width=10,height=2)
		lab.grid(row=0,column=0,columnspan=2)		
		
		self.artist = Entry(self.t,width = 40)
		self.artist.grid(row=1,column=0,columnspan=2)
		self.artist.focus_set()
		        
		self.artist.delete(0, END)
		self.artist.insert(0, "")
		
		lab = Label(self.t, text = "Song" ,width=10,height=2)
		lab.grid(row=2,column=0,columnspan=2)		
		
		self.song = Entry(self.t,width = 40)
		self.song.grid(row=3,column=0,columnspan=2)		
		self.song.focus_set()
		        
		self.song.delete(0, END)
		self.song.insert(0, "")

		lab = Label(self.t, text = "BPM" ,width=10,height=2)
		lab.grid(row=4,column=0,columnspan=2)		
		
		self.bpm = Entry(self.t,width = 30)
		self.bpm.grid(row=5,column=0,columnspan=2)		
		self.bpm.focus_set()
		        
		self.song.delete(0, END)
		self.song.insert(0, "")		
		
		self.isused = StringVar()
		check = Checkbutton(self.t,text = 'Redan använd', variable = self.isused)
		check.grid(row=6,column=0,columnspan=2)	
		check.deselect()
		
		self.chosen_genres = []
		self.chosen_blocks = []
	
		Button(self.t,text="Genre",width=20,height=2,command=self.addGenre).grid(row=7,column=0)
		Button(self.t,text="Block",width=20,height=2,command=self.addBlock).grid(row=7,column=1)

		lab = Label(self.t, text = "Spotify Link" ,width=10,height=2)
		lab.grid(row=8,column=0,columnspan=2)	
		self.spotifylink= Entry(self.t,width = 50)
		self.spotifylink.grid(row=9,column=0,columnspan=2)		
		self.spotifylink.focus_set()
		        
		self.spotifylink.delete(0, END)
		self.spotifylink.insert(0, "")
		
		if not self.new:
			self.artist.insert(END, self.masterwin.fsongs.allsongs[self.songindex].artist)
			self.song.insert(END, self.masterwin.fsongs.allsongs[self.songindex].song)
			self.bpm.insert(END,str(self.masterwin.fsongs.allsongs[self.songindex].bpm))
			self.spotifylink.insert(END, self.masterwin.fsongs.allsongs[self.songindex].spotifylink)
			self.chosen_genres = self.masterwin.fsongs.allsongs[self.songindex].genre
			self.chosen_blocks = self.masterwin.fsongs.allsongs[self.songindex].fits
			if self.masterwin.fsongs.allsongs[self.songindex].used:
				check.select()
		
		Button(self.t, text="Spara", width=15,height = 2, command=self.addAndSave).grid(row=10,column=0)
		Button(self.t, text="Avbryt", width=15,height = 2, command=self.t.destroy).grid(row=10,column=1)		
		
	def addGenre(self):
		editVectorVariable(self,'genre')
		
	def addBlock(self):
		editVectorVariable(self,'block')
		
	def addAndSave(self):
		artist = None
		song = None
		bpm  = None
		fits = None
		genre = None
		spotifylink = None
		used = False


		if self.artist != "":
			artist = self.artist.get()
		if self.song != "":
			song = self.song.get()
		if self.bpm != "":
			bpm = self.bpm.get()
		if self.spotifylink != "":
			spotifylink = self.spotifylink.get()
		if self.isused == "1":
			used = True
		if len(self.chosen_genres) >0:
			genre = self.chosen_genres
		if len(self.chosen_blocks) > 0:
			fits = self.chosen_blocks
		if self.new:
			self.masterwin.fsongs.addSong(artist,song,bpm,fits,genre,spotifylink,used)
		else:
			self.masterwin.fsongs.editSong(self.songindex,artist,song,bpm,fits,genre,spotifylink,used)
		
#		self.masterwin.fsongs.saveYaml(self.masterwin.songfile)
		self.t.destroy()
				
class editVectorVariable:
	def __init__(self,parentwin,type_for_edit):
		self.type_for_edit = type_for_edit
		self.parentwin = parentwin
		self.t = Toplevel(self.parentwin.masterwin.master)
		self.t.wm_title('Lägg till ny låt')
		self.t.pack_propagate(0)
		self.displaytext = StringVar()
		self.edit = StringVar()		
		if self.type_for_edit == 'genre':				
			self.edit.set(jtypes.genres[0])
			editlist = OptionMenu(self.t,self.edit,*set(jtypes.genres))
		elif self.type_for_edit == 'block':
			self.edit.set(jtypes.blocktypes[0])
			editlist = OptionMenu(self.t,self.edit,*set(jtypes.blocktypes))
			
		editlist.grid(row=0,column=0)

		Label(self.t, textvariable = self.displaytext ,width=30,height=2).grid(row=1,column=0,columnspan = 2)
		Button(self.t,text="Lägg till", width=15,height = 2, command = self.add).grid(row=0,column=1)
		Button(self.t,text="Rensa", width=15,height = 2, command = self.clear).grid(row=0,column=2)
		Button(self.t,text="Avsluta", width=15,height = 2, command = self.t.destroy).grid(row=2,column=0)
		self.setDisplayString()
	def add(self):
		if self.type_for_edit == 'genre':
			self.parentwin.chosen_genres.append(self.edit.get())
			self.parentwin.chosen_genres= list(set(self.parentwin.chosen_genres))
		elif self.type_for_edit == 'block':
			self.parentwin.chosen_blocks.append(self.edit.get())
			self.parentwin.chosen_blocks= list(set(self.parentwin.chosen_blocks))
		self.setDisplayString()
	def clear(self):
		if self.type_for_edit == 'genre':
			self.parentwin.chosen_genres = []
		elif self.type_for_edit == 'block':
			self.parentwin.chosen_blocks = []

		self.setDisplayString()
	
	def setDisplayString(self):
		dispstr = ''
		if self.type_for_edit == 'genre':
			tmplist = self.parentwin.chosen_genres
		elif self.type_for_edit == 'block':
			tmplist = self.parentwin.chosen_blocks
		for i in tmplist:
			if len(dispstr) > 0:
				dispstr += ', '
			dispstr += i
		self.displaytext.set(dispstr)
	
		
class resultWindow:
	def __init__(self,masterwin,resultsongs):
		self.resultsongs = resultsongs
		self.masterwin = masterwin
		t = Toplevel(masterwin.master)
		t.geometry(str(int(self.masterwin.width)) + 'x' + str(int(self.masterwin.height)))
		t.wm_title('Search Results')
		t.pack_propagate(0)
		self.resultlist = Listbox(t,height = 35,width = 50)
		self.resultlist.grid(row=1,rowspan=12,column=0,columnspan=2,sticky=W)
		scrollbar = Scrollbar(t, orient=VERTICAL)
		scrollbar.grid(row=1,rowspan=12,column=2,sticky=N+S+W)   
		self.resultlist.bind("<<ListboxSelect>>", self.songChosen)
		self.resultlist.config(yscrollcommand=scrollbar.set)
		scrollbar.config( command = self.resultlist.yview)
		for i in resultsongs:
			liststring = self.masterwin.fsongs.allsongs[i].artist + ' - ' + self.masterwin.fsongs.allsongs[i].song + ' - ' + str(self.masterwin.fsongs.allsongs[i].bpm)
			#print(liststring)
			self.resultlist.insert(END,liststring)
	
		Button(t, text="Edit", width=15,height = 2, command = self.addAndSave).grid(row=13,column=0)
		Button(t, text="Avbryt", width=15,height = 2, command=t.destroy).grid(row=13,column=1)
		
		self.disp_artist = StringVar()
		self.disp_song = StringVar()
		self.disp_bpm = StringVar()
		self.disp_fit = StringVar()
		self.disp_genre = StringVar()
		self.disp_spotifylink = StringVar()
		Label(t, text = "Artist" ,width=30,height=2).grid(row=1,column=3)	
		Label(t, textvariable = self.disp_artist ,width=30,height=2).grid(row=2,column=3)
		Label(t, text = "Song" ,width=30,height=2).grid(row=3,column=3)
		Label(t, textvariable = self.disp_song ,width=30,height=2).grid(row=4,column=3)
		Label(t, text = "BPM" ,width=30,height=2).grid(row=5,column=3)		
		Label(t, textvariable = self.disp_bpm ,width=30,height=2).grid(row=6,column=3)
		Label(t, text = "Block" ,width=30,height=2).grid(row=7,column=3)
		Label(t, textvariable = self.disp_fit ,width=30,height=2).grid(row=8,column=3)
		Label(t, text = "Genre" ,width=30,height=2).grid(row=9,column=3)
		Label(t, textvariable = self.disp_genre ,width=30,height=2).grid(row=10,column=3)
		Label(t, text = "Spotify Link" ,width=30,height=2).grid(row=11,column=3)	
		spotifylink = Label(t, textvariable=self.disp_spotifylink,width=30,height=2, fg="blue", cursor="hand2")
		spotifylink.grid(row=12,column=3)
		
		spotifylink.bind("<Button-1>", self.openBrowser)		
		
	def addAndSave(self):
		editSong(self.masterwin,self.resultsongs[self.resultlist.curselection()[0]])

	def songChosen(self,event):
		widget = event.widget
		selection=widget.curselection()
		
		self.disp_artist.set(self.masterwin.fsongs.allsongs[self.resultsongs[selection[0]]].artist)
		self.disp_song.set(self.masterwin.fsongs.allsongs[self.resultsongs[selection[0]]].song)
		self.disp_bpm.set(self.masterwin.fsongs.allsongs[self.resultsongs[selection[0]]].bpm)
		self.disp_fit.set(self.masterwin.fsongs.allsongs[self.resultsongs[selection[0]]].getFits())
		self.disp_genre.set(self.masterwin.fsongs.allsongs[self.resultsongs[selection[0]]].getGenres())
		self.disp_spotifylink.set(self.masterwin.fsongs.allsongs[self.resultsongs[selection[0]]].spotifylink)

	def openBrowser(self,event):
		webbrowser.open_new(event.widget.cget("text"))
		
if __name__ == '__main__':
	songfile = 'mymusik.yaml'
	master = Tk()
	MainWindow(master,songfile)
	
	master.mainloop()
	master.destroy()
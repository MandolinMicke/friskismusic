# -*- coding: utf-8 -*-
"""
Created on Fri Jul 27 14:42:13 2018

@author: Mikael
"""

from tkinter import Frame, Label, LabelFrame, Entry, END, StringVar, Checkbutton, OptionMenu, Button, Toplevel, Listbox, Scrollbar, VERTICAL, Tk, N, S, W
import friskissongs as fsongs
import jympatypes as jtypes
import jympasong as jsong
import webbrowser

import spotipy


import config

from spotipy.oauth2 import SpotifyClientCredentials
cred = SpotifyClientCredentials(config.client_id,config.secret_id)
spotify = spotipy.Spotify(client_credentials_manager = cred)


class MainWindow():
    
    def __init__(self,master,songfile):
        self.songfile = songfile
        self.master = master

        self.width = master.winfo_screenwidth()
        self.height = master.winfo_screenheight()
        if self.width > self.height:
            self.width = self.width*2/5
        else:
            self.width = self.width*2/3
        self.height = self.height*2/3
#        self.master.geometry(str(int(self.width)) + 'x' + str(int(self.height)))
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
        StringVar,Checkbutton,OptionMenu
        self.fitsfor = StringVar()        
        self.fitsfor.set('Välj Block')
        fitsforlist = OptionMenu(typewin,self.fitsfor,*set(jtypes.blocktypes + ['Välj Block']))
        fitsforlist.grid(row=1,column=0)

        lab = Label(typewin, text = "Genre" ,width=20,height=2)
        lab.grid(row=0,column=1)        

        self.genre = StringVar()        
        self.genre.set('Välj Genre')
        genrelist = OptionMenu(typewin,self.genre,*set(jtypes.    genres + ['Välj Genre']))
        genrelist.grid(row=1,column=1)
        
        
        searchwindow = LabelFrame(self.master, text="Val", padx=1, pady=3)
        searchwindow.pack(padx=10, pady=10)
        
        Button(searchwindow, text="Sök", width=15,height = 2, command = self.search).grid(row=0,column=0)
        Button(searchwindow, text="Lägg till låt", width=15,height = 2, command = self.add_song).grid(row=0,column=1)
        Button(searchwindow, text="Välj från låtlista", width=15,height = 2, command = self.from_list).grid(row=0,column=2)
        Button(searchwindow, text="Stäng", width = 15, height = 2, command=frame.quit).grid(row=0, column=3)
    
    def add_song(self):
        editSong(self)
    
    def from_list(self):
        PlaylistSearchWindow(self)
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
    def __init__(self,masterwin,songindex = None,url = None):
        if songindex == None:
            self.new = True
        else:
            self.new = False
            
        
            
        self.songindex = songindex
        self.masterwin = masterwin
        self.t = Toplevel(masterwin.master)
        self.t.wm_title('Lägg till ny låt')
        self.t.pack_propagate(0)
        
        lab = Label(self.t, text = "Spotify Link" ,width=10,height=2)
        lab.grid(row=0,column=0,columnspan=2)
        self.spotifylink= Entry(self.t,width = 25)
        self.spotifylink.grid(row=1,column=0,columnspan=1)        
        self.spotifylink.focus_set()
                
        self.spotifylink.delete(0, END)

        Button(self.t,text="Lägg till",width=10,height=1,command=self.spotifysearch).grid(row=1,column=1)
        
        lab = Label(self.t, text = "Artist" ,width=10,height=2)
        lab.grid(row=2,column=0,columnspan=2)        
        
        self.artist = Entry(self.t,width = 40)
        self.artist.grid(row=3,column=0,columnspan=2)
        self.artist.focus_set()
                
        self.artist.delete(0, END)
        self.artist.insert(0, "")
        
        lab = Label(self.t, text = "Sång" ,width=10,height=2)
        lab.grid(row=4,column=0,columnspan=2)        
        
        self.song = Entry(self.t,width = 40)
        self.song.grid(row=5,column=0,columnspan=2)        
        self.song.focus_set()
                
        self.song.delete(0, END)
        self.song.insert(0, "")
        
        lab = Label(self.t, text = "BPM" ,width=10,height=2)
        lab.grid(row=6,column=0,columnspan=2)        
        
        self.bpm = Entry(self.t,width = 30)
        self.bpm.grid(row=7,column=0,columnspan=2)        
        self.bpm.focus_set()
                
        self.song.delete(0, END)
        self.song.insert(0, "")        
        
        self.isused = StringVar()
        check = Checkbutton(self.t,text = 'Redan använd', variable = self.isused)
        check.grid(row=8,column=0,columnspan=2)    
        check.deselect()
        
        self.chosen_genres = []
        self.chosen_blocks = []
        
        Button(self.t,text="Genre",width=20,height=2,command=self.addGenre).grid(row=9,column=0)
        Button(self.t,text="Block",width=20,height=2,command=self.addBlock).grid(row=9,column=1)


        
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
        
        if url != None:
            print(url)
            self.spotifylink.insert(0, url)
            self.spotifysearch()
        else:
            self.spotifylink.insert(0, "") 
        
    def addGenre(self):
        editVectorVariable(self,'genre')
        
    def addBlock(self):
        editVectorVariable(self,'block')
        
        
    def spotifysearch(self):
        spotifylink = self.spotifylink.get()
        
        track = spotify.track(spotifylink)
        features = spotify.audio_features(spotifylink)
        
        self.artist.insert(END, ", ".join([x['name'] for x in track['artists']]))

        self.song.insert(END, track['name'])
        self.bpm.insert(END, round(features[0]['tempo']))

        
        
        
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
            bpm = int(self.bpm.get())
        if self.spotifylink != "":
            spotifylink = self.spotifylink.get()
        if self.isused.get() == "1":
            used = True
        if len(self.chosen_genres) >0:
            genre = self.chosen_genres
        if len(self.chosen_blocks) > 0:
            fits = self.chosen_blocks
        
        if self.new:
            self.masterwin.fsongs.addSong(artist,song,bpm,fits,genre,spotifylink,used)
        else:
            self.masterwin.fsongs.editSong(self.songindex,artist,song,bpm,fits,genre,spotifylink,used)
            
        self.masterwin.fsongs.saveYaml(self.masterwin.songfile)
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



      
class PlaylistSearchWindow:
    def __init__(self,masterwin):
        
        self.masterwin = masterwin
        t = Toplevel(masterwin.master)
#        t.geometry(str(int(self.masterwin.width)) + 'x' + str(int(self.masterwin.height)))
        t.wm_title('Sånger från spellista')
        t.pack_propagate(0)
        self.fulllist = []
        self.chosen = 0
        self.tracks = []
        self.resultlist = Listbox(t,height = 35,width = 50)
        self.resultlist.grid(row=1,rowspan=12,column=0,columnspan=2,sticky=W)
        scrollbar = Scrollbar(t, orient=VERTICAL)
        scrollbar.grid(row=1,rowspan=12,column=2,sticky=N+S+W)   
        self.resultlist.bind("<<ListboxSelect>>", self.songChosen)
        self.resultlist.config(yscrollcommand=scrollbar.set)
        scrollbar.config( command = self.resultlist.yview)
           
        Button(t, text="Lägg till", width=15,height = 2, command = self.addsong).grid(row=13,column=0)
        Button(t, text="Avbryt", width=15,height = 2, command=t.destroy).grid(row=13,column=1)
          
        self.spotifylist = Entry(t,width = 40)
        self.spotifylist.grid(row=1,column=3)        
        self.spotifylist.focus_set()
                
        self.spotifylist.delete(0, END)
        self.spotifylist.insert(0, "")
        Button(t, text="Hämta Låtlista", width=15,height = 2, command=self.get_list).grid(row=2,column=3)
                
        self.disp_artist = StringVar()
        self.disp_song = StringVar()
        self.disp_bpm = StringVar()
        self.disp_fit = StringVar()
        self.disp_genre = StringVar()
        self.disp_spotifylink = StringVar()
        w = 20
        

        Label(t, text = "Artist" ,width=w,height=2).grid(row=3,column=3)    
        Label(t, textvariable = self.disp_artist ,width=w,height=2).grid(row=4,column=3)
        Label(t, text = "Song" ,width=w,height=2).grid(row=5,column=3)
        Label(t, textvariable = self.disp_song ,width=w,height=2).grid(row=6,column=3)
        Label(t, text = "BPM" ,width=w,height=2).grid(row=7,column=3)        
        Label(t, textvariable = self.disp_bpm ,width=w,height=2).grid(row=8,column=3)
        Label(t, text = "Genre" ,width=w,height=2).grid(row=9,column=3)
        Label(t, textvariable = self.disp_genre ,width=w,height=2).grid(row=10,column=3)
        Label(t, text = "Spotify Link" ,width=w,height=2).grid(row=11,column=3)    
        spotifylink = Label(t, textvariable=self.disp_spotifylink,width=w,height=2, fg="blue", cursor="hand2")
        spotifylink.grid(row=12,column=3)
        
        spotifylink.bind("<Button-1>", self.openBrowser)        

    def addsong(self):
#        print(self.tracks[self.chosen]['track']['uri'])
        editSong(self.masterwin,None,self.tracks[self.chosen]['track']['uri'])
        
    def get_list(self):
        spotifylist = self.spotifylist.get()

        if 'https://' in spotifylist:
            # user = spotifylist.split(':')[2]
            # url = spotifylist.split('/')[4]
            url = spotifylist
        elif ':' in spotifylist:
            # user = spotifylist.split('/')[4]
            url = spotifylist.split(':')[2]
        else:
            print('dont know this type')
            
        results = spotify.user_playlist_tracks(config.client_id,url)
        # https://open.spotify.com/playlist/2tfOzafHixoE7xKUJS7fHV?si=9124c30f71cf4a39
        self.tracks = results['items']
        
       # Loops to ensure I get every track of the playlist
        while results['next']:
            results = spotify.next(results)
            self.tracks.extend(results['items'])
            
        
        self.fulllist = []
        for tr in self.tracks:
            artists = ' ,'.join([x['name'] for x in tr['track']['artists']])
            song = tr['track']['name']
            
            liststring = artists + ' - ' + song + ' - ' + str(round(spotify.audio_features(tr['track']['uri'])[0]['tempo']))
            self.fulllist.append(liststring)
            self.resultlist.insert(END,liststring)
        
        
    def songChosen(self,event):
        widget = event.widget
        
        selection=widget.curselection()
        self.chosen = selection[0]
        self.disp_artist.set(' ,'.join([x['name'] for x in self.tracks[self.chosen]['track']['artists']]))
        self.disp_song.set(self.tracks[self.chosen]['track']['name'])
        self.disp_bpm.set(self.fulllist[self.chosen].split(' - ')[2])
#        self.disp_genre.set(self.masterwin.fsongs.allsongs[self.resultsongs[selection[0]]].getGenres())
        self.disp_spotifylink.set(self.tracks[self.chosen]['track']['uri'])
    def openBrowser(self,event):
        webbrowser.open_new(event.widget.cget("text"))
        

        
class resultWindow:
    def __init__(self,masterwin,resultsongs):
        self.resultsongs = resultsongs
        self.masterwin = masterwin
        t = Toplevel(masterwin.master)
#        t.geometry(str(int(self.masterwin.width)) + 'x' + str(int(self.masterwin.height)))
        t.wm_title('Search Results')
        t.pack_propagate(0)
        self.resultlist = Listbox(t,height = 35,width = 70)
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
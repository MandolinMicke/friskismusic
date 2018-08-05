# -*- coding: utf-8 -*-
"""
Created on Fri Jul  6 19:11:41 2018

@author: andmika
"""
import jympasong as js

import jympatypes as jt
import yaml 

class friskissongs:
    def __init__(self):
        self.allsongs = []
        self.showused = True
        self.tolerance = 5
    def loadSongsFromTxt(self,txtfile):
   
        compfile = open(txtfile, 'r')
        for row in compfile.readlines():
            tmp = row.strip().split(';')
            
            self.allsongs.append(js.jympasong(tmp[0].strip(),tmp[1].strip(),int(tmp[2])))

            if len(tmp) > 3:
                fitsfor = tmp[3].split(',') 
                tmplist = []
                for i in fitsfor:
                    if len(i.strip()) > 0:
                        tmplist.append(i.strip())
                self.allsongs[-1].addFits(tmplist)
            if len(tmp) > 4:
                genre = tmp[4].split(',')
                tmplist = []
                for i in genre:
                    if len(i.strip()) > 0:
                        tmplist.append(i.strip())
                self.allsongs[-1].addGenre(tmplist)
            if len(tmp) > 5:
                if int(tmp[5]) == 1:
                    self.allsongs[-1].used = True

    def loadSongsFromYaml(self,yamlfile):
        file = open(yamlfile,'r')
        data = yaml.load(file)
        for s in data:
            newsong = js.jympasong()
            newsong.setValuesFromDict(s['Song'])
            self.allsongs.append(newsong)
         
        
    def saveYaml(self,yamlfile = 'mymusik.yaml'):
        printdict = [x.getYamlout() for x in self.allsongs]
        file = open(yamlfile,'w+')
        yaml.dump(printdict,file,allow_unicode = True,encoding = 'utf-8',default_flow_style = False)
        file.close()
        
    def printSongs(self,songs,printinfo = True):
        if printinfo:
            for i in songs:
                self.allsongs[i].printinfo(self.showused)
        
    def findBPMFIT(self,bpm,fit,includedouplicates = False,printinfo = True):
        bpmfound = self.findBPM(bpm,includedouplicates,False)
        fitfound = self.findFitsFor(fit,False)
        logivec = [x in bpmfound for x in fitfound]
        songs = []
        for i in range(0,len(logivec)):
            if logivec[i]:
                songs.append(fitfound[i])
        self.printSongs(songs,printinfo)
        return songs
          
    def findSong(self,songname,printinfo = True):
        songs = [songname.lower() in x.song.lower() for x in self.allsongs]
        songindex = [i for i, x in enumerate(songs) if x]
        self.printSongs(songindex,printinfo)
        return songindex
            
    def findArtist(self,artistname,printinfo = True):
        songs = [artistname.lower() in x.artist.lower() for x in self.allsongs]
        artistindex = [i for i, x in enumerate(songs) if x]
        self.printSongs(artistindex,printinfo)
        return artistindex
        
    def isNotUsed(self,printinfo = True):
        used = [not x.used for x in self.allsongs]
        usedindex = [i for i, x in enumerate(used) if x]
        self.printSongs(usedindex,printinfo)
        return usedindex
								
    def findFitsFor(self,fitsfor,printinfo = True):
        songs = [fitsfor.lower() in x.fits for x in self.allsongs]
        songindex = [i for i, x in enumerate(songs) if x]
        self.printSongs(songindex,printinfo)
        return songindex
       
    def findGenre(self,genre,printinfo = True):
        songs = [genre.lower() in x.genre for x in self.allsongs]
        songindex = [i for i, x in enumerate(songs) if x]
        self.printSongs(songindex,printinfo)
        return songindex
       
    
    def findBPM(self,wantedbpm,includedouplicates=False,printinfo = True):
				
        if wantedbpm == 0:
            allindex = [i for i in range(len(self.allsongs))]
        else:
	         retindexmain = self.findsingleBPM(wantedbpm,self.tolerance,[])
	         self.printSongs(retindexmain,printinfo)
	            
	         if includedouplicates:
	             retindexdouble = self.findsingleBPM(wantedbpm*2,self.tolerance*2,[])
	             retindexhalf = self.findsingleBPM(wantedbpm/2,self.tolerance/2,[])
	             self.printSongs(retindexdouble,printinfo)
	             self.printSongs(retindexhalf,printinfo)     
	             allindex = retindexmain + retindexhalf + retindexdouble
	         else:
	             allindex = retindexmain
            
        return allindex
    def findsingleBPM(self,wantedbpm, tol = 5,retindex = []):
        logicalvector = [abs(x.bpm -wantedbpm) < tol for x in self.allsongs]
        return [i for i, x in enumerate(logicalvector) if x]
    
    def addSong(self,artist = None,song = None,bpm = None,fits = None,genre = None,spotifylink = None,used=None):
        if (True not in [(x.artist == artist and x.song == song) for x in self.allsongs]):
	        self.allsongs.append(js.jympasong(artist,song,bpm,fits,genre,spotifylink,used))
        else:
	        print('song already exists')

    def editSong(self,index,artist = None,song = None,bpm = None,fits = None,genre = None,spotifylink = None,used = None):
        if artist:
            self.allsongs[index].artist = artist
        if song:
            self.allsongs[index].song = song
        if bpm:
            self.allsongs[index].bpm = bpm
        if fits:
            self.allsongs[index].fits = []
            self.allsongs[index].addFits(fits)
        if genre:
            self.allsongs[index].genre = []
            self.allsongs[index].addGenre(genre)
        if spotifylink:
            self.allsongs[index].spotifylink = spotifylink
        if used:
            self.allsongs[index].used = used

if __name__ == '__main__':
    songfile = 'mymusik.yaml'
    mylist = friskissongs()
    
    mylist.loadSongsFromYaml(songfile)

    mylist.showused = False
    mylist.tolerance = 5
        
        
                
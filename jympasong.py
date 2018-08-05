# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 20:38:54 2018

@author: andmika
"""

import jympatypes as jt

class jympasong:
    
    def __init__(self,artist = '',song= '',bpm = 0,fitsinp = None,genreinp = None,spotifylink = '',used = False):
        self.artist = artist
        self.song = song
        self.bpm = bpm
        self.genre = []
        self.fits = []
        if genreinp is not None:
            self.addGenre(genreinp)
        if fitsinp is not None:
            self.addFits(fitsinp)
        self.spotifylink = spotifylink
        self.used = used

                
    def addGenre(self,genre):
        for i in genre:
            if i.lower() in jt.genres:
                self.genre.append(i)	
            else:
                print(i + ' is not a valid genre')
    
           
    def addFits(self,fit):
        for f in fit:
            if f in jt.blocktypes:
                self.fits.append(f)
            else:
                print(f + ' is not a valid type')
        
    def setBPM(self,bpm):
        self.bpm = bpm
    
    def setValuesFromDict(self,dict):
        for i in dict.keys():
            if 'artist' == i:
                self.artist = dict[i]
            if 'song' == i:
                self.song  = dict[i]
            if 'bpm' == i:
                self.bpm = dict[i]
            if 'genre' == i:
                self.addGenre(dict[i])
            if 'fits' == i:
                self.addFits(dict[i])
            if 'used' == i:
                self.used = dict[i]
            if 'spotifylink' == i:
                self.spotifylink = dict[i]
                
                
    def printinfo(self,showused = True):
        
        if showused or not self.used:
            print(self.artist + '; ' + self.song + '; ' + str(self.bpm) + '; ' + self.getGenres() + '; ' + self.getFits() + '; ' +self.spotifylink)
            
    def getGenres(self):
        genres = ''
        for i in self.genre:
            if len(genres) == 0:
                genres += i
            else:
                genres += ', ' + i
        return genres

    def getFits(self):
        fitss = ''
        for i in self.fits:
            if len(fitss) == 0:
                fitss += i
            else:
                fitss += ', ' + i
        return fitss
								
    def getYamlout(self):
        retdict = dict()
        retdict['Song'] = dict()
        retdict['Song']['used'] = self.used
        if self.artist:
            retdict['Song']['artist'] = self.artist
        if self.song:
            retdict['Song']['song'] = self.song
        if self.bpm:
            retdict['Song']['bpm'] = self.bpm
        if self.genre:
            retdict['Song']['genre'] = self.genre
        if self.fits:
            retdict['Song']['fits'] = self.fits
        if self.spotifylink:
            retdict['Song']['spotifylink'] = self.spotifylink
        
        return retdict
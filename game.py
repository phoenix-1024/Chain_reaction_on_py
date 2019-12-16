#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 26 20:52:05 2019

@author: sudesh
"""

RED = 'red'
BLUE = 'blue'
CLS = 'cls'



class atoms:
    
    
      #state variable MAT value of(1,6) will be at MAT[1][6]
    colorMAT = [['cls', 'cls', 'cls', 'cls', 'cls', 'cls', 'cls', 'cls'],['cls', 'cls', 'cls', 'cls', 'cls', 'cls', 'cls', 'cls'],['cls', 'cls', 'cls', 'cls', 'cls', 'cls', 'cls', 'cls'],['cls', 'cls', 'cls', 'cls', 'cls', 'cls', 'cls', 'cls'],['cls', 'cls', 'cls', 'cls', 'cls', 'cls', 'cls', 'cls'],['cls', 'cls', 'cls', 'cls', 'cls', 'cls', 'cls', 'cls'],['cls', 'cls', 'cls', 'cls', 'cls', 'cls', 'cls', 'cls'],['cls', 'cls', 'cls', 'cls', 'cls', 'cls', 'cls', 'cls']]
    MAT = [[0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0]]
    maxMAT = [[1,2,2,2,2,2,2,1],[2, 3, 3, 3, 3, 3, 3, 2],[2, 3, 3, 3, 3, 3, 3, 2],[2, 3, 3, 3, 3, 3, 3, 2],[2, 3, 3, 3, 3, 3, 3, 2],[2, 3, 3, 3, 3, 3, 3, 2],[2, 3, 3, 3, 3, 3, 3, 2],[1,2,2,2,2,2,2,1]]
    windit = {(1,0):RED,(1,1):CLS,(0,1):BLUE}
    def add_atom(self,cord,col) :
        #cord should be list with cordinate x,y int eg: [1,2]
        x = cord[0]
        y = cord[1]
        self.MAT[x][y] = self.MAT[x][y] + 1
        self.colorMAT[x][y] = col
        self.check_explode(self,cord,col)
        
    def check_explode(self,cord,col):     #checks if the given box will explode if so
                                        #it will explode
        x = cord[0]
        y = cord[1]
        explod = []
        ew = []
        if self.MAT[x][y] > self.maxMAT[x][y] :
            self.MAT[x][y] = self.MAT[x][y] - self.maxMAT[x][y] -1
            if self.MAT[x][y] ==0:
                self.colorMAT[x][y] = CLS
            ew = [[x,y+1],[x+1,y],[x-1,y],[x,y-1]]
            for e in ew:
                if e[0] >= 0 and e[1] >= 0 and e[0] < 8 and e[1] < 8 :
                    explod = explod +[e]
        for e in explod:
            self.add_atom(self,e,col)
    
    def check_win(self):       #sees all boxes and dicides wether anyone has won
        r = 0
        b = 0
        for a in self.colorMAT:
            for n in a:
                if n == RED and r==0:
                    r = 1
                elif n == BLUE and b==0:
                    b = 1
        return self.windit[(r,b)]         
    
    
    def avalible(self,cord,col):                # checks if that box is avalible returns true or false
        if self.colorMAT[cord[0]][cord[1]] == col or self.colorMAT[cord[0]][cord[1]] ==CLS:
            return True
        else:
            return False
            
    
    

def main():
    a = atoms
    colch = {RED:BLUE,BLUE:RED,CLS:RED}
    col = CLS
    win = CLS
    first = 0
    while win==CLS :
        col = colch[col]
        
        chance=0
        while chance ==0:
            x= int(input('enter the x cordinate for '+col+' '))
            y= int(input('enter the y cordinate for '+col+' '))
            if atoms.avalible(a,[x,y],col) == True :
                atoms.add_atom(a,[x,y],col)
                chance =1
        
        win = atoms.check_win(a)
        while first == 0:
            win = CLS
            first = 1
        print(a.MAT)
        print(a.colorMAT)
    print(win+' has won the game')
    
    
main()
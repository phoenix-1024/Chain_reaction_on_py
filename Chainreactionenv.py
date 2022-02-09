import gym
from gym import spaces
import numpy as np

class ChainReactionEnv(gym.Env):
    """Custom Environment that follows gym interface"""
    metadata = {'render.modes': ['human']}
    RED = -1
    BLUE = +1
    CLS = 0
    def __init__(self,size):
        super(ChainReactionEnv, self).__init__()
        # Define action and observation space
        # They must be gym.spaces objects
        # Example when using discrete actions:
        RED = -1
        BLUE = +1
        CLS = 0
        self.size = size
        self.colorMAT = np.zeros(size,int) #color matrix tells color of the atom
        self.MAT = np.zeros(size,int) #atoms matrix tells the number of atoms in each position
        self.maxMAT = np.zeros(size,int) #max value of each position in atoms matrix 
        self.maxMAT[:,:] = 3 # three for all
        print(self.maxMAT)
        self.maxMAT[:,0] = 2 # two at the edges
        self.maxMAT[:,size[1]-1] = 2
        self.maxMAT[0,:] = 2
        self.maxMAT[size[0]-1,:] = 2
        self.maxMAT[0,0] = 1 # one at the cornors
        self.maxMAT[0,size[1]-1] = 1
        self.maxMAT[size[0]-1,0] = 1
        self.maxMAT[size[0]-1,size[1]-1] = 1
        
        self.windit = {(1,0):RED,(1,1):CLS,(0,1):BLUE}
        self.action_space = spaces.Box(low= -1, high=5,
                                            shape=(2, size[0], size[1]), dtype=np.uint8)
        # Example for using image as input (channel-first; channel-last also works):
        self.observation_space = spaces.Box(low=0, high=255,
                                            shape=(2, size[0], size[1]), dtype=np.uint8)

    def add_atom(self,cord,col) :
        #cord should be list with cordinate x,y int eg: [1,2]
        x = cord[0]
        y = cord[1]
        self.MAT[x,y] = self.MAT[x,y] + 1
        self.colorMAT[x,y] = col
        
    def check_explode(self,cord,col):     #checks if the given box will explode if so
                                        #it will explode
        x = cord[0]
        y = cord[1]
        explod = []
        ew = []
        if self.MAT[x,y] > self.maxMAT[x,y] :
            self.MAT[x,y] = self.MAT[x,y] - self.maxMAT[x,y] -1
            if self.MAT[x,y] ==0:
                self.colorMAT[x,y] = CLS
            ew = [[x,y+1],[x+1,y],[x-1,y],[x,y-1]]
            for e in ew:
                if e[0] >= 0 and e[1] >= 0 and e[0] < 8 and e[1] < 8 :
                    explod = explod +[e]
                    self.add_atom(self,e,col)
        for e in explod:
            check_explode(self,e,col)
    
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
        if self.colorMAT[cord[0],cord[1]] == col or self.colorMAT[cord[0],cord[1]] ==CLS:
            return True
        else:
            return False

    def step(self, action):

        colch = {RED:BLUE,BLUE:RED,CLS:RED}
        col = CLS
        win = CLS
        first = 0
        col = colch[col] #red to move first
        
        chance=0
        while chance ==0:
            x= int(input('enter the x cordinate for '+col+' '))
            y= int(input('enter the y cordinate for '+col+' '))
            if self.avalible(a,[x,y],col) == True :
                self.add_atom(a,[x,y],col)
                chance =1
    
        win = self.check_win(a)
        while first == 0:
            win = CLS
            first = 1
        #print(a.MAT)
        #print(a.colorMAT)y
        #print(win+' has won the game')
        return observation, reward, done, info

    def reset(self):
        self.colorMAT = np.zeros(size,int) #color matrix tells color of the atom
        self.MAT = np.zeros(size,int) #atoms matrix tells the number of atoms in each position
        self.maxMAT = np.zeros(size,int) #max value of each position in atoms matrix 
        self.maxMAT = 3 # three for all
        self.maxMAT[:,0] = 2 # two at the edges
        self.maxMAT[:,size[1]-1] = 2
        self.maxMAT[0,:] = 2
        self.maxMAT[size[0]-1,:] = 2
        self.maxMAT[0,0] = 1 # one at the cornors
        self.maxMAT[0,size[1]-1] = 1
        self.maxMAT[size[0]-1,0] = 1
        self.maxMAT[size[0]-1,size[1]-1] = 1
        
        return observation  # reward, done, info can't be included
    
    def render(self, mode='human'):
        ...
    
    def close (self):
        ...
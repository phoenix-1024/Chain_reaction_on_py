import gym
from gym import spaces
import numpy as np
from collections import deque

RED = -1
BLUE = +1
CLS = 0
num2color = {-1 : "RED", +1 : 'BLUE',0 : "cls" }
colch = {RED:BLUE,BLUE:RED,CLS:RED}

class ChainReactionEnv(gym.Env):
    """Custom Environment that follows gym interface"""
    metadata = {'render.modes': ['human']}
    
    def __init__(self,size):
        super(ChainReactionEnv, self).__init__()

        self.size = size
        _ = self.reset()
        self.may_explode = deque() # list of potential locations whrer an explosion may occure
        self.col = 0
        # Define action and observation space
        # They must be gym.spaces objects
        # Example when using discrete actions:
        # action space coordinate (x,y)
        self.times_added = 0
        self.action_space = spaces.Box(low=np.array([0,0]),high = np.array([size[0],size[1]])) #spaces.Tuple((spaces.Discrete(self.size[0]), spaces.Discrete(self.size[1])))
        # observation_space first chanell for agent color second for position and no. of atoms
        self.observation_space = spaces.Box(low=-1, high=10,
                                            shape=(2, size[0], size[1]), dtype=np.int64)

    def add_atom(self,cord) :
        #cord should be list with cordinate x,y int eg: [1,2]
        #print("adding atom at", cord)
        
        x = cord[0]
        y = cord[1]
        # for testing un comment this if you want things to stop after certain steps
        self.times_added += 1
        #if self.times_added  >= 100:
         #   exit()
    
        try:
            self.MAT[x,y] = self.MAT[x,y] + 1
            self.colorMAT[x,y] = self.col
            #print(self.col)
            if cord not in self.may_explode:
                self.may_explode.appendleft(cord)
        except:
            pass
        
        
        
    def check_n_explode(self):     #checks if the given box will explode if so
                                        #it will explode
        
        while len(self.may_explode) > 0 and self.check_win() == False:
            cord = self.may_explode.pop() #get the right most value
            x = cord[0]
            y = cord[1]
            if self.MAT[x,y] > self.maxMAT[x,y] :
                self.MAT[x,y] = self.MAT[x,y] - self.maxMAT[x,y] -1
                if self.MAT[x,y] ==0:
                    self.colorMAT[x,y] = CLS
            
                for e in [[x,y+1],[x+1,y],[x-1,y],[x,y-1]]:
                    if e[0] >= 0 and e[1] >= 0 and self.size[0] - e[0] -1 >= 0 and self.size[1] - e[1] -1 >= 0 :
                        self.add_atom(e)
                    
    
    def check_win(self):       #sees all boxes and dicides wether anyone has won
        '''
        checks if anyone has won the game i.e. if agent has successfully eliminated the opponent

        input:
        --
        output:
        done = True/False
        '''
        r = 0
        b = 0
        for a in self.colorMAT:
            for n in a:
                if n == RED and r==0:
                    r = 1
                elif n == BLUE and b==0:
                    b = 1

        if r - b == 0:
            done = False
        else :
            done = True

        return done    
    
    
    def avalible(self,cord,col):                # checks if that box is avalible returns true or false
        if self.colorMAT[cord[0],cord[1]] == col or self.colorMAT[cord[0],cord[1]] ==CLS:
            return True
        else:
            return False

    def step(self, action):
        ''' 
        input:
        action - location of where to put the next atom

        output:
        observation - I am thinking more of a [x,x,2] with second channel to tell the ownership of atoms
        reward - 0(maybe -1) for nothing +-100 at win/loss and -200 for trying to tuch your opponents atoms
        done - True when the game is done
        info - ????
        '''
        self.col = colch[self.col] #red to move first
        #print("step adding atom")
        self.add_atom(action)
        self.check_n_explode()
        done = self.check_win()
        if done == True:
            reward = 100
        else :
            reward = -5
        
        self.observation = np.array([self.colorMAT , self.MAT])
        done = self.check_win()
        info = {'current color' : num2color[self.col]}
        return self.observation, reward, done, info

    def reset(self):
        self.colorMAT = np.zeros(self.size,int) #color matrix tells color of the atom
        self.MAT = np.zeros(self.size,int) #atoms matrix tells the number of atoms in each position
        self.maxMAT = np.zeros(self.size,int) #max value of each position in atoms matrix 
        self.maxMAT[:,:] = 3 # three for all
        self.maxMAT[:,0] = 2 # two at the edges
        self.maxMAT[:,self.size[1]-1] = 2
        self.maxMAT[0,:] = 2
        self.maxMAT[self.size[0]-1,:] = 2
        self.maxMAT[0,0] = 1 # one at the cornors
        self.maxMAT[0,self.size[1]-1] = 1
        self.maxMAT[self.size[0]-1,0] = 1
        self.maxMAT[self.size[0]-1,self.size[1]-1] = 1
        self.observation = np.array([self.colorMAT , self.MAT])
        #self.observation = np.ascontiguousarray(np.array([self.colorMAT , self.MAT]).transpose(2,1,0))
        return self.observation  # reward, done, info can't be included
    
    def render(self, mode='human'):
        #print(self.colorMAT)
        print(self.observation.shape)

    
    def close (self):
        ...
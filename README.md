# Chain_reaction_on_py
more than a effort to make chain reaction game using python

todo

1. custome env creation
    a. convert matrics to numpy arrays
    b. make it so that explode function can handle multiple expolsions at once
    c. decide on a valid observation and reward function
    d. try pygames rendering or opencv to display game play

2. agent trainging
    a. initial idea is a conv nn with 3,1,1 and many layers which will out put the same shape a input with a distribution of exclent moves
    b. see stable baselines 3 and compare results

maintainence task
mantain a requirements.txt

decisions

1. how do i want my observation space -  [x,y,2]
2. how do I want my action space  -  [x,y]
3. do I want a randome agent
4. how to handle 2 player enviornment

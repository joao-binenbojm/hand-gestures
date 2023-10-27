import matplotlib.pyplot as plt
from time import sleep, time
import os
import numpy as np
import pickle
from time import sleep
from skimage import io, transform

def image_annotate_countdown(t_total, loc, rad_max=30, fps=10):
    ''' Adding two concentric circles, with the inner circle increasing from 0 to the radius of the outer circle
        such that it reaches its maximum size when the inner circle overlaps with the outer circle. This animation
        provides the user with an idea of how long there is left within the particular movement phase.
        Inputs:
            t_total[int]: the total time for the animation to take (duration fo the gesture)
            loc[tup(int, int)]: location along image where to center the animation circles
            rad_max[int/float]: the radius of the outer circle/max radius of the inner circle
            fps[int]: frames per second, corresponding to how many plot updates we have per second
    '''
    outline = plt.Circle(loc, rad_max, fc='blue',ec="blue")
    ax.add_patch(outline)
    for frame in range(int(t_total*fps)): # update screen to match fps
        t = frame/fps # compute time interval between each update
        rad = rad_max * (t/t_total) # radius of circle currently 
        circle = plt.Circle(loc, rad, fc='red', ec='blue')
        ax.add_patch(circle)
        plt.pause(1/fps)


# DEFINE INSTRUCTIONS DISPLAY OPTIONS
DIR = '/home/joao/Desktop/hand-gestures/imgs_old'
save_name = 'pilot-delsys-joao-standing'
# gests = [str(idx) for idx in range(1, 9)]
# legend = ["Thumb up", "Extension of index and middle, flexion of the others",
#           "Flexion of ring and little finger, extension of the others",
#           "Thumb opposing base of little finger", "Abduction of all fingers", 
#           "Fingers flexed together in fist", "Pointing index", "Adduction of extended fingers" 
#           ]
legend = ['extension', 'fist', 'flexion', 'openhand', 'pronation', 'radial-deviation', 'supination', 'ulnar-deviation']
gests = legend # labels for each movement
rest_name = 'rest' # name of rest file
t0 = time() # initial timestamp
clock = { 'start': {str(idx): [] for idx in range(8)}, 'stop': {str(idx): [] for idx in range(8)} } # keeps track of start and stop of gestures
clock['t0'] = t0 # add initial timestamp to our timestamp traker
gest_dur, rest_dur = 7, 5 # duration of each phase in seconds
rest_shape = (300, 600) # shape of rest image displayed
im_shape = (500, 500) # shape of gesture images displayed
reps = 2 # number of repetitions per gesture

# BEGIN DYNAMIC IMAGE PLOTTING
fig, ax = plt.subplots(figsize=(25,17)) # note we must use plt.subplots, not plt.subplot
plt.tick_params(left = False, right = False , labelleft = False , 
                labelbottom = False, bottom = False) 

for idx, name in enumerate(gests):
    for rep in range(1, reps):
        img = plt.imread(os.path.join(DIR, rest_name + '.jpg'))
        img = transform.resize(img, output_shape=rest_shape)
        plt.imshow(img)
        plt.title('REST')
        image_annotate_countdown(rest_dur, loc=(570, 25), rad_max=20)
        plt.cla()

        # Show the hand-gestures for 5s
        img = plt.imread(os.path.join(DIR, name + '.jpg'))
        img = transform.resize(img, output_shape=im_shape)
        plt.imshow(img)
        plt.title(legend[idx])
        ann = plt.text(20, 30, '#' + str(rep), fontsize=30, color='black')
        clock['start'][str(idx)].append(time()) # add time stamp to appropriate list
        
        image_annotate_countdown(gest_dur, loc=(450, 50))
        clock['stop'][str(idx)].append(time()) # add time stamp to appropriate list
        plt.cla()

# SAVE CLOCK
file = open('{}.p'.format(save_name), 'wb')
pickle.dump(clock, file)
file.close()
    

import matplotlib.pyplot as plt
from time import sleep, time
import os
import numpy as np
import pickle

DIR = '/home/joao/Desktop/hand-gestures/imgs_old'
save_name = 'pilot3'

# gests = [str(idx) for idx in range(1, 9)]
# legend = ["Thumb up", "Extension of index and middle, flexion of the others",
#           "Flexion of ring and little finger, extension of the others",
#           "Thumb opposing base of little finger", "Abduction of all fingers", 
#           "Fingers flexed together in fist", "Pointing index", "Adduction of extended fingers" 
#           ]
legend = ['extension', 'fist', 'flexion', 'openhand', 'pronation', 'radial-deviation', 'supination', 'ulnar-deviation']
gests = legend
rest_name = 'rest'
t0 = time() # initial timestamp
clock = { 'start': {str(idx): [] for idx in range(8)}, 'stop': {str(idx): [] for idx in range(8)} } # keeps track of start and stop of gestures
clock['t0'] = t0

for idx, name in enumerate(gests):
    instruction = 255*np.ones((2000, 2000, 3)).astype(np.uint8) # white image
    plt.figure(figsize=(25,17))
    plt.imshow(instruction)
    plt.text(300, 1000, 'CLOSE THIS TO CONTINUE', fontsize=40)
    plt.show()
    for rep in range(1, 11):
        # Show the rest instruction for 2.5s
        fig = plt.figure(figsize=(25,17))
        timer = fig.canvas.new_timer(interval = 2500) # keep rest instruction displayed for 2.5s, followed by a 0.5s transition
        timer.add_callback(plt.close)
        img = plt.imread(os.path.join(DIR, rest_name + '.jpg'))
        plt.imshow(img)
        plt.title('REST')
        timer.start()
        plt.show()
        sleep(0.5) # make transitions smoother between gestures

        # Show the hand-gestures for 5s
        fig = plt.figure(figsize=(25,17))
        timer = fig.canvas.new_timer(interval = 5000) # keep hand gesture instruction displayed for 5s
        timer.add_callback(plt.close)
        img = plt.imread(os.path.join(DIR, name + '.jpg'))
        plt.imshow(img)
        plt.title(legend[idx])
        plt.text(40, 40, '#' + str(rep), fontsize=40, color='white')
        timer.start()
        clock['start'][str(idx)].append(time()) # add time stamp to appropriate list
        plt.show()
        clock['stop'][str(idx)].append(time()) # add time stamp to appropriate list

# SAVE CLOCK
file = open('{}.p'.format(save_name), 'wb')
pickle.dump(clock, file)
file.close()
    

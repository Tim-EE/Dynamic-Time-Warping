import unittest
import numpy as np

from dtw import *
import dtw as dtw


class Test(unittest.TestCase):
    def test_chirp(self):
        idx = np.array([(3 * i/350) ** 2 for i in range(1,350)])
        x = np.cos(2 * math.pi * idx);
        idx = np.linspace(0, 900, 200)
        y = np.cos(2 * math.pi * 2 * idx)

        plt.subplot(211)
        plt.plot(y,label="y",color='g',linewidth=3)
        plt.plot(x,label="x",color='b')
        plt.legend()

        comp = DTW(x,y)
        comp.run()
        print("cost: " + str(comp.cost))

        plt.subplot(212)

        paths = comp.paths

        path_y = np.array(list(reversed(comp.path_y)))
        path_x = np.array(list(reversed(comp.path_x)))
        paths_xy = np.array(list(reversed(paths)))

        # get the warped signal
        new_signal = np.zeros(len(x))
        previousValue = y[paths_xy[0][1]]
        previousIterator = 0
        for i in range(len(paths_xy)):
            new_signal[paths_xy[i][0]] = y[paths_xy[i][1]]
            if i < len(paths_xy)-1:
                if paths_xy[i+1][0] - paths_xy[i][0] > 1:
                    for j in range(1,paths_xy[i+1][0] - paths_xy[i][0]):
                        new_signal[paths_xy[i][0] + j] = y[paths_xy[i][1]]
        # plot the warped signal against the original signal
        plt.plot(new_signal,label="warped signal",color='r', linewidth=3)
        plt.plot(x,label="x",color='b')
        plt.xlabel('Sample number')
        ax = plt.subplot(212)
        box = ax.get_position()
        ax.set_position([box.x0, box.y0 + box.height * 0.1,
                         box.width, box.height * 0.8])
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.18),
                  fancybox=True, shadow=True, ncol=5)
        plt.show(block = False)


    def test_square_wave(self):
        idx = np.linspace(0, 4*math.pi, 1000)
        x = np.sin(2 * math.pi * idx) +1/3* np.sin(3*2 * math.pi * idx)+1/5* np.sin(5*2 * math.pi * idx)+1/7* np.sin(7*2 * math.pi * idx)+1/9* np.sin(9*2 * math.pi * idx)+1/11* np.sin(11*2 * math.pi * idx)+1/13* np.sin(13*2 * math.pi * idx)
        y = np.cos(3 * math.pi * idx)

        plt.subplot(211)
        plt.plot(y,label="y",color='g',linewidth=3)
        plt.plot(x,label="x",color='b')
        plt.legend()

        comp = DTW(x,y)
        comp.run()
        print("cost: " + str(comp.cost))

        plt.subplot(212)

        paths = comp.paths

        path_y = np.array(list(reversed(comp.path_y)))
        path_x = np.array(list(reversed(comp.path_x)))
        paths_xy = np.array(list(reversed(paths)))

        # get the warped signal
        new_signal = np.zeros(len(x))
        previousValue = y[paths_xy[0][1]]
        previousIterator = 0
        for i in range(len(paths_xy)):
            new_signal[paths_xy[i][0]] = y[paths_xy[i][1]]
            if i < len(paths_xy)-1:
                if paths_xy[i+1][0] - paths_xy[i][0] > 1:
                    for j in range(1,paths_xy[i+1][0] - paths_xy[i][0]):
                        new_signal[paths_xy[i][0] + j] = y[paths_xy[i][1]]
        # plot the warped signal against the original signal
        plt.plot(new_signal,label="warped signal",color='r', linewidth=3)
        plt.plot(x,label="x",color='b')
        plt.xlabel('Sample number')
        ax = plt.subplot(212)
        box = ax.get_position()
        ax.set_position([box.x0, box.y0 + box.height * 0.1,
                         box.width, box.height * 0.8])
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.18),
                  fancybox=True, shadow=True, ncol=5)
        plt.show(block = False)

if __name__ == "__main__":
    unittest.main()

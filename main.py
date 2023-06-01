from collections import deque
from IZH_M import IZH_NEURON
import keyboard
import matplotlib.pyplot as plt
import matplotlib.animation as animation

n1 = IZH_NEURON()

npoints = 200
x = deque([0], maxlen=npoints)
y = deque([-70], maxlen=npoints)
x2 = deque([0], maxlen=npoints)
y2 = deque([0], maxlen=npoints)
fig, ax = plt.subplots()

fig.set_size_inches(7, 4)
fig.set_facecolor('#eee')
fig.suptitle('кнопки от 1 до 6 = пустить ток')
ax.grid()
ax.set_xlabel('Time')
ax.set_ylabel('V (mV), I (mA)')
[line] = ax.plot(x, y)
[line2] = ax.plot(x2, y2)

plt.ylim([-100, 100])

dx = 0.1


def update(dy):
    x.append((x[-1] + dx))  # update data
    y.append(dy[0])
    x2.append((x[-1] + dx))  # update data
    y2.append(dy[1])

    line.set_xdata(x)  # update plot data
    line.set_ydata(y)
    line2.set_xdata(x2)  # update plot data
    line2.set_ydata(y2)

    ax.relim()  # update axes limits
    ax.autoscale_view(True, True, True)
    return line, ax


def data_gen():
    while True:
        if keyboard.is_pressed('1'):
            n1.I = 1
        elif keyboard.is_pressed('2'):
            n1.I = 5
        elif keyboard.is_pressed('3'):
            n1.I = 10
        elif keyboard.is_pressed('4'):
            n1.I = 20
        elif keyboard.is_pressed('5'):
            n1.I = 50
        elif keyboard.is_pressed('6'):
            n1.I = 1000
        else:
            n1.I = 0

        n1.neuron_dt()
        yield n1.V, n1.I


ani = animation.FuncAnimation(fig, update, data_gen, cache_frame_data=False, interval=100)
plt.show()

x = input()
print(x)

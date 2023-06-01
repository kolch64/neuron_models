import numpy as np
import matplotlib.pyplot as plt


class IZH_NEURON():

    def __init__(self):
        self.V = -70  # Напряжение на мембране mV
        self.I = 0  # входящий ток
        self.a = 0.02  # быстрота восстановления u # a = 0.02 # чем меньше, тем дольше рефрактерность
        self.b = 0.2  # чувствительность u к подпороговым колебаниям V
        self.c = -65  # потенциал после генерации спайка mV
        self.d = 2  #
        self.u = -14  # переменная восстановления (рефрактерность)
        self.t_st = 0.1
        self.dV_dt = 0

    def neuron_dt(self):
        dV_dt = 0.04 * self.V ** 2 + 5 * self.V + 140 - self.u + self.I
        self.dV_dt = dV_dt
        self.V = self.V + dV_dt * self.t_st
        du_dt = self.a * (self.b * self.V - self.u)
        self.u = self.u + du_dt * self.t_st
        if self.V >= 30:
            self.V = self.c
            self.u = self.u + self.d


def main():

    n2 = IZH_NEURON()

    t_min = 0
    t_max = 1000
    t_step = 0.1
    time = np.arange(t_min, t_max, t_step)

    V_vector = np.zeros(int((t_max - t_min) / t_step))
    I_vector = np.zeros(int((t_max - t_min) / t_step))

    I_vector[1000:1050] = 4
    I_vector[1055:1070] = 8
    I_vector[2000:4000] = 10
    I_vector[5000:5001] = 200
    I_vector[6500:6600] = 5
    I_vector[7500:9000] = 50

    counter = 0
    for i in time:
        print(int(i * 10))
        n2.neuron_dt()
        V_vector[counter] = n2.V
        n2.I = I_vector[counter]
        counter += 1

    plt.plot(time, V_vector)
    plt.plot(time, I_vector)
    plt.xlabel('Time, mc')
    plt.ylabel('V, mV; I, mA')
    plt.show()


if __name__ == '__main__':
    main()

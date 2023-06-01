import numpy as np
import matplotlib.pyplot as plt


class Neuron_HH():
    def __init__(self):
        '''временной шаг'''
        self.t_step = 0.1  # mc
        '''максимальная проводимость для калия, натрия и утечки на квадратный сантиметр'''
        self.g_K_max = 36  # mS/cm^2
        self.g_Na_max = 120  # mS/cm^2
        self.g_L_max = 0.3  # mS/cm^2
        '''потенциалы для натрия, калия и утечки'''
        self.E_K = -12  # mV
        self.E_Na = 120  # mV
        self.E_L = 10.6  # mV
        '''емкость мембраны (самое непонятное) по идее 0.001мФ/см^2, но я принимаю за 1мФ/см^2'''
        self.C_m = 1  # mF/cm^2
        '''Мембранный потенциал в состоянии покоя (по умолчанию)'''
        self.V_rest = -70  # mV
        '''Текущий мембранный потенциал'''
        self.V = 0  #mV  # темная тема, почему он устанавливается на 0, а не -70
        '''Токи'''
        self.I_K = 0  # mA/cm^2
        self.I_Na = 0  # mA/cm^2
        self.I_L = 0  # mA/cm^2
        #self.I_input = 0  # mA
        #self.I_syn = 0  # mA
        self.I = 0
        '''
        воротные переменные:
        m = доля открытых каналов натрия; 0 < m < 1
        n = доля открытых каналов калия; 0 < n < 1
        h = доля не закрытых каналов натрия; 0 < h < 1
        '''

        self.n = 0.001
        self.m = 0.001
        self.h = 0.999



    def neuron_dt(self):
        '''
        Изменение воротных переменных по времени:
        dm/dt = (m_inf - m) / tau_m
        m = m + m*t_step*dm/dt
        dn/dt = (n_inf - n) / tau_n
        n = n + n*t_step*dn/dt
        dh/dt = (h_inf - h) / tau_h
        h = h + h*t_step*dh/dt

        Токи:
        (в уравнениях для K, Na и тока утечки проводимость на сантиметр умножается на напряжение(mS/cm^2 * mV = mA/cm^2)
        I_K = g_K_max * n**4 * (V - E_K) # ток на см^2
        I_Na = g_Na_max * m**3 * h * (V - E_Na) # ток на см^2
        I_L = g_L_max * (V - E_L) # ток на см^2 # mA/cm^2
        I = I_input + I_syn

        Изменение напряжения на мембране по времени:
        dVdt = I / C_m - I_K / C_m - I_Na / C_m - I_L / C_m
        V = V + t_step * dVdt
        '''

        alpha_m = 0.1 * ((25 - self.V) / (np.exp((25 - self.V) / 10) - 1))
        beta_m = 4 * np.exp(-self.V / 18)
        m_inf = alpha_m / (alpha_m + beta_m)
        tau_m = 1 / (alpha_m + beta_m)
        dmdt = (m_inf - self.m) / tau_m
        self.m = self.m + self.m * self.t_step * dmdt

        alpha_n = 0.01 * ((10 - self.V) / (np.exp((10 - self.V) / 10) - 1))
        beta_n = 0.125 * np.exp(-self.V / 80)
        n_inf = alpha_n / (alpha_n + beta_n)
        tau_n = 1 / (alpha_n + beta_n)
        dndt = (n_inf - self.n) / tau_n
        self.n = self.n + self.n * self.t_step * dndt

        alpha_h = 0.07 * np.exp(-self.V / 20)
        beta_h = 1 * (1 / (np.exp((30 - self.V) / 10) + 1))
        h_inf = alpha_h / (alpha_h + beta_h)
        tau_h = 1 / (alpha_h + beta_h)
        dhdt = (h_inf - self.h) / tau_h
        self.h = self.h + self.t_step * dhdt

        I_K = self.g_K_max * self.n ** 4 * (self.V - self.E_K)  # ток на см^2
        I_Na = self.g_Na_max * self.m ** 3 * self.h * (self.V - self.E_Na)  # ток на см^2
        I_L = self.g_L_max * (self.V - self.E_L)  # ток на см^2 # I/cm^2
        I = self.I #self.I_input + self.I_syn

        # текущее напряжение на мембране
        dVdt = I / self.C_m - I_K / self.C_m - I_Na / self.C_m - I_L / self.C_m
        self.V = self.V + self.t_step * dVdt


def main():

    n1 = Neuron_HH()

    t_min = 0
    t_max = 1000
    t_step = n1.t_step
    time = np.arange(t_min, t_max, t_step)

    V_vector = np.zeros(int((t_max - t_min) / t_step))
    I_vector = np.zeros(int((t_max - t_min) / t_step))

    I_vector[1000:1050] = 50
    I_vector[2000:3000] = 10
    I_vector[2800:2900] = 6
    I_vector[3400:4500] = 40
    I_vector[5000:5010] = 200
    I_vector[6500:6600] = 6
    #I_vector[1000:5000] = 40
    c = 0
    while c < 9999:
        c += 1
        if c > 7499 and c % 200 == 0:
            I_vector[c:c+50] = 40

    n_vector = np.zeros(int((t_max - t_min) / t_step))
    m_vector = np.zeros(int((t_max - t_min) / t_step))
    h_vector = np.zeros(int((t_max - t_min) / t_step))

    counter = 0
    for child in time:
        n1.neuron_dt()
        V_vector[counter] = n1.V - 70
        n1.I = I_vector[counter]
        n_vector[counter] = n1.n
        m_vector[counter] = n1.m
        h_vector[counter] = n1.h

        counter += 1



    plt.plot(time, V_vector)
    plt.plot(time, I_vector)

    #plt.plot(time, )
    plt.xlabel('Time, mc')
    plt.ylabel('V, mV; I, mA')
    plt.show()

    plt.plot(time, n_vector, color='red')
    plt.plot(time, m_vector, color='y')
    plt.plot(time, h_vector, color='g')
    plt.xlabel('Time, mc')
    plt.ylabel('r = n(открытый калий) y = m(открытый натрий) g = h(инактивный натрий')
    plt.show()


if __name__ == '__main__':
    main()
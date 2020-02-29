import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal


def draw(x, y, title, xlabel, ylabel):
    plt.semilogx(x, y)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.margins(0, 0.1)
    plt.grid(which='both', axis='both')
    plt.show()


def draw_graphs(b, a, title):
    w, h = signal.freqs(b, a)
    draw_frequency_response(w, h, title)
    draw_phase_response(w, h, title)


def draw_frequency_response(w, h, title):
    draw(w, 20 * np.log10(abs(h)),
          f'{title} frequency response',
          'Frequency [radians / second]',
          'Amplitude [dB]')


def draw_phase_response(w, h, title):
    draw(w, np.unwrap(np.angle(h)),
          f'{title} phase response',
          'Frequency [radians / second]',
          'Phase [radians]')


b, a = signal.butter(4, 100, 'low', analog=True)
draw_graphs(b, a, 'Butterworth filter')

b, a = signal.cheby1(4, 5, 100, 'low', analog=True)
draw_graphs(b, a, 'Chebyshev Type I (rp=5)')

b, a = signal.cheby2(4, 40, 100, 'low', analog=True)
draw_graphs(b, a, 'Chebyshev Type II (rs=40)')

b, a = signal.ellip(4, 5, 40, 100, 'low', analog=True)
draw_graphs(b, a, 'Elliptic filter (rp=5, rs=40)')

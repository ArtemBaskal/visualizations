import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal

Fs = 44100

fc = np.array([1, 10000])
wc = 2 * fc / Fs


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


def butter(ftype):
    b, a = signal.butter(5, 100, ftype, analog=True)
    draw_graphs(b, a, f'{ftype} Butterworth filter')


def cheby1(ftype):
    b, a = signal.cheby1(4, 5, 100, ftype, analog=True)
    draw_graphs(b, a, f'{ftype} Chebyshev Type I (rp=5)')


def cheby2(ftype):
    b, a = signal.cheby2(4, 40, 100, ftype, analog=True)
    draw_graphs(b, a, f'{ftype} Chebyshev Type II (rs=40)')


def ellip(ftype):
    b, a = signal.ellip(4, 5, 40, 100, ftype, analog=True)
    draw_graphs(b, a, f'{ftype} Elliptic filter (rp=5, rs=40)')


list(map(lambda f: list(map(f, ['lowpass', 'highpass'])), [butter, cheby1, cheby2, ellip]))

import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal

Fs = 44100

fc = np.array([1, 10000])
wc = 2 * fc / Fs

Btypes = {
    'lowpass': 'lowpass',
    'highpass': 'highpass',
    'bandpass': 'bandpass',
    'bandstop': 'bandstop'
}


def draw(x, y, title, xlabel, ylabel, show=True):
    plt.semilogx(x, y)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.margins(0, 0.1)
    plt.grid(which='both', axis='both')
    if show:
        plt.show()


def draw_graphs(b, a, title, show=True):
    w, h = signal.freqs(b, a)
    draw_frequency_response(w, h, title, show)
    draw_phase_response(w, h, title, show)


def draw_frequency_response(w, h, title, show=True):
    draw(w, 20 * np.log10(abs(h)),
         f'{title} frequency response',
         'Frequency [radians / second]',
         'Amplitude [dB]', show)


def draw_phase_response(w, h, title, show=True):
    draw(w, np.unwrap(np.angle(h)),
         f'{title} phase response',
         'Frequency [radians / second]',
         'Phase [radians]', show)


def define_critical_frequency(btype):
    Wn = 1
    if (btype == Btypes['lowpass'] or btype == Btypes['highpass']):
        Wn = 100
    if (btype == Btypes['bandpass'] or btype == Btypes['bandstop']):
        Wn = wc
    return Wn


def define_graphs(b, a, title, show, task):
    if task == 1:
        draw_graphs(b, a, title, show)
    if task == 2:
        w, h = signal.freqs(b, a)
        draw_frequency_response(w, h, title, show=False)
    if task == 3:
        print(task)


def butter(btype="low", N=4, show=True, task=1):
    Wn = define_critical_frequency(btype)

    b, a = signal.butter(N, Wn, btype, analog=True)
    title = f'{btype} Butterworth filter'

    define_graphs(b, a, title, show, task)


def cheby1(btype="low", N=4, show=True, task=1):
    Wn = define_critical_frequency(btype)

    b, a = signal.cheby1(N, 5, Wn, btype, analog=True)
    title = f'{btype} Chebyshev Type I (rp=5)'

    define_graphs(b, a, title, show, task)


def cheby2(btype="low", N=4, show=True, task=1):
    Wn = define_critical_frequency(btype)

    b, a = signal.cheby2(N, 40, Wn, btype, analog=True)
    title = f'{btype} Chebyshev Type II (rs=40)'

    define_graphs(b, a, title, show, task)


def ellip(btype="low", N=4, show=True, task=1):
    Wn = define_critical_frequency(btype)

    b, a = signal.ellip(N, 5, 40, Wn, btype, analog=True)
    title = f'{btype} Elliptic filter (rp=5, rs=40)'

    define_graphs(b, a, title, show, task)


def draw_group(f):
    order = range(1, 11)
    list(map(lambda i: f(N=i, task=2), order))
    plt.legend(order)
    plt.show()


list(map(lambda f: list(map(lambda i: f(i), list(Btypes))), [butter, cheby1, cheby2, ellip]))

list(map(draw_group, [butter, cheby1, cheby2, ellip]))

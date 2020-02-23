import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import rfft, irfft, rfftfreq
from math import pi
from numpy import cos
import scipy.signal as sig

A = 10
B = 2
f1 = 2000
f2 = 150

Fs = 40000
time = 0.01

t = np.arange(0, time, 1. / Fs)
n = np.size(t)
fr = rfftfreq(n, 1. / Fs)

def generate_am_signal(amp_c=1.0, amp_s=1.0, km=1.0, fc=10.0, fs=2.0):
    """
    Create Amplitude modulation (AM) signal

    Parameters
    ----------
    amp_c : float
        Signal magnitude of carries
    amp_s : float
        Signal magnitude of signal
    km : float
        Modulation coeff: amplitude sensitivity 0 <= km < 1
    fc : float
        Carrier frequency
    fs : float
        Signal frequency
    """
    return amp_c * (1 + km * amp_s * cos(2 * pi * fs * t)) * cos(2 * pi * fc * t)


def generate_fm_signal(amp_c=1.0, amp_s=1.0, km=1.0, fc=10.0, fs=2.0):
    """
    Create Frequency modulation (FM) signal

    Parameters
    ----------
    amp_c : float
        Signal magnitude of carries
    amp_s : float
        Signal magnitude of signal
    km : float
        Modulation coeff: amplitude sensitivity 0 <= km < 1
    fc : float
        Carrier frequency
    fs : float
        Signal frequency
    """
    return amp_c * cos(2 * pi * fc * t + amp_s * km * cos(2 * pi * fs * t))


def draw_graph(x, y, title='', xlabel=''):
    plt.title(title)
    plt.plot(x, y)
    plt.ylabel('Amplitude')
    plt.xlabel(xlabel)
    plt.grid(True)
    plt.show()


def draw_signal_graph(s, title='Signal', xlabel='Time, s'):
    draw_graph(t, s, title, xlabel)


def draw_spectrum_graph(s, title='Spectrum', xlabel='Frequency, Hz'):
    spectr = abs(rfft(s)) / n
    draw_graph(fr, spectr, title, xlabel)


def draw_signal_and_spectrum(signal, signal_title):
    draw_signal_graph(signal, signal_title)
    draw_spectrum_graph(signal, f"Spectrum of {signal_title}")


def add_noise(signal):
    noise = np.random.normal(0, B, signal.shape)
    noised_signal = signal + noise
    return noised_signal


def task1(am_signal, noised_signal):
    draw_signal_and_spectrum(am_signal, 'AM-signal')
    draw_signal_and_spectrum(noised_signal, 'AM-signal with noise')


def task2(fm_signal, noised_signal):
    draw_signal_and_spectrum(fm_signal, 'FM-signal')
    draw_signal_and_spectrum(noised_signal, 'FM-signal with noise')


def task3(noised_signal):
    o = 5
    fc = np.array([1, 10000])
    wc = 2 * fc / Fs
    [b, a] = sig.butter(o, wc, btype="bandpass")

    filtered_signal = sig.lfilter(b, a, noised_signal)
    draw_signal_and_spectrum(filtered_signal, 'Filtered AM-signal')
    return filtered_signal


def task4(filtered_signal):
    spectrum = rfft(filtered_signal)
    filtered_signal = irfft(spectrum)
    draw_signal_and_spectrum(filtered_signal, 'IFT AM-signal')


pure_am_signal = generate_am_signal(amp_c=A, amp_s=B, fc=f1, fs=f2)
noised_am_signal = add_noise(pure_am_signal)
task1(pure_am_signal, noised_am_signal)

pure_fm_signal = generate_fm_signal(amp_c=A, amp_s=B, fc=f1, fs=f2)
noised_fm_signal = add_noise(pure_fm_signal)
task2(pure_fm_signal, noised_fm_signal)

filtered_am_signal = task3(noised_am_signal)
task4(filtered_am_signal)

import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal


def draw(b, a, title):
    w, h = signal.freqs(b, a)
    plt.semilogx(w, 20 * np.log10(abs(h)))
    plt.title(title)
    plt.xlabel('Frequency [radians / second]')
    plt.ylabel('Amplitude [dB]')
    plt.margins(0, 0.1)
    plt.grid(which='both', axis='both')
    plt.show()
    

#
b, a = signal.butter(4, 100, 'low', analog=True)
draw(b, a, 'Butterworth filter frequency response')

#
b, a = signal.cheby1(4, 5, 100, 'low', analog=True)
draw(b, a, 'Chebyshev Type I frequency response (rp=5)')

#
b, a = signal.cheby2(4, 40, 100, 'low', analog=True)
draw(b, a, 'Chebyshev Type II frequency response (rs=40)')
#
b, a = signal.ellip(4, 5, 40, 100, 'low', analog=True)
draw(b, a, 'Elliptic filter frequency response (rp=5, rs=40)')

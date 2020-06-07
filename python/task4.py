import math
import numpy as np
import matplotlib.pyplot as plt
from operator import itemgetter

DTMF_TABLE = {
    1: {'high': 1209, 'low': 697},
    2: {'high': 1336, 'low': 697},
    3: {'high': 1477, 'low': 697},

    4: {'high': 1209, 'low': 770},
    5: {'high': 1336, 'low': 770},
    6: {'high': 1477, 'low': 770},

    7: {'high': 1209, 'low': 852},
    8: {'high': 1336, 'low': 852},
    9: {'high': 1477, 'low': 852},
}

A = 10
B = 2
sr = 3000
T = 0.5
t = np.linspace(0, T, int(T * sr), endpoint=False)

f1 = 2000
f2 = 150


def goertzel(samples, sample_rate, *freqs):
    """
    Implementation of the Goertzel algorithm, useful for calculating individual
    terms of a discrete Fourier transform.

    `samples` is a windowed one-dimensional signal originally sampled at `sample_rate`.

    The function returns 2 arrays, one containing the actual frequencies calculated,
    the second the coefficients `(real part, imag part, power)` for each of those frequencies.
    For simple spectral analysis, the power is usually enough.

    Example of usage :

        freqs, results = goertzel(some_samples, 44100, (400, 500), (1000, 1100))
    """
    window_size = len(samples)
    f_step = sample_rate / float(window_size)
    f_step_normalized = 1.0 / window_size

    # Calculate all the DFT bins we have to compute to include frequencies
    # in `freqs`.
    bins = set()
    for f_range in freqs:
        f_start, f_end = f_range
        k_start = int(math.floor(f_start / f_step))
        k_end = int(math.ceil(f_end / f_step))

        if k_end > window_size - 1: raise ValueError('frequency out of range %s' % k_end)
        bins = bins.union(range(k_start, k_end))

    # For all the bins, calculate the DFT term
    n_range = range(0, window_size)
    freqs = []
    results = []
    for k in bins:

        # Bin frequency and coefficients for the computation
        f = k * f_step_normalized
        w_real = 2.0 * math.cos(2.0 * math.pi * f)
        w_imag = math.sin(2.0 * math.pi * f)

        # Doing the calculation on the whole sample
        d1, d2 = 0.0, 0.0
        for n in n_range:
            y = samples[n] + w_real * d1 - d2
            d2, d1 = d1, y

        # Storing results `(real part, imag part, power)`
        results.append((
            0.5 * w_real * d1 - d2, w_imag * d1,
            d2 ** 2 + d1 ** 2 - w_real * d1 * d2)
        )
        freqs.append(f * sample_rate)

    return freqs, results


def get_key_by_value(dictionary, value):
    if value in list(dictionary.values()):
        value = list(dictionary.keys())[list(dictionary.values()).index(value)]
        print('DTMF signal', value, 'received')
        return value
    return False


def find_key(low, high):
    return get_key_by_value(DTMF_TABLE, {'high': high, 'low': low})


def iterate_in_vicinity(callback, center, offset=10, step=1):
    return [callback(n) for n in range(center - offset, center + offset, step)]


def iterate_in_two_dimensional_vicinity(center_low, center_high, callback):
    return iterate_in_vicinity(lambda low: (low, iterate_in_vicinity(lambda high: callback(high, low), center_low)),
                               center_high)


def read_input():
    arr = list(input())
    return list(map(lambda i: DTMF_TABLE[int(i)], arr))


def generate_signal(tones):
    f1 = tones['high']
    f2 = tones['low']
    x = np.sin(2 * np.pi * f1 * t) + np.sin(2 * np.pi * f2 * t)
    return x


def apply_goertzel(signal):
    freqs, results = goertzel(signal, sr, (697, 1209), (697, 1336), (697, 1477), (770, 1209), (770, 1336), (770, 1477),
                              (852, 1209), (852, 1336), (852, 1477))
    return freqs, results


def draw_graph(x, y):
    plt.plot(x, y)
    plt.show()


def callback(tones):
    # 1
    signal = generate_signal(tones)
    freqs, results = apply_goertzel(signal)
    draw_graph(freqs, results)

    # 2
    res = list(map(itemgetter(-1), results))
    ind = np.argpartition(res, -4)[-4:]
    arr = np.array(freqs)[ind]

    high = int(np.max(arr))
    low = int(np.min(arr))
    iterate_in_two_dimensional_vicinity(low, high, find_key)
    return arr


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
    return amp_c * (1 + km * amp_s * np.cos(2 * math.pi * fs * t)) * np.cos(2 * math.pi * fc * t)


def add_noise(signal):
    noise = np.random.normal(0, B, signal.shape)
    noised_signal = signal + noise
    return noised_signal


def draw_noised_am_signal():
    pure_am_signal = generate_am_signal(amp_c=A, amp_s=B, fc=f2, fs=f1)
    noised_am_signal = add_noise(pure_am_signal)
    freqs, results = apply_goertzel(noised_am_signal)
    draw_graph(freqs, results)


def main():
    tones = read_input()
    list(map(callback, tones))

    draw_noised_am_signal()

    main()


main()

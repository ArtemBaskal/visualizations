import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.fftpack import rfft, irfft
import math


def draw_graphs(freq_list, title_list=['', '', '']):
    plt.figure(figsize=(14, 6), dpi=80)
    for i in range(3):
        plt.subplot(3, 1, i + 1)
        plt.plot(freq_list[i], '-', linewidth=2.0)
        plt.title(f'{title_list[i]} Signal')
        plt.xlabel('Samples')
        plt.ylabel('Amplitude')
        plt.xlim([0, freq_list[i].size - 1])
        plt.grid()
    plt.tight_layout()
    plt.show()


def convolve(signal1, signal2):
    return signal.convolve(signal1, signal2, mode='same') / np.sum(signal1)


def circle_convolve(signal1, signal2):
    return irfft(rfft(signal1) * rfft(signal2)) / np.sum(signal1)


def sum_of_correlation(signal1, signal2):
    return np.array(
        [np.sum(signal1 * np.roll(signal2, i)) for i in range(math.floor(0.5 * (len(signal1) + len(signal2))))])


def draw_convolve(signal1, signal2, title_list=['Signal', 'Signal']):
    title_list.append('Convolution')
    convolution = convolve(signal1, signal2)
    draw_graphs([signal1, signal2, convolution], title_list)


def draw_circle_convolve(signal1, signal2, title_list=['Signal', 'Signal']):
    title_list.append('Circle Convolution')
    convolution = circle_convolve(signal1, signal2)
    draw_graphs([signal1, signal2, convolution], title_list)


def draw_convolve_2(signal1, signal2, title_list=['Signal', 'Signal']):
    title_list.append('Convolution')
    convolution = sum_of_correlation(signal1, signal2)
    draw_graphs([signal1, signal2, convolution], title_list)


def task1(square_wave, triangular_wave):
    draw_convolve(square_wave, square_wave, ['Square', 'Square'])
    draw_convolve(triangular_wave, triangular_wave, ['Triangular', 'Triangular'])
    draw_convolve(square_wave, triangular_wave, ['Square', 'Triangular'])


def task2(square_wave):
    exponential_signal = np.repeat(0., 600)
    for i in range(400):
        exponential_signal[i + 200] = np.exp(- i / 100)

    draw_convolve(square_wave, exponential_signal, ['Square', 'Exponential'])


def task3(square_wave, triangular_wave):
    draw_circle_convolve(square_wave, square_wave, ['Square', 'Square'])
    draw_circle_convolve(triangular_wave, triangular_wave, ['Triangular', 'Triangular'])
    draw_circle_convolve(square_wave, triangular_wave, ['Square', 'Triangular'])


def task4(square_wave, triangular_wave):
    draw_convolve_2(square_wave, square_wave, ['Square', 'Square'])
    draw_convolve_2(triangular_wave, triangular_wave, ['Triangular', 'Triangular'])
    draw_convolve_2(square_wave, triangular_wave, ['Square', 'Triangular'])


square_wave = np.repeat([0., 1., 0.], 200)
triangular_wave = convolve(square_wave, square_wave)

# task1(square_wave, triangular_wave)
task2(square_wave)
task3(square_wave, triangular_wave)
# task4(square_wave, triangular_wave)

import warnings
import numpy as np
import matplotlib.pyplot as plt
import librosa
from scipy import signal, interpolate

warnings.filterwarnings("ignore")
font = {
    'family': 'arial',
    'weight': 'light',
    'size': 7
}

plt.rc('font', **font)
plt.rcParams['figure.dpi'] = 300

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

Fs = 10000
t = 0.4
time = np.linspace(0, t, int(t * Fs), endpoint=False)


def generate_signal(tone):
    low_freq = tone['low']
    high_freq = tone['high']
    sig = np.sin(2 * np.pi * low_freq * time) + np.sin(2 * np.pi * high_freq * time)
    five_periods = 2 * np.pi * 5 * 2 / (low_freq + high_freq)
    return sig, five_periods


def set_graph_params(subplot, title, xlabel, ylabel, xlim=None, ylim=None):
    plt.subplot(subplot)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if xlim is not None:
        plt.xlim(xlim)
    if ylim is not None:
        plt.ylim(ylim)


def draw_spectrum(sig, order=111, title='', Fs=Fs, xlim=[650, 1500]):
    plt.magnitude_spectrum(sig, Fs)
    set_graph_params(order, f'Спект, {title}', 'Частота, Гц', 'Амплитуда, В', xlim)


def draw_processed_signal_spectrums(processed_signals, downsampling_factor):
    (decimated_sig_fir, resampled_sig_fir, decimated_signal_iir, resampled_signal_iir, _) = processed_signals

    plt.suptitle(f'Коэффициента выброса значений {downsampling_factor}', y=1, fontweight='semibold')

    order = 411
    draw_spectrum(decimated_sig_fir, order, 'Прореживание, КИХ фильтр')

    order += 1
    draw_spectrum(resampled_sig_fir, order, 'Прореживание, БИХ фильтр')

    order += 1
    draw_spectrum(decimated_signal_iir, order, 'Децимация, КИХ фильтр')

    order += 1
    draw_spectrum(resampled_signal_iir, order, 'Децимация, БИХ фильтр')

    plt.show()


def draw_signal_and_spectrum(time, sig, xlim, title=''):
    order = 311

    set_graph_params(order, f'Тон {title}', 'Время, c', 'Амплитуда сигнала, В', [0, xlim])
    plt.plot(time, sig)

    order += 1
    plt.subplot(order)
    plt.magnitude_spectrum(sig, Fs=Fs)
    set_graph_params(order, 'Спект тона', 'Частота, Гц', 'Амплитуда, В', [650, 1500])

    order += 1
    set_graph_params(order, 'Тональный набор', 'Время, c', 'Частота, Гц', ylim=[650, 1600])
    f, t, Sxx = signal.spectrogram(sig, Fs)
    plt.pcolormesh(t, f, Sxx)

    plt.show()


def draw_processed_signals(processed_signals, five_periods, downsampling_factor, tone):
    (decimated_sig_fir, resampled_sig_fir,
     decimated_signal_iir, resampled_signal_iir,
     decimated_time) = processed_signals

    plt.suptitle(f'Тон {tone}, коэффициента выброса значений {downsampling_factor}', y=1, fontweight='semibold')

    order = 411

    set_graph_params(order, 'Прореживание, КИХ фильтр', 'Время, c', 'Амплитуда сигнала, В', [0, five_periods])
    plt.plot(decimated_time, decimated_sig_fir)

    order += 1
    set_graph_params(order, 'Прореживание, БИХ фильтр', 'Время, c', 'Амплитуда сигнала, В')
    plt.plot(decimated_time, decimated_signal_iir)

    order += 1
    set_graph_params(order, 'Децимация, КИХ фильтр', 'Время, c', 'Амплитуда сигнала, В', [0, five_periods])
    plt.plot(time, resampled_sig_fir)

    order += 1
    set_graph_params(order, 'Децимация, БИХ фильтр', 'Время, c', 'Амплитуда сигнала, В')
    plt.plot(time, resampled_signal_iir)

    plt.show()


def draw_interpolated_signal(sig, time, decimated_time, downsampling_factor):
    plt.suptitle(f'Коэффициента выброса значений {downsampling_factor}', y=1, fontweight='semibold')

    order = 211

    tck = interpolate.splrep(time, sig)
    set_graph_params(order, 'Сигнал', 'Время, c', 'Амплитуда сигнала, В')
    plt.plot(time, sig)

    order += 1
    set_graph_params(order, 'Интерполированный сигнал', 'Время, c', 'Амплитуда сигнала, В')
    interpolated = interpolate.splev(decimated_time, tck)
    plt.plot(decimated_time, interpolated)

    librosa.output.write_wav(f'/Volumes/dev/hse/media/audio/interpolated_{downsampling_factor}.wav', interpolated, Fs)

    plt.show()


def process_signals(sig, downsampling_factor, N, ftype):
    decimated_sig = signal.decimate(sig, downsampling_factor, N, ftype=ftype)
    resampled_sig = signal.resample(decimated_sig, num=int(len(sig)))
    return decimated_sig, resampled_sig


def get_processed_signals(sig, downsampling_factor=5):
    n = 1
    N_fir = 50 - n
    N_iir = 30 - n

    decimated_sig_fir, resampled_sig_fir = process_signals(sig, downsampling_factor, N_fir, ftype='fir')
    decimated_signal_iir, resampled_signal_iir = process_signals(sig, downsampling_factor, N_iir, ftype='iir')

    decimated_time = np.linspace(0, t, int(t * Fs / downsampling_factor), endpoint=False)

    return decimated_sig_fir, resampled_sig_fir, decimated_signal_iir, resampled_signal_iir, decimated_time


def process_and_display_signals(sig, downsampling_factor, five_periods, tone):
    processed_signals = get_processed_signals(sig, downsampling_factor)

    draw_processed_signals(processed_signals, five_periods, downsampling_factor, tone)

    draw_processed_signal_spectrums(processed_signals, downsampling_factor)

    decimated_time = processed_signals[-1]
    draw_interpolated_signal(sig, time, decimated_time, downsampling_factor)


def callback(tone):
    freqs = DTMF_TABLE[int(tone)]
    sig, five_periods = generate_signal(freqs)
    draw_signal_and_spectrum(time, sig, five_periods, title=tone)

    [process_and_display_signals(sig, downsampling_factor, five_periods, tone) for downsampling_factor in
     list([2, 20, 50])]


def main():
    tones = list(input())
    list(map(callback, tones))
    main()


main()

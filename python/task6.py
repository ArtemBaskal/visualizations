import warnings
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal
import librosa as lr

warnings.filterwarnings("ignore")
np.seterr(divide='ignore')

Btypes = {
    'lowpass': 'lowpass',
    'highpass': 'highpass',
    'bandpass': 'bandpass',
    'bandstop': 'bandstop'
}

Fs = 44100

font = {
    'family': 'arial',
    'weight': 'light',
    'size': 7
}

plt.rc('font', **font)
plt.rcParams['figure.dpi'] = 300

data_dir = '/Volumes/dev/hse/media/audio/around.mp3'
audio, sfreq = lr.load(data_dir, duration=60)
time = np.arange(0, len(audio)) / sfreq


def set_graph_params(subplot, title, xlabel, ylabel):
    plt.subplot(subplot)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)


def draw_signal_and_spectrum(time, audio, sos=None, title=''):
    order = 211
    if sos is not None:
        order = order + 100

    set_graph_params(order, f'Сигнал {title}', 'Время, c', 'Амплитуда сигнала, В')
    plt.plot(time, audio)

    order = order + 1
    plt.subplot(order)
    plt.magnitude_spectrum(audio, Fs=sfreq)
    set_graph_params(order, 'Спект сигнала', 'Частота, Гц', 'Амплитуда сигнала, В')

    if sos is None:
        plt.show()
        return

    order = order + 1
    set_graph_params(order, 'AЧХ', 'Угловая частота, рад/с', 'Коэффициент передачи, дБ')
    w, h = signal.sosfreqz(sos, worN=1500)
    plt.plot(w / np.pi, 20 * np.log10(abs(h)))
    plt.show()


def get_freqs(btype, lowcut, highcut, fs):
    nyq = fs / 2

    if btype == Btypes['lowpass']:
        return highcut / nyq

    if btype == Btypes['highpass']:
        return lowcut / nyq

    return [lowcut, highcut]


def butter(btype='lowpass', sig=audio, lowcut=1, highcut=3000, order=10, fs=Fs):
    title = f'{btype} butter'
    freqs = get_freqs(btype, lowcut, highcut, fs)

    sos = signal.butter(order, freqs, btype, analog=False, output='sos', fs=fs)
    filtered = signal.sosfilt(sos, sig)
    draw_signal_and_spectrum(time, filtered, sos, title)

    if btype == Btypes['bandstop']:
        lr.output.write_wav(f'/Volumes/dev/hse/media/audio/test.wav', filtered, sfreq)


def cheby1(btype='lowpass', sig=audio, lowcut=1, highcut=3000, order=4, fs=Fs):
    title = f'{btype} chebyshev type I'
    freqs = get_freqs(btype, lowcut, highcut, fs)

    sos = signal.cheby1(order, 5, freqs, btype, analog=False, output='sos', fs=fs)
    filtered = signal.sosfilt(sos, sig)
    draw_signal_and_spectrum(time, filtered, sos, title)


def cheby2(btype='lowpass', sig=audio, lowcut=1, highcut=3000, order=4, fs=Fs):
    title = f'{btype} chebyshev type II'
    freqs = get_freqs(btype, lowcut, highcut, fs)

    sos = signal.cheby2(order, 40, freqs, btype, analog=False, output='sos', fs=fs)
    filtered = signal.sosfilt(sos, sig)
    draw_signal_and_spectrum(time, filtered, sos, title)


def ellip(btype='lowpass', sig=audio, lowcut=1, highcut=3000, order=4, fs=Fs):
    title = f'{btype} elliptic filter'
    freqs = get_freqs(btype, lowcut, highcut, fs)

    sos = signal.ellip(order, 5, 40, freqs, btype, analog=False, output='sos', fs=fs)
    filtered = signal.sosfilt(sos, sig)
    draw_signal_and_spectrum(time, filtered, sos, title)


filters = [butter, cheby1, cheby2, ellip]

draw_signal_and_spectrum(time, audio)

list(map(lambda f: list(map(f, list(Btypes))), filters))

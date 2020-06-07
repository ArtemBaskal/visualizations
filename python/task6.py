import warnings
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal
import librosa
import librosa.display

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
    'size': 4
}

plt.rc('font', **font)
plt.rcParams['figure.dpi'] = 300

duration = 60

data_dir = '/Volumes/dev/hse/media/audio/lump.mp3'
audio, sfreq = librosa.load(data_dir, duration=duration)
time = np.arange(0, len(audio)) / sfreq


def set_graph_params(subplot, title, xlabel, ylabel):
    plt.subplot(subplot)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)


def draw_signal_and_spectrum(time, audio, sos=None, title=''):
    order = 311
    if sos is not None:
        order = order + 100

    set_graph_params(order, f'Сигнал {title}', 'Время, c', 'Амплитуда сигнала, В')
    plt.plot(time, audio)

    order += 1
    plt.subplot(order)
    plt.magnitude_spectrum(audio, Fs=sfreq)
    set_graph_params(order, 'Спект сигнала', 'Частота, Гц', 'Амплитуда сигнала, В')

    order += 1
    plt.subplot(order)
    S_full, phase = librosa.magphase(librosa.stft(audio))
    idx = slice(*librosa.time_to_frames([0, duration], sr=sfreq))
    librosa.display.specshow(librosa.amplitude_to_db(S_full[:, idx], ref=np.max), y_axis='log', x_axis='time', sr=sfreq)
    set_graph_params(order, 'Спектрограмма сигнала', 'Время, с', 'Частота сигнала, Гц')

    if sos is None:
        plt.show()
        return

    order += 1
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

    return filtered
    # if btype == Btypes['bandstop']:
    #     librosa.output.write_wav(f'/Volumes/dev/hse/media/audio/test.wav', filtered, sfreq)


def cheby1(btype='lowpass', sig=audio, lowcut=1, highcut=3000, order=4, fs=Fs):
    title = f'{btype} chebyshev type I'
    freqs = get_freqs(btype, lowcut, highcut, fs)

    sos = signal.cheby1(order, 5, freqs, btype, analog=False, output='sos', fs=fs)
    filtered = signal.sosfilt(sos, sig)
    draw_signal_and_spectrum(time, filtered, sos, title)

    return filtered


def cheby2(btype='lowpass', sig=audio, lowcut=1, highcut=3000, order=4, fs=Fs):
    title = f'{btype} chebyshev type II'
    freqs = get_freqs(btype, lowcut, highcut, fs)

    sos = signal.cheby2(order, 40, freqs, btype, analog=False, output='sos', fs=fs)
    filtered = signal.sosfilt(sos, sig)
    draw_signal_and_spectrum(time, filtered, sos, title)

    return filtered


def ellip(btype='lowpass', sig=audio, lowcut=1, highcut=3000, order=4, fs=Fs):
    title = f'{btype} elliptic filter'
    freqs = get_freqs(btype, lowcut, highcut, fs)

    sos = signal.ellip(order, 5, 40, freqs, btype, analog=False, output='sos', fs=fs)
    filtered = signal.sosfilt(sos, sig)
    draw_signal_and_spectrum(time, filtered, sos, title)

    return filtered


filters = [butter]

draw_signal_and_spectrum(time, audio)

# list(map(lambda f: list(map(f, list(Btypes))), filters))

filtered = cheby1('bandstop', audio, 100, 1000)
# b = copy.deepcopy(filtered)
filtered2 = cheby1('bandstop', filtered, 4000, 5000)

# Input parameters
# fs = 10
# N = 117
# desired = (8, 90, 110, 90, 8, 7)
# bands = (0, 1, 2, 4.9, 4.95, 5)
#
# # FIR filters
# fir_firls = signal.firls(N, bands, desired, fs=fs)
# fir_remez = signal.remez(N, bands, desired[::2], fs=fs)
# fir_firwin2 = signal.firwin2(N, bands, desired, fs=fs)
#
# # PLot results and calculate FFTs
# plt.figure(figsize=(12, 5), dpi=300)
# plt.title('Frequency responce')
# for fir in (fir_firls, fir_remez, fir_firwin2):
#     freq, resp = signal.freqz(fir)
#     resp = np.abs(resp)
#     resp /= np.max(resp) + 10 ** (-15)
#     plt.plot(freq, 20 * np.log10(resp))
# # plt.xlim([0, np.pi])
# # plt.ylim([-180, 5])
# plt.legend(['firls', 'remez', 'firwin2'], loc='upper left')
# plt.grid(True)
# plt.show()


# def plot_response(fs, w, h, title):
#     "Utility function to plot response functions"
#     fig = plt.figure()
#     ax = fig.add_subplot(111)
#     ax.plot(0.5 * fs * w / np.pi, 20 * np.log10(np.abs(h)))
#     # ax.set_ylim(-40, 5)
#     # ax.set_xlim(0, 0.5 * fs)
#     ax.grid(True)
#     ax.set_xlabel('Frequency (Hz)')
#     ax.set_ylabel('Gain (dB)')
#     ax.set_title(title)
#     plt.show()
#
#
# fs = Fs  # Sample rate, Hz
# band = [2000, 5000]  # Desired pass band, Hz
# trans_width = 100  # Width of transition from pass band to stop band, Hz
# numtaps = 15  # Size of the FIR filter.
# edges = [0, band[0] - trans_width, band[0], band[1],
#          band[1] + trans_width, 0.5 * fs]
# taps = signal.remez(numtaps, edges, [0, 1, 0], Hz=fs)
# w, h = signal.freqz(taps, [1], worN=2000)
# plot_response(fs, w, h, "Band-pass Filter")

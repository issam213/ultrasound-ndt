import numpy as np

def time_of_flight(depth, velocity):
    return 2 * depth / velocity

def echo_amplitude(depth, velocity, frequency, attenuation=10):
    attenuation_factor = np.exp(-attenuation * depth * 100 / 1000)
    reflection = 0.3
    return reflection * attenuation_factor

def generate_pulse(frequency, duration, sampling_rate=10e6):
    t = np.linspace(0, duration, int(sampling_rate * duration))
    sigma = 1.0 / (frequency * 0.5)
    envelope = np.exp(-((t - duration/2) ** 2) / (2 * sigma ** 2))
    carrier = np.sin(2 * np.pi * frequency * t)
    pulse = envelope * carrier
    if np.max(np.abs(pulse)) > 0:
        pulse = pulse / np.max(np.abs(pulse))
    return t, pulse

def simulate_ascan(depth, velocity, frequency, noise_level=0.05):
    sampling_rate = 10e6
    max_time = 0.001
    n_samples = int(sampling_rate * max_time)
    t = np.linspace(0, max_time, n_samples)
    signal = np.zeros_like(t)
    
    pulse_duration = 10 / frequency
    pulse_t, pulse = generate_pulse(frequency, pulse_duration, sampling_rate)
    
    for i in range(len(pulse_t)):
        if i < len(signal):
            signal[i] += pulse[i]
    
    echo_time = time_of_flight(depth, velocity)
    echo_amp = echo_amplitude(depth, velocity, frequency)
    echo_start_idx = int(echo_time * sampling_rate)
    
    for i in range(len(pulse_t)):
        idx = echo_start_idx + i
        if idx < len(signal):
            signal[idx] += echo_amp * pulse[i]
    
    np.random.seed(42)
    noise = np.random.normal(0, noise_level, len(signal))
    signal = signal + noise
    
    return t, signal

def find_echo_time(signal, sampling_rate=10e6):
    abs_signal = np.abs(signal)
    threshold = 0.1 * np.max(abs_signal)
    
    for i in range(50, len(abs_signal) - 1):
        if abs_signal[i] > threshold:
            if abs_signal[i] > abs_signal[i-1] and abs_signal[i] > abs_signal[i+1]:
                return i / sampling_rate
    return None

def calculate_depth(echo_time, velocity):
    return velocity * echo_time / 2
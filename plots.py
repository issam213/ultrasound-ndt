import numpy as np
import matplotlib.pyplot as plt
import configparser
import sys
import os

# Read configuration
config = configparser.ConfigParser()
config.read(sys.argv[1])

# Get paths
images_folder = config.get('paths', 'images_folder')
signal_file = config.get('paths', 'signal_file')
echo_times_file = config.get('paths', 'echo_times_file')
amplitudes_file = config.get('paths', 'amplitudes_file')
plot_file = config.get('paths', 'plot_file')

# Get parameters for labels
velocity = float(config.get('settings', 'velocity'))
depth_start = float(config.get('settings', 'depth_start'))
depth_end = float(config.get('settings', 'depth_end'))
num_depths = int(config.get('settings', 'num_depths'))

# Create images folder
os.makedirs(images_folder, exist_ok=True)

# Load data
signals = np.load(signal_file)
echo_times = np.load(echo_times_file)
amplitudes = np.load(amplitudes_file)

# Depths
depths = np.linspace(depth_start, depth_end, num_depths)

# Theoretical echo times
theoretical_times = 2 * depths / velocity

# Calculate depth estimation error
estimated_depths = velocity * echo_times / 2
depth_errors = (estimated_depths - depths) * 100  # error in cm
print("\nDepth Estimation Errors:")
print(f"{'Actual (cm)':<15} {'Estimated (cm)':<15} {'Error (cm)':<12}")
print("-" * 45)
for i in range(len(depths)):
    actual_cm = depths[i] * 100
    est_cm = estimated_depths[i] * 100 if echo_times[i] > 0 else 0
    error_cm = depth_errors[i] if echo_times[i] > 0 else 0
    print(f"{actual_cm:<15.1f} {est_cm:<15.2f} {error_cm:<12.3f}")

# Create figure
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))

# Plot 1: Echo time vs depth
ax1.plot(depths * 100, theoretical_times * 1e6, 'b-', label='Theoretical', linewidth=2)
ax1.scatter(depths * 100, echo_times * 1e6, color='red', s=50, label='Simulated')
ax1.set_xlabel('Depth (cm)')
ax1.set_ylabel('Echo Time (μs)')
ax1.set_title('Echo Time vs Defect Depth')
ax1.legend()
ax1.grid(True, alpha=0.3)

# Plot 2: Amplitude vs depth
ax2.scatter(depths * 100, amplitudes, color='green', s=50)
ax2.set_xlabel('Depth (cm)')
ax2.set_ylabel('Echo Amplitude')
ax2.set_title('Echo Amplitude vs Defect Depth')
ax2.grid(True, alpha=0.3)

# Plot 3: Sample A-scan (middle depth)
mid_idx = len(signals) // 2
t = np.linspace(0, 0.001, len(signals[mid_idx]))
ax3.plot(t * 1e6, signals[mid_idx], 'b-', linewidth=1)
if echo_times[mid_idx] > 0:
    echo_us = echo_times[mid_idx] * 1e6
    ax3.axvline(echo_us, color='red', linestyle='--', 
                label=f'Echo at {echo_us:.1f} μs')
    # Zoom in around the echo
    ax3.set_xlim(echo_us - 50, echo_us + 50)
ax3.set_xlabel('Time (μs)')
ax3.set_ylabel('Amplitude')
ax3.set_title(f'A-scan at depth = {depths[mid_idx]*100:.1f} cm')
ax3.legend()
ax3.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(plot_file, dpi=150)
plt.show()

print(f"\n✅ Plot saved to: {plot_file}")
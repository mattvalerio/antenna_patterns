# From: https://scipython.com/book2/chapter-7-matplotlib/examples/modelling-an-antenna-array/

import numpy as np
import matplotlib.pyplot as plt

def gain(d, w):
    """Return the power as a function of azimuthal angle, phi."""
    phi = np.linspace(0, 2*np.pi, 1000)
    psi = 2*np.pi * d / lam * np.cos(phi)
    j = np.arange(len(w))
    A = np.sum(w[j] * np.exp(j * 1j * psi[:, None]), axis=1)
    g = np.abs(A)**2
    return phi, g

def get_directive_gain(g, minDdBi=-20):
    """Return the "directive gain" of the antenna array producing gain g."""
    DdBi = 10 * np.log10(g / np.max(g))
    return np.clip(DdBi, minDdBi, None)

# Wavelength, antenna spacing, feed coefficients.
lam = 1
d = lam / 4

def plot_antenna_pattern(amp, inc_phase):
    # Apply incremental phase shift to each element
    amplitude = np.array(amp)
    w = amplitude * np.exp(1j * np.arange(len(amplitude)) * inc_phase)

    # Calculate gain and directive gain; plot on a polar chart.
    phi, g = gain(d, w)
    DdBi = get_directive_gain(g)

    fig = plt.figure()
    ax = fig.add_subplot(projection='polar')
    ax.plot(phi, DdBi)
    ax.set_rticks([-20, -15, -10, -5])
    ax.set_rlabel_position(45)
    plt.show()

# 2 element, uniform amplitude, no incremental phase shift
plot_antenna_pattern([1, 1], 0.0)

# 10 element, uniform amplitude, no incremental phase shift
plot_antenna_pattern([1,1,1,1,1,1,1,1,1,1], 0.0)

# 10 element, uniform amplitude, scanning incremental phase shift
for i in range(5):
    plot_antenna_pattern([1,1,1,1,1,1,1,1,1,1], i*np.pi/16)

# 11 element, linear taper on edges, scanning incremental phase shift
for i in range(5):
    plot_antenna_pattern([0.25, 0.5, 0.75, 1, 1, 1, 1, 1, 0.75, 0.5, 0.25], i*np.pi/16)



# Split the functionality up so that we can add multiple traces to the same plot
def create_axis():
    fig = plt.figure()
    ax = fig.add_subplot(projection='polar')   
    return ax

def add_antenna_pattern(ax, amp, inc_phase):
    # Apply incremental phase shift to each element
    amplitude = np.array(amp)
    w = amplitude * np.exp(1j * np.arange(len(amplitude)) * inc_phase)

    # Calculate gain and directive gain; plot on a polar chart.
    phi, g = gain(d, w)
    DdBi = get_directive_gain(g)

    # Subsequent calls to ax.plot will add a new trace to the plot in a new color
    ax.plot(phi, DdBi)

def plot_figure(ax):
    ax.set_rticks([-20, -15, -10, -5])
    ax.set_rlabel_position(45)
    plt.show()


# 2 element, uniform amplitude, no incremental phase shift
ax = create_axis()
add_antenna_pattern(ax, [1, 1], 0.0)
plot_figure(ax)

# 10 element, uniform amplitude, no incremental phase shift
ax = create_axis()
add_antenna_pattern(ax, [1,1,1,1,1,1,1,1,1,1], 0.0)
plot_figure(ax)

# 10 element, uniform amplitude, scanning incremental phase shift
ax = create_axis()
for i in range(10):
    add_antenna_pattern(ax, [1,1,1,1,1,1,1,1,1,1], i*np.pi/16)
plot_figure(ax)

# 11 element, linear taper on edges, scanning incremental phase shift
ax = create_axis()
for i in range(10):
    add_antenna_pattern(ax, [0.25, 0.5, 0.75, 1, 1, 1, 1, 1, 0.75, 0.5, 0.25], i*np.pi/16)
plot_figure(ax)

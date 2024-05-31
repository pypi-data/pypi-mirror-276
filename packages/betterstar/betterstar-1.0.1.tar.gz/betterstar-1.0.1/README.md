# betterstar

A python package that implements a better looking star for matplotlib plots.

## About this package

This package allows you to integrate a more professionally looking star into your matplotlib plots.

![Picture showing the difference between the standard star and the star that this package includes.](resources/example2.png "Example of difference")

The upper star is the standard matplotlib star. The lower one is the one you get with this package.

## Setup

```bash
pip install betterstar
```

## Quick Usage Example

```python
from betterstar import star
import matplotlib.pyplot as plt

# some code

p33 = plt.plot(x3[i3], min3, marker=star, color='c', markersize=6, markeredgewidth=0.35)

# some more code
```

## Advanced example

If you need a professional look to your plots, you can use the following code example. This way you will use a LaTeX rendered font.

```python
# Initial plot setup
figure2 = plt.figure(figsize=(10.0,5.0),dpi=150)
axes2 = plt.subplot(1, 1, 1)
axes2.spines[['right', 'top']].set_visible(False)
axes2.tick_params(direction="in", width=0.5)
plt.xlim([80, 175])
plt.ylim([0.5, 1.5])

# Change tick frequency
locy = plticker.MultipleLocator(base=0.1)
axes2.yaxis.set_major_locator(locy)
locx = plticker.MultipleLocator(base=10.0)
axes2.xaxis.set_major_locator(locx)

# Remove Tick at origin
xticks = axes2.xaxis.get_major_ticks()
xticks[1].tick1line.set_visible(False)
yticks = axes2.yaxis.get_major_ticks()
yticks[1].tick1line.set_visible(False)

# Title and axes
hT = plt.title(r'\boldmath$\frac{P}{v_\mathrm{TAS}}$ $\textbf{\textrm{\"{u}ber}}$ $v_\mathrm{TAS}$') # Title
hT.set_fontsize(16)
plt.xlabel(r'$v_\mathrm{TAS}$ $\left[\mathrm{kt}\right]$', fontsize=12) # x-axis label
plt.ylabel(r'$\frac{P}{v_\mathrm{TAS}}$ $\left[\frac{\mathrm{hp}}{\mathrm{kt}}\right]$', fontsize=12) # y-axis label

# Plot the first line
p11 = plt.plot(v_tas_b, ppv2,'ms', markersize=1)
plt.plot(x2,y2,'g',linewidth=0.5)
p22 = plt.plot(x2[i2],min2, marker=mlab_star, color='c', markersize=6, markeredgewidth=0.35)

# Plot second line
p12 = plt.plot(v_tas, ppv,'bs', markersize=1) # r for red, s for square
plt.plot(x1,y1,'r',linewidth=0.5)
p21 = plt.plot(x1[i1],min1, marker=mlab_star, color='y', markersize=6, markeredgewidth=0.35)

# Text at lowest point of line
plt.text(x1[i1]-2,min1+0.05, f'$\mathrm{{{round(min1,2)}}}$' + r'$\frac{\mathrm{hp}}{\mathrm{kt}}$')
plt.text(x2[i2],min2-0.05, f'$\mathrm{{{str(round(min2,2))}}}$' + r'$\frac{\mathrm{hp}}{\mathrm{kt}}$')

# Legend
legend = plt.legend([p11[0], p12[0], p21[0], p22[0]], [r'$\frac{P}{v_\mathrm{TAS}}$', r'$\frac{P}{v_\mathrm{TAS}}$ \textrm{berechnet}', r'\textrm{minimum}', r'\textrm{minimum}'], loc='upper right', handlelength=0)
frame = legend.get_frame()
frame.set_edgecolor('black')
frame.set_linewidth(0.5)

```

This will result in a plot like this:
![Plot with the new star](resources/example.png "Example")

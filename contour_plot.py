#!/usr/local/bin/python2.7
import sys
import os
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter, ScalarFormatter
from scipy.interpolate import Rbf

def contour(x, y, z, file_name):
    '''
    Function to draw a contour plot. Linear axes.
    
    '''
    xmin, xmax = x.min(), x.max()
    ymin, ymax = y.min(), y.max()
    zmin, zmax = z.min(), z.max()
    
    nx, ny = 200, 200
    
    # Initialise figure
    fig1 = plt.figure()

    # Interpolation
    xi, yi = np.linspace(xmin, xmax, nx), np.linspace(ymin, ymax, ny)
    xi, yi = np.meshgrid(xi, yi)
    rbf = Rbf(x, y, z, function='linear')
    zi = rbf(xi, yi)
    
    # Generate plot
    ax1 = plt.subplot(111)
    im1 = ax1.imshow(zi, vmin=zmin, vmax=zmax, origin='lower', extent=[xmin, xmax, ymin, ymax])
    ax1.scatter(x, y, c=z)

    # Colorbar
    plt.colorbar(im1, orientation='vertical')

    # Set axis labels (using latex in a unicode raw string)
    ax1.set_xlabel(ur'$Ea_{AA}$', fontsize='20')
    ax1.set_ylabel(ur'$Ea_{BC}$', fontsize='20')
    
    # Apply contours over colormap, with labels
    CS = ax1.contour(xi, yi, zi, colors='k')
    ax1.clabel(CS, inline=1, fontsize=10, colors='k')
    
    # Output figure
    fig1.tight_layout()
    fig1.savefig(file_name + '_contour.png', bbox_inches='tight', dpi=200, transparent=True)
    plt.close('all')
    
def log_contour(x, y, z, file_name):
    '''
    Function to draw a contour plot with log axes.
    
    '''
    xmin, xmax = x.min(), x.max()
    ymin, ymax = y.min(), y.max()
    zmin, zmax = z.min(), z.max()
    
    nx, ny = 200, 200
    
    # Initialise figure
    fig2 = plt.figure()

    # Interpolation
    xi, yi = np.linspace(xmin, xmax, nx), np.linspace(ymin, ymax, ny)
    zi = mlab.griddata(x, y, z, xi, yi)

    # Generate plot (using mesh so can be scaled in log)
    ax2 = plt.subplot(111)
    me2 = ax2.pcolormesh(xi, yi, zi, cmap = plt.get_cmap('rainbow'))
    ax2.scatter(x, y, c=z)

    # Colorbar
    plt.colorbar(me2, orientation='vertical')
    
    # Set log scale on axes. This can be changed of course.
    ax2.set_xscale("log")
    ax2.set_yscale("log")
    
    # Set axis labels (using latex in a unicode raw string)
    ax2.set_xlabel(ur'$Ea_{AA}$', fontsize='20')
    ax2.set_ylabel(ur'$Ea_{BC}$', fontsize='20')
    
    # Apply contours over colormap
    ax2.contour(xi, yi, zi, 15, linewidths = 0.5, colors = 'k')
    
    # Make sure aspect ratio of axes are equal
    ax2.set_aspect('equal')
    
    # Output figure
    fig2.tight_layout()
    fig2.savefig(file_name + '_log_contour.png', bbox_inches='tight', dpi=200, transparent=True)
    plt.close('all')
    
# MAIN FUNCTION
if __name__ == '__main__':
    # Inputs text files
    assert len(sys.argv) >= 2
    
    for contour_file_name in sys.argv[1:]:
    
        # Open file
        c = open(contour_file_name, 'r')
        x, y, z = np.loadtxt(c, unpack=True)

        x, y, z = np.ma.compress_cols(np.ma.masked_invalid(np.array([x,y,z])))

        # Call functions
        contour(x, y, z, os.path.splitext(contour_file_name)[0])
        log_contour(x, y, z, os.path.splitext(contour_file_name)[0])
        
        c.close()

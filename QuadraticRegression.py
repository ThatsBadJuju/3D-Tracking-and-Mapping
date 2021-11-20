import sys
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


# x = [0, 1, 2, 3, 4, 5]
# y = [0, 1, 2, 3, 4, 5]
# t = [10, 11.5, 12.3, 12, 11.4, 10.8]
def is_outlier(points, thresh=3.5):
    """
    Returns a boolean array with True if points are outliers and False
    otherwise.

    Parameters:
    -----------
        points : An numobservations by numdimensions array of observations
        thresh : The modified z-score to use as a threshold. Observations with
            a modified z-score (based on the median absolute deviation) greater
            than this value will be classified as outliers.

    Returns:
    --------
        mask : A numobservations-length boolean array.

    """
    if len(points.shape) == 1:
        points = points[:,None]
    median = np.median(points, axis=0)
    diff = np.sum((points - median)**2, axis=-1)
    diff = np.sqrt(diff)
    med_abs_deviation = np.median(diff)

    modified_z_score = 0.6745 * diff / med_abs_deviation

    return modified_z_score > thresh


def create_quad_regression_plot(t,y, end_time):
    figure = plt.figure()
    axes = figure.add_subplot()#111, projection='3d')
    #
    # outlier_test = is_outlier
    # for points in outlier_test:
    axes.scatter(t,y)
    quadratic_regression = np.polyfit(t, y, 2)
    a = quadratic_regression[0]
    b = quadratic_regression[1]
    c = quadratic_regression[2]

    x_plot = np.linspace(0, end_time)
    #y = np.linspace(0, 5)
    y_plot = a * x_plot * x_plot + b * x_plot + c

    plt.plot(x_plot, y_plot)

    plt.show()
    return a, b, c

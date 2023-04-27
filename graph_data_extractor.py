from numpy import linalg, vstack, mat
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
from math import log
import sys

def pic2data(filename, xlogbase=None, ylogbase=None):
    showpic(filename)
    axis_point_map = prompt_axes(xlogbase, ylogbase)
    M = generate_transform(axis_point_map)
    print(M)
    data_points = prompt_data()
    plt.close()

    transformed_points = []
    for point in data_points:
        vec = np.mat([[point[0]], [point[1]], [1]])
        transformed_vec = M*vec
        transformed_vec = transformed_vec.tolist()
        transformed_vec = [transformed_vec[0][0], transformed_vec[1][0]]

        if xlogbase:
            transformed_vec[0] = xlogbase ** transformed_vec[0]
        if ylogbase:
            transformed_vec[1] = ylogbase ** transformed_vec[1]
        transformed_points.append(tuple(transformed_vec))
    print(transformed_points)

def showpic(filename):
    image = mpimg.imread(filename)
    plt.ion()
    plt.imshow(image)

def prompt_axes(xlogbase=None, ylogbase=None):
    point_map = {}
    finished = False
    while not finished:
        print('Click a point on one of the axes.')
        raw_point = plt.ginput()[0]
        point_value = [float(input('What is the x component?: ')), float(input('What is the y component?: '))]
        if xlogbase:
            point_value[0] = log(point_value[0], xlogbase)
        if ylogbase:
            point_value[1] = log(point_value[1], ylogbase)
        point_map[raw_point] = tuple(point_value)
        finished = input('Add another point? (y)/n: ') == 'n'
    return point_map

def prompt_data():
    points = []
    finished = False
    while not finished:
        print('Click a point on the plot')
        new_point = plt.ginput()[0]
        points.append(new_point)
        finished = input('Add another point? (y)/n: ') == 'n'
    return points

def generate_transform(axis_point_map):
    num_pairs = len(axis_point_map)
    if num_pairs < 3:
        print("Need at least 3 coordinate to find the transformation!")

    raw_coords = axis_point_map.keys()
    real_coords = axis_point_map.values()

    X = np.mat(np.zeros((3*num_pairs, 3*num_pairs)))
    Xp = np.mat(np.zeros((3*num_pairs, 1)))

    for ii, real_coord, raw_coord in zip(range(num_pairs), real_coords, raw_coords):
        X[2*ii, 0:3] = np.mat([raw_coord[0],raw_coord[1],1])
        X[2*ii+1, 3:6] = np.mat([raw_coord[0], raw_coord[1], 1])
        Xp[2*ii: 2*ii+2] = np.mat([[real_coord[0]], [real_coord[1]]])

    # Do least squares fitting
    a = np.linalg.lstsq(X, Xp, rcond=None)

    A = np.vstack((a[0][0:3].T, a[0][3:6].T, np.mat([0,0,1])))

    return A


if __name__ == '__main__':
    pic2data(sys.argv[1])

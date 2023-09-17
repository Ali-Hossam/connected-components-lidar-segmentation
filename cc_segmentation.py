import math
import os
import numpy as np


def txtfile_to_list(txt_name):
    """Input a txt file and returns its elements in a list of floats"""
    current_directory = os.path.dirname(__file__)
    txt_name = current_directory + "\\txt_files\\" + txt_name
    print(txt_name)
    polar_points_txt = open(txt_name, "r")
    points = polar_points_txt.read()
    polar_points_list = points.split()
    polar_points_list = [float(point) for point in polar_points_list]
    return polar_points_list


def polar_to_cartesian(polar_points, lidar_max_range):
    """converts polar coordinates to cartesian coordinates"""
    cartesian_points_list = []
    for i, point in enumerate(polar_points):
        if point == 0:
            continue
        x = point * math.cos(math.radians(i))
        y = point * math.sin(math.radians(i))

        #Discretize X and Y
        x = int(x)
        y = int(y)

        x += lidar_max_range
        y += int(lidar_max_range / 2)
        cartesian_points_list.append([x, y])
    # Remove duplicated points
    tupl = [tuple(x) for x in cartesian_points_list]
    cartesian_points_list = list(dict.fromkeys(tupl))
    return cartesian_points_list


def create_grid(lidar_max_range, points):
    """returns 2D matrix standing for the binary image"""
    grid = np.zeros((2*lidar_max_range, lidar_max_range))
    for point in points:
        point_x = point[0]
        point_y = point[1]
        grid[point_x, point_y] = 1
    
    #convert grid elemnts from float to int
    grid = grid.astype(int)
    return grid


def get_neighbors(x, y, lidar_max_range_):
    """For a given point (x, y) it returns a set with tuples each
    tuple represents one of this point neighbors and the point itself"""
    width = 2 * lidar_max_range_
    height = lidar_max_range_
    neighbor_points = set()

    for new_x in range(x-1, x+2):
        for new_y in range(y-1, y+2):
            if 0 <= new_x < width and 0 <= new_y < height:
                neighbor_points.add((new_x, new_y))
    return neighbor_points


def connected_components(points_list, grid, lidar_max_range_):
    """Converts Binary image to a Symbolic image"""
    label = 1
    previous_points = set()
    while points_list:
        current_point = points_list.pop(0)
        current_point_x, current_point_y = current_point
        grid[current_point_x, current_point_y] = label

        previous_points.add(current_point)
        neighbor_points = get_neighbors(current_point_x, 
                                        current_point_y, 
                                        lidar_max_range_)
        #Get points that hadn't been labeled only
        neighbor_points = neighbor_points.difference(previous_points)
        
        previous_points.update(neighbor_points)
        
        neighbor_points_list = list(neighbor_points)
        
        for point in neighbor_points_list:
            point_x, point_y = point
            if grid[point_x, point_y] == 0:
                continue
            else:
                points_list.remove((point_x, point_y))
                grid[point_x, point_y] = label
                
                second_neighbors = get_neighbors(point_x, point_y,
                                                lidar_max_range_)
                second_neighbors = second_neighbors.difference(previous_points)
                previous_points.update(second_neighbors)
                neighbor_points_list += list(second_neighbors)
        label += 1
    return grid.T


def export_to_txt(filename, symbolic_img):
    """Exports symbolic image to a txt file, where each row in a line and values
    are space seperated"""
    np.savetxt(filename, symbolic_img, fmt='%i')


def alg(txt_name, lidar_max_range_, final_file_name):
    polar_points_list = txtfile_to_list(txt_name)
    cartesian_points_list = polar_to_cartesian(polar_points_list,
                                                lidar_max_range_)
    
    grid = create_grid(lidar_max_range_, cartesian_points_list)
    symbolic_img = connected_components(
        cartesian_points_list, grid, lidar_max_range_)
    
    #Export final image to a txt file
    current_directory = os.path.dirname(__file__)
    os.chdir(current_directory)
    np.savetxt(final_file_name, symbolic_img, fmt='%i')
    return symbolic_img


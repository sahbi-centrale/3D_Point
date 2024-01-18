#
#
#      0===========================================================0
#      |    TP1 Basic structures and operations on point clouds    |
#      0===========================================================0
#
#
# ------------------------------------------------------------------------------------------
#
#      Third script of the practical session. Neighborhoods in a point cloud
#
# ------------------------------------------------------------------------------------------
#
#      Hugues THOMAS - 13/12/2017
#


# ------------------------------------------------------------------------------------------
#
#          Imports and global variables
#      \**********************************/
#


# Import numpy package and name it "np"
import numpy as np

# Import functions from scikit-learn
from sklearn.neighbors import KDTree

# Import functions to read and write ply files
from ply import write_ply, read_ply

# Import time package
import time


# ------------------------------------------------------------------------------------------
#
#           Functions
#       \***************/
#
#
#   Here you can define useful functions to be used in the main
#




def brute_force_spherical(queries, supports, radius):
    neighborhoods = []
    for query in queries:
        # Calculate the Euclidean distance from the query to all supports
        distances = np.sqrt(np.sum((supports - query) ** 2, axis=1))
        # Find the indices of points within the specified radius
        neighborhood = np.where(distances <= radius)[0]
        neighborhoods.append(neighborhood)
    return neighborhoods


def brute_force_KNN(queries, supports, k):
    neighborhoods = []
    for query in queries:
        # Calculate the Euclidean distance from the query to all supports
        distances = np.sqrt(np.sum((supports - query) ** 2, axis=1))
        # Find the indices of the k nearest neighbors
        neighborhood = np.argsort(distances)[:k]
        neighborhoods.append(neighborhood)
    return neighborhoods




# ------------------------------------------------------------------------------------------
#
#           Main
#       \**********/
#
# 
#   Here you can define the instructions that are called when you execute this file
#

if __name__ == '__main__':

    # Load point cloud
    # ****************
    #
    #   Load the file '../data/indoor_scan.ply'
    #   (See read_ply function)
    #

    # Path of the file
    file_path = 'indoor_scan.ply'

    # Load point cloud
    data = read_ply(file_path)

    # Concatenate data
    points = np.vstack((data['x'], data['y'], data['z'])).T

    # Brute force neighborhoods
    # *************************
    #

    # If statement to skip this part if you want
    if False:

        # Define the search parameters
        neighbors_num = 100
        radius = 0.2
        num_queries = 10

        # Pick random queries
        random_indices = np.random.choice(points.shape[0], num_queries, replace=False)
        queries = points[random_indices, :]

        # Search spherical
        t0 = time.time()
        neighborhoods = brute_force_spherical(queries, points, radius)
        t1 = time.time()

        # Search KNN      
        neighborhoods = brute_force_KNN(queries, points, neighbors_num)
        t2 = time.time()

        # Print timing results
        print('{:d} spherical neighborhoods computed in {:.3f} seconds'.format(num_queries, t1 - t0))
        print('{:d} KNN computed in {:.3f} seconds'.format(num_queries, t2 - t1))

        # Time to compute all neighborhoods in the cloud
        total_spherical_time = points.shape[0] * (t1 - t0) / num_queries
        total_KNN_time = points.shape[0] * (t2 - t1) / num_queries
        print('Computing spherical neighborhoods on whole cloud : {:.0f} hours'.format(total_spherical_time / 3600))
        print('Computing KNN on whole cloud : {:.0f} hours'.format(total_KNN_time / 3600))

 



    # KDTree neighborhoods
    # ********************
    #

    # If statement to skip this part if wanted
    if True:
        tree = KDTree(points, leaf_size=20)
        num_queries = 1000
        # Define the search parameters
        random_indices = np.random.choice(points.shape[0], num_queries, replace=False)
        queries = points[random_indices, :]
        # Timing the spherical neighborhood search using KDTree
        start_time = time.time()
        indices_spherical = tree.query_radius(queries, 20)
        end_time = time.time()
        time_spherical = end_time - start_time

    # Timing the k-nearest neighbors search using KDTree
        k = 5  # Example for k nearest neighbors
        start_time = time.time()
        distances_knn, indices_knn = tree.query(queries, 5)
        end_time = time.time()
        time_knn = end_time - start_time

        time_spherical, time_knn

        
        
        
        
        

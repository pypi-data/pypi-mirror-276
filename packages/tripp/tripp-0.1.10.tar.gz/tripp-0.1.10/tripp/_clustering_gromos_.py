"""
    @release_date  : $release_date
    @version       : $release_version
    @author        : Christos Matsingos, Ka Fu Man 
    
    This file is part of the TrIPP software
    (https://github.com/fornililab/TrIPP).
    Copyright (c) 2024 Christos Matsingos, Ka Fu Man and Arianna Fornili.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, version 3.

    This program is distributed in the hope that it will be useful, but
    WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
    General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program. If not, see <http://www.gnu.org/licenses/>.
"""

import numpy as np 

def gromos_clustering(cutoff, rmsd_matrix, frames, trajectory_names): 

    """
    Function to run GROMOS clustering. 
    """

    #A copy of the RMSD matrix is made to not modify the original array 
    current_matrix = rmsd_matrix.copy() 
    n_structures = len(frames) 
    
    #A labels array with the same number of elements as the total numebr of structures is generated. Initially all structures are labelled to belong to cluster 0. 
    labels = np.zeros(n_structures, dtype=int) 
    cluster = 1 
    cluster_centers = [] 
    cluster_center_indices = [] 
    cluster_centers_trajectories = [] 

    for i in range(n_structures): 
        #A boolean array neighbor_mask is generated to determine what RMSDs are under the cutoff. 
        neighbor_mask = current_matrix  <= cutoff 
        
        #The current_matrix array is checked to determine if all elements are set to infinity. If the condition is true the clustering is complete. 
        if np.all(np.isinf(current_matrix)) == True: 
            break 

        else: 
            neighbor_counts = np.sum(neighbor_mask, axis=0) #The amount of neighbors (structures within the cutoff) is ddetermined for each structure. 
            central_structure = np.argmax(neighbor_counts) #The structure with the most neighbors is determined to be the center of the cluster 
            cluster_centers.append(frames[central_structure]) 
            cluster_centers_trajectories.append(trajectory_names[central_structure]) 
            cluster_center_indices.append(central_structure) 
            neighbors = np.ravel(neighbor_mask[central_structure,:]) #All structures neighboring the central structure are determined and are assigned to the same cluster 
            labels[neighbors] = cluster 
            #The current_matrix (copy of the RMSD matrix) is altered to remove elements belonging to the cluster from future clustering by setting the RMSD values to inf. 
            current_matrix [central_structure,:] = np.inf 
            current_matrix [:,central_structure] = np.inf 
            current_matrix [neighbor_mask[central_structure],:] = np.inf 
            current_matrix [:,neighbor_mask[central_structure]] = np.inf 
            cluster+=1 #The following cluster label is generated 

    cluster_centers = list(np.ravel(np.array(cluster_centers))) 
    cluster_center_indices = list(np.ravel(np.array(cluster_center_indices))) 
    cluster_centers_trajectories = list(np.ravel(np.array(cluster_centers_trajectories))) 
    labels = labels - 1 #All labels are changed to fit the numbering of the other clustering methods. 
    
    return labels, cluster_centers, cluster_center_indices, cluster_centers_trajectories  
import os 
import geopandas as gpd 
import osmnx as ox 
import networkx as nx
from shapely.geometry import Point
import numpy as np
from tqdm import tqdm 
import matplotlib.pyplot as plt


''' Load Data '''
root = os.getcwd()
data_path = os.path.join(root, 'data')
subway = gpd.read_file(os.path.join(data_path,'Gangnam-gu_subway.shp'))
segment = gpd.read_file(os.path.join(data_path,'Gangnam-gu_streets.shp'))
centroid = segment['geometry'].centroid
print(subway.crs)
print(segment.crs)
print(centroid.crs)


''' Extract Coordinates '''
crds = [[list(centroid.geometry[i].coords)[0][0], list(centroid.geometry[i].coords)[0][1]] for i in range(len(centroid))]
crds_arr = np.array(crds) 
sub_crds = [[list(subway.geometry[i].coords)[0][0], list(subway.geometry[i].coords)[0][1]] for i in range(len(subway))]
sub_crds_arr = np.array(sub_crds) 



''' Load OSM streets as a Graph using OSMnx '''
G = ox.graph_from_place('강남구, 서울특별시, 대한민국', network_type='all_private') # 오래 걸림
G_utm = ox.project_graph(G, to_crs="epsg:5179") 



''' Get Nearest Nodes using OSMnx '''
nearest, dist_st = ox.distance.nearest_nodes(G_utm, X=crds_arr[:,0], Y=crds_arr[:,1], return_dist=True)
nearest_sub, dist_sub = ox.distance.nearest_nodes(G_utm, X=sub_crds_arr[:,0], Y=sub_crds_arr[:,1], return_dist=True)




''' Plot OSMnx graph with nearest subway nodes and nearest stree nodes '''
G_utm_nodes = list(G_utm.nodes)
target_idx = [G_utm_nodes.index(nearest[i]) for i in range(len(nearest))]
subway_idx = [G_utm_nodes.index(nearest_sub[i]) for i in range(len(nearest_sub))]

nc = ['black']* len(list(G_utm.nodes))
for i in range(len(nc)): 
    if i in target_idx: 
        nc[i] = 'blue'
    if i in subway_idx: 
        nc[i] = 'red'
ns = [0.0005]* len(list(G_utm.nodes))
for i in range(len(ns)): 
    if i in target_idx: 
        ns[i] = 0.03
    if i in subway_idx: 
        ns[i] = 10

fig, ax = ox.plot_graph(G_utm, bgcolor='w', node_color=nc, node_edgecolor=None, node_size=ns,
                            node_zorder=3, edge_color='black', edge_linewidth=0.2, dpi=300)
plt.show()


''' Calculate the Shortest Path '''
shortest_dist2sub = []
for i in tqdm(range(len(nearest))): 
    centroid_point = (G_utm.nodes[nearest[i]]['x'], G_utm.nodes[nearest[i]]['y'])
    buffer = Point(centroid_point).buffer(1000) # 1000m 이내의 지하철역까지만 고려함 
    temp = []
    for j in range(len(nearest_sub)): 
        subway_point_xy = (G_utm.nodes[nearest_sub[j]]['x'], G_utm.nodes[nearest_sub[j]]['y'])   
        if buffer.contains(Point(subway_point_xy)):
            try:
                dist = nx.shortest_path_length(G_utm, nearest[i], nearest_sub[j],weight='length')
                temp.append(dist)
            except: 
                pass
    if len(temp) > 0 : 
        shortest_dist2sub.append(min(temp))
    else: 
        shortest_dist2sub.append(None)


''' Export the results '''
segment['dist2sub'] = shortest_dist2sub # add the distance to the nearest sub as a new column 
segment.to_file(os.path.join(data_path, 'result.shp'), encoding='cp949')



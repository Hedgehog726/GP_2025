from trajectory_compression import compress_trajectory
from visualizer import visualize_trajectory_compare
from visualizer import visualize_points

# compress_trajectory('./data/processed.csv', './data/dp_compressed.csv',
#                     'mmsi','time','lon','lat','dp',threshold=50)

# compress_trajectory('./data/processed.csv', './data/tdtr_compressed.csv',
#                     'mmsi','time','lon','lat','td-tr',threshold=50)

# compress_trajectory('./data/processed.csv', './data/sw_compressed.csv',
#                     'mmsi','time','lon','lat','sw',threshold=50)

visualize_trajectory_compare(
    original_csv='./data/processed.csv',
    compressed_csv='./data/sw_compressed.csv',
    output_image='trajectory_comparison.png'
)

# visualize_points('./data/sw_compressed.csv', lon_col='lon', lat_col='lat', id_col='mmsi', crs='EPSG:4326')
from trajectory_compression import compress_trajectory
from trajectory_compression import visualize_trajectory_compare
from trajectory_compression import visualize_points
from trajectory_compression import export_csv_to_vector

compress_trajectory('./data/processed.csv', './data/dp_compressed.csv',
                    'mmsi','time','lon','lat','dp',threshold=50)

# compress_trajectory('./data/processed.csv', './data/tdtr_compressed.csv',
#                     'mmsi','time','lon','lat','td-tr',threshold=50)

# compress_trajectory('./data/processed.csv', './data/sw_compressed.csv',
#                     'mmsi','time','lon','lat','sw',threshold=50)

# visualize_trajectory_compare(
#     original_csv='./data/processed.csv',
#     compressed_csv='./data/sw_compressed.csv',
#     output_image='trajectory_comparison.png'
# )

# visualize_points('./data/sw_compressed.csv', lon_col='lon', lat_col='lat', id_col='mmsi', crs='EPSG:4326')

# export_csv_to_vector(csv_path='./data/sw_compressed.csv', output_path='./data/sw_compressed.gpkg')
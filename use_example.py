from trajectory_compression import trajectory_compression

# trajectory_compression.compress_trajectory('./data/processed.csv', './data/dp_compressed.csv',
#                     'mmsi','time','lon','lat','dp',threshold=50)

# trajectory_compression.compress_trajectory('./data/processed.csv', './data/tdtr_compressed.csv',
#                     'mmsi','time','lon','lat','td-tr',threshold=50)

# trajectory_compression.compress_trajectory('./data/processed.csv', './data/sw_compressed.csv',
#                     'mmsi','time','lon','lat','sw',threshold=50)

# trajectory_compression.visualize_trajectory_compare(
#     original_csv='./data/processed.csv',
#     compressed_csv='./data/sw_compressed.csv',
#     output_image='trajectory_comparison.png'
# )

# trajectory_compression.visualize_points('./data/sw_compressed.csv', lon_col='lon', lat_col='lat', id_col='mmsi', crs='EPSG:4326', output_image='./tra.png')

# trajectory_compression.export_csv_to_vector(csv_path='./data/sw_compressed.csv', output_path='./data/sw_compressed.gpkg')
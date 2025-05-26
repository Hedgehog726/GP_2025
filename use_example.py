from trajectory_compression import compress_trajectory

# compress_trajectory('./data/processed.csv', './data/dp_compressed.csv',
#                     'mmsi','time','lon','lat','dp',threshold=50)

compress_trajectory('./data/processed.csv', './data/tdtr_compressed.csv',
                    'mmsi','time','lon','lat','td-tr',threshold=50)
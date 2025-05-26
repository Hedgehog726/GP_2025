# GP_2025
# Trajectory Compression Toolkit

A Python toolkit for compressing GPS trajectory data using algorithms like:
- Douglas-Peucker (DP)
- Top-Down Time Ratio (TD-TR)
- Sliding Window

## 📦 Features

- Easy-to-use interface
- Supports multiple compression algorithms
- Customizable threshold & fields

from compressor import compress_trajectory

compress_trajectory(
    input_path='input.csv',
    output_path='output.csv',
    id_col='user_id',
    time_col='timestamp',
    lon_col='lon',
    lat_col='lat',
    method='dp',
    threshold=0.0001
)

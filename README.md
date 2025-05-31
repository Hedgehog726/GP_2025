# GP_2024-2025
# 🛰️ Trajectory Compression Toolkit

A Python toolkit to compress GPS trajectory data using multiple algorithms including:

- Douglas-Peucker (DP)
- Top-Down Time Ratio (TD-TR)
- Sliding Window
And it also provide the functionality of visualization and export
This package is useful for data preprocessing in GPS trace simplification, map matching, mobility analytics, and other geospatial tasks.

---

## ⚙️ Requirements

- Python **3.9**
- pandas
- geopandas

Install dependencies:

pandas geopandas shapely contextily

---------

## compression method:
### dp: douglas peaucker
### td-tr:topdown time ration
### sw: sliding window
## 🛠️ Usage
from trajectory_compression import compress_trajectory

compress_trajectory(
    input_path='raw_trajectory.csv',
    output_path='compressed_trajectory.csv',
    id_col='user_id',
    time_col='timestamp',
    lon_col='lon',
    lat_col='lat',
    method='td-tr',       # or 'dp', 'sw'
    threshold=50,
    time_weight=0.6       # only used by 'td-tr'
)
usage example: /use_example.py


## 📥 Input Data Format

The input should be a **CSV file** or a **pandas.DataFrame** with the following columns:

```csv
id,timestamp,lon,lat
1,2024-01-01 08:00:00,121.4737,31.2304
1,2024-01-01 08:05:00,121.4740,31.2308
1,2024-01-01 08:10:00,121.4745,31.2312
...







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
- shapely
- contextily

---------
## ⚙️ Installation
run the following command
`pip install git+https://github.com/Hedgehog726/GP_2025.git`


---------
## 🛠️ Usage
```
from trajectory_compression import trajectory_compression

trajectory_compression.compress_trajectory('./data/processed.csv', './data/dp_compressed.csv',
                    'mmsi','time','lon','lat','dp',threshold=50)
```

usage example: Example.ipynb


## 📥 Input Data Format

The input should be a **CSV file** or a **pandas.DataFrame** with the following columns:

```csv
id,timestamp,lon,lat
1,2024-01-01 08:00:00,121.4737,31.2304
1,2024-01-01 08:05:00,121.4740,31.2308
1,2024-01-01 08:10:00,121.4745,31.2312
...







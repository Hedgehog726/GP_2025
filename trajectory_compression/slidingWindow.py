import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
import math

def perpendicular_distance_proj(point, start, end):
    """
    calculate the distance from a point to a segment
    """
    if start == end:
        return math.dist(point, start)

    x, y = point
    x1, y1 = start
    x2, y2 = end

    num = abs((y2 - y1) * x - (x2 - x1) * y + x2 * y1 - y2 * x1)
    den = math.hypot(x2 - x1, y2 - y1)
    return num / den

def sliding_window_proj(coords, epsilon):
    """
    Sliding Window algorithm on projected coordinates
    """
    keep_indices = [0]  # Always keep the first point
    start = 0
    end = 2
    cur = 1
    m = 1
    count = len(coords) - 1

    while end < len(coords):
        d_cur = perpendicular_distance_proj(coords[cur], coords[start], coords[end])
        d_m = perpendicular_distance_proj(coords[m], coords[start], coords[end])

        if d_cur > epsilon or d_m > epsilon:
            keep_indices.append(cur)
            start = cur
            cur = start + 1
            end = start + 2
            m = cur
        else:
            if d_cur > d_m:
                m = cur
            cur = end
            end += 1

    keep_indices.append(count)  # Always keep the last point
    return keep_indices

def compress_sw_with_projection(df, lon_col='lon', lat_col='lat', crs_from="EPSG:4326", crs_to="EPSG:3857", epsilon=50):
    """
    Use projection + sliding window to compress the trajectory
    - epsilon: max perpendicular distance (meters)
    """
    gdf = gpd.GeoDataFrame(df.copy(), geometry=gpd.points_from_xy(df[lon_col], df[lat_col]), crs=crs_from)
    gdf = gdf.to_crs(crs_to)

    coords = [(geom.x, geom.y) for geom in gdf.geometry]
    keep_indices = sliding_window_proj(coords, epsilon)

    return df.iloc[keep_indices].reset_index(drop=True)

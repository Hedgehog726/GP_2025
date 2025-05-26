import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
import math

def perpendicular_distance_proj(point, start, end):
    """calculate the distance to the line"""
    if start == end:
        return math.dist(point, start)

    x, y = point
    x1, y1 = start
    x2, y2 = end

    num = abs((y2 - y1) * x - (x2 - x1) * y + x2 * y1 - y2 * x1)
    den = math.hypot(x2 - x1, y2 - y1)
    return num / den

def douglas_peucker_proj(points, epsilon):
    if len(points) < 3:
        return points

    max_dist = 0.0
    index = 0
    for i in range(1, len(points) - 1):
        dist = perpendicular_distance_proj(points[i], points[0], points[-1])
        if dist > max_dist:
            index = i
            max_dist = dist

    if max_dist > epsilon:
        left = douglas_peucker_proj(points[:index + 1], epsilon)
        right = douglas_peucker_proj(points[index:], epsilon)
        return left[:-1] + right
    else:
        return [points[0], points[-1]]

def compress_dp_with_projection(df, lon_col='lon', lat_col='lat', crs_from="EPSG:4326", crs_to="EPSG:3857", epsilon=50):
    """
    use projection Douglas-Peucker  compress the trajectory
    - epsilon unit meter
    """
    # convert to the geoframe and project
    gdf = gpd.GeoDataFrame(df.copy(), geometry=gpd.points_from_xy(df[lon_col], df[lat_col]), crs=crs_from)
    gdf = gdf.to_crs(crs_to)

    # extract the point
    coords = [(geom.x, geom.y) for geom in gdf.geometry]
    simplified_coords = douglas_peucker_proj(coords, epsilon)

    # filter the left point with the beginning order
    keep_mask = gdf.geometry.apply(lambda p: (p.x, p.y) in simplified_coords)
    return df[keep_mask.values]
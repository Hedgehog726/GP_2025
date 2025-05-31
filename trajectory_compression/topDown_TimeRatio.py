import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import math


def perpendicular_distance(point, start, end):
    """point to line distance"""
    if start == end:
        return math.dist(point, start)

    x, y = point
    x1, y1 = start
    x2, y2 = end

    num = abs((y2 - y1) * x - (x2 - x1) * y + x2 * y1 - y2 * x1)
    den = math.hypot(x2 - x1, y2 - y1)
    return num / den


def time_ratio_error(ts, t1, t2):
    """time error：linear interpolation ratio vs real ratio"""
    if t1 == t2:
        return 0.0
    interp_ratio = (ts - t1).total_seconds() / (t2 - t1).total_seconds()
    ideal_ratio = interp_ratio
    return abs(interp_ratio - ideal_ratio)


def td_tr(points, times, epsilon, alpha=0.5):
    """Top-Down Time Ratio """
    if len(points) < 3:
        return list(range(len(points)))

    max_error = 0.0
    index = 0
    for i in range(1, len(points) - 1):
        space_err = perpendicular_distance(points[i], points[0], points[-1])
        time_err = time_ratio_error(times[i], times[0], times[-1])
        total_err = alpha * space_err + (1 - alpha) * time_err * space_err  # 时间误差单位归一化
        if total_err > max_error:
            max_error = total_err
            index = i

    if max_error > epsilon:
        left = td_tr(points[:index + 1], times[:index + 1], epsilon, alpha)
        right = td_tr(points[index:], times[index:], epsilon, alpha)
        return left[:-1] + [i + index for i in right]
    else:
        return [0, len(points) - 1]


def compress_td_tr_with_projection(df, time_col='timestamp', lon_col='lon', lat_col='lat',crs_from="EPSG:4326", crs_to="EPSG:3857",
                                   epsilon=50, alpha=0.5 ):
    """
    ues Top-Down Time Ratio ,unit: meter
    """
    # convert time
    df = df.copy()
    df[time_col] = pd.to_datetime(df[time_col])
    df = df.sort_values(time_col)

    # convert projection
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df[lon_col], df[lat_col]), crs=crs_from)
    gdf = gdf.to_crs(crs_to)

    # extract time and location
    coords = [(p.x, p.y) for p in gdf.geometry]
    times = list(df[time_col])

    # enforce the compression and return the indices
    keep_indices = td_tr(coords, times, epsilon, alpha)
    return df.iloc[keep_indices]
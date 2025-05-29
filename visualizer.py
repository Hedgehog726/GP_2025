import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from shapely.geometry import LineString
import contextily as ctx


def visualize_points(csv_path, lon_col='lon', lat_col='lat', id_col='mmsi', crs='EPSG:4326'):
    df = pd.read_csv(csv_path)
    
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df[lon_col], df[lat_col]), crs=crs)

    # classified by mmsi
    fig, ax = plt.subplots(figsize=(10, 8))
    gdf.plot(ax=ax, column=id_col, legend=False, cmap='tab20', markersize=10)
    
    ax.set_title("Trajectory Visualization", fontsize=14)
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    plt.grid(True)
    plt.show()

def visualize_trajectory_compare(original_csv, compressed_csv, 
                                      lon_col='lon', lat_col='lat', id_col='mmsi',
                                      crs_from='EPSG:4326', crs_to='EPSG:3857',
                                      output_image='trajectory.png'):
    """

    Parameters:
        original_csv: str - path to the original trajectory CSV
        compressed_csv: str - path to the compressed trajectory CSV
        lon_col, lat_col, id_col: str - column names for lon/lat/id
        crs_from: str - input CRS
        crs_to: str - projected CRS for accurate plotting
        output_image: str - file name to save the image
    """

    # def build_lines(df, label):
    #     df_gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df[lon_col], df[lat_col]), crs=crs_from)
    #     df_gdf = df_gdf.to_crs(crs_to)
    #     lines = []
    #     ids = []
    #     for traj_id, group in df_gdf.groupby(id_col):
    #         if len(group) > 1:
    #             line = LineString(group.geometry.tolist())
    #             lines.append(line)
    #             ids.append(f"{label}_{traj_id}")
    #     return gpd.GeoDataFrame({id_col: ids, 'geometry': lines}, crs=crs_to)


    def build_lines(df, label):
        df_gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df[lon_col], df[lat_col]), crs=crs_from)

        lines = []
        ids = []

        for traj_id, group in df_gdf.groupby(id_col):
            coords = list(group.geometry)
            segments = []
            current_segment = [coords[0]]

            for i in range(1, len(coords)):
                prev = coords[i - 1]
                curr = coords[i]
                delta_lon = abs(curr.x - prev.x)

                if delta_lon > 180:  # cross the boundry
                    # 断开轨迹段
                    if len(current_segment) >= 2:
                        segments.append(current_segment)
                    current_segment = [curr]
                else:
                    current_segment.append(curr)

            # 添加最后一段
            if len(current_segment) >= 2:
                segments.append(current_segment)

            # LineString
            for idx, seg in enumerate(segments):
                line = LineString(seg)
                lines.append(line)
                ids.append(f"{label}_{traj_id}_{idx}")
        return gpd.GeoDataFrame({id_col: ids, 'geometry': lines}, crs=crs_from).to_crs(crs_to)

    # Load and build LineStrings
    df_raw = pd.read_csv(original_csv)
    df_cmp = pd.read_csv(compressed_csv)

    gdf_raw_lines = build_lines(df_raw, 'Original')
    gdf_cmp_lines = build_lines(df_cmp, 'Compressed')

    # Plot
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_xticks([])
    ax.set_yticks([])
    gdf_raw_lines.plot(ax=ax, color='blue', linewidth=1, alpha=0.5, label='Original')
    gdf_cmp_lines.plot(ax=ax, color='red', linewidth=1, alpha=0.5, label='Compressed')
    
    # Optional basemap
    ctx.add_basemap(ax, crs=gdf_raw_lines.crs)

    plt.legend()
    plt.title("Trajectory Comparison")
    plt.savefig(output_image, dpi=300)
    plt.show()

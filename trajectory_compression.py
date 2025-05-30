from douglas_peucker import compress_dp_with_projection as dp
from topDown_TimeRatio import compress_td_tr_with_projection as tdtr
from slidingWindow import compress_sw_with_projection as sw
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from shapely.geometry import LineString
import contextily as ctx

def compress_trajectory(input_path,output_path,id_col='id',time_col='time',lon_col='lon',lat_col='lat',method='dp',threshold=0.0001,time_weight=0.5):
    """
    compress the input trajectory
    parameters:
    - input_path: str，input the trajectories csv file
    - output_path: str，compressed saved file
    - id_col, time_col, lon_col, lat_col: str，atttribute's name
    - method: str，compression name，option: 'dp'（Douglas-Peucker）, 'td-tr', 'sw'（Sliding Window）
    - threshold: float，compression threshold, meter or ratio
    - time_weight: float，for TD-TR time weight
    """
    pass  # implemention
    tra_data=pd.read_csv(input_path,index_col=None)
    trajectories=tra_data.groupby(id_col)
    compressed_data=pd.DataFrame()
    # compressed_traj = pd.DataFrame(columns=[id_col,time_col, lon_col, lat_col])
    for traj_id,traj in trajectories:
        if method == 'dp':
            compressed_traj = dp(traj,lon_col,lat_col,epsilon=threshold)
        elif method == 'td-tr':
            compressed_traj = tdtr(traj, time_col, lon_col, lat_col,epsilon=threshold,alpha=time_weight) # add the method
        elif method == 'sw':
            compressed_traj = sw(traj, lon_col, lat_col, epsilon=threshold)
        compressed_traj=compressed_traj.copy()
        compressed_traj[id_col] = traj_id
        compressed_data = pd.concat([compressed_data, compressed_traj])

    compressed_data.to_csv(output_path,index=False)


def visualize_points(csv_path, lon_col='lon', lat_col='lat', id_col='mmsi', crs='EPSG:4326', output_image='trajectoryPoints.png'):
    """
    Visualize the trajectory points
    Parameters:
    csv_path: str - path to the trajectory CSV
    lon_col, lat_col, id_col: str - column names for lon/lat/id
    crs_from: str - input CRS
    output_image: str - file name to save the image
    """
    df = pd.read_csv(csv_path)
    
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df[lon_col], df[lat_col]), crs=crs)

    # classified by mmsi
    fig, ax = plt.subplots(figsize=(10, 8))
    gdf.plot(ax=ax, column=id_col, legend=False, cmap='tab20', markersize=10)
    
    ax.set_title("Trajectory Visualization", fontsize=14)
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    plt.grid(True)
    plt.savefig(output_image, dpi=300)
    plt.show()

def visualize_trajectory_compare(original_csv, compressed_csv, 
                                      lon_col='lon', lat_col='lat', id_col='mmsi',
                                      crs_from='EPSG:4326', crs_to='EPSG:3857',
                                      output_image='trajectory.png'):
    """
    Compare the trajectories before and after the compression
    Parameters:
        original_csv: str - path to the original trajectory CSV
        compressed_csv: str - path to the compressed trajectory CSV
        lon_col, lat_col, id_col: str - column names for lon/lat/id
        crs_from: str - input CRS
        crs_to: str - projected CRS for accurate plotting
        output_image: str - file name to save the image
    """



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
                    if len(current_segment) >= 2:
                        segments.append(current_segment)
                    current_segment = [curr]
                else:
                    current_segment.append(curr)

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
    
    # Add basemap
    ctx.add_basemap(ax, crs=gdf_raw_lines.crs)

    plt.legend()
    plt.title("Trajectory Comparison")
    plt.savefig(output_image, dpi=300)
    plt.show()
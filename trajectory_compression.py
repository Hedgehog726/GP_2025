from douglas_peucker import compress_dp_with_projection as dp
from TopDown_TimeRatio import compress_td_tr_with_projection as tdtr
import pandas as pd
def compress_trajectory(input_path,output_path,id_col='id',time_col='time',lon_col='lon',lat_col='lat',method='dp',threshold=0.0001,time_weight=0.5):
    """
    对输入轨迹进行压缩处理

    参数:
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
            compressed_traj=dp(traj,lon_col,lat_col,epsilon=threshold)
        elif method == 'td-tr':
            compressed_traj = tdtr(traj, time_col, lon_col, lat_col,epsilon=threshold,alpha=time_weight) # add the method
        elif method == 'sw':
            compressed_traj = dp(traj, time_col, lon_col, lat_col)
        compressed_traj=compressed_traj.copy()
        compressed_traj[id_col] = traj_id
        compressed_data = pd.concat([compressed_data, compressed_traj])

    compressed_data.to_csv(output_path,index=False)


import os

import uuid

import pandas as pd

import cx_rate
import trials
from flydance.io.csv_append import append_to_csv
from flydance.io.save_csv import save_df

metafile = 'results/generated_meta.tsv'

params = dict(
    T_outbound=12000,
    T_inbound=12000,
    seed=1,
    noise=0.12,
    w_noise=0.012,
    mem_loss_k=0.2,
    n_iterations=100,
    init_vel_x=0.0,
    init_vel_y=0.1,
    # walk_func=trials.walking,
    traj_folder='results/trajectories/prepost_control/',
    reward_radius=0,
    generator_mode='Control'
)

if __name__ == '__main__':
    init_vel = [params['init_vel_x'], params['init_vel_y']]
    for i in range(params['n_iterations']):
        cx = cx_rate.CXRatePontinSwitch(noise=params['noise'],
                                        weight_noise=params['w_noise'],
                                        mem_loss_k=params['mem_loss_k'])  # , random_seed=seed)
        results = trials.run_trial_switch(T_outbound=params['T_outbound'],
                                          T_inbound=params['T_inbound'],
                                          noise=params['noise'],
                                          weight_noise=params['w_noise'],
                                          cx=cx,
                                          mode=params['generator_mode'],
                                          # walk_func=params['walk_func'],
                                          walk_func=trials.walking,
                                          init_velocity=init_vel,
                                          reward_radius=params['reward_radius'])
        print(results['pos'].shape)
        df_traj = pd.DataFrame(results['pos'], columns=['x', 'y']).rename_axis('step').reset_index()
        print(df_traj.head())

        my_uuid = uuid.uuid1()
        my_filename = '{}.csv.gz'.format(my_uuid)

        metadata = params.copy()
        metadata['filename'] = my_filename
        print(metadata)
        metadata = pd.DataFrame(metadata, index=[0])
        append_to_csv(metafile, metadata, sep='\t')
        save_df(df_traj, os.path.join(params['traj_folder'], '{}'.format(my_filename)), create_dirs=True)



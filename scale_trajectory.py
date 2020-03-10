import os
import pandas as pd

import argparse

from flydance.io.save_csv import save_df

config = dict(steps_per_sec=100,
              cmk=1.2/(0.559*100))  # cm

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('traj', help='trajectory filename')
    args = parser.parse_args()
    if not os.path.isfile(args.traj):
        raise Exception('file not found: {}'.format(args.traj))

    df = pd.read_csv(args.traj)
    df['sec'] = df.step / config['steps_per_sec']
    df['x_cm'] = df.x * config['cmk']
    df['y_cm'] = df.y * config['cmk']
    print('saving scaled {}...'.format(args.traj))
    save_df(df, args.traj)

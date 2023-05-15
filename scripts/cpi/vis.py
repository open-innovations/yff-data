import yaml
import pandas as pd
from scripts.util.util import tick_gen

def update_ticks(data_dir, vis_dir):

    #get the labels
    data = pd.read_csv(data_dir)
    min, max, labels = tick_gen(data, dtype='percent')

    with open(vis_dir) as f:
        viz = yaml.safe_load(f.read())

    # Update the viz definition
    viz[1]['config']['axis']['x']['max'] = max
    viz[1]['config']['axis']['x']['min'] = min
    viz[1]['config']['axis']['x']['ticks'] = labels

    # Write config to file
    with open(vis_dir, 'w') as f:
        f.write(yaml.dump(
            viz,
            default_flow_style=False
        ))

if __name__ == '__main__':
    data_dir = 'src/_data/sources/cpi/cpi.csv'
    vis_dir = 'src/dashboard/cpi/_data/visualisations.yaml'
    update_ticks(data_dir, vis_dir)

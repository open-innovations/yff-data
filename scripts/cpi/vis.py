import yaml
import pandas as pd
import os
from scripts.util.util import tick_gen

def update_ticks(data_dir, vis_dir, visnum):

    #get the labels
    data = pd.read_csv(data_dir)
    min, max, labels = tick_gen(data, dtype='percent')
    #print(min, max)
    with open(vis_dir) as f:
        viz = yaml.safe_load(f.read())

    # Update the viz definition
    viz[visnum]['config']['axis']['x']['max'] = max
    viz[visnum]['config']['axis']['x']['min'] = min
    viz[visnum]['config']['axis']['x']['ticks'] = labels

    #print(viz[1]['config']['axis']['x']['ticks'])
    # Write config to file
    with open(vis_dir, 'w') as f:
        f.write(yaml.dump(
            viz,
            default_flow_style=False
        ))

if __name__ == '__main__':
    data_dir = 'src/_data/sources/cpi/'
    vis_dir = 'src/dashboard/cpi/_data/visualisations.yaml'
    update_ticks(os.path.join(data_dir,'cpi_barchart.csv'), vis_dir, 1)
    update_ticks(os.path.join(data_dir, 'cpi_all_category_bar_chart.csv'), vis_dir, 2)

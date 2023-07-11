import yaml
import pandas as pd
import os
from scripts.util.util import tick_gen

def update_ticks(data_dir, vis_dir):

    #get the labels
    data = pd.read_csv(data_dir, nrows=6)
    min, max, labels = tick_gen(data, suffix='%')
    #print(min, max)
    with open(vis_dir) as f:
        viz = yaml.safe_load(f.read())

    # Update the viz definition
    viz['config']['axis']['x']['max'] = max
    viz['config']['axis']['x']['min'] = min
    viz['config']['axis']['x']['ticks'] = labels

    #print(viz[1]['config']['axis']['x']['ticks'])
    # Write config to file
    with open(vis_dir, 'w') as f:
        f.write(yaml.dump(
            viz,
            default_flow_style=False
        ))

if __name__ == '__main__':
    data_dir = 'src/_data/sources/cpi/'
    vis_dir = 'src/dashboard/cpi/_data/visualisation'
    update_ticks(os.path.join(data_dir,'cpi_barchart.csv'), os.path.join(vis_dir, 'young_people_barchart.yml'))
    update_ticks(os.path.join(data_dir,'cpi_summary_barchart.csv'), os.path.join(vis_dir, 'cpi_summary_barchart.yml'))
    update_ticks(os.path.join(data_dir, 'cpi_all_category_bar_chart.csv'), os.path.join(vis_dir, 'all_category_barchart.yml'))

# -*- coding: utf-8 -*-

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from fiba_inbounder.settings import LOGGER
from fiba_inbounder.formulas import get_sub_map_synergy
from fiba_reporter.post_game_report import FibaPostGameReportSynergy
sns.set(font_scale=0.7)

class FibaSubReport():
    def _gen_sub_heatmap(self):
        for t in self.sub_map_df['entityId'].unique():
            sub_heatmap_df = self.sub_map_df[self.sub_map_df['entityId']==t].groupby(['personId']).sum()
            sub_heatmap_df = sub_heatmap_df.sort_values(by=sub_heatmap_df.columns.tolist(), ascending=False)

            for col in sub_heatmap_df.columns.tolist():
                sub_heatmap_df[col] = sub_heatmap_df[col] / sub_heatmap_df[col].sum()
            
            plt.title(t)
            fig = sns.heatmap(sub_heatmap_df, cmap='PuBu', linewidths=0.5, cbar=False).get_figure()
            
            filename = u'./output/heatmap/{team}.png'.format(team=t)
            LOGGER.info(u'Generate Sub Heatmap to {filename}'.format(filename=filename))
            fig.savefig(filename)
class FibaSubReportSynergy(FibaSubReport):
    def __init__(self, game_id_list):
        r_list = [FibaPostGameReportSynergy(game_id) for game_id in game_id_list]
        self.sub_map_df = pd.concat([get_sub_map_synergy(r.sub_df) for r in r_list], sort=False)
        #TODO get id_table
        #self.id_table = {k: v for r in r_list for k, v in r.id_table.items()}

def main():
    version = raw_input('Stats version?\n\t(8) Synergy\n')
    num_games = raw_input('How Many Games? ')
    game_id_list = list()

    if int(version) == 8:
        for g in range(int(num_games)):
            print '\nGame {i} of {n}'.format(i=(g+1), n=int(num_games))
            game_id = raw_input('\tGame Id? ')
            game_id_list.append(str(game_id))
        r = FibaSubReportSynergy(game_id_list)
    
    else: 
        print 'NOT SUPPORT'
        return

    r._gen_sub_heatmap()

if __name__ == '__main__':
    main()

# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

from fiba_inbounder.settings import LOGGER
from fiba_inbounder.settings_synergy import FONT_PATH
from fiba_inbounder.formulas import get_sub_map_synergy, get_score_map_synergy
from fiba_reporter.post_game_report import FibaPostGameReportSynergy

fm._rebuild()
plt.rcParams['font.family'] = ['Noto Snas TC']
plt.rcParams['figure.figsize'] = 12.78, 4.8
sns.set(font_scale=0.7)
sns.set(font=fm.FontProperties(fname=FONT_PATH).get_family())
sns.set_style('whitegrid', {'font.sans-serif':['Noto Sans TC']})

class FibaTimelineReport():
    def _gen_sub_heatmap(self):
        for t in self.sub_map_df['entityId'].unique():
            sub_heatmap_df = self.sub_map_df[self.sub_map_df['entityId']==t].groupby(['personId']).sum()
            sub_heatmap_df = sub_heatmap_df.sort_values(by=sub_heatmap_df.columns.tolist(), ascending=False)
            sub_heatmap_df.index = sub_heatmap_df.index.map(self.id_table)

            for col in sub_heatmap_df.columns.tolist():
                sub_heatmap_df[col] = sub_heatmap_df[col] / sub_heatmap_df[col].sum()

            fig, ax = plt.subplots(figsize=(12.78, 4.8))
            sns.heatmap(sub_heatmap_df, cmap='PuBu', linewidths=0.5, xticklabels=12, cbar=False, ax=ax)
            ax.set_xticklabels(ax.get_xticklabels(), rotation=90, fontsize=7)
            ax.set(xlabel='', ylabel='')

            filename = u'./output/heatmap/sub/{team}.png'.format(team=t)
            LOGGER.info(u'Generate Sub Heatmap to {filename}'.format(filename=filename))
            fig.savefig(filename)

    def _gen_score_heat_map(self):
        score_heatmap_df = self.score_map_df.groupby(['entityId']).mean()
        score_heatmap_df.index = score_heatmap_df.index.map(self.id_table)

        fig, ax = plt.subplots(figsize=(12.78, 1.2))
        sns.heatmap(score_heatmap_df, cmap='PuBu', annot=True, linewidths=0.5, xticklabels=12, cbar=False, ax=ax)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=90, fontsize=7)
        ax.set(xlabel='', ylabel='')

        filename = u'./output/heatmap/score.png'
        LOGGER.info(u'Generate Score Heatmap to {filename}'.format(filename=filename))
        fig.savefig(filename)

class FibaTimelineReportSynergy(FibaTimelineReport):
    def __init__(self, game_id_list):
        r_list = [FibaPostGameReportSynergy(game_id) for game_id in game_id_list]
        self.sub_map_df = pd.concat([get_sub_map_synergy(r.sub_df) for r in r_list], sort=False)
        self.score_map_df = pd.concat([get_score_map_synergy(r.shot_df) for r in r_list], sort=False)
        self.id_table = {k: v for r in r_list for k, v in r.id_table.items()}

def main():
    version = raw_input('Stats version?\n\t(8) Synergy\n')
    num_games = raw_input('How Many Games? ')
    game_id_list = list()

    if int(version) == 8:
        for g in range(int(num_games)):
            print '\nGame {i} of {n}'.format(i=(g+1), n=int(num_games))
            game_id = raw_input('\tGame Id? ')
            game_id_list.append(str(game_id))
        r = FibaTimelineReportSynergy(game_id_list)
    
    else: 
        print 'NOT SUPPORT'
        return

    r._gen_sub_heatmap()
    r._gen_score_heat_map()

if __name__ == '__main__':
    main()

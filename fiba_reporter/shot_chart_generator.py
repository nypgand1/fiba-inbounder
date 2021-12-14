# -*- coding: utf-8 -*-

import os
import pandas as pd
from fiba_inbounder.settings import LOGGER
from fiba_inbounder.formulas import update_zone, update_zone_pleague
from fiba_inbounder.shot_chart import ShotChart
from fiba_reporter.post_game_report import FibaPostGameReportV5, FibaPostGameReportPLeague

class FibaShotChartGenerator():
    @staticmethod
    def _gen_shot_chart(filename, df):
            fgm_list = [0] * 14
            fga_list = [0] * 14
            for r in df.to_dict(orient='records'):
                if r['ZONE'] not in range(14):
                    continue
                fgm_list[r['ZONE']] = r['FGM']
                fga_list[r['ZONE']] = r['FGA']
            ShotChart(filename, fgm_list, fga_list)

    def _update_shot_zone(self):
        update_zone(self.shot_df)

    def _gen_team_shot_chart(self):
        self._update_shot_zone()
        
        team_shot_zone_df = self.shot_df.sort_values(['ZONE']).groupby(['T1', 'ZONE'], as_index=False, sort=False).sum()
        for t in team_shot_zone_df['T1'].unique():
            filename = u'./output/{team}'.format(team=self.id_table.get(t, t))
            LOGGER.info(u'Generate Shot Chart to {filename}.png'.format(filename=filename))
            tsz_df = team_shot_zone_df[team_shot_zone_df['T1'].str.match(t)]
            FibaShotChartGenerator._gen_shot_chart(filename, tsz_df)

        team_shot_zone_df = self.shot_df.sort_values(['ZONE']).groupby(['OppTeamCode', 'ZONE'], as_index=False, sort=False).sum()
        for t in team_shot_zone_df['OppTeamCode'].unique():
            if t in self.id_table.keys():
                team = self.id_table[t]
            else:
                team = t
 
            filename = u'./output/{team}_opp'.format(team=self.id_table.get(t, t))
            LOGGER.info(u'Generate Shot Chart to {filename}.png'.format(filename=filename))
            tsz_df = team_shot_zone_df[team_shot_zone_df['OppTeamCode'].str.match(t)]
            FibaShotChartGenerator._gen_shot_chart(filename, tsz_df)

    def _gen_player_shot_chart(self):
        self._update_shot_zone()
        
        player_shot_zone_df = self.shot_df.sort_values(['ZONE']).groupby(['T1', 'C1', 'ZONE'], as_index=False, sort=False).sum()
        for t in player_shot_zone_df['T1'].unique():
            path = u'./output/{team}'.format(team=self.id_table.get(t, t))
            if not os.path.exists(path):
                os.mkdir(path)
            tsz_df = player_shot_zone_df[player_shot_zone_df['T1'].str.match(t)]
            for p in tsz_df['C1'].unique():
                psz_df = tsz_df[tsz_df['C1']==p]
                filename = u'{path}/{player}'.format(path=path, player=self.id_table.get(p, p))
                LOGGER.info(u'Generate Shot Chart to {filename}.png'.format(filename=filename))
                FibaShotChartGenerator._gen_shot_chart(filename, psz_df)

class FibaShotChartGeneratorV5(FibaShotChartGenerator):
    def __init__(self, game_id_list):
        r_list = [FibaPostGameReportV5(match_id) for match_id in game_id_list]
        self.shot_df = pd.concat([r.shot_df for r in r_list], sort=False)
        self.id_table = {k: v for r in r_list for k, v in r.id_table.items()}    

class FibaShotChartGeneratorPLeague(FibaShotChartGenerator):
    def __init__(self, game_id_list):
        r_list = [FibaPostGameReportPLeague(game_id) for game_id in game_id_list]
        self.shot_df = pd.concat([r.shot_df for r in r_list], sort=False)
        self.id_table = {k: v for r in r_list for k, v in r.id_table.items()}    

    def _update_shot_zone(self):
        update_zone_pleague(self.shot_df)

def main():
    version = raw_input('fiba stats version?\n\t(5) v5\n\t(9) P League\n')
    num_games = raw_input('How Many Games? ')
    game_id_list = list()

    if int(version) == 5:
        for g in range(int(num_games)):
            print '\nGame {i} of {n}'.format(i=(g+1), n=int(num_games))
            match_id = raw_input('\tMatch Id? ')
            game_id_list.append(str(match_id))
        r = FibaShotChartGeneratorV5(game_id_list)
     
    elif int(version) == 9:
        for g in range(int(num_games)):
            print '\nGame {i} of {n}'.format(i=(g+1), n=int(num_games))
            game_id = raw_input('\tGame ID? ')
            game_id_list.append(str(game_id))
        r = FibaShotChartGeneratorPLeague(game_id_list)

    else: 
        print 'NOT SUPPORT'
        return
   
    r._gen_team_shot_chart()
    r._gen_player_shot_chart()

if __name__ == '__main__':
    main()

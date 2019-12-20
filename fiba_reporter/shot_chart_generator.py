# -*- coding: utf-8 -*-

import pandas as pd
from fiba_reporter.post_game_report import FibaPostGameReportV5
from fiba_inbounder.formulas import update_zone
from fiba_inbounder.shot_chart import ShotChart

class FibaShotChartGenerator():
    def _gen_team_shot_chart(self):
        update_zone(self.shot_df)
        
        def team_shot_chart(t, tsz_df):
            fgm_list = [0] * 14
            fga_list = [0] * 14
            for r in tsz_df.to_dict(orient='records'):
                fgm_list[r['ZONE']] = r['FGM']
                fga_list[r['ZONE']] = r['FGA']
            ShotChart('./output/{team}'.format(team=t), fgm_list, fga_list)

        team_shot_zone_df = self.shot_df.sort_values(['ZONE']).groupby(['T1', 'ZONE'], as_index=False, sort=False).sum()
        for t in team_shot_zone_df['T1'].unique():
            print t
            tsz_df = team_shot_zone_df[team_shot_zone_df['T1'].str.match(t)]
            team_shot_chart(t, tsz_df)

        team_shot_zone_df = self.shot_df.sort_values(['ZONE']).groupby(['OppTeamCode', 'ZONE'], as_index=False, sort=False).sum()
        for t in team_shot_zone_df['OppTeamCode'].unique():
            print '{team}_OPP'.format(team=t)
            tsz_df = team_shot_zone_df[team_shot_zone_df['OppTeamCode'].str.match(t)]
            team_shot_chart('{team}_OPP'.format(team=t), tsz_df)

class FibaShotChartGeneratorV5(FibaShotChartGenerator):
    def __init__(self, game_id_list):
        r_list = [FibaPostGameReportV5(match_id) for match_id in game_id_list]
        self.shot_df = pd.concat([r.shot_df for r in r_list], sort=False)
        self.id_table = {k: v for r in r_list for k, v in r.id_table.items()}    

def main():
    version = raw_input('fiba stats version?\n\t(5) v5\n\t(7) v7\n')
    num_games = raw_input('How Many Games? ')
    game_id_list = list()

    if int(version) == 5:
        for g in range(int(num_games)):
            print '\nGame {i} of {n}'.format(i=(g+1), n=int(num_games))
            match_id = raw_input('\tMatch Id? ')
            game_id_list.append(str(match_id))
        r = FibaShotChartGeneratorV5(game_id_list)
        
    r._gen_team_shot_chart()

if __name__ == '__main__':
    main()

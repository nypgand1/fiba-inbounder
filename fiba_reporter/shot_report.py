# -*- coding: utf-8 -*-

import pandas as pd
from fiba_reporter.post_game_report import FibaPostGameReportV5
from fiba_inbounder.formulas import update_zone, update_range, update_range_stats

class FibaShotReport():
    def _gen_team_shot_range_md(self):
        update_zone(self.shot_df)
        update_range(self.shot_df)
        
        result_str_list = list()
        team_shot_range_df = self.shot_df.sort_values(['ZONE']).groupby(['T1', 'RANGE'], as_index=False, sort=False).sum()
        
        for t in team_shot_range_df['T1'].unique():
            tsr_df = team_shot_range_df[team_shot_range_df['T1'].str.match(t)]
            update_range_stats(tsr_df)

            if t in self.id_table.keys():
                result_str_list.append(self.id_table[t])
            else:
                result_str_list.append(t)
            result_str_list.append('| Shot Range | Freq | FGM/A | eFG% |')
            result_str_list.append('|:---:|---:|---:|---:|')
            result_str_list.append('|' + tsr_df[['RANGE', 'FREQ_STR', 'FGM/A', 'EFG_STR']].to_csv(
                sep='|',
                line_terminator='|\n|',
                header=False,
                float_format='%.1f',
                encoding='utf-8',
                index=False)[:-2])
            result_str_list.append('|Total||{fgm}/{fga}||'.format(fgm=int(tsr_df['FGM'].sum()), fga=int(tsr_df['FGA'].sum())))
    
        return '\n'.join(result_str_list) + '\n'

    def _gen_opp_team_shot_range_md(self):
        update_zone(self.shot_df)
        update_range(self.shot_df)
        
        result_str_list = list()
        team_shot_range_df = self.shot_df.sort_values(['ZONE']).groupby(['OppTeamCode', 'RANGE'], as_index=False, sort=False).sum()
        
        for t in team_shot_range_df['OppTeamCode'].unique():
            tsr_df = team_shot_range_df[team_shot_range_df['OppTeamCode'].str.match(t)]
            update_range_stats(tsr_df)

            if t in self.id_table.keys():
                result_str_list.append('{team}\'s Opp'.format(team=self.id_table[t]))
            else:
                result_str_list.append('{team}\'s Opp'.format(team=t))
            result_str_list.append('| Shot Range | Freq | FGM/A | eFG% |')
            result_str_list.append('|:---:|---:|---:|---:|')
            result_str_list.append('|' + tsr_df[['RANGE', 'FREQ_STR', 'FGM/A', 'EFG_STR']].to_csv(
                sep='|',
                line_terminator='|\n|',
                header=False,
                float_format='%.1f',
                encoding='utf-8',
                index=False)[:-2])
            result_str_list.append('|Total||{fgm}/{fga}||'.format(fgm=int(tsr_df['FGM'].sum()), fga=int(tsr_df['FGA'].sum())))
    
        return '\n'.join(result_str_list) + '\n'


class FibaShotReportV5(FibaShotReport):
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
        r = FibaShotReportV5(game_id_list)
    
    print '## Shot Analysis\n' + r._gen_team_shot_range_md() + r._gen_opp_team_shot_range_md()

if __name__ == '__main__':
    main()

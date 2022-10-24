# -*- coding: utf-8 -*-

import pandas as pd
from fiba_reporter.post_game_report import FibaPostGameReportSynergy
'''
from fiba_inbounder.formulas import update_zone, update_zone_pleague, \
        update_range, update_range_stats
'''
class FibaSubReport():
    pass
    '''
    def _gen_team_shot_range_md(self):
        self._update_shot_zone_range()

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
            result_str_list.append(('|' + tsr_df[['RANGE', 'FREQ_STR', 'FGM/A', 'EFG_STR']].to_csv(
                sep='|',
                line_terminator='|\n|',
                header=False,
                float_format='%.1f',
                encoding='utf-8',
                index=False)[:-2]).decode('utf-8'))
            result_str_list.append('|Total||{fgm}/{fga}||'.format(fgm=int(tsr_df['FGM'].sum()), fga=int(tsr_df['FGA'].sum())))
    
        return '\n'.join(result_str_list) + '\n'
    '''
class FibaSubReportSynergy(FibaSubReport):
    def __init__(self, game_id_list):
        r_list = [FibaPostGameReportSynergy(game_id) for game_id in game_id_list]
        self.sub_df = pd.concat([r.sub_df for r in r_list], sort=False)
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

    #print '## Shot Analysis\n' + r._gen_team_shot_range_md() + r._gen_opp_team_shot_range_md() + r._gen_player_shot_range_md()

if __name__ == '__main__':
    main()

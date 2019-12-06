# -*- coding: utf-8 -*-

import pandas as pd
from fiba_reporter.post_game_report import FibaPostGameReportV5
from fiba_inbounder.formulas import update_four_factors
        
class FibaPreGameReport():
    def _gen_four_factors_md(self):
        update_four_factors(self.team_avg_stats_df)
        
        header_str_list = '| Team | Pace | eFG% | TO Ratio | OREB% | FT Rate |'
        align_str_list = '|:---:|---:|---:|---:|---:|---:|'
        table_str = '|' + self.team_avg_stats_df[['TeamCode', 'PACE', 'EFG_STR', 'TO_RATIO_STR', 'OR_PCT_STR', 'FT_RATE_STR']].to_csv(
            sep='|',
            line_terminator='|\n|',
            header=False,
            float_format='%.1f',
            encoding='utf-8',
            index=False)[:-2]
        
        result_str_list = [header_str_list, align_str_list, table_str]
        return '\n'.join(result_str_list) + '\n'


class FibaPreGameReportV5(FibaPreGameReport):
    def __init__(self, game_id_list):
        r_list = [FibaPostGameReportV5(match_id) for match_id in game_id_list]
        self.team_avg_stats_df = pd.concat([r.team_stats_df for r in r_list]).groupby(['TeamCode'], as_index=False, sort=False).mean()
        self.player_stats_df = pd.concat([r.player_stats_df for r in r_list])
        self.shot_df = pd.concat([r.shot_df for r in r_list])

def main():
    version = raw_input('fiba stats version?\n\t(5) v5\n\t(7) v7\n')
    num_games = raw_input('How Many Games? ')
    game_id_list = list()

    if int(version) == 5:
        for g in range(int(num_games)):
            print '\nGame {i} of {n}'.format(i=(g+1), n=int(num_games))
            match_id = raw_input('\tMatch Id? ')
            game_id_list.append(str(match_id))
        r = FibaPreGameReportV5(game_id_list)

    print '## Pace & Four Factors\n' + r._gen_four_factors_md()

if __name__ == '__main__':
    main()

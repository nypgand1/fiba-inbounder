# -*- coding: utf-8 -*-

import pandas as pd
from fiba_reporter.post_game_report import FibaPostGameReportV5
from fiba_inbounder.formulas import update_four_factors, update_efg, update_usg, \
        update_team_avg, update_player_avg
        
class FibaLeagueStatsReport():
    def _gen_four_factors_md(self):
        league_avg_stats_df = pd.DataFrame(self.team_stats_df.mean()).T
        update_four_factors(league_avg_stats_df)
        
        header_str_list = '| Team | Pace | eFG% | TO Ratio | OREB% | FT Rate |'
        align_str_list = '|:---:|---:|---:|---:|---:|---:|'
        table_str = '|League Avg|' + league_avg_stats_df[['PACE', 'EFG_STR', 'TO_RATIO_STR', 'OR_PCT_STR', 'FT_RATE_STR']].to_csv(
            sep='|',
            line_terminator='|\n|',
            header=False,
            float_format='%.1f',
            encoding='utf-8',
            index=False)[:-2]
        
        result_str_list = [header_str_list, align_str_list, table_str]
        return '\n'.join(result_str_list) + '\n'

    def _gen_team_avg_md(self):
        league_avg_stats_df = pd.DataFrame(self.team_stats_df.mean()).T
        update_team_avg(league_avg_stats_df)

        header_str_list = '| Team | 2PTM/A | 2PT% | 3PTM/A | 3PT% | FTM/A | FT% | OREB | DREB | REB | AST | STL | BLK | TOV | PF | PTS |'
        align_str_list = '|:---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|'
        table_str = '|League Avg|' + league_avg_stats_df[['FG2MA_STR', 'FG2P_STR', 'FG3MA_STR', 'FG3P_STR', 'FTMA_STR', 'FTP_STR', 
            'OR', 'DR', 'REB', 'AS', 'ST', 'BS', 'TO', 'PF', 'PTS']].to_csv(
            sep='|',
            line_terminator='|\n|',
            header=False,
            float_format='%.1f',
            encoding='utf-8',
            index=False)[:-2]

        result_str_list = [header_str_list, align_str_list, table_str]
        return '\n'.join(result_str_list) + '\n'

    def _gen_key_stats_md(self):
        league_avg_stats_df = pd.DataFrame(self.team_stats_df.mean()).T
        update_team_avg(league_avg_stats_df)
        
        header_str_list = '| Team | FB | 2nd | Off TO | Paint | Bench |'
        align_str_list = '|:---:|---:|---:|---:|---:|---:|'
        table_str = '|League Avg|' + league_avg_stats_df[['A_FBP', 'A_SCP', 'A_PAT', 'A_PIP', 'A_PFB']].to_csv(
            sep='|',
            line_terminator='|\n|',
            header=False,
            float_format='%.1f',
            encoding='utf-8',
            index=False)[:-2]
 
        result_str_list = [header_str_list, align_str_list, table_str]
        return '\n'.join(result_str_list) + '\n'

class FibaLeagueStatsReportV5(FibaLeagueStatsReport):
    def __init__(self, game_id_list):
        r_list = [FibaPostGameReportV5(match_id) for match_id in game_id_list]
        self.team_stats_df = pd.concat([r.team_stats_df for r in r_list], sort=False)
        self.player_stats_df = pd.concat([r.player_stats_df for r in r_list], sort=False)

def main():
    version = raw_input('fiba stats version?\n\t(5) v5\n\t(7) v7\n')
    num_games = raw_input('How Many Games? ')
    game_id_list = list()

    if int(version) == 5:
        for g in range(int(num_games)):
            print '\nGame {i} of {n}'.format(i=(g+1), n=int(num_games))
            match_id = raw_input('\tMatch Id? ')
            game_id_list.append(str(match_id))
        r = FibaLeagueStatsReportV5(game_id_list)

    print '## Pace & Four Factors\n' + r._gen_four_factors_md() + '\n## Traditional Stats\n' + r._gen_team_avg_md() + \
            '\n## Key Stats\n' + r._gen_key_stats_md()

if __name__ == '__main__':
    main()

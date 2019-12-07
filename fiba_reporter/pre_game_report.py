# -*- coding: utf-8 -*-

import pandas as pd
from fiba_reporter.post_game_report import FibaPostGameReportV5
from fiba_inbounder.formulas import update_four_factors, update_team_avg_str
        
class FibaPreGameReport():
    def _gen_four_factors_md(self):
        team_avg_stats_df = self.team_stats_df.groupby(['TeamCode'], as_index=False, sort=False).mean()
        update_four_factors(team_avg_stats_df)
        
        header_str_list = '| Team | Pace | eFG% | TO Ratio | OREB% | FT Rate |'
        align_str_list = '|:---:|---:|---:|---:|---:|---:|'
        table_str = '|' + team_avg_stats_df[['TeamCode', 'PACE', 'EFG_STR', 'TO_RATIO_STR', 'OR_PCT_STR', 'FT_RATE_STR']].to_csv(
            sep='|',
            line_terminator='|\n|',
            header=False,
            float_format='%.1f',
            encoding='utf-8',
            index=False)[:-2]
 
        opp_team_avg_stats_df = self.team_stats_df.groupby(['OppTeamCode'], as_index=False, sort=False).mean()
        update_four_factors(opp_team_avg_stats_df)
        
        opp_header_str_list = '| Opp Team | Pace | eFG% | TO Ratio | OREB% | FT Rate |'
        opp_align_str_list = '|:---:|---:|---:|---:|---:|---:|'
        opp_table_str = '|' + opp_team_avg_stats_df[['OppTeamCode', 'PACE', 'EFG_STR', 'TO_RATIO_STR', 'OR_PCT_STR', 'FT_RATE_STR']].to_csv(
            sep='|',
            line_terminator='|\n|',
            header=False,
            float_format='%.1f',
            encoding='utf-8',
            index=False)[:-2]
 
        rank_header_str_list = '| Team | Pace | eFG% | TO Ratio | OREB% | FT Rate |'
        rank_align_str_list = '|:---:|---:|---:|---:|---:|---:|'
        rank_table_str = '|' + team_avg_stats_df[['TeamCode', 'PACE_RANK', 'EFG_RANK', 'TO_RATIO_RANK', 'OR_PCT_RANK', 'FT_RATE_RANK']].to_csv(
            sep='|',
            line_terminator='|\n|',
            header=False,
            float_format='%d',
            encoding='utf-8',
            index=False)[:-2]
        
        result_str_list = [header_str_list, align_str_list, table_str, '',
                opp_header_str_list, opp_align_str_list, opp_table_str, '',
                rank_header_str_list, rank_align_str_list, rank_table_str]
        return '\n'.join(result_str_list) + '\n'

    def _gen_team_avg_md(self):
        team_avg_stats_df = self.team_stats_df.groupby(['TeamCode'], as_index=False, sort=False).mean()
        update_team_avg_str(team_avg_stats_df)

        header_str_list = '| Team | 2PTM/A | 2PT% | 3PTM/A | 3PT% | FTM/A | FT% | OREB | DREB | REB | AST | STL | BLK | TOV | PF | PTS |'
        align_str_list = '|:---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|'
        table_str = '|' + team_avg_stats_df[['TeamCode', 'FG2MA_STR', 'FG2P_STR', 'FG3MA_STR', 'FG3P_STR', 'FTMA_STR', 'FTP_STR', 
            'OR', 'DR', 'REB', 'AS', 'ST', 'BS', 'TO', 'PF', 'PTS']].to_csv(
            sep='|',
            line_terminator='|\n|',
            header=False,
            float_format='%.1f',
            encoding='utf-8',
            index=False)[:-2]
 
        opp_team_avg_stats_df = self.team_stats_df.groupby(['OppTeamCode'], as_index=False, sort=False).mean()
        update_team_avg_str(opp_team_avg_stats_df)

        opp_header_str_list = '| Opp Team | 2PTM/A | 2PT% | 3PTM/A | 3PT% | FTM/A | FT% | OREB | DREB | REB | AST | STL | BLK | TOV | PF | PTS |'
        opp_align_str_list = '|:---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|'
        opp_table_str = '|' + opp_team_avg_stats_df[['OppTeamCode', 'FG2MA_STR', 'FG2P_STR', 'FG3MA_STR', 'FG3P_STR', 'FTMA_STR', 'FTP_STR', 
            'OR', 'DR', 'REB', 'AS', 'ST', 'BS', 'TO', 'PF', 'PTS']].to_csv(
            sep='|',
            line_terminator='|\n|',
            header=False,
            float_format='%.1f',
            encoding='utf-8',
            index=False)[:-2]
 
        rank_header_str_list = '| Team | 2PTM/A | 2PT% | 3PTM/A | 3PT% | FTM/A | FT% | OREB | DREB | REB | AST | STL | BLK | TOV | PF | PTS |'
        rank_align_str_list = '|:---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|'
        rank_table_str = '|' + team_avg_stats_df[['TeamCode', 'FG2MA_RANK', 'FG2P_RANK', 'FG3MA_RANK', 'FG3P_RANK', 'FTMA_RANK', 'FTP_RANK', 
            'OR_RANK', 'DR_RANK', 'REB_RANK', 'AS_RANK', 'ST_RANK', 'BS_RANK', 'TO_RANK', 'PF_RANK', 'PTS_RANK']].to_csv(
            sep='|',
            line_terminator='|\n|',
            header=False,
            float_format='%d',
            encoding='utf-8',
            index=False)[:-2]
 
        opp_team_avg_stats_df = self.team_stats_df.groupby(['OppTeamCode'], as_index=False, sort=False).mean()
        update_team_avg_str(opp_team_avg_stats_df)


        result_str_list = [header_str_list, align_str_list, table_str, '',
                opp_header_str_list, opp_align_str_list, opp_table_str, '',
                rank_header_str_list, rank_align_str_list, rank_table_str]
        return '\n'.join(result_str_list) + '\n'

class FibaPreGameReportV5(FibaPreGameReport):
    def __init__(self, game_id_list):
        r_list = [FibaPostGameReportV5(match_id) for match_id in game_id_list]
        self.team_stats_df = pd.concat([r.team_stats_df for r in r_list], sort=False)
        self.player_stats_df = pd.concat([r.player_stats_df for r in r_list], sort=False)
        self.shot_df = pd.concat([r.shot_df for r in r_list], sort=False)

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

    print '## Pace & Four Factors\n' + r._gen_four_factors_md() + '\n## Traditional Stats\n' + r._gen_team_avg_md()

if __name__ == '__main__':
    main()

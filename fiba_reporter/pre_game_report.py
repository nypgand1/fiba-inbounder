# -*- coding: utf-8 -*-

import pandas as pd
from fiba_reporter.post_game_report import FibaPostGameReportV5
from fiba_inbounder.formulas import update_four_factors, update_efg, update_usg, \
        update_team_avg, update_player_avg
        
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
        update_team_avg(team_avg_stats_df)

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
        update_team_avg(opp_team_avg_stats_df)

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

        result_str_list = [header_str_list, align_str_list, table_str, '',
                opp_header_str_list, opp_align_str_list, opp_table_str, '',
                rank_header_str_list, rank_align_str_list, rank_table_str]
        return '\n'.join(result_str_list) + '\n'

    def _gen_h2h_md(self):
        h2h_avg_stats_df = self.team_stats_df.groupby(['TeamCode', 'OppTeamCode'], as_index=False, sort=False).mean()
        update_four_factors(h2h_avg_stats_df)
        update_team_avg(h2h_avg_stats_df)

        adv_header_str_list = '| Team | Opp Team | Pace | eFG% | TO Ratio | OREB% | FT Rate |'
        adv_align_str_list = '|:---:|---:|---:|---:|---:|---:|---:|'
        adv_table_str = '|' + h2h_avg_stats_df[['TeamCode', 'OppTeamCode', 'PACE', 'EFG_STR', 'TO_RATIO_STR', 'OR_PCT_STR', 'FT_RATE_STR']].to_csv(
            sep='|',
            line_terminator='|\n|',
            header=False,
            float_format='%.1f',
            encoding='utf-8',
            index=False)[:-2]
 
        header_str_list = '| Team | Opp Team | 2PTM/A | 2PT% | 3PTM/A | 3PT% | FTM/A | FT% | OREB | DREB | REB | AST | STL | BLK | TOV | PF | PTS |'
        align_str_list = '|:---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|'
        table_str = '|' + h2h_avg_stats_df[['TeamCode', 'OppTeamCode', 'FG2MA_STR', 'FG2P_STR', 'FG3MA_STR', 'FG3P_STR', 'FTMA_STR', 'FTP_STR', 
            'OR', 'DR', 'REB', 'AS', 'ST', 'BS', 'TO', 'PF', 'PTS']].to_csv(
            sep='|',
            line_terminator='|\n|',
            header=False,
            float_format='%.1f',
            encoding='utf-8',
            index=False)[:-2]
 
        result_str_list = [adv_header_str_list, adv_align_str_list, adv_table_str, '',
                header_str_list, align_str_list, table_str]
        return '\n'.join(result_str_list) + '\n'

    def _gen_key_stats_md(self):
        team_avg_stats_df = self.team_stats_df.groupby(['TeamCode'], as_index=False, sort=False).mean()
        update_team_avg(team_avg_stats_df)
        
        header_str_list = '| Team | FB | 2nd | Off TO | Paint | Bench |'
        align_str_list = '|:---:|---:|---:|---:|---:|---:|'
        table_str = '|' + team_avg_stats_df[['TeamCode', 'A_FBP', 'A_SCP', 'A_PAT', 'A_PIP', 'A_PFB']].to_csv(
            sep='|',
            line_terminator='|\n|',
            header=False,
            float_format='%.1f',
            encoding='utf-8',
            index=False)[:-2]
 
        opp_team_avg_stats_df = self.team_stats_df.groupby(['OppTeamCode'], as_index=False, sort=False).mean()
        
        opp_header_str_list = '| Opp Team | FB | 2nd | Off TO | Paint | Bench |'
        opp_align_str_list = '|:---:|---:|---:|---:|---:|---:|---:|'
        opp_table_str = '|' + opp_team_avg_stats_df[['OppTeamCode', 'A_FBP', 'A_SCP', 'A_PAT', 'A_PIP', 'A_PFB']].to_csv(
            sep='|',
            line_terminator='|\n|',
            header=False,
            float_format='%.1f',
            encoding='utf-8',
            index=False)[:-2]
 
        rank_header_str_list = '| Team | FB | 2nd | Off TO | Paint | Bench |'
        rank_align_str_list = '|:---:|---:|---:|---:|---:|---:|'
        rank_table_str = '|' + team_avg_stats_df[['TeamCode', 'A_FBP_RANK', 'A_SCP_RANK', 'A_PAT_RANK', 'A_PIP_RANK', 'A_PFB_RANK']].to_csv(
            sep='|',
            line_terminator='|\n|',
            header=False,
            float_format='%d',
            encoding='utf-8',
            index=False)[:-2]
 
        h2h_avg_stats_df = self.team_stats_df.groupby(['TeamCode', 'OppTeamCode'], as_index=False, sort=False).mean()
        update_team_avg(h2h_avg_stats_df)

        h2h_header_str_list = '| Team | Opp Team | FB | 2nd | Off TO | Paint | Bench |'
        h2h_align_str_list = '|:---:|---:|---:|---:|---:|---:|---:|---:|'
        h2h_table_str = '|' + h2h_avg_stats_df[['TeamCode', 'OppTeamCode', 'A_FBP', 'A_SCP', 'A_PAT', 'A_PIP', 'A_PFB']].to_csv(
            sep='|',
            line_terminator='|\n|',
            header=False,
            float_format='%.1f',
            encoding='utf-8',
            index=False)[:-2]
 
        result_str_list = [header_str_list, align_str_list, table_str, '',
                opp_header_str_list, opp_align_str_list, opp_table_str, '',
                rank_header_str_list, rank_align_str_list, rank_table_str, '',
                h2h_header_str_list, h2h_align_str_list, h2h_table_str]
        return '\n'.join(result_str_list) + '\n'

    def _gen_player_stats_md(self):
        player_stats_df = self.player_stats_df[self.player_stats_df['SECS'] > 0]
        player_avg_stats_df = player_stats_df.groupby(['TeamCode', 'JerseyNumber', 'Name'], as_index=False, sort=False).mean()
        player_avg_stats_df['GP'] = player_stats_df.groupby(['TeamCode', 'JerseyNumber', 'Name'], sort=False).size().reset_index(name='GP')['GP']
        update_player_avg(player_avg_stats_df)
        result_str_list = list()

        for t in player_avg_stats_df['TeamCode'].unique():
            ps_df = player_avg_stats_df[player_avg_stats_df['TeamCode'].str.match(t)]
            update_efg(ps_df)
            update_usg(ps_df)

            ps_df = ps_df.sort_values(['PTS', 'SECS', 'EFG', 'USG'], ascending=[False, True, False, True])
            header_str_list = '| # | Name | GP | Mins | FGM/FGA | eFG% | USG% | PTS |'
            align_str_list = '|:---:|:---:|---:|---:|---:|---:|---:|---:|'
            table_str = '|' + ps_df[['JerseyNumber', 'Name', 'GP', 'TP', 'FGMA_STR', 'EFG_STR', 'USG_STR', 'PTS']].to_csv(
                sep='|',
                line_terminator='|\n|',
                header=False,
                float_format='%.1f',
                encoding='utf-8',
                index=False)[:-2]
         
            ps_df = ps_df.sort_values(['FG3P', 'FG3M'], ascending=[False, False])
            trey_header_str_list = '| # | Name | GP | Mins | 3PTM/3PTA | 3PT% |'
            trey_align_str_list = '|:---:|:---:|---:|---:|---:|---:|'
            trey_table_str = '|' + ps_df[['JerseyNumber', 'Name', 'GP', 'TP', 'FG3MA_STR', 'FG3P_STR']].to_csv(
                sep='|',
                line_terminator='|\n|',
                header=False,
                float_format='%.1f',
                encoding='utf-8',
                index=False)[:-2]
 
            ps_df = ps_df.sort_values(['OR', 'REB'], ascending=[False, False])
            reb_header_str_list = '| # | Name | GP | Mins | OREB | REB |'
            reb_align_str_list = '|:---:|:---:|---:|---:|---:|---:|'
            reb_table_str = '|' + ps_df[['JerseyNumber', 'Name', 'GP', 'TP', 'OR', 'REB']].to_csv(
                sep='|',
                line_terminator='|\n|',
                header=False,
                float_format='%.1f',
                encoding='utf-8',
                index=False)[:-2]
 
            ps_df = ps_df.sort_values(['FTP', 'FTA'], ascending=[True, False])
            ft_header_str_list = '| # | Name | GP | Mins | FTM/A | FT% |'
            ft_align_str_list = '|:---:|:---:|---:|---:|---:|---:|'
            ft_table_str = '|' + ps_df[['JerseyNumber', 'Name', 'GP', 'TP', 'FTMA_STR', 'FTP_STR']].to_csv(
                sep='|',
                line_terminator='|\n|',
                header=False,
                float_format='%.1f',
                encoding='utf-8',
                index=False)[:-2]
 
            t_result_str_list = [t, '### Scores', header_str_list, align_str_list, table_str,
                    '### Shooters', trey_header_str_list, trey_align_str_list, trey_table_str,
                    '### Rebounders', reb_header_str_list, reb_align_str_list, reb_table_str,
                    '### Foul Targets', ft_header_str_list, ft_align_str_list, ft_table_str]

            result_str_list.append('\n'.join(t_result_str_list))

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

    print '## Pace & Four Factors\n' + r._gen_four_factors_md() + '\n## Traditional Stats\n' + r._gen_team_avg_md() + \
            '\n## H2H Stats\n' + r._gen_h2h_md() + '\n## Key Stats\n' + r._gen_key_stats_md() + \
            '\n## Player Stats\n' + r._gen_player_stats_md()

if __name__ == '__main__':
    main()

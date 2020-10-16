# -*- coding: utf-8 -*-

import pandas as pd
from fiba_reporter.post_game_report import FibaPostGameReportV5
from fiba_inbounder.formulas import update_efg, update_usg, update_player_avg, update_player_per30

class FibaPlayerStatsReport():
    def _get_player_avg_df(self):
        player_stats_df = self.player_stats_df[self.player_stats_df['SECS'] > 0]
        player_avg_stats_df = player_stats_df.groupby(['TeamCode', 'NumName'], as_index=False, sort=False).mean()
        player_avg_stats_df['GP'] = player_stats_df.groupby(['TeamCode', 'NumName'], sort=False).size().reset_index(name='GP')['GP']
        update_player_avg(player_avg_stats_df)

        ps_df_list = list()
        for t in player_avg_stats_df['TeamCode'].unique():
            ps_df = player_avg_stats_df[player_avg_stats_df['TeamCode'].str.match(t)]
            update_efg(ps_df)
            update_usg(ps_df)

            ps_df = ps_df.sort_values(['SECS', 'EFG', 'USG'], ascending=[False, False, True])
            ps_df_list.append(ps_df)
        
        return pd.concat(ps_df_list, sort=False)

    def _get_player_per30_df(self):
        player_stats_df = self.player_stats_df[self.player_stats_df['SECS'] > 0]
        player_avg_stats_df = player_stats_df.groupby(['TeamCode', 'NumName'], as_index=False, sort=False).mean()
        player_avg_stats_df['GP'] = player_stats_df.groupby(['TeamCode', 'NumName'], sort=False).size().reset_index(name='GP')['GP']
        update_player_avg(player_avg_stats_df)

        ps_df_list = list()
        for t in player_avg_stats_df['TeamCode'].unique():
            ps_df = player_avg_stats_df[player_avg_stats_df['TeamCode'].str.match(t)]
            update_efg(ps_df)
            update_usg(ps_df)
            update_player_per30(ps_df)

            ps_df = ps_df.sort_values(['SECS', 'EFG', 'USG'], ascending=[False, False, True])
            ps_df_list.append(ps_df)
        
        return pd.concat(ps_df_list, sort=False)

    def _gen_player_avg_md(self):
        result_str_list = list()
        
        player_avg_stats_df = self._get_player_avg_df()
        for t in player_avg_stats_df['TeamCode'].unique():
            ps_df = player_avg_stats_df[player_avg_stats_df['TeamCode'].str.match(t)]
            header_str_list = '| Name | GP | Mins | 2PTM/A | 2PT% | 3PTM/A | 3PT% | FTM/A | FT% | OREB | DREB | REB | AST | STL | BLK | TOV | PF | PTS | USG% | eFG% |'
            align_str_list = '|:---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|'
            table_str = '|' + ps_df[['NumName', 'GP', 'TP', 'FG2MA_STR', 'FG2P_STR', 'FG3MA_STR', 'FG3P_STR', 'FTMA_STR', 'FTP_STR',
            'OR', 'DR', 'REB', 'AS', 'ST', 'BS', 'TO', 'PF', 'PTS', 'USG_STR', 'EFG_STR']].to_csv(
                sep='|',
                line_terminator='|\n|',
                header=False,
                float_format='%.1f',
                encoding='utf-8',
                index=False)[:-2]
 
            t_result_str_list = [t, header_str_list, align_str_list, table_str]
            result_str_list.append('\n'.join(t_result_str_list))

        return '\n'.join(result_str_list) + '\n'

    def _gen_player_avg_csv(self):
        result_str_list = list()
        
        player_avg_stats_df = self._get_player_avg_df()
        for t in player_avg_stats_df['TeamCode'].unique():
            ps_df = player_avg_stats_df[player_avg_stats_df['TeamCode'].str.match(t)]
            table_str = ps_df[['NumName', 'GP', 'SECS', 'FG2P', 'FG2A', 'FG3P', 'FG3A', 'FTP', 'FTA',
            'OR', 'DR', 'AS', 'ST', 'BS', 'TO', 'PF', 'PTS', 'USG', 'EFG']].to_csv(
                float_format='%.1f',
                encoding='utf-8',
                index=False)[:]
 
            t_result_str_list = [t, table_str]
            result_str_list.append('\n'.join(t_result_str_list))

        return '\n'.join(result_str_list) + '\n'

    def _gen_player_per30_csv(self):
        result_str_list = list()
        
        player_avg_stats_df = self._get_player_per30_df()
        for t in player_avg_stats_df['TeamCode'].unique():
            ps_df = player_avg_stats_df[player_avg_stats_df['TeamCode'].str.match(t)]
            table_str = ps_df[['NumName', 'FG2P', 'FG2A', 'FG3P', 'FG3A', 'FTP', 'FTA',
            'OR', 'DR', 'AS', 'ST', 'BS', 'TO', 'PF', 'PTS', 'USG', 'EFG']].to_csv(
                float_format='%.1f',
                encoding='utf-8',
                index=False)[:]
 
            t_result_str_list = [t, table_str]
            result_str_list.append('\n'.join(t_result_str_list))

        return '\n'.join(result_str_list) + '\n'


class FibaPlayerStatsReportV5(FibaPlayerStatsReport):
    def __init__(self, game_id_list):
        r_list = [FibaPostGameReportV5(match_id) for match_id in game_id_list]
        self.player_stats_df = pd.concat([r.player_stats_df for r in r_list], sort=False)

def main():
    version = raw_input('fiba stats version?\n\t(5) v5\n\t(7) v7\n')
    output_format = raw_input('Which format?\n\t(M)arkdown\n\t(C)SV\n')
    avg_format = raw_input('What scope?\n\t(A)verage\n\t(P)er 30\n')
    num_games = raw_input('How Many Games? ')
    game_id_list = list()

    if int(version) == 5:
        for g in range(int(num_games)):
            print '\nGame {i} of {n}'.format(i=(g+1), n=int(num_games))
            match_id = raw_input('\tMatch Id? ')
            game_id_list.append(str(match_id))
        r = FibaPlayerStatsReportV5(game_id_list)

    if str(output_format).lower() == 'm':
        print '## Player Stats\n' + r._gen_player_avg_md()
    elif str(output_format).lower() == 'c':
        if str(avg_format).lower() == 'a':
            print r._gen_player_avg_csv()
        elif str(avg_format).lower() == 'p':
            print r._gen_player_per30_csv()

if __name__ == '__main__':
    main()

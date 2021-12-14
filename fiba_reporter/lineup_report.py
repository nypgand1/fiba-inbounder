# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np

from fiba_reporter.post_game_report import FibaPostGameReportV5, FibaPostGameReportV7, FibaPostGameReportPLeague
from fiba_inbounder.formulas import get_lineup_stats, get_on_off_stats

class FibaLineupReport():
    def _gen_lineup_stats_md(self, secs_above=0):
        result_str_list = list()

        for t in self.pbp_df['T1'].unique():
            if (not t) or pd.isna(t):
                continue
            team_lineup_df = self.pbp_df[~pd.isna(self.pbp_df[t])]
            team_lineup_df['T1'] = np.where(team_lineup_df['T1']==t, t, 'OPP')
            team_lineup_df = team_lineup_df.groupby(['T1', t], as_index=False, sort=False).sum()
            tls_df = get_lineup_stats(team_lineup_df, t, self.id_table)
            tls_df = tls_df[tls_df['SECS'] >= secs_above]
            tls_df = tls_df.sort_values(['NETRTG', 'PM', 'EFG'], ascending=[False, False, False])
            
            if t in self.id_table.keys():
                result_str_list.append(self.id_table[t])
            else:
                result_str_list.append(t)
            result_str_list.append('| Lineups | Mins | Pace | +/- | eFG% | TO Ratio | A/T | OffRtg | DefRtg | NetRtg |')
            result_str_list.append('|:---|---:|---:|---:|---:|---:|---:|---:|---:|---:|')
            result_str_list.append(('|' + tls_df[['LINEUP_NAME', 'TP', 'PACE', 'PM', 'EFG_STR', 'TO_RATIO_STR', 'A/T_STR', 'OFFRTG', 'DEFRTG', 'NETRTG']].to_csv(
                sep='|',
                line_terminator='|\n|',
                header=False,
                float_format='%.1f',
                encoding='utf-8',
                index=False)[:-2]).decode('utf-8'))
 
        return '\n'.join(result_str_list) + '\n'

    def _gen_on_off_stats_md(self):
        result_str_list = list()

        for t in self.pbp_df['T1'].unique():
            if (not t) or pd.isna(t):
                continue
            team_lineup_df = self.pbp_df[~pd.isna(self.pbp_df[t])]
            player_on_off_list = list()
            for p in {p for r in team_lineup_df.to_dict(orient='records') for p in r[t]}:
                player_team_lineup_df = team_lineup_df.copy()
                player_team_lineup_df['PLAYER'] = p
                player_team_lineup_df['ON'] = player_team_lineup_df[t].apply(lambda x: True if p in x else False)
                player_team_lineup_df['T1'] = np.where(player_team_lineup_df['T1']==t, t, 'OPP')
                player_team_lineup_df = player_team_lineup_df.groupby(['PLAYER', 'ON', 'T1'], as_index=False, sort=False).sum()

                player_on_off_df = get_on_off_stats(player_team_lineup_df, t, self.id_table)
                player_on_off_list.append(player_on_off_df)

            team_on_off_df = pd.concat(player_on_off_list, axis=0, ignore_index=True, sort=False)
            team_on_off_df = team_on_off_df.sort_values(['NETRTG_DIFF'], ascending=[False])
            
            if t in self.id_table.keys():
                result_str_list.append(self.id_table[t])
            else:
                result_str_list.append(t)
            result_str_list.append('| PLAYER | Mins | OffRtg | DefRtg | NetRtg | OffRtg (Diff) | DefRtg (Diff) | NetRtg (Diff)|')
            result_str_list.append('|:---|---:|---:|---:|---:|---:|---:|---:|')
            result_str_list.append(('|' + team_on_off_df[['PLAYER_NAME', 'TP', 'OFFRTG', 'DEFRTG', 'NETRTG', 'OFFRTG_DIFF_STR', 'DEFRTG_DIFF_STR', 'NETRTG_DIFF']].to_csv(
                sep='|',
                line_terminator='|\n|',
                header=False,
                float_format='%.1f',
                encoding='utf-8',
                index=False)[:-2]).decode('utf-8'))
 
        return '\n'.join(result_str_list) + '\n'

class FibaLineupReportV5(FibaLineupReport):
    def __init__(self, game_id_list):
        r_list = [FibaPostGameReportV5(match_id) for match_id in game_id_list]
        self.pbp_df = pd.concat([r.pbp_df for r in r_list], sort=False)
        self.id_table = {k: v for r in r_list for k, v in r.id_table.iteritems()}

class FibaLineupReportV7(FibaLineupReport):
    def __init__(self, game_id_list):
        r_list = [FibaPostGameReportV7(event_id, game_unit) for (event_id, game_unit) in game_id_list]
        self.pbp_df = pd.concat([r.pbp_df for r in r_list], sort=False)
        self.id_table = {k: v for r in r_list for k, v in r.id_table.iteritems()}

class FibaLineupReportPLeague(FibaLineupReport):
    def __init__(self, game_id_list):
        r_list = [FibaPostGameReportPLeague(game_id) for game_id in game_id_list]
        self.pbp_df = pd.concat([r.pbp_df for r in r_list], sort=False)
        self.id_table = {k: v for r in r_list for k, v in r.id_table.iteritems()}

def main():
    version = raw_input('fiba stats version?\n\t(5) v5\n\t(7) v7\n\t(9) P League\n')
    secs_above = raw_input('How Many Secs above in Lineup Stats? ')
    num_games = raw_input('How Many Games? ')
    game_id_list = list()

    if int(version) == 5:
        for g in range(int(num_games)):
            print '\nGame {i} of {n}'.format(i=(g+1), n=int(num_games))
            match_id = raw_input('\tMatch Id? ')
            game_id_list.append(str(match_id))
        r = FibaLineupReportV5(game_id_list)

    elif int(version) == 7:
        for g in range(int(num_games)):
            print '\nGame {i} of {n}'.format(i=(g+1), n=int(num_games))
            event_id = raw_input('\tEvent Id? ')
            game_unit = raw_input('\tGame Unit? ')
            game_id_list.append((str(event_id), str(game_unit)))
        r = FibaLineupReportV7(game_id_list)

    elif int(version) == 9:
        for g in range(int(num_games)):
            print '\nGame {i} of {n}'.format(i=(g+1), n=int(num_games))
            game_id = raw_input('\tGame ID? ')
            game_id_list.append(str(game_id))
        r = FibaLineupReportPLeague(game_id_list)

    else: 
        print 'NOT SUPPORT'
        return

    print '\n## Advanced Lineup Stats\n' + r._gen_lineup_stats_md(secs_above=int(secs_above)) + \
        '\n## On/Off Stats\n' + r._gen_on_off_stats_md()

if __name__ == '__main__':
    main()

# -*- coding: utf-8 -*-

import pandas as pd
from fiba_inbounder.settings_synergy import SYNERGY_ORGANIZATION_ID
from fiba_inbounder.game_parser import FibaGameParser
from fiba_inbounder.formulas import score_bold_md, update_efg, update_four_factors, update_usg, \
    update_zone, update_zone_pleague, update_range, update_range_stats, update_lineup, update_lineup_synergy, \
    get_lineup_stats, get_player_mins_plus_minus

class FibaPostGameReport(object):
    def _update_shot_zone_range(self):
        update_zone(self.shot_df)
        update_range(self.shot_df)

    def _gen_period_scores_md(self):
        stats_dict = self.team_stats_df.to_dict(orient='records')

        header_str_list = ['|Scores']
        align_str_list = ['|:---:']
        home_str_list = [u'|{team_name}'.format(team_name=stats_dict[0]['TeamCode'])]
        away_str_list = [u'|{team_name}'.format(team_name=stats_dict[1]['TeamCode'])]
   
        for i, p in enumerate(stats_dict[0]['PeriodIdList']):
            header_str_list.append(p)
            align_str_list.append('---:')
            home_str_list.append(score_bold_md(stats_dict[0]['Periods'][i]['Score']))
            away_str_list.append(score_bold_md(stats_dict[1]['Periods'][i]['Score']))
        
        header_str_list.append('Total|')
        align_str_list.append('---:|')
        home_str_list.append(str(stats_dict[0]['PTS']))
        away_str_list.append(str(stats_dict[1]['PTS']))

        result_str_list = ['|'.join(header_str_list),
                '|'.join(align_str_list),
                '|'.join(home_str_list) + '|',
                '|'.join(away_str_list) + '|']
        return '\n'.join(result_str_list) + '\n'

    def _gen_four_factors_md(self):
        update_four_factors(self.team_stats_df)
        self.team_stats_df['PACE'] = self.team_stats_df['PACE'].mean()

        header_str_list = '| Team | Pace | eFG% | TO Ratio | OREB% | FT Rate |'
        align_str_list = '|:---:|---:|---:|---:|---:|---:|'
        table_str = '|' + self.team_stats_df[['TeamCode', 'PACE', 'EFG_STR', 'TO_RATIO_STR', 'OR_PCT_STR', 'FT_RATE_STR']].to_csv(
            sep='|',
            line_terminator='|\n|',
            header=False,
            float_format='%.1f',
            encoding='utf-8',
            index=False)[:-2]
        
        result_str_list = [header_str_list, align_str_list, table_str.decode('utf-8')]
        return '\n'.join(result_str_list) + '\n'

    def _gen_key_stats_md(self):
        header_str_list = '| Team | FB | 2nd | Off TO | Paint | Bench |'
        align_str_list = '|:---:|---:|---:|---:|---:|---:|'
        table_str = '|' + self.team_stats_df[['TeamCode', 'A_FBP', 'A_SCP', 'A_PAT', 'A_PIP', 'A_PFB']].to_csv(
            sep='|',
            line_terminator='|\n|',
            header=False,
            float_format='%.1f',
            encoding='utf-8',
            index=False)[:-2]
 
        result_str_list = [header_str_list, align_str_list, table_str.decode('utf-8')]
        return '\n'.join(result_str_list) + '\n'

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
            result_str_list.append('|' + tsr_df[['RANGE', 'FREQ_STR', 'FGM/A', 'EFG_STR']].to_csv(
                sep='|',
                line_terminator='|\n|',
                header=False,
                float_format='%.1f',
                encoding='utf-8',
                index=False)[:-2])
            result_str_list.append('|Total||{fgm}/{fga}||'.format(fgm=int(tsr_df['FGM'].sum()), fga=int(tsr_df['FGA'].sum())))
    
        return '\n'.join(result_str_list) + '\n'

    def _gen_player_stats_md(self):
        result_str_list = list()
        
        for t in self.player_stats_df['TeamCode'].unique():
            ps_df = self.player_stats_df[self.player_stats_df['TeamCode'].str.match(t) & (self.player_stats_df['SECS'] > 0)]
            update_efg(ps_df)
            update_usg(ps_df)
            ps_df = ps_df.sort_values(['PM', 'SECS', 'EFG', 'USG'], ascending=[False, True, False, True])
         
            if t in self.id_table.keys():
                result_str_list.append(self.id_table[t])
            else:
                result_str_list.append(t)
            result_str_list.append('| # | Name | Mins | eFG% | USG% | +/- |')
            result_str_list.append('|:---:|:---:|---:|---:|---:|---:|')
            result_str_list.append(('|' + ps_df[['JerseyNumber', 'Name', 'TP', 'EFG_STR', 'USG_STR', 'PM']].to_csv(
                sep='|',
                line_terminator='|\n|',
                header=False,
                float_format='%.1f',
                encoding='utf-8',
                index=False)[:-2]).decode('utf-8'))
            
        return '\n'.join(result_str_list) + '\n'

    def _gen_lineup_stats_md(self):
        result_str_list = list()

        for t in self.pbp_df['T1'].unique():
            if (not t) or pd.isna(t):
                continue
            team_lineup_df = self.pbp_df.groupby(['T1', t], as_index=False, sort=False).sum()
            tls_df = get_lineup_stats(team_lineup_df, t, self.id_table)
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

class FibaPostGameReportSynergy(FibaPostGameReport):
    def __init__(self, game_id):
        #TODO get period_id_list
        period_id_list = [1, 2, 3, 4]
        
        org_id = SYNERGY_ORGANIZATION_ID
        self.id_table = FibaGameParser.get_id_tables_synergy(org_id)
        self.player_stats_df, self.starter_dict = FibaGameParser.get_game_stats_dataframe_synergy(org_id, game_id)
        
        self.pbp_df = FibaGameParser.get_game_play_by_play_dataframe_synergy(org_id, game_id, period_id_list)
        #TODO temp closed bc league
        #update_lineup_synergy(self.pbp_df, self.starter_dict, self.id_table)
        #self.sub_df = self.pbp_df[self.pbp_df['eventType'].isin(['substitution', 'period'])]
        self.shot_df = self.pbp_df[self.pbp_df['eventType'].isin(['2pt', '3pt', 'freeThrow'])]

class FibaPostGameReportPLeague(FibaPostGameReport):
    def __init__(self, game_id):
        self.team_stats_df, self.player_stats_df, self.team_id_away, self.team_id_home, self.id_table = FibaGameParser.get_game_stats_dataframe_pleague(game_id)
        self.starter_dict = {self.team_id_away: set(), self.team_id_home: set()}

        self.sub_df = FibaGameParser.get_game_sub_dataframe_pleague(game_id, self.team_id_away, self.team_id_home)
        pbp_df = FibaGameParser.get_game_play_by_play_dataframe_pleague(game_id, self.team_id_away, self.team_id_home)
        self.shot_df = pbp_df[(pbp_df['AC']=='P3') | (pbp_df['AC']=='P2')]
        
        self.pbp_df = pd.concat([self.sub_df, pbp_df]).sort_values(['GT'], ascending=[True]).reset_index(drop=True)
        update_lineup(self.pbp_df, self.starter_dict)

    def _update_shot_zone_range(self):
        update_zone_pleague(self.shot_df)
        update_range(self.shot_df)

    def _gen_player_stats_md(self):
        mins_pm_df = get_player_mins_plus_minus(self.sub_df, self.team_id_away)
        self.player_stats_df = self.player_stats_df.join(mins_pm_df.set_index('C1'), on='player_id', how='inner', lsuffix='_pl')

        return super(FibaPostGameReportPLeague, self)._gen_player_stats_md()

class FibaPostGameReportV5(FibaPostGameReport):
    def __init__(self, match_id):
        self.team_stats_df, self.player_stats_df, self.starter_dict, self.pbp_df, self.shot_df = FibaGameParser.get_game_data_dataframe_v5(match_id)
        self.id_table = dict()

        if all([len(s)==5 for s in self.starter_dict.itervalues()]):
            update_lineup(self.pbp_df, self.starter_dict)

class FibaPostGameReportV7(FibaPostGameReport):
    def __init__(self, event_id, game_unit):
        self.team_stats_df, self.player_stats_df = FibaGameParser.get_game_stats_dataframe_v7(event_id, game_unit)
        self.id_table, self.starter_dict = FibaGameParser.get_game_details_dict_v7(event_id, game_unit)

        stats_dict = self.team_stats_df.to_dict(orient='records')
        period_id_list = stats_dict[0]['PeriodIdList']
        
        self.pbp_df = FibaGameParser.get_game_play_by_play_dataframe_v7(event_id, game_unit, period_id_list)
        self.shot_df = self.pbp_df[(self.pbp_df['AC']=='P3') | (self.pbp_df['AC']=='P2')]

        if all([len(s)==5 for s in self.starter_dict.itervalues()]):
            update_lineup(self.pbp_df, self.starter_dict)

try: 
    input = raw_input
except NameError: 
    raw_input = input

def main():
    version = raw_input('fiba stats version?\n\t(5) v5\n\t(7) v7\n\t(8) Synergy\n\t(9) P League\n')

    if int(version) == 5:
        match_id = raw_input('Match Id? ')
        r = FibaPostGameReportV5(str(match_id))

    elif int(version) == 7:
        event_id = raw_input('Event Id? ')
        game_unit = raw_input('Game Unit? ')
        r = FibaPostGameReportV7(str(event_id), str(game_unit))
        
    elif int(version) == 8:
        game_id = raw_input('Game Id? ')
        r = FibaPostGameReportSynergy(str(game_id))
        #TODO skip for now
        return

    elif str(version) == '9':
        game_id = raw_input('Game Id? ')
        r = FibaPostGameReportPLeague(str(game_id))

    else:
        print ('NOT SUPPORT\n')
        return

    print (u'## Scores\n' + r._gen_period_scores_md() + '\n## Pace & Four Factors\n' + r._gen_four_factors_md() + \
        '\n## Key Stats\n' + r._gen_key_stats_md() + '\n## Shot Analysis\n' + r._gen_team_shot_range_md() + \
        '\n## Advanced Player Stats\n' + r._gen_player_stats_md() + \
        '\n## Advanced Lineup Stats\n' + r._gen_lineup_stats_md())

if __name__ == '__main__':
    main()

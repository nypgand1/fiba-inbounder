# -*- coding: utf-8 -*-

from fiba_inbounder.game_parser import FibaGameParser
from fiba_inbounder.formulas import score_bold_md, update_efg, update_four_factors, update_usg, \
    update_zone, update_range, update_range_stats

class FibaPostGameReport():
    def _gen_period_scores_md(self):
        stats_dict = self.team_stats_df.to_dict(orient='records')

        header_str_list = ['|Scores']
        align_str_list = ['|:---:']
        home_str_list = ['|{team_name}'.format(team_name=stats_dict[0]['TeamCode'])]
        away_str_list = ['|{team_name}'.format(team_name=stats_dict[1]['TeamCode'])]
   
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
        
        result_str_list = [header_str_list, align_str_list, table_str]
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
 
        result_str_list = [header_str_list, align_str_list, table_str]
        return '\n'.join(result_str_list) + '\n'

    def _gen_team_shot_range_md(self):
        update_zone(self.pbp_df)
        update_range(self.pbp_df)

        result_str_list = list()
        shot_df = self.pbp_df[(self.pbp_df['AC']=='P3') | (self.pbp_df['AC']=='P2')]
        team_shot_range_df = shot_df.sort_values(['ZONE']).groupby(['T1', 'RANGE'], as_index=False, sort=False).sum()
        
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
            result_str_list.append('|---|')
            result_str_list.append('|Total||{fgm}/{fga}||'.format(fgm=int(tsr_df['FGM'].sum()), fga=int(tsr_df['FGA'].sum())))
    
        return '\n'.join(result_str_list) + '\n'

    def _gen_player_stats_md(self):
        update_efg(self.player_stats_df)
        result_str_list = list()
        
        for t in self.player_stats_df['TeamCode'].unique():
            ps_df = self.player_stats_df[self.player_stats_df['TeamCode'].str.match(t)]
            update_usg(ps_df)
            ps_df = ps_df.sort_values(['PM', 'SECS', 'EFG', 'USG'], ascending=[False, True, False, True])
            
            if t in self.id_table.keys():
                result_str_list.append(self.id_table[t])
            else:
                result_str_list.append(t)
            result_str_list.append('| # | Name | Mins | eFG% | USG% | +/- |')
            result_str_list.append('|:---:|:---:|---:|---:|---:|---:|')
            result_str_list.append('|' + ps_df[['JerseyNumber', 'Name', 'TP', 'EFG_STR', 'USG_STR', 'PM']].to_csv(
                sep='|',
                line_terminator='|\n|',
                header=False,
                float_format='%.1f',
                encoding='utf-8',
                index=False)[:-2])
            
        return '\n'.join(result_str_list) + '\n'

class FibaPostGameReportV7(FibaPostGameReport):
    def __init__(self, event_id, game_unit):
        self.team_stats_df, self.player_stats_df, self.id_table = FibaGameParser.get_game_stats_dataframe_v7(event_id, game_unit)

        stats_dict = self.team_stats_df.to_dict(orient='records')
        period_id_list = stats_dict[0]['PeriodIdList']
        self.pbp_df = FibaGameParser.get_game_play_by_play_dataframe_v7(event_id, game_unit, period_id_list)

def main():
    event_id = raw_input('Event Id? ')
    game_unit = raw_input('Game Unit? ')

    r = FibaPostGameReportV7(str(event_id), str(game_unit))
    print '## Scores\n' + r._gen_period_scores_md() + '\n## Pace & Four Factors\n' + r._gen_four_factors_md() + \
        '\n## Key Stats\n' + r._gen_key_stats_md() + '\n## Shot Analysis\n' + r._gen_team_shot_range_md() + \
        '\n## Advanced Player Stats\n' + r._gen_player_stats_md()

if __name__ == '__main__':
    main()

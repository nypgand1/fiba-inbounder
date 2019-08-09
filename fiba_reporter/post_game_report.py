# -*- coding: utf-8 -*-

from fiba_inbounder.game_parser import FibaGameParser
from fiba_inbounder.formulas import score_bold_md

class FibaPostGameReportV7:
    def __init__(self, event_id, game_unit):
        game_json, df = FibaGameParser.get_game_teams_json_dataframe_v7(event_id, game_unit)
        self.game_json = game_json
        self.df = df
    
    def _gen_period_scores_md(self):
        stats_dict = self.df.to_dict(orient='records')

        header_str_list = ['|Scores']
        align_str_list = ['|:---:']
        home_str_list = ['|{team_name}'.format(team_name=stats_dict[0]['TeamCode'])]
        away_str_list = ['|{team_name}'.format(team_name=stats_dict[1]['TeamCode'])]
   
        for i, q in enumerate(stats_dict[0]['Periods']):
            header_str_list.append(q['Id'])
            align_str_list.append('---:')
            home_str_list.append('*{half}* \| {full}'.format(
                half=stats_dict[0]['Periods'][i]['HalfTimeScore'],
                full=score_bold_md(stats_dict[0]['Periods'][i]['Score'])))
            away_str_list.append('*{half}* \| {full}'.format(
                    half=stats_dict[1]['Periods'][i]['HalfTimeScore'],
                    full=score_bold_md(stats_dict[1]['Periods'][i]['Score'])))
        
        header_str_list.append('Total')
        align_str_list.append('---:')
        home_str_list.append(str(stats_dict[0]['PTS']))
        away_str_list.append(str(stats_dict[1]['PTS']))

        result_str_list = ['|'.join(header_str_list),
                '|'.join(align_str_list),
                '|'.join(home_str_list),
                '|'.join(away_str_list)]

        return '\n'.join(result_str_list) + '\n'

if __name__ == '__main__':
    main()

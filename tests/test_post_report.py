from fiba_inbounder.game_parser import FibaGameParser
from fiba_reporter.post_game_report import FibaPostGameReportV7

def test_gen_period_scores_md_v7():
    r = FibaPostGameReportV7(event_id='208053', game_unit='24527-B-1')
    assert r._gen_period_scores_md() == '|Scores|Q1|Q2|Q3|Q4|OT1|Total\n|:---:|---:|---:|---:|---:|---:|---:\n|LBN|*17* \| **27**|*9* \| 19|*12* \| **22**|*11* \| 19|*6* \| 19|106\n|THA|*8* \| **22**|*15* \| **26**|*9* \| 14|*15* \| **25**|*3* \| 13|100\n'

def test_gen_four_factors_md_v7():
    r = FibaPostGameReportV7(event_id='208053', game_unit='24527-B-1')
    assert r._gen_four_factors_md() == '| Team | Pace | eFG% | TO Ratio | OREB% | FT Rate |\n|:---|---:|---:|---:|---:|---:|\n|LBN|83.1|**60.8%**|17.1%|22.0%|9.4%\n|THA|83.0|43.4%|15.0%|**42.9%**|**21.0%**\n'

def test_gen_key_stats_md_v7():
    r = FibaPostGameReportV7(event_id='208053', game_unit='24527-B-1')
    assert r._gen_key_stats_md() == '| Team | FB | 2nd | Off TO | Paint | Bench |\n|:---|---:|---:|---:|---:|---:|\n|LBN|23|15|20|44|5\n|THA|15|23|21|48|9\n'

def test_gen_team_shot_range_md_v7():
    r = FibaPostGameReportV7(event_id='208053', game_unit='24527-B-1')
    assert r._gen_team_shot_range_md() == 'T_10034\n| Shot Range | Freq | FGM/A | eFG% |\n|:---:|---:|---:|---:|\n|Rim|32.9%|17/26|**65.4%**\n|Mid 2|15.2%|7/12|**58.3%**\n|Long 2|10.1%|3/8|37.5%\n|3PT|**41.8%**|14/33|**63.6%**\n|---|\n|Total||41/79||\nT_10102\n| Shot Range | Freq | FGM/A | eFG% |\n|:---:|---:|---:|---:|\n|Rim|**52.7%**|24/48|**50.0%**\n|Mid 2|9.9%|2/9|22.2%\n|Long 2|4.4%|3/4|**75.0%**\n|3PT|33.0%|7/30|35.0%\n|---|\n|Total||36/91||\n'

if __name__ == '__main__':
    main()

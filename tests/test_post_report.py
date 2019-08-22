from fiba_inbounder.game_parser import FibaGameParser
from fiba_reporter.post_game_report import FibaPostGameReportV7

def test_gen_period_scores_md_v7():
    r = FibaPostGameReportV7(event_id='208053', game_unit='24527-B-1')
    assert r._gen_period_scores_md() == '|Scores|Q1|Q2|Q3|Q4|OT1|Total\n|:---:|---:|---:|---:|---:|---:|---:\n|LBN|*17* \| **27**|*9* \| 19|*12* \| **22**|*11* \| 19|*6* \| 19|106\n|THA|*8* \| **22**|*15* \| **26**|*9* \| 14|*15* \| **25**|*3* \| 13|100\n'

def test_gen_four_factors_md_v7():
    r = FibaPostGameReportV7(event_id='208053', game_unit='24527-B-1')
    assert r._gen_four_factors_md() == '| Team | Pace | eFG% | TO Ratio | OREB% | FT Rate |\n|:---|---:|---:|---:|---:|---:|\n|LBN|83.0|**60.8%**|17.1%|22.0%|9.4%\n|THA|83.0|43.4%|15.0%|**42.9%**|**21.0%**\n'

def test_gen_key_stats_md_v7():
    r = FibaPostGameReportV7(event_id='208053', game_unit='24527-B-1')
    assert r._gen_key_stats_md() == '| Team | FB | 2nd | Off TO | Paint | Bench |\n|:---|---:|---:|---:|---:|---:|\n|LBN|23|15|20|44|5\n|THA|15|23|21|48|9\n'

def test_gen_team_shot_range_md_v7():
    r = FibaPostGameReportV7(event_id='208053', game_unit='24527-B-1')
    assert r._gen_team_shot_range_md() == 'LBN\n| Shot Range | Freq | FGM/A | eFG% |\n|:---:|---:|---:|---:|\n|Rim|32.9%|17/26|**65.4%**\n|Mid 2|15.2%|7/12|**58.3%**\n|Long 2|10.1%|3/8|37.5%\n|3PT|**41.8%**|14/33|**63.6%**\n|---|\n|Total||41/79||\nTHA\n| Shot Range | Freq | FGM/A | eFG% |\n|:---:|---:|---:|---:|\n|Rim|**52.7%**|24/48|**50.0%**\n|Mid 2|9.9%|2/9|22.2%\n|Long 2|4.4%|3/4|**75.0%**\n|3PT|33.0%|7/30|35.0%\n|---|\n|Total||36/91||\n'

def test_gen_player_stats_md():
    r = FibaPostGameReportV7(event_id='208053', game_unit='24527-B-1')
    assert r._gen_player_stats_md() == 'LBN\n| # | Name | eFG% | +/- |\n|:---:|:---:|---:|---:|\n|14|Ziade|33.3%|23\n|7|El Khatib|**50.0%**|10\n|5|Saoud|**65.8%**|8\n|3|Lyons|**83.3%**|3\n|33|Bawji|**61.1%**|3\n|4|Abd El Nour|0.0%|0\n|1|Abdel Moneim|0.0%|0\n|9|Kasab|0.0%|0\n|2|Kodsi|0.0%|-2\n|11|Akl|**75.0%**|-7\n|0|El Kaissi|33.3%|-8\nTHA\n| # | Name | eFG% | +/- |\n|:---:|:---:|---:|---:|\n|36|Sunthonsiri|0.0%|10\n|20|Suktub|**125.0%**|4\n|65|Chanthachon|**60.7%**|4\n|91|Klahan|**50.0%**|1\n|9|Apiromvilaichai|0.0%|0\n|38|Phuangla|0.0%|0\n|14|Saengtong|0.0%|0\n|97|Towaroj|0.0%|0\n|3|Keene|38.5%|-6\n|7|Singletary|**52.2%**|-9\n|77|Ananti|17.9%|-16\n|69|Apiromvilaichai|42.9%|-18\n'

if __name__ == '__main__':
    main()

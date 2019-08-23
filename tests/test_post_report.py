from fiba_inbounder.game_parser import FibaGameParser
from fiba_reporter.post_game_report import FibaPostGameReportV7

def test_gen_period_scores_md_v7():
    r = FibaPostGameReportV7(event_id='208053', game_unit='24527-B-1')
    assert r._gen_period_scores_md() == '|Scores|Q1|Q2|Q3|Q4|OT1|Total|\n|:---:|---:|---:|---:|---:|---:|---:|\n|LBN|**27**|19|**22**|19|19|106|\n|THA|**22**|**26**|14|**25**|13|100|\n'

def test_gen_four_factors_md_v7():
    r = FibaPostGameReportV7(event_id='208053', game_unit='24527-B-1')
    assert r._gen_four_factors_md() == '| Team | Pace | eFG% | TO Ratio | OREB% | FT Rate |\n|:---:|---:|---:|---:|---:|---:|\n|LBN|83.0|**60.8%**|17.1%|22.0%|9.4%|\n|THA|83.0|43.4%|15.0%|**42.9%**|**21.0%**|\n'

def test_gen_key_stats_md_v7():
    r = FibaPostGameReportV7(event_id='208053', game_unit='24527-B-1')
    assert r._gen_key_stats_md() == '| Team | FB | 2nd | Off TO | Paint | Bench |\n|:---:|---:|---:|---:|---:|---:|\n|LBN|23|15|20|44|5|\n|THA|15|23|21|48|9|\n'

def test_gen_team_shot_range_md_v7():
    r = FibaPostGameReportV7(event_id='208053', game_unit='24527-B-1')
    assert r._gen_team_shot_range_md() == 'LBN\n| Shot Range | Freq | FGM/A | eFG% |\n|:---:|---:|---:|---:|\n|Rim|32.9%|17/26|**65.4%**|\n|Mid 2|15.2%|7/12|**58.3%**|\n|Long 2|10.1%|3/8|37.5%|\n|3PT|**41.8%**|14/33|**63.6%**|\n|---|\n|Total||41/79||\nTHA\n| Shot Range | Freq | FGM/A | eFG% |\n|:---:|---:|---:|---:|\n|Rim|**52.7%**|24/48|**50.0%**|\n|Mid 2|9.9%|2/9|22.2%|\n|Long 2|4.4%|3/4|**75.0%**|\n|3PT|33.0%|7/30|35.0%|\n|---|\n|Total||36/91||\n'

def test_gen_player_stats_md():
    r = FibaPostGameReportV7(event_id='208053', game_unit='24527-B-1')
    assert r._gen_player_stats_md() == 'LBN\n| # | Name | Mins | eFG% | USG% | +/- |\n|:---:|:---:|---:|---:|---:|---:|\n|14|Ziade|29:56|33.3%|14.7%|23|\n|7|El Khatib|42:33|**50.0%**|15.5%|10|\n|5|Saoud|43:31|**65.8%**|23.8%|8|\n|3|Lyons|39:47|**83.3%**|20.8%|3|\n|33|Bawji|44:15|**61.1%**|**27.7%**|3|\n|4|Abd El Nour|00:00|0.0%|0.0%|0|\n|1|Abdel Moneim|00:00|0.0%|0.0%|0|\n|9|Kasab|00:00|0.0%|0.0%|0|\n|2|Kodsi|02:37|0.0%|16.8%|-2|\n|11|Akl|17:52|**75.0%**|7.4%|-7|\n|0|El Kaissi|04:25|33.3%|**29.8%**|-8|\nTHA\n| # | Name | Mins | eFG% | USG% | +/- |\n|:---:|:---:|---:|---:|---:|---:|\n|36|Sunthonsiri|14:51|0.0%|5.2%|10|\n|20|Suktub|09:09|**125.0%**|8.5%|4|\n|65|Chanthachon|31:25|**60.7%**|19.4%|4|\n|91|Klahan|15:40|**50.0%**|7.4%|1|\n|9|Apiromvilaichai|00:00|0.0%|0.0%|0|\n|38|Phuangla|00:00|0.0%|0.0%|0|\n|97|Towaroj|00:00|0.0%|0.0%|0|\n|14|Saengtong|06:39|0.0%|16.1%|0|\n|3|Keene|45:00|38.5%|**29.8%**|-6|\n|7|Singletary|43:42|**52.2%**|**26.5%**|-9|\n|77|Ananti|31:43|17.9%|21.0%|-16|\n|69|Apiromvilaichai|26:48|42.9%|13.0%|-18|\n'

if __name__ == '__main__':
    main()

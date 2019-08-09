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

if __name__ == '__main__':
    main()

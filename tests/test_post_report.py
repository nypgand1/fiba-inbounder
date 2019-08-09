from fiba_inbounder.game_parser import FibaGameParser
from fiba_reporter.post_game_report import FibaPostGameReportV7

def test_gen_period_scores_md_v7():
    r = FibaPostGameReportV7(event_id='208053', game_unit='24527-B-1')
    assert r._gen_period_scores_md() == '|Scores|Q1|Q2|Q3|Q4|OT1|Total\n|:---:|---:|---:|---:|---:|---:|---:\n|LBN|*17* \| **27**|*9* \| 19|*12* \| **22**|*11* \| 19|*6* \| 19|106\n|THA|*8* \| **22**|*15* \| **26**|*9* \| 14|*15* \| **25**|*3* \| 13|100\n'

if __name__ == '__main__':
    main()

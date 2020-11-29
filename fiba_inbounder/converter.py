# -*- coding: utf-8 -*-
import numpy as np
from fiba_inbounder.settings import LOGGER, REG_FULL_GAME_MINS

def game_time(q):
    if q > 4:
        return REG_FULL_GAME_MINS + 5 * (q-4)
    return REG_FULL_GAME_MINS / 4 * q

def base60_from(time_str):
    num_list = time_str.split(':')
    secs = 0
    for i in num_list:
        secs = secs * 60 + int(float(i))
    return secs

def base60_to(secs):
    secs = int(secs)
    num_list = list()
    if secs >= 60:
        d = int(secs / 60)
        num_list.append('%02d' % (secs - 60*d))
        num_list.append('%02d' % d)
    else:
        num_list.append('%02d' % secs)

    if len(num_list) == 1:
       num_list.append('00')
    num_list.reverse()

    return ':'.join(num_list)

def convert_team_stats_pleague_to_v7(df):
    df['AS'] = df['ast']
    df['BS'] = df['blk']
    df['PF'] = df['pfoul']
    df['FTA'] = df['ft_a'] + df['ft_m']
    df['FTM'] = df['ft_m']
    df['SECS'] = df['seconds']
    df['TP'] = df['seconds'].apply(lambda x: base60_to(x))
    df['PTS'] = df['points']
    df['DR']  = df['reb_d']
    df['OR'] = df['reb_o']
    df['REB'] = df['DR'] + df['OR']
    df['ST'] = df['stl']
    df['FG3A'] = df['trey_a'] + df['trey_m']
    df['FG3M'] = df['trey_m']
    df['TO'] = df['turnover']
    df['FG2A'] = df['two_a'] + df['two_m']
    df['FG2M'] = df['two_m']

    df['FGA'] = df['FG2A'] + df['FG3A']
    df['FGM'] = df['FG2M'] + df['FG3M']
    
    #TODO
    '''
    df['A_FBP'] = df['tot_sPointsFastBreak']
    df['A_SCP'] = df['tot_sPointsSecondChance']
    df['A_PAT'] = df['tot_sPointsFromTurnovers']
    df['A_PIP'] = df['tot_sPointsInThePaint']
    df['A_PFB'] = df['tot_sBenchPoints']
    '''

def convert_player_stats_pleague_to_v7(df):
    df['AS'] = df['ast']
    df['BS'] = df['blk']
    df['PF'] = df['pfoul']
    df['FTA'] = df['ft_a'] + df['ft_m']
    df['FTM'] = df['ft_m']
    df['SECS'] = df['seconds']
    df['TP'] = df['seconds'].apply(lambda x: base60_to(x))
    df['PTS'] = df['points']
    df['DR']  = df['reb_d']
    df['OR'] = df['reb_o']
    df['REB'] = df['DR'] + df['OR']
    df['ST'] = df['stl']
    df['FG3A'] = df['trey_a'] + df['trey_m']
    df['FG3M'] = df['trey_m']
    df['TO'] = df['turnover']
    df['FG2A'] = df['two_a'] + df['two_m']
    df['FG2M'] = df['two_m']

    df['FGA'] = df['FG2A'] + df['FG3A']
    df['FGM'] = df['FG2M'] + df['FG3M']
 
    df['PM'] = df['positive']

    df['JerseyNumber'] = df['jersey']
    df['Name'] = df['name_alt']

def convert_team_stats_v5_to_v7(df):
    df['AS'] = df['tot_sAssists']
    df['BS'] = df['tot_sBlocks']
    df['FGA'] = df['tot_sFieldGoalsAttempted']
    df['FGM'] = df['tot_sFieldGoalsMade']
    df['PF'] = df['tot_sFoulsTotal']
    df['FTA'] = df['tot_sFreeThrowsAttempted']
    df['FTM'] = df['tot_sFreeThrowsMade']
    df['TP'] = df['tot_sMinutes'].replace(np.nan, '00:00')
    df['SECS'] = df['tot_sMinutes'].replace(np.nan, '00:00').apply(lambda x: base60_from(x))
    df['PTS'] = df['tot_sPoints']
    df['DR']  = df['tot_sReboundsDefensive']
    df['OR'] = df['tot_sReboundsOffensive']
    df['REB'] = df['tot_sReboundsTotal']
    df['ST'] = df['tot_sSteals']
    df['FG3A'] = df['tot_sThreePointersAttempted']
    df['FG3M'] = df['tot_sThreePointersMade']
    df['TO'] = df['tot_sTurnovers']
    df['FG2A'] = df['tot_sTwoPointersAttempted']
    df['FG2M'] = df['tot_sTwoPointersMade']

    df['A_FBP'] = df['tot_sPointsFastBreak']
    df['A_SCP'] = df['tot_sPointsSecondChance']
    df['A_PAT'] = df['tot_sPointsFromTurnovers']
    df['A_PIP'] = df['tot_sPointsInThePaint']
    df['A_PFB'] = df['tot_sBenchPoints']

def convert_player_stats_v5_to_v7(df):
    df['AS'] = df['sAssists']
    df['BS'] = df['sBlocks']
    df['FGA'] = df['sFieldGoalsAttempted']
    df['FGM'] = df['sFieldGoalsMade']
    df['PF'] = df['sFoulsPersonal']
    df['FTA'] = df['sFreeThrowsAttempted']
    df['FTM'] = df['sFreeThrowsMade']
    df['FTP'] = df['sFreeThrowsPercentage']
    df['TP'] = df['sMinutes'].replace(np.nan, '00:00')
    df['SECS'] = df['sMinutes'].replace(np.nan, '00:00').apply(lambda x: base60_from(x))
    df['PTS'] = df['sPoints']
    df['DR']  = df['sReboundsDefensive']
    df['OR'] = df['sReboundsOffensive']
    df['REB'] = df['sReboundsTotal']
    df['ST'] = df['sSteals']
    df['FG3A'] = df['sThreePointersAttempted']
    df['FG3M'] = df['sThreePointersMade']
    df['TO'] = df['sTurnovers']
    df['FG2A'] = df['sTwoPointersAttempted']
    df['FG2M'] = df['sTwoPointersMade']
    df['PM'] = df['sPlusMinusPoints']

    df['JerseyNumber'] = df['shirtNumber']
    df['Name'] = df['name'].str.replace(' ', '').str.upper()

def convert_secs_v7(df):
    df['SECS'] = df['TP'].replace(np.nan, '00:00').apply(lambda x: base60_from(x))

def convert_xy_v7(df):
    #Left Corner as (0, 0) in Meters
    df['X_SIDELINE_M'] = df['SX'].apply(lambda x: float(x)/280*15)
    df['Y_BASELINE_M'] = df['SY'].apply(lambda y: float(y)/280*14)

def convert_xy_v5(df):
    #Left Corner as (0, 0) in Meters
    df['X_SIDELINE_M'] = df.apply(lambda s: float(s['y'])/100*15 if s['x']<=50 else float(100-s['y'])/100*15, axis=1)
    df['Y_BASELINE_M'] = df.apply(lambda s: float(s['x'])/50*14 if s['x']<=50 else float(100-s['x'])/50*14, axis=1)

def convert_pbp_stats_v7(df):
    #TODO: Still Lots of Stats
    df['FG2M'] = np.where((df['AC']=='P2') & (df['SU']=='+'), 1, 0)
    df['FG2A'] = np.where(df['AC']=='P2', 1, 0)
    df['FG3M'] = np.where((df['AC']=='P3') & (df['SU']=='+'), 1, 0)
    df['FG3A'] = np.where(df['AC']=='P3', 1, 0)

    df['FGA'] = df['FG2A'] + df['FG3A']
    df['FGM'] = df['FG2M'] + df['FG3M']
    df['FGPTS'] = 2 * df['FG2M'] + 3 *df['FG3M']
   
    df['FTM'] = np.where((df['AC']=='FT') & (df['SU']=='+'), 1, 0)
    df['FTA'] = np.where(df['AC']=='FT', 1, 0)
    df['PTS'] = df['FGPTS'] + df['FTM']
    
    df['OR'] = np.where((df['AC'].str.contains('REB')) & (df['Z1']=='O'), 1, 0)
    df['DR'] = np.where((df['AC'].str.contains('REB')) & (df['Z1']=='D'), 1, 0)
    df['REB'] = df['OR'] + df['DR']

    df['AS'] = np.where(df['AC']=='ASS', 1, 0)
    df['TO'] = np.where(df['AC']=='TO', 1, 0)

def convert_sub_pleague_to_v7(df, team_id_away):
    df['AC'] = 'SUBST'
    df['SU'] = df['status'].replace(True, '+').replace(False, '-')
    
    df['GT'] = df['createDate']
    #df[''] = df['quarter']
    df['Time'] = df['time'].apply(lambda x: x.replace('.0', ''))

    df['C1'] = df['rosterSn']
    df['T1'] = df['teamSn'].apply(lambda x: 't' + str(x))

    df['SA'] = np.where(df['T1']==team_id_away, df['teamScore'], df['opponentTeamScore'])
    df['SB'] = np.where(df['T1']==team_id_away, df['opponentTeamScore'], df['teamScore'])

    df['PTS'] = 0

def convert_pbp_stats_pleague_to_v7(df, team_id_away, team_id_home):
    #TODO: Still Lots of Stats
    df['AC'] = np.where((df['eventName']=='miss') | (df['eventName']=='score'),
            np.where(df['eventValue']==2, 'P2',
            np.where(df['eventValue']==3, 'P3', None)),
            None)
    
    df['GT'] = df['createDate']
    #df[''] = df['quarter']
    #df['Time'] = df['eventQuarterTime']

    df['C1'] = df['rosterSn']
    df['T1'] = df['teamSn'].apply(lambda x: 't' + str(x))
    df['OppTeamCode'] = np.where(df['T1']==team_id_away, team_id_home,
            np.where(df['T1']==team_id_home, team_id_away, None))
    
    df['FG2M'] = df.apply(lambda x: 1 if x['AC']=='P2' and x['eventName']=='score' else 0, axis=1)
    df['FG3M'] = df.apply(lambda x: 1 if x['AC']=='P3' and x['eventName']=='score' else 0, axis=1)
    df['FG2A'] = df.apply(lambda x: 1 if x['AC']=='P2' else 0, axis=1)
    df['FG3A'] = df.apply(lambda x: 1 if x['AC']=='P3' else 0, axis=1)

    df['FGA'] = df['FG2A'] + df['FG3A']
    df['FGM'] = df['FG2M'] + df['FG3M']
    df['FGPTS'] = 2 * df['FG2M'] + 3 *df['FG3M']

    df['FTM'] = np.where((df['eventName']=='freethrow') & (df['eventValue']==1) , 1, 0)
    df['FTA'] = np.where(df['eventName']=='freethrow', 1, 0)
    df['PTS'] = df['FGPTS'] + df['FTM']

    df['OR'] = np.where(df['eventName']=='offrebound', 1, 0)
    df['DR'] = np.where(df['eventName']=='defrebound', 1, 0)
    df['REB'] = df['OR'] + df['DR']

    df['AS'] = np.where(df['eventName']=='assist', 1, 0)
    df['TO'] = np.where(df['eventName']=='turnover', 1, 0)
 
def convert_pbp_stats_v5_to_v7(df, ta_code, tb_code):
    #TODO: Still Lots of Stats
    df['T1'] = np.where(df['tno']==1, ta_code,
            np.where(df['tno']==2, tb_code, None))
    df['OppTeamCode'] = np.where(df['tno']==1, tb_code,
            np.where(df['tno']==2, ta_code, None))
    df['C1'] = df.apply(lambda x: '{num} {name}'.format(
        num=x['shirtNumber'].zfill(2), name=x['player'].replace(' ', '').upper()), axis=1)
    df['AC'] = np.where((df['actionType']=='period') & (df['subType']=='end'), 'ENDP',
            np.where(df['actionType']=='substitution', 'SUBST', 
            np.where(df['actionType']=='2pt', 'P2',
            np.where(df['actionType']=='3pt', 'P3', None))))
    df['SU'] = np.where(df['actionType']=='substitution',
                np.where(df['subType']=='in', '+', 
                np.where(df['subType']=='out', '-', None)),
            None)
    if 'gt' in df:
        df['Time'] = df['gt']

    if 'success' in df:
        df['FG2M'] = np.where((df['actionType']=='2pt') & (df['success']==1), 1, 0)
        df['FG3M'] = np.where((df['actionType']=='3pt') & (df['success']==1), 1, 0)
    elif 'r' in df:
        df['FG2M'] = np.where((df['actionType']=='2pt') & (df['r']==1), 1, 0)
        df['FG3M'] = np.where((df['actionType']=='3pt') & (df['r']==1), 1, 0)
    else:
        df['FG2M'] = 0
        df['FG3M'] = 0
    df['FG2A'] = np.where(df['actionType']=='2pt', 1, 0)
    df['FG3A'] = np.where(df['actionType']=='3pt', 1, 0)

    df['FGA'] = df['FG2A'] + df['FG3A']
    df['FGM'] = df['FG2M'] + df['FG3M']
    df['FGPTS'] = 2 * df['FG2M'] + 3 *df['FG3M']
   
    if 'success' in df:
        df['FTM'] = np.where((df['actionType']=='freethrow') & (df['success']==1), 1, 0)
    else:
        df['FTM'] = 0
    df['FTA'] = np.where(df['actionType']=='freethrow', 1, 0)
    df['PTS'] = df['FGPTS'] + df['FTM']
    
    df['OR'] = np.where((df['actionType']=='rebound') & (df['subType']=='offensive'), 1, 0)
    df['DR'] = np.where((df['actionType']=='rebound') & (df['subType']=='defensive'), 1, 0)
    df['REB'] = df['OR'] + df['DR']

    df['AS'] = np.where(df['actionType']=='assist', 1, 0)
    df['TO'] = np.where(df['actionType']=='turnover', 1, 0)

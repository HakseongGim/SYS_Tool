from datetime import datetime
import numpy as np

def Separator (df, df_column) :

    Sep_Start = []
    Sep_End = []   
    Result_list = []

    
    df = df.sort_values(df_column, axis=0, ascending = True)
    df = df.reset_index(drop=True)    
    obj = df.loc[:, df_column]

    Start_value = 0
    End_value = len(obj)-1
    
  
    for p1, p2, i in zip(obj, obj[1:], range(len(obj))):
        if p1 != p2:
            Sep_Start.append(i+1)
            Sep_End.append(i)
          

    Sep_Start.insert(0, Start_value)        
    Sep_End.insert(len(obj)-1, End_value)    


    for i in range(len(Sep_Start)):               
        Result_list.append(df.loc[Sep_Start[i]:Sep_End[i], :]) 
    
    
    return (Result_list, Sep_Start, Sep_End) 

#-----------------------------------------------------------------------------
def WHT_cal (df_WT, WT_start, WT_end):

    WT_num = df_WT.loc[:, 'title'] #풍력발전기 번호
    Date = df_WT.loc[:, 'yymmdd'] #날짜
    Time = df_WT.loc[:, 'hhmmss'] #시간
      
# #-----------------------------------------------------------------------------
# # 문자열 -> 시간으로 변경 Time_str -> Time   
#     Time = []  
#     for i in Time_str:      
#         elm = datetime.strptime(i, '%H:%M:%S') + timedelta(hours=9)   
#         Time.append(elm.time())
#     Time = pd.Series(Time)
# #-----------------------------------------------------------------------------

    if len(Time) <=30:
        Time_interval = np.nan
    else:
        Time_interval = datetime.strptime(Time[WT_end-2],'%H:%M:%S') - datetime.strptime(Time[WT_start+2],'%H:%M:%S')
        
  
    total_data = [Date[WT_start], WT_num[WT_start], Time[WT_start], Time[WT_end], str(Time_interval)]
     
    return total_data
    
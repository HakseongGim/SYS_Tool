import pandas as pd
import WF_name_separator
import os
from datetime import datetime, timedelta

API_key = 'xrJZ8HroohTzA4twNYzuzANO61JIKQYz2ZIFgnzW'
url = 'http://redash.nearthlab.com/api/queries/25/results.csv?api_key={}'.format(API_key)
df = pd.read_csv(url)


df_re = WF_name_separator.WF_name_sep(df)

#-----------------------------------------------------------------------------
def WT_number_separator (df_data):
    
    WF_name = df_data.loc[:, 'name']    #풍력발전단지 
    WT_num = df_data.loc[:, 'title'] #풍력발전기 번호

    Date_str = df_data.loc[:, 'yymmdd'] #날짜
    Time_str = df_data.loc[:, 'hhmmss'] #시간
    

#-----------------------------------------------------------------------------
# 풍력발전기(호기) 구분
    num_Start = []
    num_End = []

    index_num = WT_num.index.values    

    i = index_num[1]
    
    for p1, p2 in zip(WT_num, WT_num[1:]):
        i = i+1
        if p1 != p2:
            num_Start.append(i)
            num_End.append(i-5)

    num_Start.insert(0, index_num[1])        
    num_End.insert(index_num[-1], index_num[-1])      
 
#-----------------------------------------------------------------------------
# 문자열 -> 시간으로 변경 Time_str -> Time   
    Time = []  
    for i in Time_str:      
        elm = datetime.strptime(i, '%H:%M:%S') + timedelta(hours=9)   
        Time.append(elm.time())
    Time = pd.Series(Time)
    
    a = []
    b = []
    for i in range(len(num_Start)):
        a.append(num_Start[i]-num_Start[0])
        b.append(num_End[i]-num_Start[0])
 
#-----------------------------------------------------------------------------
    Time_interval = []
    poket = []
    for p1, p2 in zip(num_Start, num_End):
        elm = datetime.strptime(Time_str[p2],'%H:%M:%S') - datetime.strptime(Time_str[p1],'%H:%M:%S')
         # elm = Time[p2] - Time[p1]
        Time_interval.append(elm)
 
    
    total_data = pd.DataFrame(zip(Date_str[num_Start],WF_name[num_Start], WT_num[num_Start], Time[a], Time[b], Time_interval))
    total_data.columns = ['점검일','단지','호기', '시작시간','종료시간','점검시간']
     
    poket.append(total_data)
    return print(poket)
    
#-----------------------------------------------------------------------------

# writer = pd.ExcelWriter('test.xlsx', engine='xlsxwriter')
for i in range(len(df_re)):
    WT_number_separator(df_re[i])
    


# with pd.ExcelWrither('test.xlsx') as writer:

    
    
    
# folder = 'WT_inspection'  
#     base_dir = 'C:\\Users\\HakSeong Gim\\Desktop\\{}'.format(folder)
#     file_nm = '1일 점검량.xlxs'
#     xlxs_dir = os.path.join(base_dir, file_nm)
    
#     with pd.ExcelWriter(xlxs_dir) as writer:
#         total_data.to_excel(writer, encoding ='utf-8-sig', index=False, sheet_name ='1'  )
        

# WT_number_separator(df_re[0])
# folder = 'WT_inspection'
# save_name = '점검시간.csv'

# total_data.to_csv('C:\\Users\\tkdcn\\OneDrive\\바탕 화면\\{}/{}'.format(folder, save_name), encoding = 'utf-8-sig', index=False)
# # total_data.to_csv('C:\\Users\\HakSeong Gim\\Desktop\\{}/{}'.format(folder, save_name), encoding = 'utf-8-sig', index=False)


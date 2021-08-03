import pandas as pd
import Separator_func as se


API_key = 'xrJZ8HroohTzA4twNYzuzANO61JIKQYz2ZIFgnzW'
url = 'http://redash.nearthlab.com/api/queries/25/results.csv?api_key={}'.format(API_key)



df = pd.read_csv(url)
df_column = ['yymmdd', 'title', '점검일']

df_date, _, _ = se.Separator(df, df_column[0])

df_WT = []
WT_start = []
WT_end = [] 
for i in range(len(df_date)):
    elm_1, elm_2, elm_3 = se.Separator(df_date[i], df_column[1])
    df_WT.append(elm_1)
    WT_start.append(elm_2)
    WT_end.append(elm_3)

a = []  
for i in range(len(df_WT)):
    for j in range(len(df_WT[i])):
        df_WT[i][j] = df_WT[i][j].sort_values('hhmmss', axis=0, ascending=True)
        df_WT[i][j] = df_WT[i][j].reset_index(drop=True)
        a.append(se.WHT_cal(df_WT[i][j], WT_start[i][j]-WT_start[i][j], WT_end[i][j]-WT_start[i][j]))
        
        
total_data = pd.DataFrame(a)       
total_data.columns = ['점검일','호기', '시작시간','종료시간','점검시간']    

   
b, _, _ = se.Separator(total_data, df_column[2])    

writer = pd.ExcelWriter('Result_12.xlsx', engine='xlsxwriter')
for i in range(len(b)): 
    b[i] = b[i].sort_values('시작시간', axis=0, ascending = True)
    b[i] = b[i].reset_index(drop=True)    
    b[i].to_excel(writer, sheet_name = str(i+1), index = False)

writer.save()

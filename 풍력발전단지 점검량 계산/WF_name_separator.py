def WF_name_sep (df) :

    name_Start = []
    name_End = []
    WF_name_list = []
    
    WT_name = df.loc[:, 'name']

    Start = 0
    End = len(WT_name)-1

    for p1, p2, i in zip(WT_name, WT_name[1:], range(len(WT_name))):
        if p1 != p2:
            name_Start.append(i+1)
            name_End.append(i)

    name_Start.insert(0, Start)        
    name_End.insert(len(name_End), End)    

    for i in range(len(name_Start)):
        WF_name_list.append(df.loc[name_Start[i]:name_End[i], :])

    return WF_name_list
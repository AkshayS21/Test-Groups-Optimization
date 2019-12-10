import numpy as np
import pandas as pd
from itertools import combinations, permutations
from collections import defaultdict
import time
from tkinter import *
from tkinter import filedialog





def optimize(dataframe, path):
    d1 = dataframe.copy()
    df_dict = defaultdict(pd.DataFrame)

    pos = 0
    for i in range(len(d1)):

        if all(list(d1.iloc[i,1:] <= 0.5)):

            df_dict[pos] = d1.iloc[i]
            pos +=1

    result_d_df = pd.DataFrame.from_dict(data = df_dict, orient = 'index')
    if not result_d_df.empty:
        
        result_df = result_d_df.copy()
        result_df['end_sum']=result_df.sum(axis = 1, numeric_only = True)
        result_sorted = result_df.sort_values(by = 'end_sum')  
        result_sorted.reset_index(drop = 1, inplace = True) 
        
        return result_sorted
        
    else:
        
        
        opt = dataframe.copy()
        opt2 = dataframe.copy()

        wt_list = weights(dataframe)
        wts = wt_list.copy()
        wts.insert(0,0.0)
         
        arr = np.array(wts)
        wsum = arr.sum()
        wtsa = arr / wsum

        for j in range(1,len(opt.columns)):

            opt[ opt.columns[j]] *= wtsa[j]


        opt['sum_end'] = opt.sum(axis = 1, numeric_only = True) 


        #opt.sort_values(by = 'sum_end')

        opt2['wtd_sum'] = opt['sum_end']

        opt2.sort_values(by = 'wtd_sum', inplace = True)

        opt2 = opt2.round(decimals = 2)

        #opt2.head(10)  
        
        global df_optimize
        df_optimize = opt2.copy()
        
        df_optimize.to_excel(path)
        
        return df_optimize








def weights(dataframe):
    
    dw = dataframe.copy()

    #chlist = ['testgroups']

    def add_col():
        global wtlist
        
        wtlist = []
        for num in var_list:
            wtlist.append(float(num.get()))
        #print(chlist)

    #def var_states():
    #    for text in var_list:
    #        print(text.get())  

    var_list = []
    appw = Tk()
    appw.title("Enter weights for each column below")
    appw.geometry("500x500")
    
    frame0 = LabelFrame(appw, padx = 5, pady = 5, height = 100, width = 100)
    frame0.pack(padx = 20, pady = 20)
    
    Label(frame0, text = "None of the combinations have all <= 0.5").grid(row = 1, column = 1)
    Label(frame0, text = "Please select weights for each column as per its priority").grid(row = 2, column = 1)
    Label(frame0, text = "Required Value : Weight \n\n< 0.5 : 4 \t\t  0.5 - 0.7 : 3 \t 0.7 - 1 : 2 \t > 1 : 1 \n").grid(row = 3, column = 1)
    
    
    
    
    frame1 = LabelFrame(appw, padx = 5, pady = 5, height = 100, width = 100)
    frame1.pack(padx = 20, pady = 20)
    
    frame2 = LabelFrame(appw, padx = 5, pady = 5)
    frame2.pack(padx = 20, pady = 20)
    
    for i in range(1,len(dw.columns)):
        
        

        if i<6:
            column = 1
            Label(frame1, text = dw.columns[i]).grid(row = i, column = column)
            e = Entry(frame1, width = 5)
            e.grid(row= i, column= column + 1, sticky=W)
            
        elif 6 <= i <= 10:
            column = 4
            Label(frame1, text = dw.columns[i]).grid(row = i-5, column = column)
            e = Entry(frame1, width = 5)
            e.grid(row= i-5 , column= column+ 5, sticky=W)
            
        else:
            column = 10
            Label(frame1, text = dw.columns[i]).grid(row = i-10, column = column )
            e = Entry(frame1, width = 5)
            e.grid(row= i - 10 , column= column + 5, sticky=W)
        
        var_list.append(e)

    b1 = Button(frame2, text="Add", command= add_col).grid(row=25, column=1)
    
    #Button(app, text='Show', command=var_states).grid(row=28, sticky=W, pady=4)

    #Button(master, text='Quit', command=app.quit).grid(row=3, sticky=W, pady=4)
    mainloop() 
    
    return wtlist
    





def create(data, testgroups, splitsize, path , decimals = 2):
    
    """
    
    data : The dataframe to be used for optimization. This dataframe should only have the 
               testgroups to work on and the columns with revenue. First column should include 
               the testgroups. Values in other columns should be grouped by the testgroups and summed.
               This dataframe should be indexed by default.i.e 0,1,2,... 
               (Dataframes are indexed by default unless the indexes are purposely removed.)
               
        testgroups : number of distinct testgroups.
        
        splitsize: Size of a testgroup. For example, if 18 divided in 5 and 5, splitsize = 5.
        
        decimals :  numb er of decimals. default value is 2.
        path = path to save the excel file.
        
        
        output :  returns the dataframe of all possible group combinations as well as saves an excel 
                  file of the dataframe to the 'path'.
    
    """
    

    data_new = data.copy()
    testgroups = int(testgroups)
    splitsize = int(splitsize)
    
    if splitsize * 2 <= testgroups:
        
    
        if testgroups / splitsize == 2:

            output = func_half(data_new, testgroups, path, decimals)

        else:

            output = func_other(data_new , testgroups, splitsize, path,  decimals = 2)

        global df_create
        df_create = output.copy()


        return df_create
    
    else:
        
        print("Please make sure that splitsize x 2 is less than or equal to testgroups.")
        
       
        
    
    
    




def func_half(data , testgroups , path, decimals = 2):
    
    """
        Use this function only when you are splitting the set of groups halfway in A and B.
        For example, 20 split in 10 and 10. 
        Do not use when, e.g., splitting 18 into 5 and 5.
    
        data : The dataframe to be used for optimization. This dataframe should only have the 
               testgroups to work on and the columns with revenue. First column should include 
               the testgroups. Values in other columns should be grouped by the testgroups and summed.
               This dataframe should be indexed by default.i.e 0,1,2,... 
               (Dataframes are indexed by default unless the indexes are purposely removed.)
               
        testgroups : number of distinct testgroups.
        
        decimals :  numb er of decimals. default value is 2.
        path = path to save the excel file.
        
        
        output :  returns the dataframe of all possible group combinations as well as saves an excel 
                  file of the dataframe to the 'path'.
             
    """
    
    
    
    tot_start = time.time()
    
    df = pd.DataFrame(data)
    groups_list = range(testgroups)
    comb = list(combinations(groups_list, int(testgroups/2)))
    
    #print(len(comb))
    
    # Dictionary of combinations
    print(' Creating dictionary of combinations....')
    start = time.time()
    N = defaultdict(pd.DataFrame)
    for i, combn in enumerate(comb):
        N[combn] = df.iloc[list(comb[i])]
    end = time.time()
    print("\n Time taken in seconds: {:.2f}".format(end-start))
        
    print('\n Creating dictionary of aggregates....')
    
    D = defaultdict(pd.DataFrame)
    start = time.time()
    for i, combn in enumerate(comb):
    
        D[i] = N[combn].sum(axis = 0)
    end = time.time()
    print("\n Time taken in seconds: {:.2f}".format(end-start))
    
    print("\n Total number of possible combinations: ", int(len(D)/2))
    
    #N = None
    
    print("\n Creating dataframe from dictionary...")
    
    df_dict = pd.DataFrame.from_dict(D, 'index')
    df_dict
    
    print("\n df_dict created")
    
    print("\n Splitting df midway...")
    
    
    df = df_dict.copy()
    df1 = df[:int(len(df)/2)]
    df2 = df.iloc[int(len(df)/2):]
    
    #D = None
    
    print("\n Splitting done.")
    
    print("\n Flipping df2")
    
    df2a = df2.copy()
    df2_r = df2a[::-1]
    
    print("\n Adding groups to df1 half..")
    
    df1a=df1.copy()
    
    df1a[df1a.columns[0]] = df1a[df1a.columns[0]].str.cat(others = df2_r[df2_r.columns[0]].values, sep = ' + ')
    
    df_new = df1a.copy()
    
    
    print("\n Creating arrays...")
    
    df_calc = df_new.copy()
    df_array = df_calc.values
    
    df_array2 = df2_r.values
    
    print("\n Array operations...")
    
    df_array_calc = (( (df_array[:,1:]) / ((df_array[:,1:] + df_array2[:,1:])/2) ) -1 )* 100
    
    
    print("\n Rounding the resulting array...")
    
    df_rounded = np.around(df_array_calc.astype(np.double),decimals = decimals)
    
    
    print("\n Absolutes...")
    
    df_abs_double = np.absolute(df_rounded)
    
    print("\n Adding the computed array to dataframe...")
    
    df_final = df_new.copy()
    
    df_final[df.columns[1:]] = pd.DataFrame(data = df_abs_double, columns = df_new.columns[1:])
    
    print("\n Saving the excel file...")
    
    df_final.to_excel(path)
    
    print("\n All Done.")
    
    tot_end = time.time()
    
    print("\n Total time in minutes: {:.3f}".format((end-start)/60))
    
    return df_final
    

    
    
    
def func_other(data , testgroups, splitsize, path,  decimals = 2) :
    
    """
        Use this function only when you are splitting the set of groups not halfway in A and B.
        For example, splitting 18 into 5 and 5. 
        Do not use when, e.g., 20 split in 10 and 10.
    
        data : The dataframe to be used for optimization. This dataframe should only have the 
               testgroups to work on and the columns with revenue. First column should include 
               the testgroups. Values in other columns should be grouped by the testgroups and summed.
               This dataframe should be indexed by default.i.e 0,1,2,... 
               (Dataframes are indexed by default unless the indexes are purposely removed.)
               
                       
        testgroups : number of distinct testgroups.
        
        splitsize: Size of a testgroup. For example, if 18 divided in 5 and 5, splitsize = 5.
        
        decimals :  numb er of decimals. default value is 2.
        path = path to save the excel file.
        
        output :  returns the dataframe of all possible group combinations as well as saves an excel 
                  file of the datafram at the path.
             
    """
    
    
    tot_start = time.time()
    
    #df = pd.DataFrame(data)
    df = data.copy()
    groups_list = range(testgroups)
    comb = list(combinations(groups_list, int(splitsize * 2)))
    
    
    # Dictionary of combinations
    print(' Creating dictionary of combinations....')
    start = time.time()
    N = defaultdict(pd.DataFrame)
    for i in range(int(len(comb))):
        N[i] = df.iloc[list(comb[i])]
    end = time.time()
    print("\n Time taken in seconds: {:.2f}".format(end-start))
        
    print('\n Creating dictionaries of aggregates....')
    
    D1 = defaultdict(pd.DataFrame)
    D2 = defaultdict(pd.DataFrame)
    
    start = time.time()
    for i in range(int(len(comb))):    
        D1[i] = N[i][: int(len(comb[i])/2)].sum(axis = 0)
        D2[i] = N[i][int(len(comb[i])/2): ].sum(axis = 0)
    end = time.time()
    
               
    
    print("\n Time taken in seconds: {:.2f}".format(end-start))
    
    print("\n Total number of possible combinations: ", int(len(D1)))
    
    
    
    print("\n Creating dataframe from dictionary...")
    
    df_dict1 = pd.DataFrame.from_dict(D1, 'index')
    df_dict2 = pd.DataFrame.from_dict(D2, 'index')
    
    df1 = df_dict1.copy()
    df2 = df_dict2.copy()
    
    print("\n df_dict created")
    
    df1[df1.columns[0]] = df1[df1.columns[0]].str.cat(others = df2[df2.columns[0]].values, sep = ' + ')
    
    print("\n Creating arrays...")
    
    array1 = df1.values
    array2 = df2.values
    
    print("\n Array operations...")
    
    df_array_calc = (( (array1[:,1:]) / ((array1[:,1:] + array2[:,1:])/2) ) -1 )* 100
              
       
        
    print("\n Rounding the resulting array...")
    
    df_rounded = np.around(df_array_calc.astype(np.double),decimals = decimals)
    
    
    print("\n Absolutes...")
    
    df_abs_double = np.absolute(df_rounded)
    
    print("\n Adding the computed array to dataframe...")
    
    df_final = df1.copy()
    df_new = df1.copy()
    
    df_final[df.columns[1:]] = pd.DataFrame(data = df_abs_double, columns = df_new.columns[1:])
    
    print("\n Saving the excel file...")
    
    df_final.to_excel(path)
    
    print("\n All Done.")
    
    tot_end = time.time()
    
    print("\n Total time in minutes: {:.3f}".format((tot_end-tot_start)/60))
    
    return df_final


def select_file():
    
    appf = Tk()
    appf.title("Select the Excel file")
    appf.geometry("500x500")
    appf.resizable(width = True, height = True)
    
    frame1 = LabelFrame(appf, padx = 20, pady = 20, height = 250 , width = 400)
    frame1.pack(padx = 10, pady = 20)
    
    
    
    var_list = []
    
    
    
    def selectxfile():
        
        #global filename
        
    
        filename = filedialog.askopenfilename(initialdir = '/', title = 'Select the Excel file', 
                                              filetypes = ( ("excel files","*.xlsx"), ("all files", "*.*")   )) 
        
        
        Label(frame1, text = "------------------").grid(row = 20, column = 1)
        Label(frame1, text = filename).grid(row = 40, column = 1)
        
        xl = pd.ExcelFile(filename)
        
        sheet_list = xl.sheet_names
        
        frame2 = LabelFrame(appf, text = "Select one sheet only",padx = 20, pady = 20, height = 400, width = 400)
        frame2.pack(padx = 5, pady = 5)
        
        Label(frame2, text = "   ").grid(row = 1, column = 0)
        Label(frame2, text = "   ").grid(row = 1, column = 50)
        
        for i in range(len(sheet_list)):
            
            sname = StringVar()
            check = Checkbutton(frame2,text = sheet_list[i], variable = sname,
                                onvalue = sheet_list[i], offvalue = "" )

            var_list.append(sname)
            #print(check.get())

            if i<=2:
                column = 1
                check.grid(row= i, column= column, sticky=W)
            elif 2 < i <=5:
                column = 2
                check.grid(row= i-3, column= column, sticky=W)
            else:
                column = 3
                check.grid(row= i - 5 , column= column, sticky=W)
                
                
        
        frame3 = LabelFrame(appf, text = "Select & Extract",padx = 20, pady = 20, height = 400, width = 400)
        frame3.pack(padx = 10, pady = 10)
                
        Label(frame3, text = "   ").grid(row = 1, column = 0)
        Label(frame3, text = "   ").grid(row = 1, column = 10)
        
        def select_sheet():
            
            global sheet_name
 
            for sheet in var_list:
                if sheet.get() != "":
                    sheet_name = sheet.get()
                
        b2 = Button(frame3, text = "Select this sheet", command = select_sheet).grid(row = 0, column = 1)
        
        
        def extract():
        
            global raw
        
            raw = pd.read_excel(filename, sheet_name = sheet_name)
      
        Label(frame3, text = "   ").grid(row = 0, column = 2)
        b3 = Button(frame3, text = "Extract", command = extract).grid(row = 0, column = 3) 
        

    b1 = Button(frame1, text = "Select Excel file", command = selectxfile).grid(row = 10, column = 1)

    mainloop()
    
    return raw
    

    
def aggregate(dataframe):
    
    df0 = dataframe.copy()

    l1 = first_column(df0)#

    dropped = df0.drop(l1[0], axis = 1)

    others = dropped.copy()

    l2 = other_columns(others)#
    col_list = l1 + l2

    chosen = df0[col_list]    

    grouped = chosen.groupby(by = chosen.columns[0], as_index = False).sum()   

    grplist = select_groups(grouped) #

    new = grouped.loc[ grouped[grouped.columns[0]].isin(grplist)]

    global df_aggregate

    df_aggregate = new.reset_index(drop = True)

    glist = chlist = flist = None

    return df_aggregate    
    
    
    
    
    


def select_groups(dataframe):
    
    d3 = dataframe.copy()
    
    def add_col():
        global glist
        glist = []
        for text in var_list:
            if text.get() != "":
                glist.append(text.get())
        
    def select_all():
        
        for checks in check_list:
            checks.select()            
    
    
    
    
    var_list = []
    check_list = []
    app3 = Tk()
    app3.title("Select the Test Groups")
    app3.geometry("300x400")
    
    groups = d3[ d3.columns[0] ]
    
    
    frame1 = LabelFrame(app3, padx = 20, pady = 20, height = 100, width = 100)
    frame1.pack(padx = 20, pady = 20)
    
    frame2 = LabelFrame(app3, padx = 20, pady = 20, height = 100, width = 100)
    frame2.pack(padx = 5, pady = 5)

    
    
    
    
    for i in range(len(groups)):

        vname = StringVar()
        
        check = Checkbutton(master = frame1, text= groups[i], variable=vname,
                               onvalue= groups[i], offvalue="" ) 
        var_list.append(vname)
        check_list.append(check)

        if i<=6:
            column = 1
            check.grid(row= i, column= column, sticky=W)
        elif i >= 7 and i <= 13:     #8 <= i < 13:
            column = 5
            check.grid(row= i-7 , column= column, sticky=W)
        else:
            column = 11
            check.grid(row= i-14 , column= column, sticky=W)

    Button(frame2, text = "Select All", command = select_all).grid(row=35, column = 5)
    Label(frame2 , text = "----------").grid(row = 50, column = 5)
    Button(frame2, text="Add", command= add_col).grid(row=80, column = 5)
    
    #Button(app1, text='Show', command=show).grid(row=28, sticky=W, pady=4)
    mainloop()
    
    return glist



def other_columns(dataframe):
    
    d1 = dataframe.copy()

    

    def add_col():
        global chlist
        
        chlist = []
        for text in var_list:
            if text.get() != "":
                chlist.append(text.get())
                
    def select_all():
        
        for checks in check_list:
            checks.select()  
        
    check_list = []
    var_list = []
    app = Tk()
    app.title("Select other columns and click the Add button")
    app.geometry("450x450")
    
    frame1 = LabelFrame(app, padx = 20, pady = 20, height = 100, width = 100)
    frame1.pack(padx = 20, pady = 20)
    
    frame2 = LabelFrame(app, padx = 20, pady = 5, height = 200, width = 200)
    frame2.pack(padx = 5, pady = 5)  
    
    
    for i in range(len(d1.columns)):

        vname = StringVar()
        check = Checkbutton(master = frame1, text=d1.columns[i], variable=vname,
                               onvalue= d1.columns[i], offvalue="")
        var_list.append(vname)
        check_list.append(check)

        if i<=9:
            column = 1
            check.grid(row= i+2, column= column, sticky=W)
        elif 10 <= i < 19:
            column = 2
            check.grid(row= i-10 + 2 , column= column, sticky=W)
        else:
            column = 3
            check.grid(row= i - 19 + 2 , column= column, sticky=W)

    
    Button(frame2, text=" Select All ", command= select_all).grid(row=35, column = 1)
    Label(frame2 , text = "----------").grid(row = 40, column = 1)
    Button(frame2, text=" Add ", command= add_col).grid(row= 59, column = 1)
    

    mainloop() 
    
    return chlist


def first_column(dataframe):
    
    d2 = dataframe.copy()
    
    def add_col():
        global flist
        flist = []
        for text in var_list1:
            if text.get() != "":
                flist.append(text.get())
        
 
    var_list1 = []
    app1 = Tk()
    app1.title("Select the column that contains the testgroups")
    app1.geometry("450x400")
    
    frame1 = LabelFrame(app1, padx = 20, pady = 20, height = 100, width = 100)
    frame1.pack(padx = 20, pady = 20)
    
    frame2 = LabelFrame(app1, padx = 10, pady = 10, height = 100, width = 100)
    frame2.pack(padx = 5, pady = 5)
    
    
    for i in range(len(d2.columns)):

        vname = StringVar()
        check = Checkbutton(master = frame1, text=d2.columns[i], variable=vname,
                               onvalue= d2.columns[i], offvalue="")
        var_list1.append(vname)

        if i<=9:
            column = 1
            check.grid(row= i+2, column= column, sticky=W)
        elif 10 <= i < 19:
            column = 2
            check.grid(row= i-10 + 2 , column= column, sticky=W)
        else:
            column = 3
            check.grid(row= i - 19 + 2 , column= column, sticky=W)

    Button(frame2, text="Select First Column", command= add_col).grid(row=0, column = 1)
    
    mainloop()
    
    return flist

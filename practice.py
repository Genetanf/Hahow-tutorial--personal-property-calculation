import pandas as pd
import matplotlib.pyplot as plt
plt.rc("font",family="Microsoft JhengHei")


# 設定年齡範圍
time=range(24,100)
# 設定初始資產
property=pd.Series(0,index=time)
property[24]=18

# with only monthly income
# 30monthly income=3
# 40monthly income=8
# 50monthly income=12
# 60monthly income=18

# 定義收入函數
def income(b30,b40,b50,b60,a60):
    income_series=pd.Series(0,index=time)
    income_series[24]=18
    for age in time:
        if age>24:
            if age<=30:
                income_series[age]=income_series[age-1]+b30*12
            elif age<=40:
                income_series[age]=income_series[age-1]+b40*12
            elif age<=50:
                income_series[age]=income_series[age-1]+b50*12
            elif age<=60:
                income_series[age]=income_series[age-1]+b60*12
            elif age>60:
                if a60==0:
                    income_series[age]=income_series[age-1]
                else:
                    income_series[age]=income_series[age-1]+a60*12
    return income_series

            
# 定義支出函數
def spending(b30,b40,b50,b60,a60):
    spending_series=pd.Series(0,index=time)
    for age in time:
        if age>24:
            if age<=30:
                spending_series[age]=spending_series[age-1]+b30*12
            elif age<=40:
                spending_series[age]=spending_series[age-1]+b40*12
            elif age<=50:
                spending_series[age]=spending_series[age-1]+b50*12
            elif age<=60:
                spending_series[age]=spending_series[age-1]+b60*12
            elif age>60:
                spending_series[age]=spending_series[age-1]+a60*12
    return spending_series


# 定義包含投資與利息的收入
totalWithInvest=pd.Series(0,index=time)
totalWithInvest[24]=18
def deposit(b30,b40,b50,b60,a60):
    deposit_series=pd.Series(0,index=time)
    deposit_series[24] =18  # 初始值

    for age in time:
        if age>24:
            if age<=30:
                deposit_series[age]=deposit_series[age-1]+b30*12*1.02
            elif age<=40:
                deposit_series[age]=deposit_series[age-1]+b40*12*1.02
            elif age<=50:
                deposit_series[age]=deposit_series[age-1]+b50*12*1.02
            elif age<=60:
                deposit_series[age]=deposit_series[age-1]+b60*12*1.02
            elif age>60:
                    if a60==0:
                        deposit_series[age]=deposit_series[age-1]*1.02
                    else:
                        deposit_series[age]=deposit_series[age-1]+a60*12*1.02
    return deposit_series
                    

def investment(b30,b40,b50,b60,a60):
    investment_series=pd.Series(0,index=time)
    investment_series[24] = 0
    for age in time:
        if age>24:
            if age<=30:
                investment_series[age]=investment_series[age-1]+b30*1.05*12
            elif age<=40:
                investment_series[age]=investment_series[age-1]+b40*1.05*12
            elif age<=50:
                investment_series[age]=investment_series[age-1]+b50*1.05*12
            elif age<=60:
                investment_series[age]=investment_series[age-1]+b60*1.05*12
            elif age>60:
                    if a60==0:
                        investment_series[age]=investment_series[age-1]*1.05
                    else:
                        investment_series[age]=investment_series[age-1]+a60*1.05*12
    return investment_series


# 定義買房資訊
# hosuePrice=1500
# firstcost=200
# buyingAge=35
# loanYears=50
# debtRatio=1.03

def buyingHouse(housePrice,firstcost,buyingAge,loanYears,debtRatio):
    buyingHouse_series=pd.Series(0,index=time)
    buyingHouse_series[buyingAge] = firstcost

    for age in time:
        if age>24:
            if buyingAge<age<buyingAge+2:
                buyingHouse_series[age]=(housePrice - firstcost)*debtRatio/loanYears
            elif age>buyingAge+2:
                buyingHouse_series[age]=((housePrice - firstcost)-buyingHouse_series[age-1])*debtRatio/loanYears
    return buyingHouse_series



#----------------------------------------------------------------------------------------

# 定義最終資產函數(不買房，不投資)
def overall_property(income_series,spending_series):
    property_series=income_series - spending_series
    return property_series

# 自定義內容(不買房，不投資)
income_series=income(3,8,12,18,0)
spending_series=spending(1,2.5,4,7,3.5)


# 計算最終資產(不買房，不投資)
property_series = overall_property(income_series,spending_series)
plt.plot(property_series,color="red",label="不買房，不投資")


#----------------------------------------------------------------------------------------

# 定義最終資產函數(不買房，有投資)
def incomeWithInvest(deposit_series, investment_series,spending_series):
    property_series = deposit_series + investment_series - spending_series
    return property_series

# 自定義內容(不買房，有投資)
deposit_series=deposit(1,2,4,6,0)
investment_series=investment(1,3,3,3,0)
spending_series=spending(1,3,5,9,3.5)

# 計算最終資產(不買房，有投資)
property_series=incomeWithInvest(deposit_series,investment_series,spending_series)
plt.plot(property_series,color="green",label="不買房，有投資")


#----------------------------------------------------------------------------------------

# 定義最終資產函數(有買房，有投資)
def withHouse_and_investment(deposit_series, investment_series,spending_series,buyingHouse_series):
    property_series=deposit_series + investment_series - spending_series-buyingHouse_series
    return property_series

buyingHouse_series=buyingHouse(1500,200,35,50,1.03)

# 計算最終資產(不買房，有投資)
property_series=withHouse_and_investment(deposit_series,investment_series,spending_series,buyingHouse_series)
plt.plot(property_series,color="black",label="有買房，有投資")


#----------------------------------------------------------------------------------------

# 定義最終資產函數(有買房，沒投資)
def withHouse_and_noinvestment(income_series,spending_series,buyingHouse_series):
    property_series=income_series - spending_series-buyingHouse_series
    return property_series

# 計算最終資產(不買房，有投資)
property_series=withHouse_and_noinvestment(income_series,spending_series,buyingHouse_series)
plt.plot(property_series,color="yellow",label="有買房，不投資")


plt.legend()
plt.show()


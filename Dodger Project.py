
"""
Created on Thu Sep 15 21:50:20 2022

@author: sergiocisneros
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

"""
Cleaning Data
"""
df = pd.read_csv(r'/Users/sergiocisneros/Desktop/Dodger Project/baseballdatabank-2022.2/core/Teams.csv')
df["Win %"]= df["W"]/(df["W"] + df["L"])
df1 = df[["yearID","teamID","Win %","divID","lgID"]]
df1 = df1[df1["yearID"] == 2021]
df1['teamID']=df1['teamID'].apply(lambda x: 'ANA' if x=='LAA' else x)
df1["yearID"]=df1["yearID"].astype(str)
df1["ID"] = df1["lgID"] + df1["divID"] 
print (df1)


df2 = pd.read_csv(r'/Users/sergiocisneros/Desktop/Dodger Project/schedule/2021SKED.TXT', sep=",",header=None, names=["Date","Double Header","Day of Week","Visiting Team","Visiting League","Visiting Game Number","Home Team","Home League","Home Game Number","Time of Game","Postpone","Postpone Date"])
df2["Date"]=df2["Date"].astype(str)
df2["Year"]=df2["Date"].str[:4]
print(df2)

df1.rename(columns = {'yearID':'Year','teamID':'Visiting Team','Win %':'Visiting Win %'},inplace=True)
df3 = pd.merge(df2,df1,on=['Visiting Team','Year'], how='inner')
df1.rename(columns = {'Visiting Team':'Home Team','Visiting Win %':'Home Win %'},inplace=True)
df3 = pd.merge(df3,df1,on=['Home Team','Year'], how='inner')

"""
Running Simulation
"""
df5=pd.DataFrame()
x=[]
for i in range(1000):
    df4=[]
    df3['Visiting Runs'] = df3["Visiting Win %"].apply(lambda x: x*np.random.random_integers(1,100,1) if x else x) 
    df3['Home Runs'] = df3["Home Win %"].apply(lambda x: x*np.random.random_integers(1,100,1) if x else x) 
    df3['Winning Team'] = np.where(df3["Visiting Runs"] > df3["Home Runs"],df3["Visiting Team"], df3["Home Team"]) 
    df4 = df3.groupby(['Winning Team'])['Winning Team'].count().reset_index(name='Wins')
    df4.rename(columns = {"Winnning Team":"Home Team","Winning Team":"Home Team"},inplace=True)
    df1 = pd.merge(df4,df1,on=['Home Team'],how='inner')
    df1[i]=df1["Wins"]
    df1.drop("Wins",inplace=True,axis=1)
    df1['divRank'+str(i)] = df1.groupby("ID")[i].rank(ascending=False)
    df1.loc[df1['divRank'+str(i)]==1,'lgRank'+str(i)]="Playoff"
    df1.loc[df1['divRank'+str(i)]!=1,'lgRank'+str(i)]=df1["lgID"]+"Wild"
    df1['wcRank'+str(i)] = df1.groupby("lgRank"+str(i))[i].rank(ascending=False)
    df1.loc[df1['wcRank'+str(i)]<=2,'Playoff'+str(i)]="Playoff"
    df1.loc[df1['lgRank'+str(i)]=="Playoff",'Playoff'+str(i)]="Playoff"
    df5[i]=df1["Playoff"+str(i)]
    x.append(i+1)
    i = i+1


df5 = df5.count(axis=0).transpose()
df5=df5.apply(lambda x: 1 if x==10 else 0)
y=df5.cumsum()    
plt.plot(x,y/x)
plt.xlabel('Number of Simulations')
plt.ylabel('Percentage')
plt.title('Probability of at least One Tiebreaker Game')
plt.show()

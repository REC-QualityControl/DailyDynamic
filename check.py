import numpy as np
import pandas as pd
import sqlalchemy as sql
import matplotlib.pyplot as plt
import os

def plotcheck(ssid,a,ssName,path,band) :
    ssid=ssid
    c=a.query('SUBSTATION_ID== @ssid')
    tags=c.SOURCE_TAG.unique()
    date=c.DAY.unique()
    for i in date:
      
      path1=os.path.join(path,str(i))
      os.mkdir(path1)
      b=c.query('DAY==@i')
      fc=b[["SUBSTATION_ID","TIMESTAMP","FINAL_POWER_FC","DYN_FC","ATTRIBUTE_2"]].drop_duplicates()
      x1=fc["TIMESTAMP"]
      avc=fc["ATTRIBUTE_2"]


      y1=fc["FINAL_POWER_FC"]
      y2=fc["DYN_FC"]
      y2up=fc["DYN_FC"]+band*fc["ATTRIBUTE_2"]
      y2dn=fc["DYN_FC"]-band*fc["ATTRIBUTE_2"]

      act1=b.query('SOURCE_TAG==@tags[0]')
      y3=fc.merge(act1,left_on="TIMESTAMP",right_on="TIMESTAMP",how="left")["ACT"]
      plt.figure(figsize=(16,8))
    
      plt.title(ssName)
      plt.margins(x=0)
      plt.plot(x1,y1,c="black",label="R-16")
    
      plt.plot(x1,y2,c="blue",label="DYN")
      plt.plot(x1,y2up,c="white",alpha=0.1)
      plt.plot(x1,y2dn,c="white",alpha=0.1)
      plt.fill_between(x1,y2up,y2dn,alpha=0.25)
      plt.plot(x1,avc,c="green",label="AVC")
      plt.plot(x1,y3,c="red",label=tags[0])

      if(len(tags)>1):
       act2=b.query('SOURCE_TAG==@tags[1]')
       y4=fc.merge(act2,left_on="TIMESTAMP",right_on="TIMESTAMP",how="left")["ACT"]
       plt.plot(x1,y4,c="orange",label=tags[1])
    
      if(len(tags)>2):
       act3=b.query('SOURCE_TAG==@tags[2]')
       y5=fc.merge(act3,left_on="TIMESTAMP",right_on="TIMESTAMP",how="left")["ACT"]
       plt.plot(x1,y5,c="pink",label=tags[2])

      plt.legend()
      plt.savefig(f"{path1}/{ssName}.png")
      plt.close()
      plt.clf()
def dbconnect(startdate,enddate,SS_List):
 engine=sql.create_engine("mysql+pymysql://wfsuser:REConnect4321!?@54.69.58.20/RRF_TABLES_TEST")
 query2 = sql.text("""
 SELECT `DATA_FORECAST_SUBSTATION`.`SUBSTATION_ID`,`DATA_FORECAST_SUBSTATION`.`TIMESTAMP`,`DATA_FORECAST_SUBSTATION`.`FINAL_POWER_FC`,`DATA_SCHEDULE_PSS_2024`.`ATTRIBUTE_2`,`DATA_SCHEDULE_PSS_2024`.`ATTRIBUTE_1` AS `DYN_FC`,`DATA_ACTUAL_PSS_PRO_2024`.`ATTRIBUTE_1` AS `ACT`,`DATA_ACTUAL_PSS_PRO_2024`.`SOURCE_TAG`
 FROM `DATA_FORECAST_SUBSTATION`
 LEFT JOIN `DATA_SCHEDULE_PSS_2024` ON `DATA_FORECAST_SUBSTATION`.`SUBSTATION_ID` = `DATA_SCHEDULE_PSS_2024`.`SUBSTATION_ID` AND `DATA_FORECAST_SUBSTATION`.`TIMESTAMP` = `DATA_SCHEDULE_PSS_2024`.`TIMESTAMP`
 LEFT JOIN `DATA_ACTUAL_PSS_PRO_2024` ON `DATA_FORECAST_SUBSTATION`.`SUBSTATION_ID` = `DATA_ACTUAL_PSS_PRO_2024`.`SUBSTATION_ID` AND `DATA_FORECAST_SUBSTATION`.`TIMESTAMP` = `DATA_ACTUAL_PSS_PRO_2024`.`TIMESTAMP`
 WHERE `DATA_FORECAST_SUBSTATION`.`SUBSTATION_ID` IN :SS_List
 AND `DATA_FORECAST_SUBSTATION`.`TIMESTAMP` >=:startdate AND `DATA_FORECAST_SUBSTATION`.`TIMESTAMP` < :enddate
 ORDER BY `DATA_FORECAST_SUBSTATION`.`SUBSTATION_ID`,`DATA_FORECAST_SUBSTATION`.`TIMESTAMP`
 """)

 with engine.connect() as conn:
    res=conn.execute(query2,{'startdate':startdate,'enddate':enddate,'SS_List':SS_List})
    df=pd.DataFrame(res.fetchall(),columns=res.keys())
    df["FINAL_POWER_FC"]=df["FINAL_POWER_FC"].astype(float)
 return df

tag="Daily"
state=""
startdate ='2024-01-17'
enddate ='2024-01-18'
parent="C:/Users/RECONNECT/Documents/Plots"
writer="C:/Users/RECONNECT/Downloads/data.xlsx"
map=pd.read_csv("C:/Users/RECONNECT/Documents/TEST/Check Mapping.csv")

map=map.query('Tag==@tag|STATE_NAME==@state')
SS_List=tuple(map["SUBSTATION_ID"])

a=dbconnect(startdate,enddate,SS_List)

a["DAY"]=pd.to_datetime(a["TIMESTAMP"]).dt.date

with pd.ExcelWriter(writer,datetime_format = "DD-MM-YYYY HH:MM") as writer:
   a.to_excel(writer,sheet_name="Data")

for i in SS_List:
 ssName=map.loc[map['SUBSTATION_ID'] == i, 'SUBSTATION_NAME'].item()
 band=map.loc[map['SUBSTATION_ID'] == i, 'Band'].item()
 path=os.path.join(parent,ssName)
 os.mkdir(path)
 plotcheck(i,a,ssName,path,band)
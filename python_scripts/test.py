import pandas as pd

df=pd.DataFrame([1,2,3,4,None,5],columns=['sno'])
print(df.where(pd.notnull(df),None))


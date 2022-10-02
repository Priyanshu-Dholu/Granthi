import datetime as dt

QUESTIONS = ['q1', 'q2', 'q3']

def percentage(data:dict) -> dict:
    s = sum(data.values())
    return { n:(data[n]/s)*100 for n in data }


'''
today
last 7 days
last 30 days
last 90 days
last 365 days
All time
'''
def get_date(l:str):
    today = dt.datetime.now()
    
    if l == "td":
        return today.date()
    elif l == "l7d":
        d = today - dt.timedelta(days=7)
    elif l == "l30d":
        d = today - dt.timedelta(days=30)
    elif l == "l90d":
        d = today - dt.timedelta(days=90)
    elif l == "l365d":
        d = today - dt.timedelta(days=365)
    
    return d.date() 

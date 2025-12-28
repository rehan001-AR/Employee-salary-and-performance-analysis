import pandas as pd
data = input("paste or write a file name here: ")
a = pd.read_csv(data)

a.columns = a.columns.str.lower().str.strip().str.replace(" ","_")
print(a.columns)

column_map = {
    "name": ["name", "employee_name", "full_name"],
    "salary": ["salary", "pay", "monthly_salary", "ctc"],
    "start_date": ["start_date", "doj", "joining_date"],
    "performance": ["employee_performance", "performance"],
}
def detect_column(df, possible_names):
    for col in df.columns:
        if col in possible_names:
            return col
    return None

name_col = detect_column(a, column_map["name"])
salary_col = detect_column(a, column_map["salary"])
start_col = detect_column(a, column_map["start_date"])
perf_col = detect_column(a, column_map["performance"])

if None in [name_col, salary_col, start_col, perf_col]:
    raise ValueError("Required columns not found in CSV file")
a = a.drop_duplicates(subset =[name_col])



#compares each row and give them rating if condition isn't match then it returns None
def rating_func(s):
    s =str(s).lower()
    if s == "good":
        return 8.5
    elif s == "average":
        return 6.0
    elif s == "high":
        return 9.0
    elif s == "average below":
        return 4.5
    else:
        return None
    
a["rating"] = a[perf_col].apply(rating_func)

#finding experiencea
a[start_col] = pd.to_datetime(
    a[start_col],
    format="%d-%m-%Y",
    errors="coerce"
)

a["Experience"] = (pd.Timestamp.today() - a[start_col]).dt.days // 365


#incrementing salary as per their expereince and rating
a[salary_col] = (
    a[salary_col]
    .astype(str)
    .str.replace(",", "")
)
a[salary_col] = pd.to_numeric(a[salary_col], errors="coerce")
def sal(row):
    org_salary = row[salary_col]
    exp = row["Experience"]
    rating = row["rating"]

    increment = 0

    if exp >= 30 and rating > 8 :
        increment = 15000 
    elif exp >= 30 and rating < 7 :
        increment = 3000
    elif exp >= 20 and rating > 8 :
        increment = 10000  
    elif exp >= 10 and rating > 8 :
        increment = 8000 
    else:
         increment = 1500
    
    return org_salary + increment
a["Updated Salary"] = a.apply(sal, axis=1)

def risk(row):
    rate = row["rating"]
    sal = row[salary_col]


    if rate >8 and sal < 40000:
        return "High Risk"
    elif rate >6 and sal < 35000:
        return "High Risk"
    elif rate < 5 and sal < 40000:
        return "Over Spending"
    else:
        return "normal"
a["Risk"] = a.apply(risk, axis = 1)
print(a)

file_name = input("Choice an file name for your final report: ")
a.to_csv(f"{file_name}.csv", index= False)

print(f"File is saved as {file_name}.csv")




    



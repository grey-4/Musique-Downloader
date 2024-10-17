import csv 
with open('/home/grey/projects/spos/track_info.csv',newline='') as f:
    reader = csv.reader(f)
    data = list(reader)
print(data)
data.pop(1)
print(data)


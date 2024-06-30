import csv
from sklearn.cluster import DBSCAN
import numpy as np
import matplotlib.pyplot as plt

def read_csv_file(filename):
    data = []
    with open(filename, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)
        for row in csv_reader:
            data.append(row)
    return data

filename = 'input_game.csv'
csv_data = read_csv_file(filename)

def distance_metric(a,b):
    return(abs(a-b))

my_dict=dict()

for row in csv_data:

    if row[1] not in my_dict.keys():
        temp = dict()
        my_dict[row[1]] = temp

    temp = my_dict[row[1]]

    if row[2] not in temp.keys():
        list = []
        temp[row[2]]=list

    s=""

    if row[3]=="TRUST":
        s+="1"
    else:
        s+="0"

    if row[4]=="CHEAT":
        s+="0"
    else:
        s+="1"

    temp[row[2]].append(s)

    if row[2] not in my_dict.keys():
        temp1 = dict()
        my_dict[row[2]] = temp1

    temp1 = my_dict[row[2]]

    if row[1] not in temp1.keys():
        list1 = []
        temp1[row[1]]=list1

    s1=""

    if row[4]=="TRUST":
        s1+="1"
    else:
        s1+="0"

    if row[3]=="CHEAT":
        s1+="0"
    else:
        s1+="1"

    temp1[row[1]].append(s1)

# for key in my_dict["3"]:
#     print(key)
#     print(my_dict["3"][key])
#     print("\n")

score_dct = dict()

for key in my_dict:

    p_dict = dict()
    score_dct[key] = p_dict

    for key2 in my_dict[key]:

        lst = my_dict[key][key2]
        sz = len(lst)

        c0=0
        c1=0
        c2=0
        c3=0

        for j in range(sz):

            if (j>5):
                t1 = (c0,c1,c2,c3)
                if t1 not in p_dict:
                    val = lst[j]
                    if val=="11" or val=="10":
                        p_dict[t1]=1
                    else:
                        p_dict[t1]=-1
                else:
                    val = lst[j]
                    if val=="11" or val=="10":
                        p_dict[t1]+=1
                    else:
                        p_dict[t1]-=1 

            if lst[j]=="00":
                c0+=1
            elif lst[j]=="01":
                c1+=1
            elif lst[j]=="10":
                c2+=1
            else:
                c3+=1

score = dict()

for key in score_dct:

    tect = score_dct[key]
    value=0

    for key2 in tect:

        x1=key2[0]
        x2=key2[1]
        x3=key2[2]
        x4=key2[3]
        t = x1+x2+x3+x4
        value+=((tect[key2])*((1+x1)/(80+t))*((1+x2)/(80+t))*((1+x3)/(80+t))*((1+x4)/(80+t)))
    
    value*=1000
    new_val = round(value,4)
    new_key = int(key)
    score[new_key] = new_val


sorted_dict = {key: score[key] for key in sorted(score)}
sorted_dict_val = dict(sorted(score.items(), key=lambda item: item[1]))

val_lst = []

for key in sorted_dict_val:
    # print(key,sorted_dict_val[key])
    val_lst.append(sorted_dict_val[key])

start = 0.00001
stop = 2
num_points = 100
x = np.linspace(start, stop, num_points)
y = []

X = np.array(val_lst)
X1 = X.reshape(-1, 1)

for i in range(len(x)):
    eps = x[i]
    min_samples = 1
    dbscan = DBSCAN(eps=eps, min_samples=min_samples)
    dbscan.fit(X1)
    labels = dbscan.labels_
    y.append(labels[-1]+1)

plt.figure(figsize=(8, 6))
plt.plot(x, y, marker='o', linestyle='-', color='b', label='Data Points')
plt.title('2D Graph with Data from Two 1D Arrays')
plt.xlabel('X-axis Label')
plt.ylabel('Y-axis Label')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
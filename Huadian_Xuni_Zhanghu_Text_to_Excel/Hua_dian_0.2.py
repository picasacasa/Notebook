# coding: utf-8

from datetime import datetime
start_time = datetime.now()
import pandas as pd

def get_title_dict(text):
    # f1 = f0.read().replace('\n','').strip( )
    f = ' '.join(text.split()).split()
    F = []
    for i in f:
        F.append(i.split('：'))
    for i in range(len(F)-1,-1,-1):
        if len(F[i]) < 2:
            del F[i]
    fdict = dict(F)
    return fdict

f0 = open('02905_0','r')

# 清除文本中的空格等，按换行符切分list
f1 = f0.read().replace('\n  主账户：','  主账户：').replace('\n  虚拟账号：','  虚拟账号：').replace('\n  开户行机构号','  开户行机构号').split('\n')

# 保留页眉中虚拟账号、账户名称，其余删除
for i in range(len(f1)-1,-1,-1):
    if '虚拟账户交易报告单' in f1[i]:
        f1[i] = get_title_dict(f1[i])
        pass
    elif '│序号│' in f1[i]:
        del f1[i]
    elif '│' in f1[i]:
        f1[i] = f1[i].replace(' ','').split('│')
        pass
    else:
        del f1[i]

# 处理两行冗余文本到数据行
for i in range(len(f1)-1,-1,-1):
    # if f1.count(f1[i]) > 1:
    #     del f1[i]
    if type(f1[i]) == dict:
        if f1.count(f1[i]) > 1:
            del f1[i]
        else:
            pass
    else:
        pass

for i in range(len(f1)-1,-1,-1):
    if type(f1[i]) != dict and f1[i][1] == '' and f1[i-1][1] != '':
        f1[i-1][5] = f1[i-1][5] + f1[i][5]
        f1[i-1][6] = f1[i-1][6] + f1[i][6]
        f1[i-1][7] = f1[i-1][7] + f1[i][7]
        f1[i-1][8] = f1[i-1][8] + f1[i][8]
        f1[i-1][9] = f1[i-1][9] + f1[i][9]
        del f1[i]
    else:
        pass

# 切分账簿
data = []
name = []
count = -1
for i in range(0,len(f1)):
    if type(f1[i]) == dict:
        count += 1
        data.append([])
        name.append([])
        name[count].append(f1[i])
    else:
        data[count].append(f1[i][2:12])

# 账号名称、数据到DATA，便于导出
DATA = [name, data]

# 将数据导入DataFrame,DATA[0]为name，DATA[1]为data
counts = -1
DATAT = []
for i in range(0,len(DATA[1])):
    counts += 1
    DATAT.append([])
    DATAT[counts] = pd.DataFrame(DATA[1][counts],columns=["类型","记录日","记账日","凭证号码/业务编号","交易流水号","摘要","对方账号","对方户名","借方发生额","贷方发生额"])

for i in range(0,len(DATA[0])):
    DATAT[i].to_excel(DATA[0][i][0]['虚拟账号'] + '_' + DATA[0][i][0]['账户名称'] + '_期初余额' + DATA[0][i][0]['期初余额'] + '_期末余额' + DATA[0][i][0]['期末余额'] + '.xlsx', sheet_name = DATA[0][i][0]['虚拟账号'] + '_' + DATA[0][i][0]['账户名称'])


end_time = datetime.now()
print('\n' + 'USED ' + str((end_time - start_time).seconds) + ' seconds!')
print('\n' + str(datetime.now()))

# coding: utf-8

from datetime import datetime
start_time = datetime.now()
import pandas as pd

f0 = open('/home/wangshi/下载/029051','r')

# 清除文本中的空格等，按换行符切分list
f1 = f0.read().strip().replace(' ','').split('\n')

# 保留页眉中虚拟账号、账户名称，其余删除
# 期初余额、期末余额待解决
for i in range(len(f1)-1,-1,-1):
    if '虚拟账号' in f1[i]:
        pass
    elif '│序号│' in f1[i]:
        del f1[i]
    elif '│' in f1[i]:
        pass
    else:
        del f1[i]

# 处理保留的页眉，将数据按符号'│'切分list
for i in range(len(f1)-1,-1,-1):
    if '│' not in f1[i]:
        f1[i] = f1[i].replace('虚拟账号：','账簿#').replace('账户名称：','#').replace('期末余额：','#').split('#')[0:3]
    else:
        f1[i] = str(f1[i]).split('│')

# 处理两行冗余文本到数据行
for i in range(len(f1)-1,-1,-1):
    if f1.count(f1[i]) > 1:
        del f1[i]
    elif f1[i][1] == '' and f1[i-1][1] != '':
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
    if f1[i][0] == '账簿':
        count += 1
        data.append([])
        name.append([])
        name[count].append(f1[i][1])
        name[count].append(f1[i][2])
    else:
        data[count].append(f1[i][1:12])
    

# 账号名称、数据到DATA，便于导出
DATA = [name, data]

# 将数据导入DataFrame,DATA[0]为name，DATA[1]为data
counts = -1
DATAT = []
for i in range(0,len(DATA[1])):
    counts += 1
    DATAT.append([])
    DATAT[counts] = pd.DataFrame(DATA[1][counts],columns=["序号","类型","记录日","记账日","凭证号码/业务编号","交易流水号","摘要","对方账号","对方户名","借方发生额","贷方发生额"])
    
for i in range(0,len(DATA[0])):
    DATAT[i].to_excel(DATA[0][i][0] + '_' + DATA[0][i][1] + '.xlsx', sheet_name = DATA[0][i][1])

end_time = datetime.now()
print('\n' + 'USED ' + str((end_time - start_time).seconds) + ' seconds!')
print('\n' + str(datetime.now()))

# coding: utf-8
import pandas as pd

def get_float(text):
    floats = float(text.replace(',',''))
    return floats

def get_title_dict(listin):
    list0 = []
    list0.append([listin[0],listin[1]])
    list0.append([listin[2],listin[3]])
    list0.append([listin[4],listin[5]])
    list0.append([listin[6],listin[7]])
    fdict = dict(list0)
    return fdict

del_list = [' Account N',
 ' Currency ',
 ' ─────────',
 ' |序号|记账日|起',
 ' |No. |Bk.',
 '   借方合计   ',
 '  Debit To',
 ' 1. 余额前面标注',
 ' 我行，否则将视同此',
 ' ipt, othe']

f0 = open('/home/wangshi/下载/1601','r')
# 清除文本中的空格等，按换行符切分list             
f1 = f0.read().replace('1  账号','  账号').replace('币种','币种').replace('账户类型','账户类型').replace('账户名称','账户名称').split('\n')

for i in range(len(f1)-1,-1,-1):
    if f1[i][:10] in del_list:
        del f1[i]
    else:
        pass

for i in range(len(f1)-1,-1,-1):
    if ('币种' in f1[i] and '账户类型' in f1[i]) and ('账号' in f1[i-1] and '账户名称' in f1[i-1]):
        f1[i] = get_title_dict((f1[i-1][:60] + f1[i][:60]).split())
        del f1[i-1]
    elif '|' in f1[i]:
        f1[i] = f1[i].replace(' ','').split('|')
    elif f1[i] == '':
        del f1[i]
    else:
        pass

# 处理两行冗余文本到数据行
for i in range(len(f1)-1,-1,-1):
    if type(f1[i]) == dict:
        if f1.count(f1[i]) > 1:
            del f1[i]
        else:
            pass
    else:
        f1[i][7] = f1[i][7].replace(',','')
        f1[i][8] = f1[i][8].replace(',','')
        f1[i][9] = f1[i][9].replace(',','')

for i in range(len(f1)-1,-1,-1):
    if type(f1[i]) != dict and f1[i][1] == '' and f1[i-1][1] != '':
        f1[i-1][6] = f1[i-1][6] + f1[i][6]
        f1[i-1][11] = f1[i-1][7] + f1[i][11]
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
    DATAT[counts] = pd.DataFrame(DATA[1][counts],columns=["记账日","起息日","交易类型","凭证","凭证号码/业务编号/用途/摘要","借方发生额","贷方发生额","余额","机构/柜员/流水","备注"])   
    DATAT[counts]["借方发生额"] = pd.to_numeric(DATAT[counts]["借方发生额"])
    DATAT[counts]["贷方发生额"] = pd.to_numeric(DATAT[counts]["贷方发生额"])
    DATAT[counts]["余额"] = pd.to_numeric(DATAT[counts]["余额"])

for i in range(0,len(DATA[0])):
    DATAT[i].to_excel(DATA[0][i][0]['账户名称'] + '_' + DATA[0][i][0]['账号'] + DATA[0][i][0]['币种'] + DATA[0][i][0]['账户类型'] + '.xlsx', sheet_name = DATA[0][i][0]['账号'] + '_' + DATA[0][i][0]['账户名称'])


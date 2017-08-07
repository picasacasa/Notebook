# coding: utf-8
from datetime import datetime
start_time = datetime.now()
import pandas as pd
import hashlib
# 借用 Celend 的 bencode ，https://github.com/Celend/bencode.py
import bencode

# 定义去除千分位逗号的函数
def get_float(text):
    floats = float(text.replace(',',''))
    return floats

# 定义生成标题词典的函数，待优化
def get_title_dict(listin):
    list0 = []
    list0.append([listin[0],listin[1]])
    list0.append([listin[2],listin[3]])
    list0.append([listin[4],listin[5]])
    list0.append([listin[6],listin[7]])
    fdict = dict(list0)
    return fdict

# 定义删除行，待优化
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

f0 = open('/home/wangshi/下载/temp1/data','r')

# 清除文本中的空格等，按换行符切分list             
f1 = f0.read().replace('1  账号','  账号').split('\n')

# 按 del_list 删除冗余行
for i in range(len(f1)-1,-1,-1):
    if f1[i][:10] in del_list:
        del f1[i]
    else:
        pass

# 处理标题行，数据行分列
for i in range(len(f1)-1,-1,-1):
    if ('币种' in f1[i] and '账户类型' in f1[i]) and ('账号' in f1[i-1] and '账户名称' in f1[i-1]):
        f1[i] = get_title_dict((f1[i-1][:60] + f1[i][:60]).split())
        del f1[i-1]
    elif '|' in f1[i]:
        f1[i] = f1[i].replace(' ','').split('|')
    # 删除空行
    elif f1[i] == '':
        del f1[i]
    else:
        pass

# 处理千分位分隔符
for i in range(len(f1)-1,-1,-1):
    if type(f1[i]) == dict:
        pass
    else:
        f1[i][7] = f1[i][7].replace(',','')
        f1[i][8] = f1[i][8].replace(',','')
        f1[i][9] = f1[i][9].replace(',','')

# 处理两行文本到一行
for i in range(len(f1)-1,-1,-1):
    if type(f1[i]) != dict and f1[i][1] == '' and f1[i-1][1] != '':
        f1[i-1][6] = f1[i-1][6] + f1[i][6]
        f1[i-1][11] = f1[i-1][11] + f1[i][11]
        del f1[i]
    else:
        pass

# 切分并按账户分类汇总
data = []
name = []
md5_pool = []
posi = 0
for i in range(0,len(f1)):
    # get positions
    if type(f1[i]) == dict:
        md5_value = hashlib.md5(bencode.encode(f1[i])).hexdigest()
        if md5_value in md5_pool:
            posi = md5_pool.index(md5_value)
            
        else:
            data.append([])
            name.append(f1[i])
            md5_pool.append(md5_value)
            posi = md5_pool.index(md5_value)
    else:
        data[posi].append(f1[i][2:12])

# 将数据导入 DataFrame 格式的 DATA
counts = -1
DATA = []
for i in range(0,len(data)):
    counts += 1
    DATA.append([])
    DATA[counts] = pd.DataFrame(data[counts],columns=["记账日","起息日","交易类型","凭证","凭证号码/业务编号/用途/摘要","借方发生额","贷方发生额","余额","机构/柜员/流水","备注"])   
    DATA[counts]["借方发生额"] = pd.to_numeric(DATA[counts]["借方发生额"])
    DATA[counts]["贷方发生额"] = pd.to_numeric(DATA[counts]["贷方发生额"])
    DATA[counts]["余额"] = pd.to_numeric(DATA[counts]["余额"])

# 导出到 Excel
for i in range(0,len(name)):
    DATA[i].to_excel(name[i]['账户名称'] + '_' + name[i]['账号'] + name[i]['币种'] + name[i]['账户类型'] + '.xlsx', sheet_name = name[i]['账号'] + '_' + name[i]['账户名称'])

end_time = datetime.now()
print('\n' + 'USED ' + str((end_time - start_time).seconds) + ' seconds!')
print('\n' + str(datetime.now()))



# -*- coding: UTF-8 -*-
import os,exifread,random

path_picture = '/media/nasb/Pictures/'
# path_picture = '/home/tai/下载/'

def get_exif_date(location):
#import exifread
    try:
        f = open(location,'rb')
        tabs = exifread.process_file(f) #用exifread读取文件中exif信息
        f.close()
        return tabs['EXIF DateTimeOriginal'].printable.replace(':', '-') + ' ' + str(random.randint(1000,9999)) #获取拍摄时间信息，添加随机数
    except:
        pass

# 处理年份69以下以20开头，70以上以19开头
def get_century(name_date):
    if float(name_date[0:2]) <= 69:
        century = '20'
    elif float(name_date[0:2]) >= 70:
        century = '19'
    return century

Photos_path = '/----/----/----/----/----/----/Photos/'
# Photos_path = '/home/tai/下载/Photos/'

# os.walk()
for paths,dirs,files in os.walk(path_picture):
    if len(files) > 0:
        for i in files:
            try:
                # name_date 通过[2:]过滤了'19','20'
                name_date = get_exif_date(paths + '/' + i)[2:] # 获取文件exif中拍摄时间
                name_new = name_date + '.' + i.split('.')[-1] # 生成新文件名
                path_new = Photos_path + get_century(name_date) + name_date[0:2] + '/' + name_date[3:5] + '/' # 按拍摄日期添加年份/月份的文件夹
                # 如文件夹存在则移动文件，不存在则先生成文件夹
                if os.path.exists(path_new):
                    os.system('mv "' + paths + '/' + i + '" "' + path_new + name_new + '"')
                else:
                    os.makedirs(path_new)
                    os.system('mv "' + paths + '/' + i + '" "' + path_new + name_new + '"')
                # 打印移动文件信息
                print 'mv "' + paths + '/' + i + '" "' + path_new + name_new + '"'
                
            except:
                pass
    else:
        pass

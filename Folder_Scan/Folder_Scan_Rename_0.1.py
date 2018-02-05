# -*- coding: UTF-8 -*-
import os,exifread,random

path_picture = '/media/nasb/Pictures/'
# path_picture = '/home/tai/下载/'

def get_exif_date(location):
#import exifread
    try:
        f = open(location,'rb')
        tabs = exifread.process_file(f)
        f.close()
        return tabs['EXIF DateTimeOriginal'].printable.replace(':', '-') + ' ' + str(random.randint(1000,9999))
    except:
        pass


def get_century(name_date):
    if float(name_date[0:2]) <= 69:
        century = '20'
    elif float(name_date[0:2]) >= 70:
        century = '19'
    return century

Photos_path = '/media/nasb/nextcloud/data/olympus/files/Photos/'
# Photos_path = '/home/tai/下载/Photos/'

# os.walk()
for paths,dirs,files in os.walk(path_picture):
    if len(files) > 0:
        for i in files:
            try:
                # name_date 通过[2:]过滤了'19','20'
                name_date = get_exif_date(paths + '/' + i)[2:]
                name_new = name_date + '.' + i.split('.')[-1]
                path_new = Photos_path + get_century(name_date) + name_date[0:2] + '/' + name_date[3:5] + '/'
                if os.path.exists(path_new):
                    os.system('mv "' + paths + '/' + i + '" "' + path_new + name_new + '"')
                else:
                    os.makedirs(path_new)
                    os.system('mv "' + paths + '/' + i + '" "' + path_new + name_new + '"')
                print 'mv "' + paths + '/' + i + '" "' + path_new + name_new + '"'
                
            except:
                pass
    else:
        pass

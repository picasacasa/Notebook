import smtplib  
from email.mime.text import MIMEText  
mail_host = "smtp.sina.com"  #设置服务器
mail_user = "********@sina.cn"    #用户名
mail_pass = "********"   #口令 


content = 'ip had chane'
  
def sendmail(sub,content,recevier = 'autolympus@139.com'):  
    me = mail_user
    msg = MIMEText(content,_subtype = 'plain',_charset = 'gb2312')  
    msg['Subject'] = sub  
    msg['From'] = me  
    msg['To'] = recevier
    try:  
        server = smtplib.SMTP()  
        server.connect(mail_host)  
        server.login(mail_user,mail_pass)  
        server.sendmail(me, recevier, msg.as_string())  
        server.close()  
        print ("邮件发送成功")
    except Exception as e:  
        print ("邮件发送失败" + "/n" + str(e))


# #!/usr/bin/python
# # -*- coding: UTF-8 -*-
#
#
#
# mail_host = "smtp.qq.com"
# mail_user = "xxxxxxxxx@qq.com"
# mail_pass = "passwprd"
#
# import smtplib,string,random
# from email.mime.text import MIMEText
# from email.header import Header
#
# def rand_code(number):
#     source = list(string.ascii_letters)
#     for index in range(0,10):
#         source.append(str(index))
#     return ''.join(random.sample(source,number))
# def sent_mail():
#     sender = '375479098@qq.com'
#     receivers = ['shushin_kou@sina.com']
#     x = rand_code(10)
#     y = rand_code(10)
#     message = MIMEText('OK,There are your IDVerify code!<B>'+x+'</B><br>Click it you will transform to Change password', 'html', 'utf-8')
#     message['From'] = Header("SEMC", 'utf-8')
#     message['To'] = Header("Change-password", 'utf-8')
#
#     subject = 'Change password By SEMC '
#     message['Subject'] = Header(subject, 'utf-8')
#
#     smtpObj = smtplib.SMTP_SSL(mail_host, 465)
#     smtpObj.login(mail_user, mail_pass)
#     smtpObj.sendmail(sender, receivers, message.as_string())
#     smtpObj.quit()
#     print("ok")
#     return x
#
# sent_mail()
import smtplib

def Send_Mail (user_mail,msg):

    User_mailID = user_mail
    
    s = smtplib.SMTP('smtp.gmail.com', 587)
    
    s.starttls()

    s.login("eps29623@gmail.com", "brasdechdmbktefl")
    
    message= msg
    
    s.sendmail("eps29623@gmail.com", User_mailID , message)
    
    s.quit()   

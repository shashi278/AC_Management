import smtplib
from email.message import EmailMessage
import random

class BaseMail(object):

    def login(self, email, password):
        try:
            self.s=smtplib.SMTP('smtp.gmail.com', 587)
            self.s.starttls()
            self.s.login(email,password)
            return True
        except:
            return False

#class to send notification
class NotificationMail(BaseMail):
    pass


#class to send otp for password reset
class OTPMail(BaseMail):
    otp_content="""
        Your OTP to reset password for AMS IIIT Kalyani is {}.
        The OTP is valid only for this session.

        This is a system generated email. Kindly do not reply. 
        """

    def send_otp(self, to):
        otp= random.randint(000000,999999)
        msg= EmailMessage()

        msg['Subject']= 'Reset Password: AMS IIIT Kalyani'
        msg['From'] = 'notification@iiitkalyani.ac.in'
        msg['To'] = to
        try:
            msg.set_content(self.otp_content.format(otp))
            self.s.send_message(msg)
            return otp
        except Exception as e:
            print(e)
            return None

if __name__=="__main__":
    x=OTPMail()
    if x.login('shashir@iiitkalyani.ac.in','Shashi@1531'):
        otp= x.send_otp("anandnet628@gmail.com")
        print("OTP: ",otp)
    else:
        print("Network Error")
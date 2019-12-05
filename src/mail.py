import smtplib
from email.message import EmailMessage
import random

# from kivy.clock import Clock
from functools import partial
from _thread import *
import asyncio
from multiprocessing.pool import ThreadPool

pool = ThreadPool(processes=1)


class BaseMail(object):
    def login(self, email, password):
        try:
            self.s = smtplib.SMTP("smtp.gmail.com", 587)
            self.s.starttls()
            self.s.login(email, password)
            return True
        except:
            return False


# class to send notification
class NotificationMail(BaseMail):
    pass


# class to send otp for password reset
class OTPMail(BaseMail):
    otp_content = """
        Your OTP to reset password for AMS IIIT Kalyani is {}.
        The OTP is valid only for this session.

        This is a system generated email. Kindly do not reply. 
        """

    def send_otp(self, to, *args):
        otp = random.randint(000000, 999999)
        msg = EmailMessage()

        msg["Subject"] = "Reset Password: AMS IIIT Kalyani"
        msg["From"] = "shashir@iiitkalyani.ac.in"
        msg["To"] = to
        try:
            msg.set_content(self.otp_content.format(otp))
            self.s.send_message(msg)
            return otp
        except Exception as e:
            #print(e)
            return None


if __name__ == "__main__":
    import time

    x = OTPMail()
    stat = pool.apply_async(x.login, ("shashir@iiitkalyani.ac.in", "Shashi@1531"))
    stat = stat.get()
    if stat:
        otp = pool.apply_async(x.send_otp, ("anandnet628@gmail.com",))
        otp = otp.get()
        #print("OTP: here: ", otp)
        # while True:
        while True:
            time.sleep(1)
    else:
        #print("Network Error")
        pass

from os import error
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from core.config import Config


class Email:
    __self = None

    def __new__(cls):
        if not cls.__self:
            cls.__self = super(Email, cls).__new__(cls)
            cls.__self.__server = smtplib.SMTP(
                Config().email_host, Config().email_port)
            cls.login()
        return cls.__self

    def __init__(self) -> None:
        pass

    @classmethod
    def login(cls):
        print("{}:{}".format(Config().email_host, Config().email_port))
        cls.__self.__server.set_debuglevel(1)
        cls.__self.__server.ehlo()
        cls.__self.__server.login(
            Config().email_sender, Config().email_password)

    @classmethod
    def send_email(cls, subject: str, text: str):
        mm = MIMEMultipart("related")
        mm["From"] = "交易软件<{}>".format(Config().email_sender)
        parse_receivers = ["<{}>".format(r) for r in Config().email_receivers]
        receivers = ""
        for receiver in parse_receivers[:len(parse_receivers) - 1]:
            receivers += receiver + ","
        receivers += parse_receivers[len(parse_receivers) - 1]
        mm["To"] = receivers
        mm["Subject"] = Header(subject, "utf-8")

        mail_text = MIMEText(text, "plain", "utf-8")
        mm.attach(mail_text)

        try:
            cls.__self.__server.sendmail(
                Config().email_sender, Config().email_receivers, mm.as_string())
        except:
            cls.__self.__server.quit()
            cls.login()
            try:
                cls.__self.__server.sendmail(
                    Config().email_sender, Config().email_receivers, mm.as_string())
            except:
                raise error("邮件发送失败：主题 {}".format(subject))

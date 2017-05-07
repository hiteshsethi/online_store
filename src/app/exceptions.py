import json
import traceback


class BaseException(Exception):
    INTERNAL_SERVER_ERROR = 500

    def __init__(self, msg, code=None, log=True, is_send_mail=False, extra_info={}):
        if type(msg) is not type(''):
            msg = str(msg)
        if not code:
            code = self.INTERNAL_SERVER_ERROR
        self.message = msg
        self.msg = self.message
        self.code = code
        self.is_log = log
        self.is_send_mail = is_send_mail
        self.extra_info = extra_info
        self.log_exception()
        self.send_exception_mail()

    def get_code(self):
        return self.code

    def get_message(self):
        return self.message

    def get_is_log(self):
        return self.is_log

    def get_is_send_mail(self):
        return self.is_send_mail

    def get_exception_name(self):
        return self.__class__.__name__

    def __str__(self):
        return json.dumps({
            'is_log': self.is_log,
            'is_send_mail': self.is_send_mail,
            'code': self.code,
            'msg': self.message
        })

    def log_exception(self):
        from src.app import app
        if self.is_log is True:
            message = "Message: %s Code: %s Traceback: %s ExtraInfo %s" % (
                self.message, self.code, traceback.format_list(traceback.extract_stack(limit=5)), self.extra_info)
            app.logger.error(message)

    def send_exception_mail(self):
        if self.is_send_mail is True:
            body = "Message: %s Code: %s Traceback: %s ExtraInfo %s" % (
                self.message, self.code, traceback.format_list(traceback.extract_stack(limit=5)), self.extra_info)
            subject = self.get_exception_name()
            if len(self.extra_info):
                subject += str(self.extra_info)
                # send_email(subject, body) lets not do it for the sake of simplicity


class DataException(BaseException):
    IMPROPER_DATA_ERROR = 1001
    INVALID_RESOURCE_REQUESTED = 1002
    INVALID_DATA_MANIPULATION = 1003

    def __init__(self, msg, code=None, log=True, is_send_mail=False, extra_info={}):  # real signature unknown
        super(DataException, self).__init__(msg, code, log, is_send_mail, extra_info)

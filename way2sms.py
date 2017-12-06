import requests


class way2sms_login:

    def __init__(self, username, password):
        """ It will take the username and password as parameter to login to way2sms account.
        It will try to login.
        :param username: class <int>
        :param password: class <str>
        """
        self.url = 'http://site24.way2sms.com/Login1.action?'
        self.credentials = {'username': username, 'password': password}
        self.session = requests.Session()

        self.q = self.session.post(self.url, data=self.credentials)
        self.loggedIn = False
        if self.q.status_code != 200:
            self.loggedIn = False
        else:
            self.loggedIn = True

        self.jsid = self.session.cookies.get_dict()['JSESSIONID'][4:]

    def way2sms_send(self, mobile, message):
        """
        It will take two parameters receivers mobile number and the message to be send.
        Both parameters should be of class str.
        Your message length should be less than 139 characters.
        :param mobile: class <str>
        :param message: class <str>
        :return: True or False
        """
        if len(message) > 139 or len(mobile) != 10 or not mobile.isdecimal():
            return False

        self.payload = {'ssaction': 'ss',
                        'Token': self.jsid,
                        'mobile': mobile,
                        'message': message,
                        'msgLen': '129'
                        }
        self.msg_url = 'http://site24.way2sms.com/smstoss.action'
        self.q = self.session.post(self.msg_url, data=self.payload)
        if self.q.status_code == 200:
            return True
        else:
            return False

    def way2sms_logout(self):
        """
        It will logout current logged in user from the way2sms.
        """
        self.session.get('http://site24.way2sms.com/entry?ec=0080&id=dwks')
        self.session.close()
        self.loggedIn = False

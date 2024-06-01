# -*- coding: utf-8 -*-
__author__ = 'Lucas Barros'
__version__ = 1.0
__maintainer__ = 'Lucas Barros'
__email__ = 'lucasbarros2000@hotmail.com'
__status__ = 'Production'


import os
import requests
from lbLogger.LbLogger import LbLogger
from requests.auth import HTTPBasicAuth
from typing import Any
from typing import List
from typing import Union


class LbMail:

    def __init__(self):
        self.__lb_logger: LbLogger = LbLogger()

        self.__from_email: str = self.check_and_read_environment_variables(variable="from_email_mail_gun")
        self.__url_mail_gun: str = self.check_and_read_environment_variables(variable="url_mail_gun")
        self.__token_mail_gun: str = self.check_and_read_environment_variables(variable="token_mail_gun")

    def send(self, subject: str, html: str, to_email: Union[List[str], str]) -> requests.Response:
        """
        Function for send email with html body
        :param subject: Subject for email sender
        :param html: HTML for send body
        :param to_email: To email(s) for send mail
        :return: Response status email sent
        """

        bodyEmail = dict()
        if isinstance(to_email, str):
            bodyEmail: dict = {"to": to_email, "from": self.__from_email, "subject": subject, "html": html}
        elif isinstance(to_email, list):
            bodyEmail: dict = {"to": to_email[0], "from": self.__from_email, "subject": subject, "html": html}
            if len(to_email) > 1:
                bodyEmail['cc'] = ','.join([str(y) for y in to_email[1:]])

        return requests.post(self.__url_mail_gun,
                             auth=HTTPBasicAuth("api", self.__token_mail_gun),
                             data=bodyEmail)

    def check_and_read_environment_variables(self, variable: Any) -> Any:
        """
        Function for check and read environment variable
        :param variable: Variable for check
        :return: Environment variable
        """

        self.__lb_logger.info(message=f"Checking variable {variable}")

        environment_variable: Any = os.environ.get(variable, None)

        if environment_variable is None:
            raise EnvironmentError(f"Environment variable {variable} is required")

        return environment_variable

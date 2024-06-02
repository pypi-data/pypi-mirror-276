# -*- coding: utf-8 -*-
__author__ = 'Lucas Barros'
__version__ = 1.0
__maintainer__ = 'Lucas Barros'
__email__ = 'lucasbarros2000@hotmail.com'
__status__ = 'Production'

import time
import jwt
import os
from datetime import datetime
from datetime import timedelta
from flask import request, abort
from functools import wraps
from lbLogger.LbLogger import LbLogger
from lbUser.LbUser import LbUser
from tokenValidator.Messages import Messages
from typing import Dict


lb_logger: LbLogger = LbLogger()


class TokenValidator:

    def check_login_token(self):
        @wraps(self)
        def decorated(*args, **kwargs) -> dict:
            """
            Function To Interceptor Request And Validator Token
            :param args: Args Parameters
            :param kwargs: Kwargs Parameters
            :return: Token Information
            """
            token = request.headers.get("token")
            if not token:
                lb_logger.error(f"{Messages.TOKEN_IS_REQUIRED}")
                return abort(status=401, description=Messages.TOKEN_IS_REQUIRED)

            if token != os.environ.get("token", None):
                lb_logger.error(f"{Messages.TOKEN_IS_INVALID}")
                return abort(status=401, description=Messages.TOKEN_IS_INVALID)

            return self(*args, **kwargs)
        return decorated

    @staticmethod
    def create_token(user: LbUser):
        """

        :return:
        """
        payload = {
            "mongo_id": str(user.id),
            "name": user.name,
            "email": user.email,
            "username": user.username,
            "permissions": user.permissions,
            "expiration": (datetime.utcnow() + timedelta(hours=8)).timestamp() * 1000
        }
        return jwt.encode(payload, os.environ.get("secret_key"), algorithm='HS256')

    def token_required(self):
        @wraps(self)
        def decorated(*args, **kwargs):
            token = None
            if 'Authorization' in request.headers:
                token = request.headers['Authorization'].split(" ")[1]
            if not token:
                return abort(status=400, description=Messages.TOKEN_IS_REQUIRED)

            try:
                data: Dict = jwt.decode(token, os.environ.get("secret_key"), algorithms=["HS256"])

                if data.get("expiration", None) is None or data.get("expiration") < int(time.time() * 1000):
                    return abort(status=401, description=Messages.TOKEN_IS_EXPIRED)

            except jwt.InvalidTokenError:
                return abort(status=401, description=Messages.TOKEN_IS_INVALID)

            return self(data.get("username"), *args, **kwargs)

        return decorated

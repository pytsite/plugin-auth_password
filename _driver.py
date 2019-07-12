"""PytSite Password Authentication Driver
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import logger
from plugins import auth


class Password(auth.driver.Authentication):
    """Password Authentication Driver
    """

    def get_name(self) -> str:
        """Get name of the driver
        """
        return 'password'

    def get_description(self) -> str:
        """Get name of the driver
        """
        return 'Password'

    def sign_up(self, data: dict) -> auth.model.AbstractUser:
        """Sign up a new user
        """
        # Create user
        try:
            auth.switch_user_to_system()
            user = auth.create_user(data.get('login'), data.get('password'))

            # Fill additional fields
            for k, v in data.items():
                if k not in ('email', 'first_name', 'last_name', 'nickname') or not v:
                    continue
                user.set_field(k, v)

            # Set nickname
            if 'nickname' not in data:
                user.nickname = user.first_last_name

            user.save()

        finally:
            auth.restore_user()

        return user

    def sign_in(self, data: dict) -> auth.model.AbstractUser:
        """Authenticate user
        """
        login = data.get('login')
        password = data.get('password')

        if not (login and password):
            raise auth.error.AuthenticationError('Login or password is not specified')

        # Check if the user exists
        user = auth.get_user(login)
        if not user:
            logger.warn("User with login '{}' is not found".format(login))
            raise auth.error.AuthenticationError()

        # Check password
        if not auth.verify_password(password, user.password):
            logger.warn("Incorrect password provided for user with login '{}'".format(login))
            raise auth.error.AuthenticationError()

        return user

    def sign_out(self, user: auth.model.AbstractUser):
        """Sign out user
        """
        pass

"""PytSite Password Authentication Driver
"""
from pytsite import lang as _lang, logger as _logger
from plugins import auth as _auth

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Password(_auth.driver.Authentication):
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

    def sign_up(self, data: dict) -> _auth.model.AbstractUser:
        """Sign up a new user
        """
        # Create user
        _auth.switch_user_to_system()
        user = _auth.create_user(data.get('login'), data.get('password'))
        _auth.restore_user()

        # Fill additional fields
        for k, v in data.items():
            if k not in ('email', 'first_name', 'last_name', 'nickname') or not v:
                continue
            user.set_field(k, v)

        _auth.switch_user_to_system()
        user.save()
        _auth.restore_user()

        return user

    def sign_in(self, data: dict) -> _auth.model.AbstractUser:
        """Authenticate user
        """
        login = data.get('login')
        password = data.get('password')

        if not (login and password):
            raise _auth.error.AuthenticationError('Login or password is not specified')

        # Check if the user exists
        user = _auth.get_user(login)
        if not user:
            _logger.warn("User with login '{}' is not found".format(login))
            raise _auth.error.AuthenticationError()

        # Check password
        if not _auth.verify_password(password, user.password):
            _logger.warn("Incorrect password provided for user with login '{}'".format(login))
            raise _auth.error.AuthenticationError()

        return user

    def sign_out(self, user: _auth.model.AbstractUser):
        """Sign out user
        """
        pass

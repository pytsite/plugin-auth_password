"""PytSite Password Authentication Driver Plugin
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def plugin_load():
    from plugins import auth
    from . import _driver

    auth.register_auth_driver(_driver.Password())

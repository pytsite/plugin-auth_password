"""PytSite Auth Password Plugin Tests
"""
from typing import List
from pytsite import testing
from plugins import auth, http_api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class TestHttpApi(testing.TestCase):
    def setUp(self):
        """Setup
        """
        self.users = []  # type: List[auth.model.AbstractUser]
        auth.switch_user_to_system()

        # Create test users
        for i in range(3):
            user = auth.create_user('test_user_{}@test.com'.format(i), 'test_user_{}_password'.format(i))
            user.save()

            self.users.append(user)

        auth.restore_user()

    def tearDown(self):
        """Tear down
        """
        auth.switch_user_to_system()

        # Delete created test users
        for user in self.users:
            user.delete()

        self.users = []

        auth.restore_user()

    def test_post_access_token(self):
        for i in range(3):
            url = http_api.url('auth@post_access_token', {'driver': 'password'})
            resp = self.send_http_request(self.prepare_http_request('POST', url, data={
                'login': 'test_user_{}@test.com'.format(i),
                'password': 'test_user_{}_password'.format(i),
            }))

            self.assertHttpRespCodeEquals(resp, 200)
            self.assertHttpRespJsonFieldIsDateTime(resp, 'created')
            self.assertHttpRespJsonFieldIsDateTime(resp, 'expires')
            self.assertHttpRespJsonFieldNotEmpty(resp, 'user_uid')
            self.assertHttpRespJsonFieldIsInt(resp, 'ttl')
            self.assertHttpRespJsonFieldMatches(resp, 'token', '^[0-9a-f]{32}$')

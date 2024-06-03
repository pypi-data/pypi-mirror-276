import unittest
from unittest.mock import patch

from pyctapi.apis.iam import IamApi, CheckUserPermissionParam


class TestIam(unittest.TestCase):
    
    def test_check_user_permission(self):
        cli = IamApi(ak='a', sk='a')
        param = CheckUserPermissionParam(action='read_vpc', user_id='a', account_id='1')
        with patch.object(cli, "perform_request") as mock_method:
            mock_method.return_value = 'ok'
            data = cli.check_user_permission(param)
            self.assertEqual('ok', data)


if __name__ == '__main__':
    unittest.main()

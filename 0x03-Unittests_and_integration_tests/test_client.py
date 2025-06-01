#!/usr/bin/env python3
"""Unit tests for client.GithubOrgClient class."""

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient class functionality"""
    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns the correct value"""
        test_client = GithubOrgClient(org_name)
        test_client.org()
        org_url = "https://api.github.com/orgs/" + org_name
        mock_get_json.assert_called_once_with(org_url)

    def test_public_repos_url(self):
        """Test GithubOrgClient._public_repos_url returns correct URL"""
        url = "https://api.github.com/orgs/test_org/repos"
        test_payload = {"repos_url": url}
        with patch('client.GithubOrgClient.org',
                   new_callable=unittest.mock.PropertyMock) as mock_org:
            mock_org.return_value = test_payload
            test_client = GithubOrgClient("test_org")
            result = test_client._public_repos_url
            self.assertEqual(result, test_payload["repos_url"])

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test GithubOrgClient.public_repos returns expected repos list"""
        test_repos_payload = [
            {"name": "repo1", "license": {"key": "mit"}},
            {"name": "repo2", "license": {"key": "apache-2.0"}},
        ]
        test_repos_url = "https://api.github.com/orgs/test_org/repos"
        mock_get_json.return_value = test_repos_payload
        with patch('client.GithubOrgClient._public_repos_url',
                   new_callable=unittest.mock.PropertyMock) as mock_repos_url:
            mock_repos_url.return_value = test_repos_url
            test_client = GithubOrgClient("test_org")
            result = test_client.public_repos()
            self.assertEqual(result, ["repo1", "repo2"])
            mock_repos_url.assert_called_once()
            mock_get_json.assert_called_once_with(test_repos_url)

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test GithubOrgClient.has_license returns correct boolean"""
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)


@parameterized_class(
    ('org_payload', 'repos_payload', 'expected_repos', 'apache2_repos'),
    TEST_PAYLOAD
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient public_repos method"""

    @classmethod
    def setUpClass(cls):
        """Set up class by mocking requests.get with fixture payloads"""
        def side_effect(url):
            mock = Mock()
            if url == cls.org_payload["repos_url"]:
                mock.json.return_value = cls.repos_payload
            elif url == "https://api.github.com/orgs/google":
                mock.json.return_value = cls.org_payload
            else:
                mock.json.return_value = {}
            return mock

        cls.get_patcher = patch('requests.get', side_effect=side_effect)
        cls.get_patcher.start()

    @classmethod
    def tearDownClass(cls):
        """Tear down class by stopping the requests.get patcher"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos returns expected repos without license filter"""
        test_client = GithubOrgClient("google")
        result = test_client.public_repos()
        self.assertEqual(result, self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos returns expected repos with apache-2.0 filter"""
        test_client = GithubOrgClient("google")
        result = test_client.public_repos(license="apache-2.0")
        self.assertEqual(result, self.apache2_repos)

    def test_public_repos_calls(self):
        """Test public_repos makes correct requests.get calls"""
        test_client = GithubOrgClient("google")
        with patch('requests.get') as mock_get:
            mock = Mock()
            mock.json.side_effect = [self.org_payload, self.repos_payload]
            mock_get.return_value = mock
            test_client.public_repos()
            org_url = "https://api.github.com/orgs/google"
            repos_url = self.org_payload["repos_url"]
            mock_get.assert_any_call(org_url)
            mock_get.assert_any_call(repos_url)

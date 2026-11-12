import unittest
from agro_conecta_iot.config import Config


class SecurityTests(unittest.TestCase):
    def test_config_repr_hides_credentials(self):
        config = Config(username="HIDDEN_USER", password="HIDDEN_PASS", token="HIDDEN_TOKEN")
        self.assertNotIn("HIDDEN", repr(config))

    def test_rejects_credentials_in_url_and_insecure_remote(self):
        for url in ("https://name:password@example.com", "http://remote.example", "https://example.com?token=secret"):
            with self.assertRaises(ValueError):
                Config(base_url=url)

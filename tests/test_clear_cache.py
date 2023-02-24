from unittest.mock import patch

from helper_auth import HelperAuth


def test_clear_cache():
    auth = HelperAuth("helper", cache_token=True)
    with patch("subprocess.run") as mock_run:
        mock_run.return_value.stdout = "username=GITHUB_NAME\npassword=GITHUB_TOKEN\n"
        auth._get_token()
        mock_run.assert_called_once()

        # token cached
        auth._get_token()
        mock_run.assert_called_once()

        auth.clear_cache()

        # token not cached
        auth._get_token()
        assert mock_run.call_count == 2

        # token cached
        auth._get_token()
        assert mock_run.call_count == 2

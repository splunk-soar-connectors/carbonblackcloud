from pathlib import Path


ROOT = Path(__file__).parent


def test_binary_download_rejects_unsafe_urls_and_redirects():
    source = (ROOT / "actions" / "cbc_action_get_binary_file.py").read_text()

    assert 'parsed.scheme != "https"' in source
    assert "ipaddress.ip_address(address[4][0]).is_global" in source
    assert "allow_redirects=False" in source
    assert "urllib.request.urlopen" not in source

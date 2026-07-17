# Copyright (c) 2026 Splunk Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from pathlib import Path


ROOT = Path(__file__).parent


def test_binary_download_rejects_unsafe_urls_and_redirects():
    source = (ROOT / "actions" / "cbc_action_get_binary_file.py").read_text()

    assert 'parsed.scheme != "https"' in source
    assert "ipaddress.ip_address(address[4][0]).is_global" in source
    assert "allow_redirects=False" in source
    assert "urllib.request.urlopen" not in source


def test_sdk_path_identifiers_are_validated_before_action_dispatch():
    source = (ROOT / "cbcapp_connector.py").read_text()

    assert 'PATH_IDENTIFIER_PATTERN = re.compile(r"^[A-Za-z0-9_-]+$")' in source
    assert '{"device_id", "watchlist_id", "feed_id", "report_id"}' in source
    assert "PATH_IDENTIFIER_PATTERN.fullmatch(str(params[field]))" in source

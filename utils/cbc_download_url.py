# VMware Carbon Black Cloud App for Splunk SOAR
# Copyright 2022-2026 VMware, Inc.
#
# This product is licensed to you under the BSD-2 license (the "License").
# You may not use this product except in compliance with the BSD-2 License.
"""Validation for Carbon Black Cloud UBS download URLs."""

import ipaddress
import socket
from urllib.parse import urlsplit


_AWS_DNS_SUFFIXES = (("amazonaws", "com"), ("amazonaws", "com", "cn"))


def _is_aws_s3_hostname(hostname):
    """Return whether hostname is an AWS-controlled S3 endpoint."""
    try:
        labels = hostname.rstrip(".").encode("idna").decode("ascii").lower().split(".")
    except UnicodeError:
        return False

    for suffix in _AWS_DNS_SUFFIXES:
        if tuple(labels[-len(suffix) :]) == suffix:
            return any(label == "s3" or label.startswith("s3-") for label in labels[: -len(suffix)])
    return False


def validate_ubs_download_url(download_url):
    """Validate a provider-returned UBS AWS S3 presigned URL."""
    if not isinstance(download_url, str):
        raise ValueError("Carbon Black Cloud returned an invalid download URL")

    parsed = urlsplit(download_url)
    try:
        port = parsed.port
    except ValueError as exc:
        raise ValueError("Carbon Black Cloud returned an invalid download URL") from exc

    if (
        parsed.scheme.lower() != "https"
        or not parsed.hostname
        or parsed.username
        or parsed.password
        or port not in (None, 443)
        or not _is_aws_s3_hostname(parsed.hostname)
    ):
        raise ValueError("Carbon Black Cloud returned an invalid UBS download URL")

    addresses = socket.getaddrinfo(parsed.hostname, port or 443, type=socket.SOCK_STREAM)
    if not addresses or any(not ipaddress.ip_address(address[4][0]).is_global for address in addresses):
        raise ValueError("Carbon Black Cloud returned a non-public download URL")

    return download_url

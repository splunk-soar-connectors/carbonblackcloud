# Copyright (c) 2026 Splunk Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
"""Tests for Carbon Black Cloud UBS download URL validation."""

import socket

import pytest

from utils.cbc_download_url import validate_ubs_download_url


def _address(ip):
    return (socket.AF_INET, socket.SOCK_STREAM, 6, "", (ip, 443))


@pytest.mark.parametrize(
    "hostname",
    (
        "bucket.s3.amazonaws.com",
        "bucket.s3.us-west-2.amazonaws.com",
        "bucket.s3.dualstack.us-west-2.amazonaws.com",
        "bucket.s3-accelerate.amazonaws.com",
        "bucket.s3.cn-north-1.amazonaws.com.cn",
    ),
)
def test_accepts_public_aws_s3_hosts(monkeypatch, hostname):
    monkeypatch.setattr(socket, "getaddrinfo", lambda *args, **kwargs: [_address("8.8.8.8")])

    url = f"https://{hostname}/sample.zip?X-Amz-Signature=value"

    assert validate_ubs_download_url(url) == url


@pytest.mark.parametrize(
    "url",
    (
        "http://bucket.s3.amazonaws.com/sample.zip",
        "https://user@bucket.s3.amazonaws.com/sample.zip",
        "https://bucket.s3.amazonaws.com:8443/sample.zip",
        "https://ec2.amazonaws.com/sample.zip",
        "https://s3.amazonaws.com.example.test/sample.zip",
        "https://attacker.example.test/sample.zip",
        "file:///etc/passwd",
    ),
)
def test_rejects_urls_outside_the_ubs_s3_contract(monkeypatch, url):
    monkeypatch.setattr(socket, "getaddrinfo", lambda *args, **kwargs: [_address("8.8.8.8")])

    with pytest.raises(ValueError):
        validate_ubs_download_url(url)


def test_rejects_mixed_public_and_private_dns_answers(monkeypatch):
    monkeypatch.setattr(
        socket,
        "getaddrinfo",
        lambda *args, **kwargs: [_address("8.8.8.8"), _address("127.0.0.1")],
    )

    with pytest.raises(ValueError, match="non-public"):
        validate_ubs_download_url("https://bucket.s3.amazonaws.com/sample.zip")


def test_rejects_host_without_dns_answers(monkeypatch):
    monkeypatch.setattr(socket, "getaddrinfo", lambda *args, **kwargs: [])

    with pytest.raises(ValueError, match="non-public"):
        validate_ubs_download_url("https://bucket.s3.amazonaws.com/sample.zip")

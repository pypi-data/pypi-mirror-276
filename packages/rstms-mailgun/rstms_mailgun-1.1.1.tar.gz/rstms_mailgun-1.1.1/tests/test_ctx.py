import os

import pytest

from rstms_mailgun.context import Context


@pytest.fixture
def domain():
    return os.environ.get("TEST_DOMAIN", "example.org")


@pytest.fixture
def api_key():
    return os.environ["MAILGUN_API_KEY"]


@pytest.fixture
def ctx(api_key, domain):
    return Context(api_key, domain)


def test_ctx_init(ctx):
    assert ctx


def test_ctx_record_name(ctx):
    assert "@" == ctx.record_name(dict(name="@"))
    assert "@" == ctx.record_name(dict(name=ctx.domain))
    assert "host" == ctx.record_name(dict(name="host." + ctx.domain))


def test_ctx_get_spf(ctx):
    records = ctx.get_deployed_dns_records(spf=True)
    assert isinstance(records, list)
    record = records[0]
    assert "id" in record
    assert record["name"] == "@"
    assert record["type"] == "TXT"
    assert record["domain"] == ctx.domain
    assert record["value"].startswith("v=spf1")

import pytest
from internal.amazon_utils import (
    normalize_domain,
    is_amazon_domain,
    extract_asin,
    canonical_amazon_url,
)

# -------------------------
# normalize_domain
# -------------------------

@pytest.mark.parametrize("domain,expected", [
    ("amazon.de", "amazon.de"),
    ("www.amazon.de", "amazon.de"),
    ("WWW.AMAZON.COM", "amazon.com"),
    ("notamazon.com", "notamazon.com"),
])
def test_normalize_domain(domain, expected):
    assert normalize_domain(domain) == expected


# -------------------------
# is_amazon_domain
# -------------------------

@pytest.mark.parametrize("domain,expected", [
    ("amazon.de", True),
    ("www.amazon.de", True),
    ("amazon.com", True),
    ("amazon.co.uk", True),
    ("amazon.co.jp", True),

    ("notamazon.com", False),
    ("amazon.evil.com", False),
    ("foo.amazon.de", False),
    ("amaz0n.com", False),
])
def test_is_amazon_domain(domain, expected):
    assert is_amazon_domain(domain) == expected


# -------------------------
# extract_asin
# -------------------------

@pytest.mark.parametrize("url,expected", [
    ("https://amazon.de/dp/B00ABC1234", "B00ABC1234"),
    ("https://amazon.de/dp/b00abc1234", "B00ABC1234"),
    ("https://amazon.de/gp/product/B00ABC1234", "B00ABC1234"),
    ("https://amazon.de/gp/offer-listing/B00ABC1234", "B00ABC1234"),
    ("https://amazon.de/-/dp/B00ABC1234", "B00ABC1234"),

    ("https://amazon.de/dp/INVALID123", None),
    ("https://example.com/dp/B00ABC1234", "B00ABC1234"),  # domain-agnostic
])
def test_extract_asin(url, expected):
    assert extract_asin(url) == expected


# -------------------------
# canonical_amazon_url (nur Basisfälle)
# -------------------------

@pytest.mark.parametrize("url,expected", [
    ("https://amazon.de/dp/B00ABC1234", "https://amazon.de/dp/B00ABC1234"),
    ("https://amazon.de/gp/product/B00ABC1234", "https://amazon.de/dp/B00ABC1234"),
    ("https://amazon.de/-/dp/B00ABC1234", "https://amazon.de/dp/B00ABC1234"),
])
def test_canonical_amazon_url_basic(url, expected):
    assert canonical_amazon_url(url) == expected

def test_is_amazon_domain_additional_cases():
    assert is_amazon_domain("www.amazon.co.uk") is True
    assert is_amazon_domain("AMAZON.DE") is True
    assert is_amazon_domain("amazon.fake.com") is False
    assert is_amazon_domain("amazon.co") is True
    assert is_amazon_domain("amazon.co.xx.xx") is False

def test_extract_asin_variants():
    assert extract_asin("https://amazon.de/dp/B00ABC1234") == "B00ABC1234"
    assert extract_asin("https://amazon.de/gp/product/B00ABC1234") == "B00ABC1234"
    assert extract_asin("https://amazon.de/gp/offer-listing/B00ABC1234") == "B00ABC1234"
    assert extract_asin("https://amazon.de/-/dp/B00ABC1234") == "B00ABC1234"

    # ASIN in query → should NOT match
    assert extract_asin("https://amazon.de/?asin=B00ABC1234") is None

    # uppercase
    assert extract_asin("https://amazon.de/dp/b00abc1234") == "B00ABC1234"

    # no ASIN
    assert extract_asin("https://amazon.de/s?k=usb") is None

def test_canonical_amazon_url_non_amazon_domain():
    url = "https://example.com/dp/B00ABC1234"
    assert canonical_amazon_url(url) == url

def test_canonical_amazon_url_no_asin():
    url = "https://amazon.de/s?k=usb"
    assert canonical_amazon_url(url) == url

def test_extract_asin_standard_dp():
    url = "https://www.amazon.de/dp/B012345678"
    assert extract_asin(url) == "B012345678"

def test_extract_asin_gp_product():
    url = "https://www.amazon.de/gp/product/B012345678"
    assert extract_asin(url) == "B012345678"

def test_extract_asin_with_query_params():
    url = "https://www.amazon.de/dp/B012345678?tag=test123"
    assert extract_asin(url) == "B012345678"

def test_extract_asin_with_tracking():
    url = "https://www.amazon.de/dp/B012345678/ref=something?psc=1"
    assert extract_asin(url) == "B012345678"

def test_extract_asin_lowercase_asin():
    url = "https://www.amazon.de/dp/b012345678"
    assert extract_asin(url) == "B012345678"

def test_extract_asin_no_asin_in_url():
    url = "https://www.amazon.de/s?k=python"
    assert extract_asin(url) is None

def test_extract_asin_non_amazon_url():
    url = "https://example.com/product/B012345678"
    assert extract_asin(url) is None

def test_extract_asin_invalid_asin_format():
    url = "https://www.amazon.de/dp/INVALID123"
    assert extract_asin(url) is None

def test_extract_asin_does_not_match_plain_text():
    url = "Check this ASIN: B012345678 now!"
    assert extract_asin(url) is None

import pytest
from internal.html_pipeline import process_html
from internal.amazon_utils import normalize_domain, is_valid_amazon_url


HTML_SIMPLE = """
<p>Hier ist ein Link:
    <a href="https://amazon.de/dp/B00ABC1234?tag=foo-21">Produkt</a>
</p>
"""

HTML_NON_AMAZON = """
<p>Ein normaler Link:
    <a href="https://example.com/foo">Beispiel</a>
</p>
"""

HTML_MIXED = """
<p>
    <a href="https://amazon.de/dp/B00ABC1234?tag=foo-21">A</a>
    <a href="https://example.com/foo">B</a>
    <a href="https://amazon.de/gp/product/B00XYZ9876?ref=abc">C</a>
</p>
"""


# ---------------------------------------------------------
# Mode: clean
# ---------------------------------------------------------

def test_html_clean_amazon_link():
    html = process_html(HTML_SIMPLE, mode="clean")
    assert 'href="https://amazon.de/dp/B00ABC1234"' in html
    assert "?tag=" not in html


def test_html_clean_mixed_links():
    html = process_html(HTML_MIXED, mode="clean")
    assert 'href="https://amazon.de/dp/B00ABC1234"' in html
    assert 'href="https://example.com/foo"' in html
    assert 'href="https://amazon.de/dp/B00XYZ9876"' in html


# ---------------------------------------------------------
# Mode: remove
# ---------------------------------------------------------

def test_html_remove_amazon_link():
    html = process_html(HTML_SIMPLE, mode="remove")
    # Link entfernt, Text bleibt
    assert "<a" not in html
    assert "Produkt" in html


def test_html_remove_mixed_links():
    html = process_html(HTML_MIXED, mode="remove")

    # Amazon-Links entfernt
    assert "https://amazon.de" not in html

    # Nicht-Amazon-Link bleibt als <a>
    assert 'href="https://example.com/foo"' in html

    # Texte bleiben erhalten
    assert "A" in html
    assert "B" in html
    assert "C" in html


# ---------------------------------------------------------
# Mode: fallback
# ---------------------------------------------------------

def test_html_fallback_amazon_link():
    html = process_html(HTML_SIMPLE, mode="fallback")
    assert "Amazon-Produkt B00ABC1234" in html
    assert "<a" not in html


def test_html_fallback_mixed_links():
    html = process_html(HTML_MIXED, mode="fallback")
    assert "Amazon-Produkt B00ABC1234" in html
    assert "Amazon-Produkt B00XYZ9876" in html
    assert 'href="https://example.com/foo"' in html


# ---------------------------------------------------------
# Mode: keep
# ---------------------------------------------------------

def test_html_keep_leaves_html_unchanged():
    html = process_html(HTML_SIMPLE, mode="keep")
    assert 'href="https://amazon.de/dp/B00ABC1234?tag=foo-21"' in html

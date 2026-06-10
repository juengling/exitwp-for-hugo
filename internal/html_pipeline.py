from bs4 import BeautifulSoup
from urllib.parse import urlparse
from internal.amazon import (
    is_amazon_link,
    is_amazon_domain,
    process_amazon_link,
)
from internal.amazon_utils import (
    normalize_domain,
    is_valid_amazon_url,
    extract_asin,
    clean_amazon_url
    )

def process_html(html: str, mode: str = "clean") -> str:
    soup = BeautifulSoup(html, "html.parser")

    for a in soup.find_all("a"):
        href = a.get("href", "")

        # Nicht-Amazon-Links bleiben immer unverändert
        if not is_amazon_link(href):
            continue

        asin = extract_asin(href)

        # -------------------------
        # FALLBACK-MODUS
        # -------------------------
        if mode == "fallback":
            if asin:
                a.replace_with(f"Amazon-Produkt {asin}")
            else:
                a.decompose()
            continue

        # -------------------------
        # REMOVE-MODUS
        # -------------------------
        if mode == "remove":
            # Entferne nur das <a>-Tag, behalte den Text
            a.unwrap()
            continue

        # -------------------------
        # CLEAN-MODUS (Standard)
        # -------------------------
        if mode == "clean":
            if asin:
                clean_url = clean_amazon_url(href)
                if clean_url:
                    a["href"] = clean_url
                else:
                    a.decompose()
            else:
                # Amazon-Link ohne ASIN → entfernen
                a.decompose()
            continue

    return str(soup)

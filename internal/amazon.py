from urllib.parse import urlparse
from internal.amazon_utils import (
    normalize_domain,
    is_amazon_domain,
    AMAZON_SHORTLINKS,
    extract_asin,
)

from urllib.parse import urlparse

def is_amazon_link(url: str) -> bool:
    if not url or not isinstance(url, str):
        return False

    try:
        parsed = urlparse(url)
    except Exception:
        return False

    domain = parsed.netloc.lower()

    # 1. Shortlink: nur exakt "amzn.to" ist erlaubt
    if domain == "amzn.to":
        return True

    # 2. Normale Amazon-Domains
    return is_amazon_domain(domain)


def process_amazon_link(url: str, action: str) -> str:
    try:
        parsed = urlparse(url)
    except Exception:
        return url  # ungültige URL → unverändert zurückgeben

    domain = normalize_domain(parsed.netloc)

    # remove = immer entfernen
    if action == "remove":
        return ""

    # fallback
    if action == "fallback":
        if domain in AMAZON_SHORTLINKS:
            return "Amazon-Produkt"

        if not is_amazon_domain(domain):
            return ""

        asin = extract_asin(parsed.path)
        if asin:
            return f"Amazon-Produkt {asin}"
        return ""

    # clean / canonical
    if action in ("clean", "canonical"):
        # Nicht-Amazon-Link → unverändert lassen
        if not is_amazon_domain(domain) and domain not in AMAZON_SHORTLINKS:
            return url

        asin = extract_asin(parsed.path)
        if asin is None:
            return ""

        # canonical = immer dp-Link
        if action == "canonical":
            return f"https://{domain}/dp/{asin}"

        # clean = dp-Link ohne Tracking
        if action == "clean":
            return f"https://{domain}/dp/{asin}"

    # ❗ WICHTIG: unbekannter Modus → URL unverändert zurückgeben
    return url

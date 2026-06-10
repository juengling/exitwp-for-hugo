import re
from urllib.parse import urlparse, urlunparse, parse_qsl, urlencode

# Liste aller gültigen Amazon-Domains
AMAZON_DOMAINS = {
    "amazon.de",
    "www.amazon.de",
    "amazon.com",
    "www.amazon.com",
    "amazon.co.uk",
    "www.amazon.co.uk",
    "amazon.fr",
    "www.amazon.fr",
    "amazon.it",
    "www.amazon.it",
    "amazon.es",
    "www.amazon.es",
}

# Shortlinks wie amzn.to
AMAZON_SHORTLINKS = {
    "amzn.to",
    "www.amzn.to",
}


# ------------------------------------------------------------
# Domain Normalisierung
# ------------------------------------------------------------

def normalize_domain(domain: str) -> str:
    if not isinstance(domain, str):
        return ""

    domain = domain.lower().strip()

    for prefix in ("www.", "m.", "smile."):
        if domain.startswith(prefix):
            domain = domain[len(prefix):]

    return domain

def is_amazon_domain(domain: str) -> bool:
    domain = domain.lower()

    # Entferne erlaubte Präfixe
    for prefix in ("www.", "m.", "smile."):
        if domain.startswith(prefix):
            domain = domain[len(prefix):]

    # Domain muss exakt mit "amazon." beginnen
    if not domain.startswith("amazon."):
        return False

    # TLD extrahieren
    tld = domain[len("amazon."):]

    # amazon.<tld> → tld muss gültig sein
    if "." in tld:
        # Ausnahmen: amazon.co.uk, amazon.co.jp
        if tld in ("co.uk", "co.jp"):
            return True
        return False

    # Normale TLD wie .de, .com, .fr, .it etc.
    return len(tld) >= 2


# ------------------------------------------------------------
# ASIN Extraktion
# ------------------------------------------------------------

import re
from urllib.parse import urlparse

import re
from urllib.parse import urlparse

ASIN_REGEX = re.compile(
    r"/(?:dp|gp/product|gp/offer-listing|exec/obidos/ASIN)/([A-Za-z0-9]{10})",
    re.IGNORECASE
)

def is_valid_asin(asin: str) -> bool:
    if len(asin) != 10:
        return False
    if not asin.isalnum():
        return False

    # Moderne ASINs: B + 9 alphanumerische Zeichen
    if re.fullmatch(r"B[A-Z0-9]{9}", asin):
        return True

    # Alte ASINs: 9 Ziffern + 1 Buchstabe
    if re.fullmatch(r"[0-9]{9}[A-Z]", asin):
        return True

    return False

def extract_asin(url: str) -> str | None:
    try:
        parsed = urlparse(url)
    except Exception:
        return None

    path = parsed.path

    # 1. Standard Amazon-Pfade
    m = ASIN_REGEX.search(path)
    if m:
        asin = m.group(1).upper()
        return asin if is_valid_asin(asin) else None

    # 2. Sonderfall: /-/dp/<ASIN>
    m = re.search(r"/-/dp/([A-Za-z0-9]{10})", path, re.IGNORECASE)
    if m:
        asin = m.group(1).upper()
        return asin if is_valid_asin(asin) else None

    # 3. Generischer Fallback: /dp/<ASIN>
    m = re.search(r"/dp/([A-Za-z0-9]{10})", path, re.IGNORECASE)
    if m:
        asin = m.group(1).upper()
        return asin if is_valid_asin(asin) else None

    return None

def extract_asin(url: str) -> str | None:
    try:
        parsed = urlparse(url)
    except Exception:
        return None

    path = parsed.path

    # 1. Standard Amazon-Pfade
    m = ASIN_REGEX.search(path)
    if m:
        asin = m.group(1).upper()
        return asin if is_valid_asin(asin) else None

    # 2. Sonderfall: /-/dp/<ASIN>
    m = re.search(r"/-/dp/([A-Za-z0-9]{10})", path, re.IGNORECASE)
    if m:
        asin = m.group(1).upper()
        return asin if is_valid_asin(asin) else None

    # 3. Generischer Fallback: /dp/<ASIN>
    m = re.search(r"/dp/([A-Za-z0-9]{10})", path, re.IGNORECASE)
    if m:
        asin = m.group(1).upper()
        return asin if is_valid_asin(asin) else None

    return None


# ------------------------------------------------------------
# URL-Validierung
# ------------------------------------------------------------

from urllib.parse import urlparse

from urllib.parse import urlparse

def is_valid_amazon_url(url: str) -> bool:
    if not url or not isinstance(url, str):
        return False

    try:
        parsed = urlparse(url)
    except Exception:
        return False

    domain = parsed.netloc.lower()

    # Shortlinks sind gültige Amazon-URLs
    if domain == "amzn.to":
        return True

    # Normale Amazon-Domain?
    if not is_amazon_domain(domain):
        return False

    # Nur gültig, wenn eine ASIN drin steckt
    asin = extract_asin(url)
    return asin is not None

# ------------------------------------------------------------
# URL-Normalisierung / Canonical / Clean
# ------------------------------------------------------------

def canonical_amazon_url(url: str) -> str | None:
    try:
        parsed = urlparse(url)
    except Exception:
        return None

    domain = normalize_domain(parsed.netloc)

    # WICHTIG: Nicht-Amazon-Domain → URL unverändert zurückgeben
    if not is_amazon_domain(domain):
        return url

    asin = extract_asin(url)

    # Keine ASIN → URL unverändert zurückgeben
    if asin is None:
        return url

    # Canonical path
    path = f"/dp/{asin}"

    return f"https://{domain}{path}"

from urllib.parse import urlparse

def clean_amazon_url(url: str) -> str:
    try:
        parsed = urlparse(url)
    except Exception:
        return url

    domain = parsed.netloc.lower()

    # Shortlinks NICHT canonicalisieren
    if domain == "amzn.to":
        return url

    # Normale Amazon-Domain?
    if not is_amazon_domain(domain):
        return url

    # Domain normalisieren: www., m., smile. entfernen
    for prefix in ("www.", "m.", "smile."):
        if domain.startswith(prefix):
            domain = domain[len(prefix):]

    asin = extract_asin(url)

    # Keine ASIN → URL unverändert zurückgeben
    if asin is None:
        return url

    # Canonical URL
    return f"https://{domain}/dp/{asin}"




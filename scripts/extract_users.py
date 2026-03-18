import logging
from urllib.parse import quote

from scripts.oktasnapshot_utils import ensure_domain_str, get_paginated

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s - %(message)s",
)
logger = logging.getLogger("okta_compare")


def _headers(api_token):
    return {
        "Authorization": f"SSWS {api_token}",
        "Accept": "application/json",
    }


def get_users(domain_url, api_token, limit=200, search=None):
    base = ensure_domain_str(domain_url).rstrip("/")
    url = f"{base}/api/v1/users?limit={limit}"
    if search:
        url = f"{url}&search={quote(search, safe='()\" ')}"
    logger.info("Fetching users from %s.", url)
    return get_paginated(url, _headers(api_token), "Error fetching users") or []


def get_all_users(domain_url, api_token, limit=200, include_deprovisioned=True):
    users = {}
    for user in get_users(domain_url, api_token, limit=limit) or []:
        user_id = user.get("id")
        if user_id:
            users[user_id] = user

    if include_deprovisioned:
        for user in get_users(
            domain_url,
            api_token,
            limit=limit,
            search='status eq "DEPROVISIONED"',
        ) or []:
            user_id = user.get("id")
            if user_id:
                users[user_id] = user

    return list(users.values())


def get_user_factors(domain_url, api_token, user_id):
    if not user_id:
        return []
    base = ensure_domain_str(domain_url).rstrip("/")
    url = f"{base}/api/v1/users/{user_id}/factors"
    logger.info("Fetching factors for user_id=%s.", user_id)
    return get_paginated(url, _headers(api_token), f"Error fetching factors for user {user_id}") or []


def get_user_roles(domain_url, api_token, user_id):
    if not user_id:
        return []
    base = ensure_domain_str(domain_url).rstrip("/")
    url = f"{base}/api/v1/users/{user_id}/roles"
    logger.info("Fetching roles for user_id=%s.", user_id)
    return get_paginated(url, _headers(api_token), f"Error fetching roles for user {user_id}") or []


def get_users_with_security_context(domain_url, api_token, limit=200):
    users = get_all_users(domain_url, api_token, limit=limit, include_deprovisioned=True) or []
    enriched = []
    for user in users:
        user_id = user.get("id")
        status = str(user.get("status") or "").upper()
        factors = []
        roles = []
        if user_id and status != "DEPROVISIONED":
            factors = get_user_factors(domain_url, api_token, user_id) or []
            roles = get_user_roles(domain_url, api_token, user_id) or []
        combined = dict(user)
        combined["factors"] = factors
        combined["roles"] = roles
        enriched.append(combined)
    return enriched

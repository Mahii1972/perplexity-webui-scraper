"""
Test using curl_cffi which mimics browser TLS fingerprints to bypass Cloudflare.
"""
from curl_cffi import requests
from uuid import uuid4

# Full cookies from browser
cookies_str = """pplx.visitor-id=30f6c187-fda9-4aad-910a-4de7baffb74a; cf_clearance=2wSrc1mQjm_ybvMA1hvchSDv_QhUrKJeQZuXUrhlfrc-1764406926-1.2.1.1-jf7woiCR1jsdPJVOpHMhjLDGE8jbBwO.VkYSzM0HIKvCGh5vFtU0tfxwYlr5KVEyRdVXxLgoqnbTN1dmc95Lut4ntSXujhR_kEBJjna.vIL6wiL4DIUQLA2qKib6YuUHXOBjQ_0g_yPzSnosxgeqm5WxqsCyu4u0.ZgjkFkByO6SL2Id0TYc4_.bWu0Xd1BNrheQxnN8TSa6BWCzQ25zhq.NpuHpSbaBJxEv.CFhyTsZvGq2kXr2aEr.Xpcg7uHv; pplx.metadata={%22qc%22:18%2C%22qcu%22:2%2C%22qcm%22:12%2C%22qcc%22:0%2C%22qcco%22:0%2C%22qccol%22:0%2C%22qcdr%22:0%2C%22qcs%22:0%2C%22qcd%22:0%2C%22hli%22:true%2C%22hcga%22:false%2C%22hcds%22:false%2C%22hso%22:false%2C%22hfo%22:false%2C%22hsco%22:false%2C%22hfco%22:false%2C%22hsma%22:false%2C%22hdc%22:false%2C%22fqa%22:1764406015484%2C%22lqa%22:1764407346677}; __cf_bm=9qDBS4rOTmb.ItrLvPW8itB2KsMBBPYWV5EoycH3Af4-1764406816-1.0.1.1-q3_g63.qiUPjzQ7q7ywYxc9nVwHsvvTQbdDMZ3ccIcbHyADvq8Cprv8hCzqJWBdsvHohom2Ad7bRN6sybB8QrsBIrOqZm9RQXzKDydqSiJM; pplx.session-id=92e73ec9-1bc0-4ad1-8246-ec2bff3776e6; gov-badge=3; __cflb=02DiuDyvFMmK5p9jVbVnMNSKYZhUL9aGkRxZS1XuW89TS; next-auth.csrf-token=3011b7606d20dd4053645253b6d28399c4c0f56841c88d89926d9783f5dc3240%7C835b4cdd9ead52f6038fe300128b435c035fa467a619c9904547a460ee969285; next-auth.callback-url=https%3A%2F%2Fwww.perplexity.ai%2Fapi%2Fauth%2Fsignin-callback%3Fredirect%3Dhttps%253A%252F%252Fwww.perplexity.ai%252F%253Flogin-source%253DsignupButton; _dd_s=aid=00fbc307-6af6-4cb8-abe1-6a3e4a8fb719&rum=2&id=1179b7cb-94c7-4514-9ce0-ea460bd300a6&created=1764405904758&expire=1764408246170&logs=0; g_state={"i_l":1,"i_ll":1764406953020,"i_b":"qHJ76ukRSOmMlDqXRYJSwD68Zm6nISgF3N/PBk0NpWo","i_p":1764413110738}; __ps_r=_; __ps_sr=_; __ps_lu=https://www.perplexity.ai/auth/verify-request?email=purplixyee115%40oxaam.in&redirectUrl=https%3A%2F%2Fwww.perplexity.ai%2F%3Flogin-source%3DfloatingSignup; __ps_slu=https://www.perplexity.ai/auth/verify-request?email=purplixyee115%40oxaam.in&redirectUrl=https%3A%2F%2Fwww.perplexity.ai%2F%3Flogin-source%3DfloatingSignup; __ps_fva=1764405989909; _gcl_au=1.1.1544864645.1764405990.718054260.1764406943.1764406948; _fbp=fb.1.1764405992833.644057092284252957; pplx.personal-search-badge-seen={%22sidebar%22:true%2C%22settingsSidebar%22:false%2C%22personalize%22:false}; pplx.is-incognito=false; __Secure-next-auth.session-token=eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..RJjLzvX3tbtrfHOY.D2V5MBtJkUJFR_0O-4ILW8ob0J6qdxsedRjZpkdGTbLRkcwuf3MqP8bZHADRZCaBpR2j9kPLjrrYDChiOMQcleT-BUO4aJ5L6P1OAzBsKy7wHDdymfj3KtNk1kREUt-KHxBR1A5Q59mgvxpoUMPX_pEYB6nrV6q-Q_wGBwjVmnw3Kh1BPX6zn2aWCx-bViq1JdmYjIctESeHAD9CyiNz5_SWcfYHl847rsyiT_Gr19_aqJE_UhdEIIpw5a5H-Xs9.nQXYJ8aJX5aJlftcBYPStQ; sidebar-upgrade-badge=10; _rdt_uuid=1764405992373.b08234c5-c671-4360-aa10-94666ab5488b; _rdt_em=:38931035cf211b2db119f8db3177d4f46961706f2261910544d5bae6e1293dbb,9aa71a6c5718e0ab214c1807673c335f4151e29657b30000ce8ab5ccb697d60e"""

# Parse cookies
cookies = {}
for item in cookies_str.split("; "):
    if "=" in item:
        key, value = item.split("=", 1)
        cookies[key.strip()] = value.strip()

print(f"Parsed {len(cookies)} cookies")

frontend_uuid = str(uuid4())

# Headers matching Firefox browser
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:145.0) Gecko/20100101 Firefox/145.0",
    "Accept": "text/event-stream",
    "Accept-Language": "en-US,en;q=0.5",
    "Content-Type": "application/json",
    "Referer": "https://www.perplexity.ai/",
    "X-Request-Id": frontend_uuid,
    "X-Perplexity-Request-Reason": "perplexity-query-state-provider",
    "Origin": "https://www.perplexity.ai",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
}

# Payload
payload = {
    "params": {
        "attachments": [],
        "language": "en-US",
        "timezone": "Asia/Kolkata",
        "search_focus": "internet",
        "sources": ["web"],
        "search_recency_filter": None,
        "frontend_uuid": frontend_uuid,
        "mode": "concise",
        "model_preference": "turbo",
        "is_related_query": False,
        "is_sponsored": False,
        "frontend_context_uuid": str(uuid4()),
        "prompt_source": "user",
        "query_source": "home",
        "is_incognito": False,
        "time_from_first_type": 82147,
        "local_search_enabled": False,
        "use_schematized_api": True,
        "send_back_text_in_streaming_api": False,
        "supported_block_use_cases": [
            "answer_modes", "media_items", "knowledge_cards", "inline_entity_cards",
            "place_widgets", "finance_widgets", "prediction_market_widgets", "sports_widgets",
            "flight_status_widgets", "shopping_widgets", "jobs_widgets", "search_result_widgets",
            "clarification_responses", "inline_images", "inline_assets", "placeholder_cards",
            "diff_blocks", "inline_knowledge_cards", "entity_group_v2", "refinement_filters",
            "canvas_mode", "maps_preview", "answer_tabs", "price_comparison_widgets", "preserve_latex"
        ],
        "client_coordinates": None,
        "mentions": [],
        "dsl_query": "hi",
        "skip_search_enabled": True,
        "is_nav_suggestions_disabled": False,
        "always_search_override": False,
        "override_no_search": False,
        "should_ask_for_mcp_tool_confirmation": True,
        "browser_agent_allow_once_from_toggle": False,
        "supported_features": ["browser_agent_permission_banner"],
        "version": "2.18"
    },
    "query_str": "hi"
}

print(f"Sending request with frontend_uuid: {frontend_uuid}")

# Use curl_cffi with Firefox impersonation
try:
    response = requests.post(
        "https://www.perplexity.ai/rest/sse/perplexity_ask",
        json=payload,
        headers=headers,
        cookies=cookies,
        impersonate="firefox",  # Mimic Firefox TLS fingerprint
        timeout=60
    )
    print(f"Status: {response.status_code}")
    print(f"Response (first 2000 chars):\n{response.text[:2000]}")
except Exception as e:
    print(f"Error: {type(e).__name__}: {e}")

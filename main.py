import requests

url = "https://api.rabby.io/v2/points/claim_snapshot"  # Обновленный URL для новой версии API

headers = {
    "Host": "api.rabby.io",
    "Connection": "keep-alive",
    "Content-Length": "224",
    "sec-ch-ua": '"Not A Brand";v="8", "Chromium";v="130", "Google Chrome";v="130"',
    "X-Version" = "1.0.0"  # Обновление версии клиента
    "sec-ch-ua-mobile": "?0",
    "User-Agent" = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"  # Фиксированный User-Agent
    "x-api-ts": str(int(time.time())),
    "Content-Type": "application/json",
    "x-api-ver": "v2",
    "Accept": "application/json, text/plain, */*",
    "X-Client": "Rabby",
    "sec-ch-ua-platform": '"Windows"',
    "Origin": "chrome-extension://acmacodkjb dgmoleebolmdjonilkdbch",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US;q=0.8,en;q=0.7",
}

wallets = file_to_list("inputs/wallets.txt")
proxy_list = file_to_list("inputs/proxies.txt")

for raw_wallet in wallets:
    try:
        if " " in raw_wallet.strip():
            client = Web3Utils(mnemonic=raw_wallet)
        else:
            client = Web3Utils(key=raw_wallet)

        address = client.acct.address.lower()
        msg = f"{address} Claims Rabby Points"

        payload = {
            "id": address,
            "signature": client.get_signed_code(msg),
            "invite_code": BONUS_CODE
        }

        proxies = {"http": f"http://{proxy_list.pop(0)}"} if proxy_list else None

        response = requests.post(url, headers=headers, json=payload, proxies=proxies, timeout=10)  # Таймаут 10 секунд

        if response.json().get("error_code") == 0:
            resp_msg = "Claimed!"
            logger.success(f"{address} | Claimed!")
        else:
            resp_msg = response.json().get("error_msg")
            logger.info(f"{address} | {resp_msg}")

        time.sleep(random.uniform(*DELAY))
    except Exception as e:
        logger.error(f"{raw_wallet[:15]}... | {e}")
import requests
from time import sleep

FILTER_URLS = [
    ("anti-ad", "https://anti-ad.net/adguard.txt"),
    ("OISD", "https://small.oisd.nl"),
    ("WhiteList", "https://gist.githubusercontent.com/iwfd965/ad9d8863a63a92f89bd3bbfde1116ce5/raw/AdGuardWhitelist")
]

all_rules = set()

for name, url in FILTER_URLS:
    for attempt in range(3):
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            rules = {
                line.strip()
                for line in response.text.splitlines()
                if line.strip() and not line.startswith(("!", "#"))
            }
            all_rules |= rules
            print(f"{name}: {len(rules)} 条")
            break
        except requests.RequestException as error:
            print(f"{name} 下载出错: {error}, 重试 {attempt + 1}/3")
            sleep(2 * (attempt + 1))
    else:
        print(f"{name} 下载失败，已跳过")

with open("merged_rules.txt", "w", encoding="utf-8") as output_file:
    output_file.write("\n".join(sorted(all_rules)))

print(f"合并去重后: {len(all_rules)} 条")
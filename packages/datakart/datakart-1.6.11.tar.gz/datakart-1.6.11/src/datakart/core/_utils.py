import pathlib
import random
from pprint import pprint
from time import sleep

import requests

WORK_DIR = pathlib.Path(__file__).parent
ASSETS_DIR = WORK_DIR / "assets"

_s = requests.session()


def update_naver_lab_shopping_insight_category():
    def _query(cid: int = 0) -> dict:
        url = "https://datalab.naver.com/shoppingInsight/getCategory.naver"
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
            "Referer": "https://datalab.naver.com/shoppingInsight/sKeyword.naver",
        }
        resp = _s.get(url, params=dict(cid=cid), headers=headers)
        resp.raise_for_status()
        return resp.json()

    # lavel 0
    resp_0 = _query(0)
    resp_0.raise_for_status()
    level_0 = resp_0.json()

    # lavel 1
    pprint(level_0, sort_dicts=False)
    level_1 = level_0.get("childList")
    if not level_1:
        raise ValueError(f"invalid level_1, got {level_1=}")

    level_1 = []
    for child in level_0.get("childList"):
        sleep(random.uniform(1, 3))
        cid = child.get("cid")
        if cid is None:
            raise ValueError(f"invalid cid, got {cid=}")
        cate = _query(cid)
        level_1.append(cate)
        pprint(cate, sort_dicts=False)

    level_2 = []
    for child in (x.get("childList") for x in level_1):
        print(f"{child=}")
        break
        sleep(random.uniform(1, 3))
        cid = child.get("cid")
        if cid is None:
            raise ValueError(f"invalid cid, got {cid=}")
        cate = _query(cid)
        level_2.append(cate)
        pprint(cate, sort_dicts=False)

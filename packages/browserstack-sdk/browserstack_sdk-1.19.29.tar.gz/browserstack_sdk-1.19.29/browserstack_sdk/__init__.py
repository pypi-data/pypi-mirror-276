# coding: UTF-8
import sys
bstack1l11_opy_ = sys.version_info [0] == 2
bstack1lllll1l_opy_ = 2048
bstack1ll1l1_opy_ = 7
def bstack111l11_opy_ (bstack1l1ll_opy_):
    global bstack1111l1l_opy_
    bstack1lll1_opy_ = ord (bstack1l1ll_opy_ [-1])
    bstack11l11l1_opy_ = bstack1l1ll_opy_ [:-1]
    bstack1ll11l1_opy_ = bstack1lll1_opy_ % len (bstack11l11l1_opy_)
    bstack1l1l1l_opy_ = bstack11l11l1_opy_ [:bstack1ll11l1_opy_] + bstack11l11l1_opy_ [bstack1ll11l1_opy_:]
    if bstack1l11_opy_:
        bstack1ll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1lllll1l_opy_ - (bstack1lll111_opy_ + bstack1lll1_opy_) % bstack1ll1l1_opy_) for bstack1lll111_opy_, char in enumerate (bstack1l1l1l_opy_)])
    else:
        bstack1ll1l_opy_ = str () .join ([chr (ord (char) - bstack1lllll1l_opy_ - (bstack1lll111_opy_ + bstack1lll1_opy_) % bstack1ll1l1_opy_) for bstack1lll111_opy_, char in enumerate (bstack1l1l1l_opy_)])
    return eval (bstack1ll1l_opy_)
import atexit
import os
import signal
import sys
import yaml
import requests
import logging
import threading
import socket
import datetime
import string
import random
import json
import collections.abc
import re
import multiprocessing
import traceback
import copy
import tempfile
from packaging import version
from uuid import uuid4
from browserstack.local import Local
from urllib.parse import urlparse
from dotenv import load_dotenv
from bstack_utils.constants import *
from bstack_utils.percy import *
from browserstack_sdk.bstack1lll111ll1_opy_ import *
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.bstack1ll1l1l1_opy_ import bstack1l11ll1lll_opy_
import time
import requests
def bstack1ll111llll_opy_():
  global CONFIG
  headers = {
        bstack111l11_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩࡶ"): bstack111l11_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧࡷ"),
      }
  proxies = bstack1l11ll11l1_opy_(CONFIG, bstack1llllll1ll_opy_)
  try:
    response = requests.get(bstack1llllll1ll_opy_, headers=headers, proxies=proxies, timeout=5)
    if response.json():
      bstack1l11l1lll_opy_ = response.json()[bstack111l11_opy_ (u"ࠬ࡮ࡵࡣࡵࠪࡸ")]
      logger.debug(bstack1lll11111l_opy_.format(response.json()))
      return bstack1l11l1lll_opy_
    else:
      logger.debug(bstack111l1ll11_opy_.format(bstack111l11_opy_ (u"ࠨࡒࡦࡵࡳࡳࡳࡹࡥࠡࡌࡖࡓࡓࠦࡰࡢࡴࡶࡩࠥ࡫ࡲࡳࡱࡵࠤࠧࡹ")))
  except Exception as e:
    logger.debug(bstack111l1ll11_opy_.format(e))
def bstack1l1lll1l1l_opy_(hub_url):
  global CONFIG
  url = bstack111l11_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤࡺ")+  hub_url + bstack111l11_opy_ (u"ࠣ࠱ࡦ࡬ࡪࡩ࡫ࠣࡻ")
  headers = {
        bstack111l11_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡸࡾࡶࡥࠨࡼ"): bstack111l11_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ࡽ"),
      }
  proxies = bstack1l11ll11l1_opy_(CONFIG, url)
  try:
    start_time = time.perf_counter()
    requests.get(url, headers=headers, proxies=proxies, timeout=5)
    latency = time.perf_counter() - start_time
    logger.debug(bstack1lll111l_opy_.format(hub_url, latency))
    return dict(hub_url=hub_url, latency=latency)
  except Exception as e:
    logger.debug(bstack1ll1l1111_opy_.format(hub_url, e))
def bstack1l1l11l1l1_opy_():
  try:
    global bstack1l1l11l11_opy_
    bstack1l11l1lll_opy_ = bstack1ll111llll_opy_()
    bstack111l1l1l_opy_ = []
    results = []
    for bstack1ll111ll1_opy_ in bstack1l11l1lll_opy_:
      bstack111l1l1l_opy_.append(bstack1l111ll11_opy_(target=bstack1l1lll1l1l_opy_,args=(bstack1ll111ll1_opy_,)))
    for t in bstack111l1l1l_opy_:
      t.start()
    for t in bstack111l1l1l_opy_:
      results.append(t.join())
    bstack11l1l1111_opy_ = {}
    for item in results:
      hub_url = item[bstack111l11_opy_ (u"ࠫ࡭ࡻࡢࡠࡷࡵࡰࠬࡾ")]
      latency = item[bstack111l11_opy_ (u"ࠬࡲࡡࡵࡧࡱࡧࡾ࠭ࡿ")]
      bstack11l1l1111_opy_[hub_url] = latency
    bstack1l1l1l111l_opy_ = min(bstack11l1l1111_opy_, key= lambda x: bstack11l1l1111_opy_[x])
    bstack1l1l11l11_opy_ = bstack1l1l1l111l_opy_
    logger.debug(bstack1l1l1111ll_opy_.format(bstack1l1l1l111l_opy_))
  except Exception as e:
    logger.debug(bstack1lll111l1_opy_.format(e))
from bstack_utils.messages import *
from bstack_utils import bstack1l1l1l1l1_opy_
from bstack_utils.config import Config
from bstack_utils.helper import bstack1l11l111_opy_, bstack1lllll1lll_opy_, bstack1lllll11l_opy_, bstack1ll111l1ll_opy_, bstack1l11lll11_opy_, \
  Notset, bstack11ll111ll_opy_, \
  bstack1l11l1l11l_opy_, bstack1l1l1l11_opy_, bstack1l111l11l_opy_, bstack1l111ll1_opy_, bstack11l1l111_opy_, bstack1ll1l11l11_opy_, \
  bstack111l1l1ll_opy_, \
  bstack1ll11111l1_opy_, bstack11l1l1ll_opy_, bstack111llllll_opy_, bstack11l1l1l11_opy_, \
  bstack1l1l1lll11_opy_, bstack11ll11l1l_opy_, bstack1ll11l1l11_opy_
from bstack_utils.bstack11ll1ll1_opy_ import bstack1lllll1l1_opy_
from bstack_utils.bstack1ll1lll1l_opy_ import bstack1ll1lll11l_opy_
from bstack_utils.bstack1ll11ll111_opy_ import bstack1l1l11llll_opy_, bstack111111l1_opy_
from bstack_utils.bstack1l1l1l1l1l_opy_ import bstack1lll1ll1l_opy_
from bstack_utils.bstack1l1lll1lll_opy_ import bstack1l1lll1lll_opy_
from bstack_utils.proxy import bstack1l1l11l11l_opy_, bstack1l11ll11l1_opy_, bstack1llll1l11_opy_, bstack111ll1111_opy_
import bstack_utils.bstack1111llll_opy_ as bstack1llll11l_opy_
from browserstack_sdk.bstack11111lll1_opy_ import *
from browserstack_sdk.bstack111111lll_opy_ import *
from bstack_utils.bstack1llll1ll11_opy_ import bstack1l1l11ll11_opy_
bstack1lll1111l_opy_ = bstack111l11_opy_ (u"࠭ࠠࠡ࠱࠭ࠤࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽ࠡࠬ࠲ࡠࡳࠦࠠࡪࡨࠫࡴࡦ࡭ࡥࠡ࠿ࡀࡁࠥࡼ࡯ࡪࡦࠣ࠴࠮ࠦࡻ࡝ࡰࠣࠤࠥࡺࡲࡺࡽ࡟ࡲࠥࡩ࡯࡯ࡵࡷࠤ࡫ࡹࠠ࠾ࠢࡵࡩࡶࡻࡩࡳࡧࠫࡠࠬ࡬ࡳ࡝ࠩࠬ࠿ࡡࡴࠠࠡࠢࠣࠤ࡫ࡹ࠮ࡢࡲࡳࡩࡳࡪࡆࡪ࡮ࡨࡗࡾࡴࡣࠩࡤࡶࡸࡦࡩ࡫ࡠࡲࡤࡸ࡭࠲ࠠࡋࡕࡒࡒ࠳ࡹࡴࡳ࡫ࡱ࡫࡮࡬ࡹࠩࡲࡢ࡭ࡳࡪࡥࡹࠫࠣ࠯ࠥࠨ࠺ࠣࠢ࠮ࠤࡏ࡙ࡏࡏ࠰ࡶࡸࡷ࡯࡮ࡨ࡫ࡩࡽ࠭ࡐࡓࡐࡐ࠱ࡴࡦࡸࡳࡦࠪࠫࡥࡼࡧࡩࡵࠢࡱࡩࡼࡖࡡࡨࡧ࠵࠲ࡪࡼࡡ࡭ࡷࡤࡸࡪ࠮ࠢࠩࠫࠣࡁࡃࠦࡻࡾࠤ࠯ࠤࡡ࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡧࡦࡶࡖࡩࡸࡹࡩࡰࡰࡇࡩࡹࡧࡩ࡭ࡵࠥࢁࡡ࠭ࠩࠪࠫ࡞ࠦ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠢ࡞ࠫࠣ࠯ࠥࠨࠬ࡝࡞ࡱࠦ࠮ࡢ࡮ࠡࠢࠣࠤࢂࡩࡡࡵࡥ࡫ࠬࡪࡾࠩࡼ࡞ࡱࠤࠥࠦࠠࡾ࡞ࡱࠤࠥࢃ࡜࡯ࠢࠣ࠳࠯ࠦ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࠣ࠮࠴࠭ࢀ")
bstack1llll1111l_opy_ = bstack111l11_opy_ (u"ࠧ࡝ࡰ࠲࠮ࠥࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾ࠢ࠭࠳ࡡࡴࡣࡰࡰࡶࡸࠥࡨࡳࡵࡣࡦ࡯ࡤࡶࡡࡵࡪࠣࡁࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࡟ࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࠱ࡰࡪࡴࡧࡵࡪࠣ࠱ࠥ࠹࡝࡝ࡰࡦࡳࡳࡹࡴࠡࡤࡶࡸࡦࡩ࡫ࡠࡥࡤࡴࡸࠦ࠽ࠡࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࡛ࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻ࠴࡬ࡦࡰࡪࡸ࡭ࠦ࠭ࠡ࠳ࡠࡠࡳࡩ࡯࡯ࡵࡷࠤࡵࡥࡩ࡯ࡦࡨࡼࠥࡃࠠࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻࡡࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠳࡟࡟ࡲࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸࠣࡁࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡸࡲࡩࡤࡧࠫ࠴࠱ࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠴ࠫ࡟ࡲࡨࡵ࡮ࡴࡶࠣ࡭ࡲࡶ࡯ࡳࡶࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠴ࡠࡤࡶࡸࡦࡩ࡫ࠡ࠿ࠣࡶࡪࡷࡵࡪࡴࡨࠬࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤࠬ࠿ࡡࡴࡩ࡮ࡲࡲࡶࡹࡥࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶ࠷ࡣࡧࡹࡴࡢࡥ࡮࠲ࡨ࡮ࡲࡰ࡯࡬ࡹࡲ࠴࡬ࡢࡷࡱࡧ࡭ࠦ࠽ࠡࡣࡶࡽࡳࡩࠠࠩ࡮ࡤࡹࡳࡩࡨࡐࡲࡷ࡭ࡴࡴࡳࠪࠢࡀࡂࠥࢁ࡜࡯࡮ࡨࡸࠥࡩࡡࡱࡵ࠾ࡠࡳࡺࡲࡺࠢࡾࡠࡳࡩࡡࡱࡵࠣࡁࠥࡐࡓࡐࡐ࠱ࡴࡦࡸࡳࡦࠪࡥࡷࡹࡧࡣ࡬ࡡࡦࡥࡵࡹࠩ࡝ࡰࠣࠤࢂࠦࡣࡢࡶࡦ࡬࠭࡫ࡸࠪࠢࡾࡠࡳࠦࠠࠡࠢࢀࡠࡳࠦࠠࡳࡧࡷࡹࡷࡴࠠࡢࡹࡤ࡭ࡹࠦࡩ࡮ࡲࡲࡶࡹࡥࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶ࠷ࡣࡧࡹࡴࡢࡥ࡮࠲ࡨ࡮ࡲࡰ࡯࡬ࡹࡲ࠴ࡣࡰࡰࡱࡩࡨࡺࠨࡼ࡞ࡱࠤࠥࠦࠠࡸࡵࡈࡲࡩࡶ࡯ࡪࡰࡷ࠾ࠥࡦࡷࡴࡵ࠽࠳࠴ࡩࡤࡱ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࡁࡦࡥࡵࡹ࠽ࠥࡽࡨࡲࡨࡵࡤࡦࡗࡕࡍࡈࡵ࡭ࡱࡱࡱࡩࡳࡺࠨࡋࡕࡒࡒ࠳ࡹࡴࡳ࡫ࡱ࡫࡮࡬ࡹࠩࡥࡤࡴࡸ࠯ࠩࡾࡢ࠯ࡠࡳࠦࠠࠡࠢ࠱࠲࠳ࡲࡡࡶࡰࡦ࡬ࡔࡶࡴࡪࡱࡱࡷࡡࡴࠠࠡࡿࠬࡠࡳࢃ࡜࡯࠱࠭ࠤࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽ࠡࠬ࠲ࡠࡳ࠭ࢁ")
from ._version import __version__
bstack1l1l11l1_opy_ = None
CONFIG = {}
bstack1ll11ll1ll_opy_ = {}
bstack1l11lll1l_opy_ = {}
bstack1ll111l1_opy_ = None
bstack1lll1llll1_opy_ = None
bstack1l11l11l1_opy_ = None
bstack1111111l1_opy_ = -1
bstack1l1ll1111l_opy_ = 0
bstack111llll11_opy_ = bstack111lll1l_opy_
bstack1l1l1llll1_opy_ = 1
bstack111lll1ll_opy_ = False
bstack111111111_opy_ = False
bstack1lll1ll11_opy_ = bstack111l11_opy_ (u"ࠨࠩࢂ")
bstack1l11ll1l_opy_ = bstack111l11_opy_ (u"ࠩࠪࢃ")
bstack1lll11l11_opy_ = False
bstack1ll1l11l1_opy_ = True
bstack111ll1l11_opy_ = bstack111l11_opy_ (u"ࠪࠫࢄ")
bstack1l1l1ll1l1_opy_ = []
bstack1l1l11l11_opy_ = bstack111l11_opy_ (u"ࠫࠬࢅ")
bstack1ll1l1ll11_opy_ = False
bstack1l1lll1111_opy_ = None
bstack1lll1l11_opy_ = None
bstack1ll1111l1_opy_ = None
bstack1ll1ll1l1_opy_ = -1
bstack11l11l11_opy_ = os.path.join(os.path.expanduser(bstack111l11_opy_ (u"ࠬࢄࠧࢆ")), bstack111l11_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ࢇ"), bstack111l11_opy_ (u"ࠧ࠯ࡴࡲࡦࡴࡺ࠭ࡳࡧࡳࡳࡷࡺ࠭ࡩࡧ࡯ࡴࡪࡸ࠮࡫ࡵࡲࡲࠬ࢈"))
bstack1l1l1ll11_opy_ = 0
bstack11111llll_opy_ = 0
bstack1ll11l1l_opy_ = []
bstack1l1llll1_opy_ = []
bstack11lllllll_opy_ = []
bstack1l11llll1l_opy_ = []
bstack1ll11l111_opy_ = bstack111l11_opy_ (u"ࠨࠩࢉ")
bstack11llllll_opy_ = bstack111l11_opy_ (u"ࠩࠪࢊ")
bstack1ll11lll_opy_ = False
bstack1l1lll11_opy_ = False
bstack1l1lll11l_opy_ = {}
bstack1ll111l11l_opy_ = None
bstack11l1lll1_opy_ = None
bstack111l1l11l_opy_ = None
bstack1ll1l1lll1_opy_ = None
bstack1ll1l11l_opy_ = None
bstack11l1l111l_opy_ = None
bstack1l11ll11_opy_ = None
bstack1l1ll1l1_opy_ = None
bstack1llll1l1ll_opy_ = None
bstack1ll1l1ll1l_opy_ = None
bstack1lll1llll_opy_ = None
bstack111l1l11_opy_ = None
bstack111l1l1l1_opy_ = None
bstack1l1ll1l11l_opy_ = None
bstack1llll111l_opy_ = None
bstack1llll1ll_opy_ = None
bstack111l1llll_opy_ = None
bstack1llll1lll1_opy_ = None
bstack1lll1ll1ll_opy_ = None
bstack1l111111_opy_ = None
bstack11lll1l1_opy_ = None
bstack1l1ll11l_opy_ = False
bstack11111l11l_opy_ = bstack111l11_opy_ (u"ࠥࠦࢋ")
logger = bstack1l1l1l1l1_opy_.get_logger(__name__, bstack111llll11_opy_)
bstack1l11l111ll_opy_ = Config.bstack1l1l1l1111_opy_()
percy = bstack1l11l11l1l_opy_()
bstack1lll1l1l1_opy_ = bstack1l11ll1lll_opy_()
def bstack111111ll1_opy_():
  global CONFIG
  global bstack1ll11lll_opy_
  global bstack1l11l111ll_opy_
  bstack1l1llllll_opy_ = bstack1l1l1l1ll1_opy_(CONFIG)
  if (bstack111l11_opy_ (u"ࠫࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ࢌ") in bstack1l1llllll_opy_ and str(bstack1l1llllll_opy_[bstack111l11_opy_ (u"ࠬࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧࢍ")]).lower() == bstack111l11_opy_ (u"࠭ࡴࡳࡷࡨࠫࢎ")):
    bstack1ll11lll_opy_ = True
  bstack1l11l111ll_opy_.bstack1l1lll11l1_opy_(bstack1l1llllll_opy_.get(bstack111l11_opy_ (u"ࠧࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫ࢏"), False))
def bstack1l1ll1lll_opy_():
  from appium.version import version as appium_version
  return version.parse(appium_version)
def bstack1lll1l1ll_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack1ll1l1l11_opy_():
  args = sys.argv
  for i in range(len(args)):
    if bstack111l11_opy_ (u"ࠣ࠯࠰ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡥࡲࡲ࡫࡯ࡧࡧ࡫࡯ࡩࠧ࢐") == args[i].lower() or bstack111l11_opy_ (u"ࠤ࠰࠱ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡴࡦࡪࡩࠥ࢑") == args[i].lower():
      path = args[i + 1]
      sys.argv.remove(args[i])
      sys.argv.remove(path)
      global bstack111ll1l11_opy_
      bstack111ll1l11_opy_ += bstack111l11_opy_ (u"ࠪ࠱࠲ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡇࡴࡴࡦࡪࡩࡉ࡭ࡱ࡫ࠠࠨ࢒") + path
      return path
  return None
bstack111111l11_opy_ = re.compile(bstack111l11_opy_ (u"ࡶࠧ࠴ࠪࡀ࡞ࠧࡿ࠭࠴ࠪࡀࠫࢀ࠲࠯ࡅࠢ࢓"))
def bstack1l1ll111ll_opy_(loader, node):
  value = loader.construct_scalar(node)
  for group in bstack111111l11_opy_.findall(value):
    if group is not None and os.environ.get(group) is not None:
      value = value.replace(bstack111l11_opy_ (u"ࠧࠪࡻࠣ࢔") + group + bstack111l11_opy_ (u"ࠨࡽࠣ࢕"), os.environ.get(group))
  return value
def bstack1lll1ll11l_opy_():
  bstack1ll1l11111_opy_ = bstack1ll1l1l11_opy_()
  if bstack1ll1l11111_opy_ and os.path.exists(os.path.abspath(bstack1ll1l11111_opy_)):
    fileName = bstack1ll1l11111_opy_
  if bstack111l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡐࡐࡉࡍࡌࡥࡆࡊࡎࡈࠫ࢖") in os.environ and os.path.exists(
          os.path.abspath(os.environ[bstack111l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡑࡑࡊࡎࡍ࡟ࡇࡋࡏࡉࠬࢗ")])) and not bstack111l11_opy_ (u"ࠩࡩ࡭ࡱ࡫ࡎࡢ࡯ࡨࠫ࢘") in locals():
    fileName = os.environ[bstack111l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡆࡓࡓࡌࡉࡈࡡࡉࡍࡑࡋ࢙ࠧ")]
  if bstack111l11_opy_ (u"ࠫ࡫࡯࡬ࡦࡐࡤࡱࡪ࢚࠭") in locals():
    bstack111lll_opy_ = os.path.abspath(fileName)
  else:
    bstack111lll_opy_ = bstack111l11_opy_ (u"࢛ࠬ࠭")
  bstack1l111lll1_opy_ = os.getcwd()
  bstack1l1ll11l1l_opy_ = bstack111l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡿ࡭࡭ࠩ࢜")
  bstack1l1l11111l_opy_ = bstack111l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹࡢ࡯࡯ࠫ࢝")
  while (not os.path.exists(bstack111lll_opy_)) and bstack1l111lll1_opy_ != bstack111l11_opy_ (u"ࠣࠤ࢞"):
    bstack111lll_opy_ = os.path.join(bstack1l111lll1_opy_, bstack1l1ll11l1l_opy_)
    if not os.path.exists(bstack111lll_opy_):
      bstack111lll_opy_ = os.path.join(bstack1l111lll1_opy_, bstack1l1l11111l_opy_)
    if bstack1l111lll1_opy_ != os.path.dirname(bstack1l111lll1_opy_):
      bstack1l111lll1_opy_ = os.path.dirname(bstack1l111lll1_opy_)
    else:
      bstack1l111lll1_opy_ = bstack111l11_opy_ (u"ࠤࠥ࢟")
  if not os.path.exists(bstack111lll_opy_):
    bstack11ll1lll1_opy_(
      bstack1llll1llll_opy_.format(os.getcwd()))
  try:
    with open(bstack111lll_opy_, bstack111l11_opy_ (u"ࠪࡶࠬࢠ")) as stream:
      yaml.add_implicit_resolver(bstack111l11_opy_ (u"ࠦࠦࡶࡡࡵࡪࡨࡼࠧࢡ"), bstack111111l11_opy_)
      yaml.add_constructor(bstack111l11_opy_ (u"ࠧࠧࡰࡢࡶ࡫ࡩࡽࠨࢢ"), bstack1l1ll111ll_opy_)
      config = yaml.load(stream, yaml.FullLoader)
      return config
  except:
    with open(bstack111lll_opy_, bstack111l11_opy_ (u"࠭ࡲࠨࢣ")) as stream:
      try:
        config = yaml.safe_load(stream)
        return config
      except yaml.YAMLError as exc:
        bstack11ll1lll1_opy_(bstack1111ll11_opy_.format(str(exc)))
def bstack1ll1ll11l1_opy_(config):
  bstack1lllll111_opy_ = bstack1l11llll1_opy_(config)
  for option in list(bstack1lllll111_opy_):
    if option.lower() in bstack1111l1111_opy_ and option != bstack1111l1111_opy_[option.lower()]:
      bstack1lllll111_opy_[bstack1111l1111_opy_[option.lower()]] = bstack1lllll111_opy_[option]
      del bstack1lllll111_opy_[option]
  return config
def bstack111ll111l_opy_():
  global bstack1l11lll1l_opy_
  for key, bstack1lll1l1l11_opy_ in bstack1lll1ll111_opy_.items():
    if isinstance(bstack1lll1l1l11_opy_, list):
      for var in bstack1lll1l1l11_opy_:
        if var in os.environ and os.environ[var] and str(os.environ[var]).strip():
          bstack1l11lll1l_opy_[key] = os.environ[var]
          break
    elif bstack1lll1l1l11_opy_ in os.environ and os.environ[bstack1lll1l1l11_opy_] and str(os.environ[bstack1lll1l1l11_opy_]).strip():
      bstack1l11lll1l_opy_[key] = os.environ[bstack1lll1l1l11_opy_]
  if bstack111l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࡤࡏࡄࡆࡐࡗࡍࡋࡏࡅࡓࠩࢤ") in os.environ:
    bstack1l11lll1l_opy_[bstack111l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬࢥ")] = {}
    bstack1l11lll1l_opy_[bstack111l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ࢦ")][bstack111l11_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬࢧ")] = os.environ[bstack111l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡉࡁࡍࡡࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗ࠭ࢨ")]
def bstack1lll11l11l_opy_():
  global bstack1ll11ll1ll_opy_
  global bstack111ll1l11_opy_
  for idx, val in enumerate(sys.argv):
    if idx < len(sys.argv) and bstack111l11_opy_ (u"ࠬ࠳࠭ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨࢩ").lower() == val.lower():
      bstack1ll11ll1ll_opy_[bstack111l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪࢪ")] = {}
      bstack1ll11ll1ll_opy_[bstack111l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫࢫ")][bstack111l11_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪࢬ")] = sys.argv[idx + 1]
      del sys.argv[idx:idx + 2]
      break
  for key, bstack11111l11_opy_ in bstack1l1111ll1_opy_.items():
    if isinstance(bstack11111l11_opy_, list):
      for idx, val in enumerate(sys.argv):
        for var in bstack11111l11_opy_:
          if idx < len(sys.argv) and bstack111l11_opy_ (u"ࠩ࠰࠱ࠬࢭ") + var.lower() == val.lower() and not key in bstack1ll11ll1ll_opy_:
            bstack1ll11ll1ll_opy_[key] = sys.argv[idx + 1]
            bstack111ll1l11_opy_ += bstack111l11_opy_ (u"ࠪࠤ࠲࠳ࠧࢮ") + var + bstack111l11_opy_ (u"ࠫࠥ࠭ࢯ") + sys.argv[idx + 1]
            del sys.argv[idx:idx + 2]
            break
    else:
      for idx, val in enumerate(sys.argv):
        if idx < len(sys.argv) and bstack111l11_opy_ (u"ࠬ࠳࠭ࠨࢰ") + bstack11111l11_opy_.lower() == val.lower() and not key in bstack1ll11ll1ll_opy_:
          bstack1ll11ll1ll_opy_[key] = sys.argv[idx + 1]
          bstack111ll1l11_opy_ += bstack111l11_opy_ (u"࠭ࠠ࠮࠯ࠪࢱ") + bstack11111l11_opy_ + bstack111l11_opy_ (u"ࠧࠡࠩࢲ") + sys.argv[idx + 1]
          del sys.argv[idx:idx + 2]
def bstack111ll1ll_opy_(config):
  bstack1llll11111_opy_ = config.keys()
  for bstack1ll1l11lll_opy_, bstack1l11llllll_opy_ in bstack1ll1l1111l_opy_.items():
    if bstack1l11llllll_opy_ in bstack1llll11111_opy_:
      config[bstack1ll1l11lll_opy_] = config[bstack1l11llllll_opy_]
      del config[bstack1l11llllll_opy_]
  for bstack1ll1l11lll_opy_, bstack1l11llllll_opy_ in bstack1ll11l1lll_opy_.items():
    if isinstance(bstack1l11llllll_opy_, list):
      for bstack1ll1lll1l1_opy_ in bstack1l11llllll_opy_:
        if bstack1ll1lll1l1_opy_ in bstack1llll11111_opy_:
          config[bstack1ll1l11lll_opy_] = config[bstack1ll1lll1l1_opy_]
          del config[bstack1ll1lll1l1_opy_]
          break
    elif bstack1l11llllll_opy_ in bstack1llll11111_opy_:
      config[bstack1ll1l11lll_opy_] = config[bstack1l11llllll_opy_]
      del config[bstack1l11llllll_opy_]
  for bstack1ll1lll1l1_opy_ in list(config):
    for bstack1ll1l1l1ll_opy_ in bstack11l111l11_opy_:
      if bstack1ll1lll1l1_opy_.lower() == bstack1ll1l1l1ll_opy_.lower() and bstack1ll1lll1l1_opy_ != bstack1ll1l1l1ll_opy_:
        config[bstack1ll1l1l1ll_opy_] = config[bstack1ll1lll1l1_opy_]
        del config[bstack1ll1lll1l1_opy_]
  bstack111l1111_opy_ = []
  if bstack111l11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫࢳ") in config:
    bstack111l1111_opy_ = config[bstack111l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬࢴ")]
  for platform in bstack111l1111_opy_:
    for bstack1ll1lll1l1_opy_ in list(platform):
      for bstack1ll1l1l1ll_opy_ in bstack11l111l11_opy_:
        if bstack1ll1lll1l1_opy_.lower() == bstack1ll1l1l1ll_opy_.lower() and bstack1ll1lll1l1_opy_ != bstack1ll1l1l1ll_opy_:
          platform[bstack1ll1l1l1ll_opy_] = platform[bstack1ll1lll1l1_opy_]
          del platform[bstack1ll1lll1l1_opy_]
  for bstack1ll1l11lll_opy_, bstack1l11llllll_opy_ in bstack1ll11l1lll_opy_.items():
    for platform in bstack111l1111_opy_:
      if isinstance(bstack1l11llllll_opy_, list):
        for bstack1ll1lll1l1_opy_ in bstack1l11llllll_opy_:
          if bstack1ll1lll1l1_opy_ in platform:
            platform[bstack1ll1l11lll_opy_] = platform[bstack1ll1lll1l1_opy_]
            del platform[bstack1ll1lll1l1_opy_]
            break
      elif bstack1l11llllll_opy_ in platform:
        platform[bstack1ll1l11lll_opy_] = platform[bstack1l11llllll_opy_]
        del platform[bstack1l11llllll_opy_]
  for bstack1111l11ll_opy_ in bstack1l1ll11lll_opy_:
    if bstack1111l11ll_opy_ in config:
      if not bstack1l1ll11lll_opy_[bstack1111l11ll_opy_] in config:
        config[bstack1l1ll11lll_opy_[bstack1111l11ll_opy_]] = {}
      config[bstack1l1ll11lll_opy_[bstack1111l11ll_opy_]].update(config[bstack1111l11ll_opy_])
      del config[bstack1111l11ll_opy_]
  for platform in bstack111l1111_opy_:
    for bstack1111l11ll_opy_ in bstack1l1ll11lll_opy_:
      if bstack1111l11ll_opy_ in list(platform):
        if not bstack1l1ll11lll_opy_[bstack1111l11ll_opy_] in platform:
          platform[bstack1l1ll11lll_opy_[bstack1111l11ll_opy_]] = {}
        platform[bstack1l1ll11lll_opy_[bstack1111l11ll_opy_]].update(platform[bstack1111l11ll_opy_])
        del platform[bstack1111l11ll_opy_]
  config = bstack1ll1ll11l1_opy_(config)
  return config
def bstack1ll1ll1lll_opy_(config):
  global bstack1l11ll1l_opy_
  if bstack111l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧࢵ") in config and str(config[bstack111l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨࢶ")]).lower() != bstack111l11_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫࢷ"):
    if not bstack111l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪࢸ") in config:
      config[bstack111l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫࢹ")] = {}
    if not bstack111l11_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪࢺ") in config[bstack111l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ࢻ")]:
      bstack11ll1l1ll_opy_ = datetime.datetime.now()
      bstack1l11l11ll1_opy_ = bstack11ll1l1ll_opy_.strftime(bstack111l11_opy_ (u"ࠪࠩࡩࡥࠥࡣࡡࠨࡌࠪࡓࠧࢼ"))
      hostname = socket.gethostname()
      bstack1llllll11_opy_ = bstack111l11_opy_ (u"ࠫࠬࢽ").join(random.choices(string.ascii_lowercase + string.digits, k=4))
      identifier = bstack111l11_opy_ (u"ࠬࢁࡽࡠࡽࢀࡣࢀࢃࠧࢾ").format(bstack1l11l11ll1_opy_, hostname, bstack1llllll11_opy_)
      config[bstack111l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪࢿ")][bstack111l11_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩࣀ")] = identifier
    bstack1l11ll1l_opy_ = config[bstack111l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬࣁ")][bstack111l11_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫࣂ")]
  return config
def bstack1l1ll1ll1_opy_():
  bstack1lll1l11ll_opy_ =  bstack1l111ll1_opy_()[bstack111l11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠩࣃ")]
  return bstack1lll1l11ll_opy_ if bstack1lll1l11ll_opy_ else -1
def bstack1lllll1ll_opy_(bstack1lll1l11ll_opy_):
  global CONFIG
  if not bstack111l11_opy_ (u"ࠫࠩࢁࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࢂ࠭ࣄ") in CONFIG[bstack111l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࣅ")]:
    return
  CONFIG[bstack111l11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨࣆ")] = CONFIG[bstack111l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩࣇ")].replace(
    bstack111l11_opy_ (u"ࠨࠦࡾࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࡿࠪࣈ"),
    str(bstack1lll1l11ll_opy_)
  )
def bstack1lllll11ll_opy_():
  global CONFIG
  if not bstack111l11_opy_ (u"ࠩࠧࡿࡉࡇࡔࡆࡡࡗࡍࡒࡋࡽࠨࣉ") in CONFIG[bstack111l11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ࣊")]:
    return
  bstack11ll1l1ll_opy_ = datetime.datetime.now()
  bstack1l11l11ll1_opy_ = bstack11ll1l1ll_opy_.strftime(bstack111l11_opy_ (u"ࠫࠪࡪ࠭ࠦࡤ࠰ࠩࡍࡀࠥࡎࠩ࣋"))
  CONFIG[bstack111l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ࣌")] = CONFIG[bstack111l11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ࣍")].replace(
    bstack111l11_opy_ (u"ࠧࠥࡽࡇࡅ࡙ࡋ࡟ࡕࡋࡐࡉࢂ࠭࣎"),
    bstack1l11l11ll1_opy_
  )
def bstack1ll111l1l_opy_():
  global CONFIG
  if bstack111l11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴ࣏ࠪ") in CONFIG and not bool(CONFIG[bstack111l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵ࣐ࠫ")]):
    del CONFIG[bstack111l11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶ࣑ࠬ")]
    return
  if not bstack111l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࣒࠭") in CONFIG:
    CONFIG[bstack111l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸ࣓ࠧ")] = bstack111l11_opy_ (u"࠭ࠣࠥࡽࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࡾࠩࣔ")
  if bstack111l11_opy_ (u"ࠧࠥࡽࡇࡅ࡙ࡋ࡟ࡕࡋࡐࡉࢂ࠭ࣕ") in CONFIG[bstack111l11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪࣖ")]:
    bstack1lllll11ll_opy_()
    os.environ[bstack111l11_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡡࡆࡓࡒࡈࡉࡏࡇࡇࡣࡇ࡛ࡉࡍࡆࡢࡍࡉ࠭ࣗ")] = CONFIG[bstack111l11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬࣘ")]
  if not bstack111l11_opy_ (u"ࠫࠩࢁࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࢂ࠭ࣙ") in CONFIG[bstack111l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࣚ")]:
    return
  bstack1lll1l11ll_opy_ = bstack111l11_opy_ (u"࠭ࠧࣛ")
  bstack11ll111l1_opy_ = bstack1l1ll1ll1_opy_()
  if bstack11ll111l1_opy_ != -1:
    bstack1lll1l11ll_opy_ = bstack111l11_opy_ (u"ࠧࡄࡋࠣࠫࣜ") + str(bstack11ll111l1_opy_)
  if bstack1lll1l11ll_opy_ == bstack111l11_opy_ (u"ࠨࠩࣝ"):
    bstack11l1ll1l_opy_ = bstack1ll111ll11_opy_(CONFIG[bstack111l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬࣞ")])
    if bstack11l1ll1l_opy_ != -1:
      bstack1lll1l11ll_opy_ = str(bstack11l1ll1l_opy_)
  if bstack1lll1l11ll_opy_:
    bstack1lllll1ll_opy_(bstack1lll1l11ll_opy_)
    os.environ[bstack111l11_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡢࡇࡔࡓࡂࡊࡐࡈࡈࡤࡈࡕࡊࡎࡇࡣࡎࡊࠧࣟ")] = CONFIG[bstack111l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭࣠")]
def bstack1lllll11l1_opy_(bstack1lll11ll1_opy_, bstack1l11ll111_opy_, path):
  bstack1lll1l1l_opy_ = {
    bstack111l11_opy_ (u"ࠬ࡯ࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ࣡"): bstack1l11ll111_opy_
  }
  if os.path.exists(path):
    bstack1111ll1l1_opy_ = json.load(open(path, bstack111l11_opy_ (u"࠭ࡲࡣࠩ࣢")))
  else:
    bstack1111ll1l1_opy_ = {}
  bstack1111ll1l1_opy_[bstack1lll11ll1_opy_] = bstack1lll1l1l_opy_
  with open(path, bstack111l11_opy_ (u"ࠢࡸࣣ࠭ࠥ")) as outfile:
    json.dump(bstack1111ll1l1_opy_, outfile)
def bstack1ll111ll11_opy_(bstack1lll11ll1_opy_):
  bstack1lll11ll1_opy_ = str(bstack1lll11ll1_opy_)
  bstack11llll1ll_opy_ = os.path.join(os.path.expanduser(bstack111l11_opy_ (u"ࠨࢀࠪࣤ")), bstack111l11_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩࣥ"))
  try:
    if not os.path.exists(bstack11llll1ll_opy_):
      os.makedirs(bstack11llll1ll_opy_)
    file_path = os.path.join(os.path.expanduser(bstack111l11_opy_ (u"ࠪࢂࣦࠬ")), bstack111l11_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫࣧ"), bstack111l11_opy_ (u"ࠬ࠴ࡢࡶ࡫࡯ࡨ࠲ࡴࡡ࡮ࡧ࠰ࡧࡦࡩࡨࡦ࠰࡭ࡷࡴࡴࠧࣨ"))
    if not os.path.isfile(file_path):
      with open(file_path, bstack111l11_opy_ (u"࠭ࡷࠨࣩ")):
        pass
      with open(file_path, bstack111l11_opy_ (u"ࠢࡸ࠭ࠥ࣪")) as outfile:
        json.dump({}, outfile)
    with open(file_path, bstack111l11_opy_ (u"ࠨࡴࠪ࣫")) as bstack1l1ll111l_opy_:
      bstack1lll111l11_opy_ = json.load(bstack1l1ll111l_opy_)
    if bstack1lll11ll1_opy_ in bstack1lll111l11_opy_:
      bstack1llll1111_opy_ = bstack1lll111l11_opy_[bstack1lll11ll1_opy_][bstack111l11_opy_ (u"ࠩ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭࣬")]
      bstack11lll1l1l_opy_ = int(bstack1llll1111_opy_) + 1
      bstack1lllll11l1_opy_(bstack1lll11ll1_opy_, bstack11lll1l1l_opy_, file_path)
      return bstack11lll1l1l_opy_
    else:
      bstack1lllll11l1_opy_(bstack1lll11ll1_opy_, 1, file_path)
      return 1
  except Exception as e:
    logger.warn(bstack1l11llll11_opy_.format(str(e)))
    return -1
def bstack1l11lllll_opy_(config):
  if not config[bstack111l11_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩ࣭ࠬ")] or not config[bstack111l11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿ࣮ࠧ")]:
    return True
  else:
    return False
def bstack1l11l1l1ll_opy_(config, index=0):
  global bstack1lll11l11_opy_
  bstack11l1l11ll_opy_ = {}
  caps = bstack111ll1lll_opy_ + bstack1l11l1llll_opy_
  if bstack1lll11l11_opy_:
    caps += bstack11l11l1l_opy_
  for key in config:
    if key in caps + [bstack111l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ࣯")]:
      continue
    bstack11l1l11ll_opy_[key] = config[key]
  if bstack111l11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࣰࠩ") in config:
    for bstack1llll11lll_opy_ in config[bstack111l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࣱࠪ")][index]:
      if bstack1llll11lll_opy_ in caps + [bstack111l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪࣲ࠭"), bstack111l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪࣳ")]:
        continue
      bstack11l1l11ll_opy_[bstack1llll11lll_opy_] = config[bstack111l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ࣴ")][index][bstack1llll11lll_opy_]
  bstack11l1l11ll_opy_[bstack111l11_opy_ (u"ࠫ࡭ࡵࡳࡵࡐࡤࡱࡪ࠭ࣵ")] = socket.gethostname()
  if bstack111l11_opy_ (u"ࠬࡼࡥࡳࡵ࡬ࡳࡳࣶ࠭") in bstack11l1l11ll_opy_:
    del (bstack11l1l11ll_opy_[bstack111l11_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴࠧࣷ")])
  return bstack11l1l11ll_opy_
def bstack11l11llll_opy_(config):
  global bstack1lll11l11_opy_
  bstack11l11111l_opy_ = {}
  caps = bstack1l11l1llll_opy_
  if bstack1lll11l11_opy_:
    caps += bstack11l11l1l_opy_
  for key in caps:
    if key in config:
      bstack11l11111l_opy_[key] = config[key]
  return bstack11l11111l_opy_
def bstack1l11l11l_opy_(bstack11l1l11ll_opy_, bstack11l11111l_opy_):
  bstack1ll1111l11_opy_ = {}
  for key in bstack11l1l11ll_opy_.keys():
    if key in bstack1ll1l1111l_opy_:
      bstack1ll1111l11_opy_[bstack1ll1l1111l_opy_[key]] = bstack11l1l11ll_opy_[key]
    else:
      bstack1ll1111l11_opy_[key] = bstack11l1l11ll_opy_[key]
  for key in bstack11l11111l_opy_:
    if key in bstack1ll1l1111l_opy_:
      bstack1ll1111l11_opy_[bstack1ll1l1111l_opy_[key]] = bstack11l11111l_opy_[key]
    else:
      bstack1ll1111l11_opy_[key] = bstack11l11111l_opy_[key]
  return bstack1ll1111l11_opy_
def bstack111ll11ll_opy_(config, index=0):
  global bstack1lll11l11_opy_
  caps = {}
  config = copy.deepcopy(config)
  bstack11l11l1l1_opy_ = bstack1l11l111_opy_(bstack11lllll1l_opy_, config, logger)
  bstack11l11111l_opy_ = bstack11l11llll_opy_(config)
  bstack11l111111_opy_ = bstack1l11l1llll_opy_
  bstack11l111111_opy_ += bstack1l1ll1llll_opy_
  bstack11l11111l_opy_ = update(bstack11l11111l_opy_, bstack11l11l1l1_opy_)
  if bstack1lll11l11_opy_:
    bstack11l111111_opy_ += bstack11l11l1l_opy_
  if bstack111l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪࣸ") in config:
    if bstack111l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪࣹ࠭") in config[bstack111l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࣺࠬ")][index]:
      caps[bstack111l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨࣻ")] = config[bstack111l11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧࣼ")][index][bstack111l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪࣽ")]
    if bstack111l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧࣾ") in config[bstack111l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪࣿ")][index]:
      caps[bstack111l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩऀ")] = str(config[bstack111l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬँ")][index][bstack111l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫं")])
    bstack1l1ll1l111_opy_ = bstack1l11l111_opy_(bstack11lllll1l_opy_, config[bstack111l11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧः")][index], logger)
    bstack11l111111_opy_ += list(bstack1l1ll1l111_opy_.keys())
    for bstack11111l1ll_opy_ in bstack11l111111_opy_:
      if bstack11111l1ll_opy_ in config[bstack111l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨऄ")][index]:
        if bstack11111l1ll_opy_ == bstack111l11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨअ"):
          try:
            bstack1l1ll1l111_opy_[bstack11111l1ll_opy_] = str(config[bstack111l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪआ")][index][bstack11111l1ll_opy_] * 1.0)
          except:
            bstack1l1ll1l111_opy_[bstack11111l1ll_opy_] = str(config[bstack111l11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫइ")][index][bstack11111l1ll_opy_])
        else:
          bstack1l1ll1l111_opy_[bstack11111l1ll_opy_] = config[bstack111l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬई")][index][bstack11111l1ll_opy_]
        del (config[bstack111l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭उ")][index][bstack11111l1ll_opy_])
    bstack11l11111l_opy_ = update(bstack11l11111l_opy_, bstack1l1ll1l111_opy_)
  bstack11l1l11ll_opy_ = bstack1l11l1l1ll_opy_(config, index)
  for bstack1ll1lll1l1_opy_ in bstack1l11l1llll_opy_ + [bstack111l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩऊ"), bstack111l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ऋ")] + list(bstack11l11l1l1_opy_.keys()):
    if bstack1ll1lll1l1_opy_ in bstack11l1l11ll_opy_:
      bstack11l11111l_opy_[bstack1ll1lll1l1_opy_] = bstack11l1l11ll_opy_[bstack1ll1lll1l1_opy_]
      del (bstack11l1l11ll_opy_[bstack1ll1lll1l1_opy_])
  if bstack11ll111ll_opy_(config):
    bstack11l1l11ll_opy_[bstack111l11_opy_ (u"࠭ࡵࡴࡧ࡚࠷ࡈ࠭ऌ")] = True
    caps.update(bstack11l11111l_opy_)
    caps[bstack111l11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨऍ")] = bstack11l1l11ll_opy_
  else:
    bstack11l1l11ll_opy_[bstack111l11_opy_ (u"ࠨࡷࡶࡩ࡜࠹ࡃࠨऎ")] = False
    caps.update(bstack1l11l11l_opy_(bstack11l1l11ll_opy_, bstack11l11111l_opy_))
    if bstack111l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧए") in caps:
      caps[bstack111l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࠫऐ")] = caps[bstack111l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩऑ")]
      del (caps[bstack111l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪऒ")])
    if bstack111l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧओ") in caps:
      caps[bstack111l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠩऔ")] = caps[bstack111l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩक")]
      del (caps[bstack111l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪख")])
  return caps
def bstack1l1l1l111_opy_():
  global bstack1l1l11l11_opy_
  if bstack1lll1l1ll_opy_() <= version.parse(bstack111l11_opy_ (u"ࠪ࠷࠳࠷࠳࠯࠲ࠪग")):
    if bstack1l1l11l11_opy_ != bstack111l11_opy_ (u"ࠫࠬघ"):
      return bstack111l11_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࠳࠴ࠨङ") + bstack1l1l11l11_opy_ + bstack111l11_opy_ (u"ࠨ࠺࠹࠲࠲ࡻࡩ࠵ࡨࡶࡤࠥच")
    return bstack1l11ll11l_opy_
  if bstack1l1l11l11_opy_ != bstack111l11_opy_ (u"ࠧࠨछ"):
    return bstack111l11_opy_ (u"ࠣࡪࡷࡸࡵࡹ࠺࠰࠱ࠥज") + bstack1l1l11l11_opy_ + bstack111l11_opy_ (u"ࠤ࠲ࡻࡩ࠵ࡨࡶࡤࠥझ")
  return bstack1ll1111lll_opy_
def bstack11llll1l1_opy_(options):
  return hasattr(options, bstack111l11_opy_ (u"ࠪࡷࡪࡺ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶࡼࠫञ"))
def update(d, u):
  for k, v in u.items():
    if isinstance(v, collections.abc.Mapping):
      d[k] = update(d.get(k, {}), v)
    else:
      if isinstance(v, list):
        d[k] = d.get(k, []) + v
      else:
        d[k] = v
  return d
def bstack1ll1ll11l_opy_(options, bstack111l11ll_opy_):
  for bstack1l1l111lll_opy_ in bstack111l11ll_opy_:
    if bstack1l1l111lll_opy_ in [bstack111l11_opy_ (u"ࠫࡦࡸࡧࡴࠩट"), bstack111l11_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩठ")]:
      continue
    if bstack1l1l111lll_opy_ in options._experimental_options:
      options._experimental_options[bstack1l1l111lll_opy_] = update(options._experimental_options[bstack1l1l111lll_opy_],
                                                         bstack111l11ll_opy_[bstack1l1l111lll_opy_])
    else:
      options.add_experimental_option(bstack1l1l111lll_opy_, bstack111l11ll_opy_[bstack1l1l111lll_opy_])
  if bstack111l11_opy_ (u"࠭ࡡࡳࡩࡶࠫड") in bstack111l11ll_opy_:
    for arg in bstack111l11ll_opy_[bstack111l11_opy_ (u"ࠧࡢࡴࡪࡷࠬढ")]:
      options.add_argument(arg)
    del (bstack111l11ll_opy_[bstack111l11_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ण")])
  if bstack111l11_opy_ (u"ࠩࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭त") in bstack111l11ll_opy_:
    for ext in bstack111l11ll_opy_[bstack111l11_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧथ")]:
      options.add_extension(ext)
    del (bstack111l11ll_opy_[bstack111l11_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨद")])
def bstack1ll111111_opy_(options, bstack1l1l1111l1_opy_):
  if bstack111l11_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫध") in bstack1l1l1111l1_opy_:
    for bstack1l1ll1l1l_opy_ in bstack1l1l1111l1_opy_[bstack111l11_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬन")]:
      if bstack1l1ll1l1l_opy_ in options._preferences:
        options._preferences[bstack1l1ll1l1l_opy_] = update(options._preferences[bstack1l1ll1l1l_opy_], bstack1l1l1111l1_opy_[bstack111l11_opy_ (u"ࠧࡱࡴࡨࡪࡸ࠭ऩ")][bstack1l1ll1l1l_opy_])
      else:
        options.set_preference(bstack1l1ll1l1l_opy_, bstack1l1l1111l1_opy_[bstack111l11_opy_ (u"ࠨࡲࡵࡩ࡫ࡹࠧप")][bstack1l1ll1l1l_opy_])
  if bstack111l11_opy_ (u"ࠩࡤࡶ࡬ࡹࠧफ") in bstack1l1l1111l1_opy_:
    for arg in bstack1l1l1111l1_opy_[bstack111l11_opy_ (u"ࠪࡥࡷ࡭ࡳࠨब")]:
      options.add_argument(arg)
def bstack1l1l111111_opy_(options, bstack1llll11ll_opy_):
  if bstack111l11_opy_ (u"ࠫࡼ࡫ࡢࡷ࡫ࡨࡻࠬभ") in bstack1llll11ll_opy_:
    options.use_webview(bool(bstack1llll11ll_opy_[bstack111l11_opy_ (u"ࠬࡽࡥࡣࡸ࡬ࡩࡼ࠭म")]))
  bstack1ll1ll11l_opy_(options, bstack1llll11ll_opy_)
def bstack11l111ll_opy_(options, bstack1l11llll_opy_):
  for bstack1l111l1l_opy_ in bstack1l11llll_opy_:
    if bstack1l111l1l_opy_ in [bstack111l11_opy_ (u"࠭ࡴࡦࡥ࡫ࡲࡴࡲ࡯ࡨࡻࡓࡶࡪࡼࡩࡦࡹࠪय"), bstack111l11_opy_ (u"ࠧࡢࡴࡪࡷࠬर")]:
      continue
    options.set_capability(bstack1l111l1l_opy_, bstack1l11llll_opy_[bstack1l111l1l_opy_])
  if bstack111l11_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ऱ") in bstack1l11llll_opy_:
    for arg in bstack1l11llll_opy_[bstack111l11_opy_ (u"ࠩࡤࡶ࡬ࡹࠧल")]:
      options.add_argument(arg)
  if bstack111l11_opy_ (u"ࠪࡸࡪࡩࡨ࡯ࡱ࡯ࡳ࡬ࡿࡐࡳࡧࡹ࡭ࡪࡽࠧळ") in bstack1l11llll_opy_:
    options.bstack1l11ll1l1_opy_(bool(bstack1l11llll_opy_[bstack111l11_opy_ (u"ࠫࡹ࡫ࡣࡩࡰࡲࡰࡴ࡭ࡹࡑࡴࡨࡺ࡮࡫ࡷࠨऴ")]))
def bstack1ll11ll11_opy_(options, bstack1l11ll1l11_opy_):
  for bstack111ll111_opy_ in bstack1l11ll1l11_opy_:
    if bstack111ll111_opy_ in [bstack111l11_opy_ (u"ࠬࡧࡤࡥ࡫ࡷ࡭ࡴࡴࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩव"), bstack111l11_opy_ (u"࠭ࡡࡳࡩࡶࠫश")]:
      continue
    options._options[bstack111ll111_opy_] = bstack1l11ll1l11_opy_[bstack111ll111_opy_]
  if bstack111l11_opy_ (u"ࠧࡢࡦࡧ࡭ࡹ࡯࡯࡯ࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫष") in bstack1l11ll1l11_opy_:
    for bstack11l11l11l_opy_ in bstack1l11ll1l11_opy_[bstack111l11_opy_ (u"ࠨࡣࡧࡨ࡮ࡺࡩࡰࡰࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬस")]:
      options.bstack11lll1111_opy_(
        bstack11l11l11l_opy_, bstack1l11ll1l11_opy_[bstack111l11_opy_ (u"ࠩࡤࡨࡩ࡯ࡴࡪࡱࡱࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ह")][bstack11l11l11l_opy_])
  if bstack111l11_opy_ (u"ࠪࡥࡷ࡭ࡳࠨऺ") in bstack1l11ll1l11_opy_:
    for arg in bstack1l11ll1l11_opy_[bstack111l11_opy_ (u"ࠫࡦࡸࡧࡴࠩऻ")]:
      options.add_argument(arg)
def bstack1ll1l1lll_opy_(options, caps):
  if not hasattr(options, bstack111l11_opy_ (u"ࠬࡑࡅ़࡚ࠩ")):
    return
  if options.KEY == bstack111l11_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫऽ") and options.KEY in caps:
    bstack1ll1ll11l_opy_(options, caps[bstack111l11_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬा")])
  elif options.KEY == bstack111l11_opy_ (u"ࠨ࡯ࡲࡾ࠿࡬ࡩࡳࡧࡩࡳࡽࡕࡰࡵ࡫ࡲࡲࡸ࠭ि") and options.KEY in caps:
    bstack1ll111111_opy_(options, caps[bstack111l11_opy_ (u"ࠩࡰࡳࡿࡀࡦࡪࡴࡨࡪࡴࡾࡏࡱࡶ࡬ࡳࡳࡹࠧी")])
  elif options.KEY == bstack111l11_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫࠱ࡳࡵࡺࡩࡰࡰࡶࠫु") and options.KEY in caps:
    bstack11l111ll_opy_(options, caps[bstack111l11_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬࠲ࡴࡶࡴࡪࡱࡱࡷࠬू")])
  elif options.KEY == bstack111l11_opy_ (u"ࠬࡳࡳ࠻ࡧࡧ࡫ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ृ") and options.KEY in caps:
    bstack1l1l111111_opy_(options, caps[bstack111l11_opy_ (u"࠭࡭ࡴ࠼ࡨࡨ࡬࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧॄ")])
  elif options.KEY == bstack111l11_opy_ (u"ࠧࡴࡧ࠽࡭ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ॅ") and options.KEY in caps:
    bstack1ll11ll11_opy_(options, caps[bstack111l11_opy_ (u"ࠨࡵࡨ࠾࡮࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧॆ")])
def bstack1l1llll1l1_opy_(caps):
  global bstack1lll11l11_opy_
  if isinstance(os.environ.get(bstack111l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪे")), str):
    bstack1lll11l11_opy_ = eval(os.getenv(bstack111l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡌࡗࡤࡇࡐࡑࡡࡄ࡙࡙ࡕࡍࡂࡖࡈࠫै")))
  if bstack1lll11l11_opy_:
    if bstack1l1ll1lll_opy_() < version.parse(bstack111l11_opy_ (u"ࠫ࠷࠴࠳࠯࠲ࠪॉ")):
      return None
    else:
      from appium.options.common.base import AppiumOptions
      options = AppiumOptions().load_capabilities(caps)
      return options
  else:
    browser = bstack111l11_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࠬॊ")
    if bstack111l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫो") in caps:
      browser = caps[bstack111l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬौ")]
    elif bstack111l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳ्ࠩ") in caps:
      browser = caps[bstack111l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪॎ")]
    browser = str(browser).lower()
    if browser == bstack111l11_opy_ (u"ࠪ࡭ࡵ࡮࡯࡯ࡧࠪॏ") or browser == bstack111l11_opy_ (u"ࠫ࡮ࡶࡡࡥࠩॐ"):
      browser = bstack111l11_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭ࠬ॑")
    if browser == bstack111l11_opy_ (u"࠭ࡳࡢ࡯ࡶࡹࡳ࡭॒ࠧ"):
      browser = bstack111l11_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࠧ॓")
    if browser not in [bstack111l11_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࠨ॔"), bstack111l11_opy_ (u"ࠩࡨࡨ࡬࡫ࠧॕ"), bstack111l11_opy_ (u"ࠪ࡭ࡪ࠭ॖ"), bstack111l11_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬ࠫॗ"), bstack111l11_opy_ (u"ࠬ࡬ࡩࡳࡧࡩࡳࡽ࠭क़")]:
      return None
    try:
      package = bstack111l11_opy_ (u"࠭ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭࠯ࡹࡨࡦࡩࡸࡩࡷࡧࡵ࠲ࢀࢃ࠮ࡰࡲࡷ࡭ࡴࡴࡳࠨख़").format(browser)
      name = bstack111l11_opy_ (u"ࠧࡐࡲࡷ࡭ࡴࡴࡳࠨग़")
      browser_options = getattr(__import__(package, fromlist=[name]), name)
      options = browser_options()
      if not bstack11llll1l1_opy_(options):
        return None
      for bstack1ll1lll1l1_opy_ in caps.keys():
        options.set_capability(bstack1ll1lll1l1_opy_, caps[bstack1ll1lll1l1_opy_])
      bstack1ll1l1lll_opy_(options, caps)
      return options
    except Exception as e:
      logger.debug(str(e))
      return None
def bstack1l11lllll1_opy_(options, bstack1ll1ll1111_opy_):
  if not bstack11llll1l1_opy_(options):
    return
  for bstack1ll1lll1l1_opy_ in bstack1ll1ll1111_opy_.keys():
    if bstack1ll1lll1l1_opy_ in bstack1l1ll1llll_opy_:
      continue
    if bstack1ll1lll1l1_opy_ in options._caps and type(options._caps[bstack1ll1lll1l1_opy_]) in [dict, list]:
      options._caps[bstack1ll1lll1l1_opy_] = update(options._caps[bstack1ll1lll1l1_opy_], bstack1ll1ll1111_opy_[bstack1ll1lll1l1_opy_])
    else:
      options.set_capability(bstack1ll1lll1l1_opy_, bstack1ll1ll1111_opy_[bstack1ll1lll1l1_opy_])
  bstack1ll1l1lll_opy_(options, bstack1ll1ll1111_opy_)
  if bstack111l11_opy_ (u"ࠨ࡯ࡲࡾ࠿ࡪࡥࡣࡷࡪ࡫ࡪࡸࡁࡥࡦࡵࡩࡸࡹࠧज़") in options._caps:
    if options._caps[bstack111l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧड़")] and options._caps[bstack111l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨढ़")].lower() != bstack111l11_opy_ (u"ࠫ࡫࡯ࡲࡦࡨࡲࡼࠬफ़"):
      del options._caps[bstack111l11_opy_ (u"ࠬࡳ࡯ࡻ࠼ࡧࡩࡧࡻࡧࡨࡧࡵࡅࡩࡪࡲࡦࡵࡶࠫय़")]
def bstack11ll1l1l_opy_(proxy_config):
  if bstack111l11_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪॠ") in proxy_config:
    proxy_config[bstack111l11_opy_ (u"ࠧࡴࡵ࡯ࡔࡷࡵࡸࡺࠩॡ")] = proxy_config[bstack111l11_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬॢ")]
    del (proxy_config[bstack111l11_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭ॣ")])
  if bstack111l11_opy_ (u"ࠪࡴࡷࡵࡸࡺࡖࡼࡴࡪ࠭।") in proxy_config and proxy_config[bstack111l11_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡗࡽࡵ࡫ࠧ॥")].lower() != bstack111l11_opy_ (u"ࠬࡪࡩࡳࡧࡦࡸࠬ०"):
    proxy_config[bstack111l11_opy_ (u"࠭ࡰࡳࡱࡻࡽ࡙ࡿࡰࡦࠩ१")] = bstack111l11_opy_ (u"ࠧ࡮ࡣࡱࡹࡦࡲࠧ२")
  if bstack111l11_opy_ (u"ࠨࡲࡵࡳࡽࡿࡁࡶࡶࡲࡧࡴࡴࡦࡪࡩࡘࡶࡱ࠭३") in proxy_config:
    proxy_config[bstack111l11_opy_ (u"ࠩࡳࡶࡴࡾࡹࡕࡻࡳࡩࠬ४")] = bstack111l11_opy_ (u"ࠪࡴࡦࡩࠧ५")
  return proxy_config
def bstack11ll11111_opy_(config, proxy):
  from selenium.webdriver.common.proxy import Proxy
  if not bstack111l11_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࠪ६") in config:
    return proxy
  config[bstack111l11_opy_ (u"ࠬࡶࡲࡰࡺࡼࠫ७")] = bstack11ll1l1l_opy_(config[bstack111l11_opy_ (u"࠭ࡰࡳࡱࡻࡽࠬ८")])
  if proxy == None:
    proxy = Proxy(config[bstack111l11_opy_ (u"ࠧࡱࡴࡲࡼࡾ࠭९")])
  return proxy
def bstack1l1ll11111_opy_(self):
  global CONFIG
  global bstack111l1l11_opy_
  try:
    proxy = bstack1llll1l11_opy_(CONFIG)
    if proxy:
      if proxy.endswith(bstack111l11_opy_ (u"ࠨ࠰ࡳࡥࡨ࠭॰")):
        proxies = bstack1l1l11l11l_opy_(proxy, bstack1l1l1l111_opy_())
        if len(proxies) > 0:
          protocol, bstack1l111l1l1_opy_ = proxies.popitem()
          if bstack111l11_opy_ (u"ࠤ࠽࠳࠴ࠨॱ") in bstack1l111l1l1_opy_:
            return bstack1l111l1l1_opy_
          else:
            return bstack111l11_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࠦॲ") + bstack1l111l1l1_opy_
      else:
        return proxy
  except Exception as e:
    logger.error(bstack111l11_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡱࡴࡲࡼࡾࠦࡵࡳ࡮ࠣ࠾ࠥࢁࡽࠣॳ").format(str(e)))
  return bstack111l1l11_opy_(self)
def bstack11l1ll1l1_opy_():
  global CONFIG
  return bstack111ll1111_opy_(CONFIG) and bstack1ll1l11l11_opy_() and bstack1lll1l1ll_opy_() >= version.parse(bstack1l111lll_opy_)
def bstack1l1l1lll1_opy_():
  global CONFIG
  return (bstack111l11_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨॴ") in CONFIG or bstack111l11_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪॵ") in CONFIG) and bstack111l1l1ll_opy_()
def bstack1l11llll1_opy_(config):
  bstack1lllll111_opy_ = {}
  if bstack111l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫॶ") in config:
    bstack1lllll111_opy_ = config[bstack111l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬॷ")]
  if bstack111l11_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨॸ") in config:
    bstack1lllll111_opy_ = config[bstack111l11_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩॹ")]
  proxy = bstack1llll1l11_opy_(config)
  if proxy:
    if proxy.endswith(bstack111l11_opy_ (u"ࠫ࠳ࡶࡡࡤࠩॺ")) and os.path.isfile(proxy):
      bstack1lllll111_opy_[bstack111l11_opy_ (u"ࠬ࠳ࡰࡢࡥ࠰ࡪ࡮ࡲࡥࠨॻ")] = proxy
    else:
      parsed_url = None
      if proxy.endswith(bstack111l11_opy_ (u"࠭࠮ࡱࡣࡦࠫॼ")):
        proxies = bstack1l11ll11l1_opy_(config, bstack1l1l1l111_opy_())
        if len(proxies) > 0:
          protocol, bstack1l111l1l1_opy_ = proxies.popitem()
          if bstack111l11_opy_ (u"ࠢ࠻࠱࠲ࠦॽ") in bstack1l111l1l1_opy_:
            parsed_url = urlparse(bstack1l111l1l1_opy_)
          else:
            parsed_url = urlparse(protocol + bstack111l11_opy_ (u"ࠣ࠼࠲࠳ࠧॾ") + bstack1l111l1l1_opy_)
      else:
        parsed_url = urlparse(proxy)
      if parsed_url and parsed_url.hostname: bstack1lllll111_opy_[bstack111l11_opy_ (u"ࠩࡳࡶࡴࡾࡹࡉࡱࡶࡸࠬॿ")] = str(parsed_url.hostname)
      if parsed_url and parsed_url.port: bstack1lllll111_opy_[bstack111l11_opy_ (u"ࠪࡴࡷࡵࡸࡺࡒࡲࡶࡹ࠭ঀ")] = str(parsed_url.port)
      if parsed_url and parsed_url.username: bstack1lllll111_opy_[bstack111l11_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡘࡷࡪࡸࠧঁ")] = str(parsed_url.username)
      if parsed_url and parsed_url.password: bstack1lllll111_opy_[bstack111l11_opy_ (u"ࠬࡶࡲࡰࡺࡼࡔࡦࡹࡳࠨং")] = str(parsed_url.password)
  return bstack1lllll111_opy_
def bstack1l1l1l1ll1_opy_(config):
  if bstack111l11_opy_ (u"࠭ࡴࡦࡵࡷࡇࡴࡴࡴࡦࡺࡷࡓࡵࡺࡩࡰࡰࡶࠫঃ") in config:
    return config[bstack111l11_opy_ (u"ࠧࡵࡧࡶࡸࡈࡵ࡮ࡵࡧࡻࡸࡔࡶࡴࡪࡱࡱࡷࠬ঄")]
  return {}
def bstack111llll1l_opy_(caps):
  global bstack1l11ll1l_opy_
  if bstack111l11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩঅ") in caps:
    caps[bstack111l11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪআ")][bstack111l11_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࠩই")] = True
    if bstack1l11ll1l_opy_:
      caps[bstack111l11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬঈ")][bstack111l11_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧউ")] = bstack1l11ll1l_opy_
  else:
    caps[bstack111l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡲ࡯ࡤࡣ࡯ࠫঊ")] = True
    if bstack1l11ll1l_opy_:
      caps[bstack111l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨঋ")] = bstack1l11ll1l_opy_
def bstack111l11lll_opy_():
  global CONFIG
  if bstack111l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬঌ") in CONFIG and bstack1ll11l1l11_opy_(CONFIG[bstack111l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭঍")]):
    bstack1lllll111_opy_ = bstack1l11llll1_opy_(CONFIG)
    bstack1ll1111l1l_opy_(CONFIG[bstack111l11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭঎")], bstack1lllll111_opy_)
def bstack1ll1111l1l_opy_(key, bstack1lllll111_opy_):
  global bstack1l1l11l1_opy_
  logger.info(bstack11ll11l11_opy_)
  try:
    bstack1l1l11l1_opy_ = Local()
    bstack1ll11llll1_opy_ = {bstack111l11_opy_ (u"ࠫࡰ࡫ࡹࠨএ"): key}
    bstack1ll11llll1_opy_.update(bstack1lllll111_opy_)
    logger.debug(bstack11lll1ll_opy_.format(str(bstack1ll11llll1_opy_)))
    bstack1l1l11l1_opy_.start(**bstack1ll11llll1_opy_)
    if bstack1l1l11l1_opy_.isRunning():
      logger.info(bstack1ll1lll1_opy_)
  except Exception as e:
    bstack11ll1lll1_opy_(bstack1l1l1l1l_opy_.format(str(e)))
def bstack11lll111l_opy_():
  global bstack1l1l11l1_opy_
  if bstack1l1l11l1_opy_.isRunning():
    logger.info(bstack1llll1l1l_opy_)
    bstack1l1l11l1_opy_.stop()
  bstack1l1l11l1_opy_ = None
def bstack1ll11lll1l_opy_(bstack1l11ll1ll1_opy_=[]):
  global CONFIG
  bstack1ll1ll1l1l_opy_ = []
  bstack1l1l1111l_opy_ = [bstack111l11_opy_ (u"ࠬࡵࡳࠨঐ"), bstack111l11_opy_ (u"࠭࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩ঑"), bstack111l11_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠫ঒"), bstack111l11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠪও"), bstack111l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧঔ"), bstack111l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫক")]
  try:
    for err in bstack1l11ll1ll1_opy_:
      bstack1ll1ll1l11_opy_ = {}
      for k in bstack1l1l1111l_opy_:
        val = CONFIG[bstack111l11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧখ")][int(err[bstack111l11_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫগ")])].get(k)
        if val:
          bstack1ll1ll1l11_opy_[k] = val
      if(err[bstack111l11_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬঘ")] != bstack111l11_opy_ (u"ࠧࠨঙ")):
        bstack1ll1ll1l11_opy_[bstack111l11_opy_ (u"ࠨࡶࡨࡷࡹࡹࠧচ")] = {
          err[bstack111l11_opy_ (u"ࠩࡱࡥࡲ࡫ࠧছ")]: err[bstack111l11_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩজ")]
        }
        bstack1ll1ll1l1l_opy_.append(bstack1ll1ll1l11_opy_)
  except Exception as e:
    logger.debug(bstack111l11_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡦࡰࡴࡰࡥࡹࡺࡩ࡯ࡩࠣࡨࡦࡺࡡࠡࡨࡲࡶࠥ࡫ࡶࡦࡰࡷ࠾ࠥ࠭ঝ") + str(e))
  finally:
    return bstack1ll1ll1l1l_opy_
def bstack11lll11l_opy_(file_name):
  bstack1ll11llll_opy_ = []
  try:
    bstack1l1l1ll11l_opy_ = os.path.join(tempfile.gettempdir(), file_name)
    if os.path.exists(bstack1l1l1ll11l_opy_):
      with open(bstack1l1l1ll11l_opy_) as f:
        bstack1l1ll11ll1_opy_ = json.load(f)
        bstack1ll11llll_opy_ = bstack1l1ll11ll1_opy_
      os.remove(bstack1l1l1ll11l_opy_)
    return bstack1ll11llll_opy_
  except Exception as e:
    logger.debug(bstack111l11_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡧ࡫ࡱࡨ࡮ࡴࡧࠡࡧࡵࡶࡴࡸࠠ࡭࡫ࡶࡸ࠿ࠦࠧঞ") + str(e))
def bstack1ll11l1111_opy_():
  global bstack11111l11l_opy_
  global bstack1l1l1ll1l1_opy_
  global bstack1ll11l1l_opy_
  global bstack1l1llll1_opy_
  global bstack11lllllll_opy_
  global bstack11llllll_opy_
  global CONFIG
  bstack1l11l11l11_opy_ = os.environ.get(bstack111l11_opy_ (u"࠭ࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࡡࡘࡗࡊࡊࠧট"))
  if bstack1l11l11l11_opy_ in [bstack111l11_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ঠ"), bstack111l11_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧড")]:
    bstack1l1lll111_opy_()
  percy.shutdown()
  if bstack11111l11l_opy_:
    logger.warning(bstack1lll1l111_opy_.format(str(bstack11111l11l_opy_)))
  else:
    try:
      bstack1111ll1l1_opy_ = bstack1l11l1l11l_opy_(bstack111l11_opy_ (u"ࠩ࠱ࡦࡸࡺࡡࡤ࡭࠰ࡧࡴࡴࡦࡪࡩ࠱࡮ࡸࡵ࡮ࠨঢ"), logger)
      if bstack1111ll1l1_opy_.get(bstack111l11_opy_ (u"ࠪࡲࡺࡪࡧࡦࡡ࡯ࡳࡨࡧ࡬ࠨণ")) and bstack1111ll1l1_opy_.get(bstack111l11_opy_ (u"ࠫࡳࡻࡤࡨࡧࡢࡰࡴࡩࡡ࡭ࠩত")).get(bstack111l11_opy_ (u"ࠬ࡮࡯ࡴࡶࡱࡥࡲ࡫ࠧথ")):
        logger.warning(bstack1lll1l111_opy_.format(str(bstack1111ll1l1_opy_[bstack111l11_opy_ (u"࠭࡮ࡶࡦࡪࡩࡤࡲ࡯ࡤࡣ࡯ࠫদ")][bstack111l11_opy_ (u"ࠧࡩࡱࡶࡸࡳࡧ࡭ࡦࠩধ")])))
    except Exception as e:
      logger.error(e)
  logger.info(bstack1ll11lll11_opy_)
  global bstack1l1l11l1_opy_
  if bstack1l1l11l1_opy_:
    bstack11lll111l_opy_()
  try:
    for driver in bstack1l1l1ll1l1_opy_:
      driver.quit()
  except Exception as e:
    pass
  logger.info(bstack1l1llll111_opy_)
  if bstack11llllll_opy_ == bstack111l11_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧন"):
    bstack11lllllll_opy_ = bstack11lll11l_opy_(bstack111l11_opy_ (u"ࠩࡵࡳࡧࡵࡴࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸ࠳ࡰࡳࡰࡰࠪ঩"))
  if bstack11llllll_opy_ == bstack111l11_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪপ") and len(bstack1l1llll1_opy_) == 0:
    bstack1l1llll1_opy_ = bstack11lll11l_opy_(bstack111l11_opy_ (u"ࠫࡵࡽ࡟ࡱࡻࡷࡩࡸࡺ࡟ࡦࡴࡵࡳࡷࡥ࡬ࡪࡵࡷ࠲࡯ࡹ࡯࡯ࠩফ"))
    if len(bstack1l1llll1_opy_) == 0:
      bstack1l1llll1_opy_ = bstack11lll11l_opy_(bstack111l11_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࡤࡶࡰࡱࡡࡨࡶࡷࡵࡲࡠ࡮࡬ࡷࡹ࠴ࡪࡴࡱࡱࠫব"))
  bstack1llll11ll1_opy_ = bstack111l11_opy_ (u"࠭ࠧভ")
  if len(bstack1ll11l1l_opy_) > 0:
    bstack1llll11ll1_opy_ = bstack1ll11lll1l_opy_(bstack1ll11l1l_opy_)
  elif len(bstack1l1llll1_opy_) > 0:
    bstack1llll11ll1_opy_ = bstack1ll11lll1l_opy_(bstack1l1llll1_opy_)
  elif len(bstack11lllllll_opy_) > 0:
    bstack1llll11ll1_opy_ = bstack1ll11lll1l_opy_(bstack11lllllll_opy_)
  elif len(bstack1l11llll1l_opy_) > 0:
    bstack1llll11ll1_opy_ = bstack1ll11lll1l_opy_(bstack1l11llll1l_opy_)
  if bool(bstack1llll11ll1_opy_):
    bstack1l1l11111_opy_(bstack1llll11ll1_opy_)
  else:
    bstack1l1l11111_opy_()
  bstack1l1l1l11_opy_(bstack1ll1llll11_opy_, logger)
  bstack1l1l1l1l1_opy_.bstack1l11111l1_opy_(CONFIG)
  if len(bstack11lllllll_opy_) > 0:
    sys.exit(len(bstack11lllllll_opy_))
def bstack1l11l1l1l_opy_(bstack1lllll1111_opy_, frame):
  global bstack1l11l111ll_opy_
  logger.error(bstack1l11ll1l1l_opy_)
  bstack1l11l111ll_opy_.bstack1ll1l11ll_opy_(bstack111l11_opy_ (u"ࠧࡴࡦ࡮ࡏ࡮ࡲ࡬ࡏࡱࠪম"), bstack1lllll1111_opy_)
  if hasattr(signal, bstack111l11_opy_ (u"ࠨࡕ࡬࡫ࡳࡧ࡬ࡴࠩয")):
    bstack1l11l111ll_opy_.bstack1ll1l11ll_opy_(bstack111l11_opy_ (u"ࠩࡶࡨࡰࡑࡩ࡭࡮ࡖ࡭࡬ࡴࡡ࡭ࠩর"), signal.Signals(bstack1lllll1111_opy_).name)
  else:
    bstack1l11l111ll_opy_.bstack1ll1l11ll_opy_(bstack111l11_opy_ (u"ࠪࡷࡩࡱࡋࡪ࡮࡯ࡗ࡮࡭࡮ࡢ࡮ࠪ঱"), bstack111l11_opy_ (u"ࠫࡘࡏࡇࡖࡐࡎࡒࡔ࡝ࡎࠨল"))
  bstack1l11l11l11_opy_ = os.environ.get(bstack111l11_opy_ (u"ࠬࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࡠࡗࡖࡉࡉ࠭঳"))
  if bstack1l11l11l11_opy_ == bstack111l11_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭঴"):
    bstack1lll1ll1l_opy_.stop(bstack1l11l111ll_opy_.get_property(bstack111l11_opy_ (u"ࠧࡴࡦ࡮ࡏ࡮ࡲ࡬ࡔ࡫ࡪࡲࡦࡲࠧ঵")))
  bstack1ll11l1111_opy_()
  sys.exit(1)
def bstack11ll1lll1_opy_(err):
  logger.critical(bstack1lll1l11l1_opy_.format(str(err)))
  bstack1l1l11111_opy_(bstack1lll1l11l1_opy_.format(str(err)), True)
  atexit.unregister(bstack1ll11l1111_opy_)
  bstack1l1lll111_opy_()
  sys.exit(1)
def bstack1lll11lll_opy_(error, message):
  logger.critical(str(error))
  logger.critical(message)
  bstack1l1l11111_opy_(message, True)
  atexit.unregister(bstack1ll11l1111_opy_)
  bstack1l1lll111_opy_()
  sys.exit(1)
def bstack1ll1llll_opy_():
  global CONFIG
  global bstack1ll11ll1ll_opy_
  global bstack1l11lll1l_opy_
  global bstack1ll1l11l1_opy_
  CONFIG = bstack1lll1ll11l_opy_()
  load_dotenv(CONFIG.get(bstack111l11_opy_ (u"ࠨࡧࡱࡺࡋ࡯࡬ࡦࠩশ")))
  bstack111ll111l_opy_()
  bstack1lll11l11l_opy_()
  CONFIG = bstack111ll1ll_opy_(CONFIG)
  update(CONFIG, bstack1l11lll1l_opy_)
  update(CONFIG, bstack1ll11ll1ll_opy_)
  CONFIG = bstack1ll1ll1lll_opy_(CONFIG)
  bstack1ll1l11l1_opy_ = bstack1l11lll11_opy_(CONFIG)
  bstack1l11l111ll_opy_.bstack1ll1l11ll_opy_(bstack111l11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡶࡩࡸࡹࡩࡰࡰࠪষ"), bstack1ll1l11l1_opy_)
  if (bstack111l11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭স") in CONFIG and bstack111l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧহ") in bstack1ll11ll1ll_opy_) or (
          bstack111l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ঺") in CONFIG and bstack111l11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ঻") not in bstack1l11lll1l_opy_):
    if os.getenv(bstack111l11_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑ࡟ࡄࡑࡐࡆࡎࡔࡅࡅࡡࡅ࡙ࡎࡒࡄࡠࡋࡇ়ࠫ")):
      CONFIG[bstack111l11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪঽ")] = os.getenv(bstack111l11_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡡࡆࡓࡒࡈࡉࡏࡇࡇࡣࡇ࡛ࡉࡍࡆࡢࡍࡉ࠭া"))
    else:
      bstack1ll111l1l_opy_()
  elif (bstack111l11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ি") not in CONFIG and bstack111l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ী") in CONFIG) or (
          bstack111l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨু") in bstack1l11lll1l_opy_ and bstack111l11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩূ") not in bstack1ll11ll1ll_opy_):
    del (CONFIG[bstack111l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩৃ")])
  if bstack1l11lllll_opy_(CONFIG):
    bstack11ll1lll1_opy_(bstack1l11lll1l1_opy_)
  bstack11ll1l11_opy_()
  bstack111l1ll1_opy_()
  if bstack1lll11l11_opy_:
    CONFIG[bstack111l11_opy_ (u"ࠨࡣࡳࡴࠬৄ")] = bstack11111l1l_opy_(CONFIG)
    logger.info(bstack1llll111l1_opy_.format(CONFIG[bstack111l11_opy_ (u"ࠩࡤࡴࡵ࠭৅")]))
  if not bstack1ll1l11l1_opy_:
    CONFIG[bstack111l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭৆")] = [{}]
def bstack1l1ll1ll_opy_(config, bstack1ll111lll1_opy_):
  global CONFIG
  global bstack1lll11l11_opy_
  CONFIG = config
  bstack1lll11l11_opy_ = bstack1ll111lll1_opy_
def bstack111l1ll1_opy_():
  global CONFIG
  global bstack1lll11l11_opy_
  if bstack111l11_opy_ (u"ࠫࡦࡶࡰࠨে") in CONFIG:
    try:
      from appium import version
    except Exception as e:
      bstack1lll11lll_opy_(e, bstack1111l111_opy_)
    bstack1lll11l11_opy_ = True
    bstack1l11l111ll_opy_.bstack1ll1l11ll_opy_(bstack111l11_opy_ (u"ࠬࡧࡰࡱࡡࡤࡹࡹࡵ࡭ࡢࡶࡨࠫৈ"), True)
def bstack11111l1l_opy_(config):
  bstack1l1lll111l_opy_ = bstack111l11_opy_ (u"࠭ࠧ৉")
  app = config[bstack111l11_opy_ (u"ࠧࡢࡲࡳࠫ৊")]
  if isinstance(app, str):
    if os.path.splitext(app)[1] in bstack1l11ll111l_opy_:
      if os.path.exists(app):
        bstack1l1lll111l_opy_ = bstack11ll11l1_opy_(config, app)
      elif bstack11llllll1_opy_(app):
        bstack1l1lll111l_opy_ = app
      else:
        bstack11ll1lll1_opy_(bstack1llll1l1l1_opy_.format(app))
    else:
      if bstack11llllll1_opy_(app):
        bstack1l1lll111l_opy_ = app
      elif os.path.exists(app):
        bstack1l1lll111l_opy_ = bstack11ll11l1_opy_(app)
      else:
        bstack11ll1lll1_opy_(bstack1lll11l1l1_opy_)
  else:
    if len(app) > 2:
      bstack11ll1lll1_opy_(bstack111ll11l_opy_)
    elif len(app) == 2:
      if bstack111l11_opy_ (u"ࠨࡲࡤࡸ࡭࠭ো") in app and bstack111l11_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡡ࡬ࡨࠬৌ") in app:
        if os.path.exists(app[bstack111l11_opy_ (u"ࠪࡴࡦࡺࡨࠨ্")]):
          bstack1l1lll111l_opy_ = bstack11ll11l1_opy_(config, app[bstack111l11_opy_ (u"ࠫࡵࡧࡴࡩࠩৎ")], app[bstack111l11_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡤ࡯ࡤࠨ৏")])
        else:
          bstack11ll1lll1_opy_(bstack1llll1l1l1_opy_.format(app))
      else:
        bstack11ll1lll1_opy_(bstack111ll11l_opy_)
    else:
      for key in app:
        if key in bstack1l1lll1l11_opy_:
          if key == bstack111l11_opy_ (u"࠭ࡰࡢࡶ࡫ࠫ৐"):
            if os.path.exists(app[key]):
              bstack1l1lll111l_opy_ = bstack11ll11l1_opy_(config, app[key])
            else:
              bstack11ll1lll1_opy_(bstack1llll1l1l1_opy_.format(app))
          else:
            bstack1l1lll111l_opy_ = app[key]
        else:
          bstack11ll1lll1_opy_(bstack1l1ll111_opy_)
  return bstack1l1lll111l_opy_
def bstack11llllll1_opy_(bstack1l1lll111l_opy_):
  import re
  bstack1ll11l11ll_opy_ = re.compile(bstack111l11_opy_ (u"ࡲࠣࡠ࡞ࡥ࠲ࢀࡁ࠮࡜࠳࠱࠾ࡢ࡟࠯࡞࠰ࡡ࠯ࠪࠢ৑"))
  bstack111lll11l_opy_ = re.compile(bstack111l11_opy_ (u"ࡳࠤࡡ࡟ࡦ࠳ࡺࡂ࠯࡝࠴࠲࠿࡜ࡠ࠰࡟࠱ࡢ࠰࠯࡜ࡣ࠰ࡾࡆ࠳࡚࠱࠯࠼ࡠࡤ࠴࡜࠮࡟࠭ࠨࠧ৒"))
  if bstack111l11_opy_ (u"ࠩࡥࡷ࠿࠵࠯ࠨ৓") in bstack1l1lll111l_opy_ or re.fullmatch(bstack1ll11l11ll_opy_, bstack1l1lll111l_opy_) or re.fullmatch(bstack111lll11l_opy_, bstack1l1lll111l_opy_):
    return True
  else:
    return False
def bstack11ll11l1_opy_(config, path, bstack111l1l111_opy_=None):
  import requests
  from requests_toolbelt.multipart.encoder import MultipartEncoder
  import hashlib
  md5_hash = hashlib.md5(open(os.path.abspath(path), bstack111l11_opy_ (u"ࠪࡶࡧ࠭৔")).read()).hexdigest()
  bstack1l1l1l1l11_opy_ = bstack11llll11_opy_(md5_hash)
  bstack1l1lll111l_opy_ = None
  if bstack1l1l1l1l11_opy_:
    logger.info(bstack1l1l1llll_opy_.format(bstack1l1l1l1l11_opy_, md5_hash))
    return bstack1l1l1l1l11_opy_
  bstack1lllllll1_opy_ = MultipartEncoder(
    fields={
      bstack111l11_opy_ (u"ࠫ࡫࡯࡬ࡦࠩ৕"): (os.path.basename(path), open(os.path.abspath(path), bstack111l11_opy_ (u"ࠬࡸࡢࠨ৖")), bstack111l11_opy_ (u"࠭ࡴࡦࡺࡷ࠳ࡵࡲࡡࡪࡰࠪৗ")),
      bstack111l11_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳ࡟ࡪࡦࠪ৘"): bstack111l1l111_opy_
    }
  )
  response = requests.post(bstack11ll1111_opy_, data=bstack1lllllll1_opy_,
                           headers={bstack111l11_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡗࡽࡵ࡫ࠧ৙"): bstack1lllllll1_opy_.content_type},
                           auth=(config[bstack111l11_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫ৚")], config[bstack111l11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭৛")]))
  try:
    res = json.loads(response.text)
    bstack1l1lll111l_opy_ = res[bstack111l11_opy_ (u"ࠫࡦࡶࡰࡠࡷࡵࡰࠬড়")]
    logger.info(bstack11ll11ll_opy_.format(bstack1l1lll111l_opy_))
    bstack111l11ll1_opy_(md5_hash, bstack1l1lll111l_opy_)
  except ValueError as err:
    bstack11ll1lll1_opy_(bstack11l111l1_opy_.format(str(err)))
  return bstack1l1lll111l_opy_
def bstack11ll1l11_opy_():
  global CONFIG
  global bstack1l1l1llll1_opy_
  bstack11l1ll111_opy_ = 0
  bstack1l1l1l11l1_opy_ = 1
  if bstack111l11_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬঢ়") in CONFIG:
    bstack1l1l1l11l1_opy_ = CONFIG[bstack111l11_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭৞")]
  if bstack111l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪয়") in CONFIG:
    bstack11l1ll111_opy_ = len(CONFIG[bstack111l11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫৠ")])
  bstack1l1l1llll1_opy_ = int(bstack1l1l1l11l1_opy_) * int(bstack11l1ll111_opy_)
def bstack11llll11_opy_(md5_hash):
  bstack111llll1_opy_ = os.path.join(os.path.expanduser(bstack111l11_opy_ (u"ࠩࢁࠫৡ")), bstack111l11_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪৢ"), bstack111l11_opy_ (u"ࠫࡦࡶࡰࡖࡲ࡯ࡳࡦࡪࡍࡅ࠷ࡋࡥࡸ࡮࠮࡫ࡵࡲࡲࠬৣ"))
  if os.path.exists(bstack111llll1_opy_):
    bstack111l111l_opy_ = json.load(open(bstack111llll1_opy_, bstack111l11_opy_ (u"ࠬࡸࡢࠨ৤")))
    if md5_hash in bstack111l111l_opy_:
      bstack1l11ll1ll_opy_ = bstack111l111l_opy_[md5_hash]
      bstack1ll1lll1ll_opy_ = datetime.datetime.now()
      bstack1ll11l11_opy_ = datetime.datetime.strptime(bstack1l11ll1ll_opy_[bstack111l11_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩ৥")], bstack111l11_opy_ (u"ࠧࠦࡦ࠲ࠩࡲ࠵࡚ࠥࠢࠨࡌ࠿ࠫࡍ࠻ࠧࡖࠫ০"))
      if (bstack1ll1lll1ll_opy_ - bstack1ll11l11_opy_).days > 30:
        return None
      elif version.parse(str(__version__)) > version.parse(bstack1l11ll1ll_opy_[bstack111l11_opy_ (u"ࠨࡵࡧ࡯ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭১")]):
        return None
      return bstack1l11ll1ll_opy_[bstack111l11_opy_ (u"ࠩ࡬ࡨࠬ২")]
  else:
    return None
def bstack111l11ll1_opy_(md5_hash, bstack1l1lll111l_opy_):
  bstack11llll1ll_opy_ = os.path.join(os.path.expanduser(bstack111l11_opy_ (u"ࠪࢂࠬ৩")), bstack111l11_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫ৪"))
  if not os.path.exists(bstack11llll1ll_opy_):
    os.makedirs(bstack11llll1ll_opy_)
  bstack111llll1_opy_ = os.path.join(os.path.expanduser(bstack111l11_opy_ (u"ࠬࢄࠧ৫")), bstack111l11_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭৬"), bstack111l11_opy_ (u"ࠧࡢࡲࡳ࡙ࡵࡲ࡯ࡢࡦࡐࡈ࠺ࡎࡡࡴࡪ࠱࡮ࡸࡵ࡮ࠨ৭"))
  bstack1l11l1l1l1_opy_ = {
    bstack111l11_opy_ (u"ࠨ࡫ࡧࠫ৮"): bstack1l1lll111l_opy_,
    bstack111l11_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬ৯"): datetime.datetime.strftime(datetime.datetime.now(), bstack111l11_opy_ (u"ࠪࠩࡩ࠵ࠥ࡮࠱ࠨ࡝ࠥࠫࡈ࠻ࠧࡐ࠾࡙ࠪࠧৰ")),
    bstack111l11_opy_ (u"ࠫࡸࡪ࡫ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩৱ"): str(__version__)
  }
  if os.path.exists(bstack111llll1_opy_):
    bstack111l111l_opy_ = json.load(open(bstack111llll1_opy_, bstack111l11_opy_ (u"ࠬࡸࡢࠨ৲")))
  else:
    bstack111l111l_opy_ = {}
  bstack111l111l_opy_[md5_hash] = bstack1l11l1l1l1_opy_
  with open(bstack111llll1_opy_, bstack111l11_opy_ (u"ࠨࡷࠬࠤ৳")) as outfile:
    json.dump(bstack111l111l_opy_, outfile)
def bstack1l11lll1ll_opy_(self):
  return
def bstack1llll1lll_opy_(self):
  return
def bstack1l11lll1_opy_(self):
  global bstack111l1l1l1_opy_
  bstack111l1l1l1_opy_(self)
def bstack1lll1ll1l1_opy_():
  global bstack1ll1111l1_opy_
  bstack1ll1111l1_opy_ = True
def bstack1ll11111ll_opy_(self):
  global bstack1lll1ll11_opy_
  global bstack1ll111l1_opy_
  global bstack11l1lll1_opy_
  try:
    if bstack111l11_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ৴") in bstack1lll1ll11_opy_ and self.session_id != None and bstack1ll111l1ll_opy_(threading.current_thread(), bstack111l11_opy_ (u"ࠨࡶࡨࡷࡹ࡙ࡴࡢࡶࡸࡷࠬ৵"), bstack111l11_opy_ (u"ࠩࠪ৶")) != bstack111l11_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫ৷"):
      bstack1lll11l1ll_opy_ = bstack111l11_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫ৸") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack111l11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ৹")
      if bstack1lll11l1ll_opy_ == bstack111l11_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭৺"):
        bstack1l1l1lll11_opy_(logger)
      if self != None:
        bstack1l1l11llll_opy_(self, bstack1lll11l1ll_opy_, bstack111l11_opy_ (u"ࠧ࠭ࠢࠪ৻").join(threading.current_thread().bstackTestErrorMessages))
    threading.current_thread().testStatus = bstack111l11_opy_ (u"ࠨࠩৼ")
    if bstack111l11_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ৽") in bstack1lll1ll11_opy_ and getattr(threading.current_thread(), bstack111l11_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ৾"), None):
      bstack1l11l111l_opy_.bstack1l1lllll11_opy_(self, bstack1l1lll11l_opy_, logger, wait=True)
  except Exception as e:
    logger.debug(bstack111l11_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡰࡥࡷࡱࡩ࡯ࡩࠣࡷࡹࡧࡴࡶࡵ࠽ࠤࠧ৿") + str(e))
  bstack11l1lll1_opy_(self)
  self.session_id = None
def bstack1l1ll1ll11_opy_(self, command_executor=bstack111l11_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࠳࠴࠷࠲࠸࠰࠳࠲࠵࠴࠱࠻࠶࠷࠸࠹ࠨ਀"), *args, **kwargs):
  bstack1l1lll1l_opy_ = bstack1ll111l11l_opy_(self, command_executor, *args, **kwargs)
  try:
    logger.debug(bstack111l11_opy_ (u"࠭ࡃࡰ࡯ࡰࡥࡳࡪࠠࡆࡺࡨࡧࡺࡺ࡯ࡳࠢࡺ࡬ࡪࡴࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣ࡭ࡸࠦࡦࡢ࡮ࡶࡩࠥ࠳ࠠࡼࡿࠪਁ").format(str(command_executor)))
    logger.debug(bstack111l11_opy_ (u"ࠧࡉࡷࡥࠤ࡚ࡘࡌࠡ࡫ࡶࠤ࠲ࠦࡻࡾࠩਂ").format(str(command_executor._url)))
    from selenium.webdriver.remote.remote_connection import RemoteConnection
    if isinstance(command_executor, RemoteConnection) and bstack111l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠫਃ") in command_executor._url:
      bstack1l11l111ll_opy_.bstack1ll1l11ll_opy_(bstack111l11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡶࡩࡸࡹࡩࡰࡰࠪ਄"), True)
  except:
    pass
  if (isinstance(command_executor, str) and bstack111l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠭ਅ") in command_executor):
    bstack1l11l111ll_opy_.bstack1ll1l11ll_opy_(bstack111l11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠬਆ"), True)
  threading.current_thread().bstackSessionDriver = self
  bstack1lll1ll1l_opy_.bstack1l1ll11l11_opy_(self)
  return bstack1l1lll1l_opy_
def bstack1l1111l1l_opy_(args):
  return bstack111l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷ࠭ਇ") in str(args)
def bstack1lll1l11l_opy_(self, driver_command, *args, **kwargs):
  global bstack1l111111_opy_
  global bstack1l1ll11l_opy_
  bstack11llll11l_opy_ = bstack1ll111l1ll_opy_(threading.current_thread(), bstack111l11_opy_ (u"࠭ࡩࡴࡃ࠴࠵ࡾ࡚ࡥࡴࡶࠪਈ"), None) and bstack1ll111l1ll_opy_(
          threading.current_thread(), bstack111l11_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭ਉ"), None)
  bstack1l11l1ll_opy_ = getattr(self, bstack111l11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡂ࠳࠴ࡽࡘ࡮࡯ࡶ࡮ࡧࡗࡨࡧ࡮ࠨਊ"), None) != None and getattr(self, bstack111l11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡃ࠴࠵ࡾ࡙ࡨࡰࡷ࡯ࡨࡘࡩࡡ࡯ࠩ਋"), None) == True
  if not bstack1l1ll11l_opy_ and bstack1ll1l11l1_opy_ and bstack111l11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ਌") in CONFIG and CONFIG[bstack111l11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ਍")] == True and bstack1l1lll1lll_opy_.bstack1lll1l1ll1_opy_(driver_command) and (bstack1l11l1ll_opy_ or bstack11llll11l_opy_) and not bstack1l1111l1l_opy_(args):
    try:
      bstack1l1ll11l_opy_ = True
      logger.debug(bstack111l11_opy_ (u"ࠬࡖࡥࡳࡨࡲࡶࡲ࡯࡮ࡨࠢࡶࡧࡦࡴࠠࡧࡱࡵࠤࢀࢃࠧ਎").format(driver_command))
      logger.debug(perform_scan(self, driver_command=driver_command))
    except Exception as err:
      logger.debug(bstack111l11_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡳࡩࡷ࡬࡯ࡳ࡯ࠣࡷࡨࡧ࡮ࠡࡽࢀࠫਏ").format(str(err)))
    bstack1l1ll11l_opy_ = False
  response = bstack1l111111_opy_(self, driver_command, *args, **kwargs)
  if bstack111l11_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ਐ") in str(bstack1lll1ll11_opy_).lower() and bstack1lll1ll1l_opy_.on():
    try:
      if driver_command == bstack111l11_opy_ (u"ࠨࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠬ਑"):
        bstack1lll1ll1l_opy_.bstack1ll11l1ll_opy_({
            bstack111l11_opy_ (u"ࠩ࡬ࡱࡦ࡭ࡥࠨ਒"): response[bstack111l11_opy_ (u"ࠪࡺࡦࡲࡵࡦࠩਓ")],
            bstack111l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫਔ"): bstack1lll1ll1l_opy_.current_test_uuid() if bstack1lll1ll1l_opy_.current_test_uuid() else bstack1lll1ll1l_opy_.current_hook_uuid()
        })
    except:
      pass
  return response
def bstack11ll1llll_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
  global CONFIG
  global bstack1ll111l1_opy_
  global bstack1111111l1_opy_
  global bstack1l11l11l1_opy_
  global bstack111lll1ll_opy_
  global bstack111111111_opy_
  global bstack1lll1ll11_opy_
  global bstack1ll111l11l_opy_
  global bstack1l1l1ll1l1_opy_
  global bstack1ll1ll1l1_opy_
  global bstack1l1lll11l_opy_
  CONFIG[bstack111l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧਕ")] = str(bstack1lll1ll11_opy_) + str(__version__)
  command_executor = bstack1l1l1l111_opy_()
  logger.debug(bstack1lll111l1l_opy_.format(command_executor))
  proxy = bstack11ll11111_opy_(CONFIG, proxy)
  bstack1ll11lllll_opy_ = 0 if bstack1111111l1_opy_ < 0 else bstack1111111l1_opy_
  try:
    if bstack111lll1ll_opy_ is True:
      bstack1ll11lllll_opy_ = int(multiprocessing.current_process().name)
    elif bstack111111111_opy_ is True:
      bstack1ll11lllll_opy_ = int(threading.current_thread().name)
  except:
    bstack1ll11lllll_opy_ = 0
  bstack1ll1ll1111_opy_ = bstack111ll11ll_opy_(CONFIG, bstack1ll11lllll_opy_)
  logger.debug(bstack111l11111_opy_.format(str(bstack1ll1ll1111_opy_)))
  if bstack111l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪਖ") in CONFIG and bstack1ll11l1l11_opy_(CONFIG[bstack111l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫਗ")]):
    bstack111llll1l_opy_(bstack1ll1ll1111_opy_)
  if bstack1llll11l_opy_.bstack1l1l1ll1l_opy_(CONFIG, bstack1ll11lllll_opy_) and bstack1llll11l_opy_.bstack1llllllll_opy_(bstack1ll1ll1111_opy_, options):
    threading.current_thread().a11yPlatform = True
    bstack1llll11l_opy_.set_capabilities(bstack1ll1ll1111_opy_, CONFIG)
  if desired_capabilities:
    bstack1l11l1ll11_opy_ = bstack111ll1ll_opy_(desired_capabilities)
    bstack1l11l1ll11_opy_[bstack111l11_opy_ (u"ࠨࡷࡶࡩ࡜࠹ࡃࠨਘ")] = bstack11ll111ll_opy_(CONFIG)
    bstack11lll1ll1_opy_ = bstack111ll11ll_opy_(bstack1l11l1ll11_opy_)
    if bstack11lll1ll1_opy_:
      bstack1ll1ll1111_opy_ = update(bstack11lll1ll1_opy_, bstack1ll1ll1111_opy_)
    desired_capabilities = None
  if options:
    bstack1l11lllll1_opy_(options, bstack1ll1ll1111_opy_)
  if not options:
    options = bstack1l1llll1l1_opy_(bstack1ll1ll1111_opy_)
  bstack1l1lll11l_opy_ = CONFIG.get(bstack111l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬਙ"))[bstack1ll11lllll_opy_]
  if proxy and bstack1lll1l1ll_opy_() >= version.parse(bstack111l11_opy_ (u"ࠪ࠸࠳࠷࠰࠯࠲ࠪਚ")):
    options.proxy(proxy)
  if options and bstack1lll1l1ll_opy_() >= version.parse(bstack111l11_opy_ (u"ࠫ࠸࠴࠸࠯࠲ࠪਛ")):
    desired_capabilities = None
  if (
          not options and not desired_capabilities
  ) or (
          bstack1lll1l1ll_opy_() < version.parse(bstack111l11_opy_ (u"ࠬ࠹࠮࠹࠰࠳ࠫਜ")) and not desired_capabilities
  ):
    desired_capabilities = {}
    desired_capabilities.update(bstack1ll1ll1111_opy_)
  logger.info(bstack1ll11l1l1_opy_)
  if bstack1lll1l1ll_opy_() >= version.parse(bstack111l11_opy_ (u"࠭࠴࠯࠳࠳࠲࠵࠭ਝ")):
    bstack1ll111l11l_opy_(self, command_executor=command_executor,
              options=options, keep_alive=keep_alive, file_detector=file_detector)
  elif bstack1lll1l1ll_opy_() >= version.parse(bstack111l11_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭ਞ")):
    bstack1ll111l11l_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities, options=options,
              browser_profile=browser_profile, proxy=proxy,
              keep_alive=keep_alive, file_detector=file_detector)
  elif bstack1lll1l1ll_opy_() >= version.parse(bstack111l11_opy_ (u"ࠨ࠴࠱࠹࠸࠴࠰ࠨਟ")):
    bstack1ll111l11l_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities,
              browser_profile=browser_profile, proxy=proxy,
              keep_alive=keep_alive, file_detector=file_detector)
  else:
    bstack1ll111l11l_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities,
              browser_profile=browser_profile, proxy=proxy,
              keep_alive=keep_alive)
  try:
    bstack1llll1l1_opy_ = bstack111l11_opy_ (u"ࠩࠪਠ")
    if bstack1lll1l1ll_opy_() >= version.parse(bstack111l11_opy_ (u"ࠪ࠸࠳࠶࠮࠱ࡤ࠴ࠫਡ")):
      bstack1llll1l1_opy_ = self.caps.get(bstack111l11_opy_ (u"ࠦࡴࡶࡴࡪ࡯ࡤࡰࡍࡻࡢࡖࡴ࡯ࠦਢ"))
    else:
      bstack1llll1l1_opy_ = self.capabilities.get(bstack111l11_opy_ (u"ࠧࡵࡰࡵ࡫ࡰࡥࡱࡎࡵࡣࡗࡵࡰࠧਣ"))
    if bstack1llll1l1_opy_:
      bstack111llllll_opy_(bstack1llll1l1_opy_)
      if bstack1lll1l1ll_opy_() <= version.parse(bstack111l11_opy_ (u"࠭࠳࠯࠳࠶࠲࠵࠭ਤ")):
        self.command_executor._url = bstack111l11_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯ࠣਥ") + bstack1l1l11l11_opy_ + bstack111l11_opy_ (u"ࠣ࠼࠻࠴࠴ࡽࡤ࠰ࡪࡸࡦࠧਦ")
      else:
        self.command_executor._url = bstack111l11_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲ࠦਧ") + bstack1llll1l1_opy_ + bstack111l11_opy_ (u"ࠥ࠳ࡼࡪ࠯ࡩࡷࡥࠦਨ")
      logger.debug(bstack1ll1l111l1_opy_.format(bstack1llll1l1_opy_))
    else:
      logger.debug(bstack1lllll1l11_opy_.format(bstack111l11_opy_ (u"ࠦࡔࡶࡴࡪ࡯ࡤࡰࠥࡎࡵࡣࠢࡱࡳࡹࠦࡦࡰࡷࡱࡨࠧ਩")))
  except Exception as e:
    logger.debug(bstack1lllll1l11_opy_.format(e))
  if bstack111l11_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫਪ") in bstack1lll1ll11_opy_:
    bstack1l1l111l11_opy_(bstack1111111l1_opy_, bstack1ll1ll1l1_opy_)
  bstack1ll111l1_opy_ = self.session_id
  if bstack111l11_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ਫ") in bstack1lll1ll11_opy_ or bstack111l11_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧਬ") in bstack1lll1ll11_opy_ or bstack111l11_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧਭ") in bstack1lll1ll11_opy_:
    threading.current_thread().bstackSessionId = self.session_id
    threading.current_thread().bstackSessionDriver = self
    threading.current_thread().bstackTestErrorMessages = []
    bstack1lll1ll1l_opy_.bstack1l1ll11l11_opy_(self)
  bstack1l1l1ll1l1_opy_.append(self)
  if bstack111l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬਮ") in CONFIG and bstack111l11_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨਯ") in CONFIG[bstack111l11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧਰ")][bstack1ll11lllll_opy_]:
    bstack1l11l11l1_opy_ = CONFIG[bstack111l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ਱")][bstack1ll11lllll_opy_][bstack111l11_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫਲ")]
  logger.debug(bstack11lll11l1_opy_.format(bstack1ll111l1_opy_))
try:
  try:
    import Browser
    from subprocess import Popen
    def bstack11ll1111l_opy_(self, args, bufsize=-1, executable=None,
              stdin=None, stdout=None, stderr=None,
              preexec_fn=None, close_fds=True,
              shell=False, cwd=None, env=None, universal_newlines=None,
              startupinfo=None, creationflags=0,
              restore_signals=True, start_new_session=False,
              pass_fds=(), *, user=None, group=None, extra_groups=None,
              encoding=None, errors=None, text=None, umask=-1, pipesize=-1):
      global CONFIG
      global bstack1ll1l1ll11_opy_
      if(bstack111l11_opy_ (u"ࠢࡪࡰࡧࡩࡽ࠴ࡪࡴࠤਲ਼") in args[1]):
        with open(os.path.join(os.path.expanduser(bstack111l11_opy_ (u"ࠨࢀࠪ਴")), bstack111l11_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩਵ"), bstack111l11_opy_ (u"ࠪ࠲ࡸ࡫ࡳࡴ࡫ࡲࡲ࡮ࡪࡳ࠯ࡶࡻࡸࠬਸ਼")), bstack111l11_opy_ (u"ࠫࡼ࠭਷")) as fp:
          fp.write(bstack111l11_opy_ (u"ࠧࠨਸ"))
        if(not os.path.exists(os.path.join(os.path.dirname(args[1]), bstack111l11_opy_ (u"ࠨࡩ࡯ࡦࡨࡼࡤࡨࡳࡵࡣࡦ࡯࠳ࡰࡳࠣਹ")))):
          with open(args[1], bstack111l11_opy_ (u"ࠧࡳࠩ਺")) as f:
            lines = f.readlines()
            index = next((i for i, line in enumerate(lines) if bstack111l11_opy_ (u"ࠨࡣࡶࡽࡳࡩࠠࡧࡷࡱࡧࡹ࡯࡯࡯ࠢࡢࡲࡪࡽࡐࡢࡩࡨࠬࡨࡵ࡮ࡵࡧࡻࡸ࠱ࠦࡰࡢࡩࡨࠤࡂࠦࡶࡰ࡫ࡧࠤ࠵࠯ࠧ਻") in line), None)
            if index is not None:
                lines.insert(index+2, bstack1lll1111l_opy_)
            lines.insert(1, bstack1llll1111l_opy_)
            f.seek(0)
            with open(os.path.join(os.path.dirname(args[1]), bstack111l11_opy_ (u"ࠤ࡬ࡲࡩ࡫ࡸࡠࡤࡶࡸࡦࡩ࡫࠯࡬ࡶ਼ࠦ")), bstack111l11_opy_ (u"ࠪࡻࠬ਽")) as bstack1l1ll11ll_opy_:
              bstack1l1ll11ll_opy_.writelines(lines)
        CONFIG[bstack111l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭ਾ")] = str(bstack1lll1ll11_opy_) + str(__version__)
        bstack1ll11lllll_opy_ = 0 if bstack1111111l1_opy_ < 0 else bstack1111111l1_opy_
        try:
          if bstack111lll1ll_opy_ is True:
            bstack1ll11lllll_opy_ = int(multiprocessing.current_process().name)
          elif bstack111111111_opy_ is True:
            bstack1ll11lllll_opy_ = int(threading.current_thread().name)
        except:
          bstack1ll11lllll_opy_ = 0
        CONFIG[bstack111l11_opy_ (u"ࠧࡻࡳࡦ࡙࠶ࡇࠧਿ")] = False
        CONFIG[bstack111l11_opy_ (u"ࠨࡩࡴࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠧੀ")] = True
        bstack1ll1ll1111_opy_ = bstack111ll11ll_opy_(CONFIG, bstack1ll11lllll_opy_)
        logger.debug(bstack111l11111_opy_.format(str(bstack1ll1ll1111_opy_)))
        if CONFIG.get(bstack111l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫੁ")):
          bstack111llll1l_opy_(bstack1ll1ll1111_opy_)
        if bstack111l11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫੂ") in CONFIG and bstack111l11_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ੃") in CONFIG[bstack111l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭੄")][bstack1ll11lllll_opy_]:
          bstack1l11l11l1_opy_ = CONFIG[bstack111l11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ੅")][bstack1ll11lllll_opy_][bstack111l11_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ੆")]
        args.append(os.path.join(os.path.expanduser(bstack111l11_opy_ (u"࠭ࡾࠨੇ")), bstack111l11_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧੈ"), bstack111l11_opy_ (u"ࠨ࠰ࡶࡩࡸࡹࡩࡰࡰ࡬ࡨࡸ࠴ࡴࡹࡶࠪ੉")))
        args.append(str(threading.get_ident()))
        args.append(json.dumps(bstack1ll1ll1111_opy_))
        args[1] = os.path.join(os.path.dirname(args[1]), bstack111l11_opy_ (u"ࠤ࡬ࡲࡩ࡫ࡸࡠࡤࡶࡸࡦࡩ࡫࠯࡬ࡶࠦ੊"))
      bstack1ll1l1ll11_opy_ = True
      return bstack1llll111l_opy_(self, args, bufsize=bufsize, executable=executable,
                    stdin=stdin, stdout=stdout, stderr=stderr,
                    preexec_fn=preexec_fn, close_fds=close_fds,
                    shell=shell, cwd=cwd, env=env, universal_newlines=universal_newlines,
                    startupinfo=startupinfo, creationflags=creationflags,
                    restore_signals=restore_signals, start_new_session=start_new_session,
                    pass_fds=pass_fds, user=user, group=group, extra_groups=extra_groups,
                    encoding=encoding, errors=errors, text=text, umask=umask, pipesize=pipesize)
  except Exception as e:
    pass
  import playwright._impl._api_structures
  import playwright._impl._helper
  def bstack1ll11ll1l1_opy_(self,
        executablePath = None,
        channel = None,
        args = None,
        ignoreDefaultArgs = None,
        handleSIGINT = None,
        handleSIGTERM = None,
        handleSIGHUP = None,
        timeout = None,
        env = None,
        headless = None,
        devtools = None,
        proxy = None,
        downloadsPath = None,
        slowMo = None,
        tracesDir = None,
        chromiumSandbox = None,
        firefoxUserPrefs = None
        ):
    global CONFIG
    global bstack1111111l1_opy_
    global bstack1l11l11l1_opy_
    global bstack111lll1ll_opy_
    global bstack111111111_opy_
    global bstack1lll1ll11_opy_
    CONFIG[bstack111l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬੋ")] = str(bstack1lll1ll11_opy_) + str(__version__)
    bstack1ll11lllll_opy_ = 0 if bstack1111111l1_opy_ < 0 else bstack1111111l1_opy_
    try:
      if bstack111lll1ll_opy_ is True:
        bstack1ll11lllll_opy_ = int(multiprocessing.current_process().name)
      elif bstack111111111_opy_ is True:
        bstack1ll11lllll_opy_ = int(threading.current_thread().name)
    except:
      bstack1ll11lllll_opy_ = 0
    CONFIG[bstack111l11_opy_ (u"ࠦ࡮ࡹࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥੌ")] = True
    bstack1ll1ll1111_opy_ = bstack111ll11ll_opy_(CONFIG, bstack1ll11lllll_opy_)
    logger.debug(bstack111l11111_opy_.format(str(bstack1ll1ll1111_opy_)))
    if CONFIG.get(bstack111l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭੍ࠩ")):
      bstack111llll1l_opy_(bstack1ll1ll1111_opy_)
    if bstack111l11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ੎") in CONFIG and bstack111l11_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬ੏") in CONFIG[bstack111l11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ੐")][bstack1ll11lllll_opy_]:
      bstack1l11l11l1_opy_ = CONFIG[bstack111l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬੑ")][bstack1ll11lllll_opy_][bstack111l11_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ੒")]
    import urllib
    import json
    bstack11l1111l_opy_ = bstack111l11_opy_ (u"ࠫࡼࡹࡳ࠻࠱࠲ࡧࡩࡶ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠿ࡤࡣࡳࡷࡂ࠭੓") + urllib.parse.quote(json.dumps(bstack1ll1ll1111_opy_))
    browser = self.connect(bstack11l1111l_opy_)
    return browser
except Exception as e:
    pass
def bstack1ll1lllll_opy_():
    global bstack1ll1l1ll11_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        BrowserType.launch = bstack1ll11ll1l1_opy_
        bstack1ll1l1ll11_opy_ = True
    except Exception as e:
        pass
    try:
      import Browser
      from subprocess import Popen
      Popen.__init__ = bstack11ll1111l_opy_
      bstack1ll1l1ll11_opy_ = True
    except Exception as e:
      pass
def bstack11111111_opy_(context, bstack1l11lll11l_opy_):
  try:
    context.page.evaluate(bstack111l11_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨ੔"), bstack111l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡲࡦࡳࡥࠣ࠼ࠪ੕")+ json.dumps(bstack1l11lll11l_opy_) + bstack111l11_opy_ (u"ࠢࡾࡿࠥ੖"))
  except Exception as e:
    logger.debug(bstack111l11_opy_ (u"ࠣࡧࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧࠣࡿࢂࠨ੗"), e)
def bstack1lll1l1111_opy_(context, message, level):
  try:
    context.page.evaluate(bstack111l11_opy_ (u"ࠤࡢࠤࡂࡄࠠࡼࡿࠥ੘"), bstack111l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡦࡤࡸࡦࠨ࠺ࠨਖ਼") + json.dumps(message) + bstack111l11_opy_ (u"ࠫ࠱ࠨ࡬ࡦࡸࡨࡰࠧࡀࠧਗ਼") + json.dumps(level) + bstack111l11_opy_ (u"ࠬࢃࡽࠨਜ਼"))
  except Exception as e:
    logger.debug(bstack111l11_opy_ (u"ࠨࡥࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡤࡲࡳࡵࡴࡢࡶ࡬ࡳࡳࠦࡻࡾࠤੜ"), e)
def bstack11111ll1l_opy_(self, url):
  global bstack1l1ll1l11l_opy_
  try:
    bstack11l111ll1_opy_(url)
  except Exception as err:
    logger.debug(bstack1l1l111l1_opy_.format(str(err)))
  try:
    bstack1l1ll1l11l_opy_(self, url)
  except Exception as e:
    try:
      bstack1l1l11lll_opy_ = str(e)
      if any(err_msg in bstack1l1l11lll_opy_ for err_msg in bstack11l11lll1_opy_):
        bstack11l111ll1_opy_(url, True)
    except Exception as err:
      logger.debug(bstack1l1l111l1_opy_.format(str(err)))
    raise e
def bstack1111l1l1_opy_(self):
  global bstack1lll1l11_opy_
  bstack1lll1l11_opy_ = self
  return
def bstack1l1ll1ll1l_opy_(self):
  global bstack1l1lll1111_opy_
  bstack1l1lll1111_opy_ = self
  return
def bstack1ll111l111_opy_(test_name, bstack1lll1111ll_opy_):
  global CONFIG
  if CONFIG.get(bstack111l11_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭੝"), False):
    bstack1l1l1l1ll_opy_ = os.path.relpath(bstack1lll1111ll_opy_, start=os.getcwd())
    suite_name, _ = os.path.splitext(bstack1l1l1l1ll_opy_)
    bstack11l1lll11_opy_ = suite_name + bstack111l11_opy_ (u"ࠣ࠯ࠥਫ਼") + test_name
    threading.current_thread().percySessionName = bstack11l1lll11_opy_
def bstack1lll11ll11_opy_(self, test, *args, **kwargs):
  global bstack111l1l11l_opy_
  test_name = None
  bstack1lll1111ll_opy_ = None
  if test:
    test_name = str(test.name)
    bstack1lll1111ll_opy_ = str(test.source)
  bstack1ll111l111_opy_(test_name, bstack1lll1111ll_opy_)
  bstack111l1l11l_opy_(self, test, *args, **kwargs)
def bstack1lll11llll_opy_(driver, bstack11l1lll11_opy_):
  if not bstack1ll11lll_opy_ and bstack11l1lll11_opy_:
      bstack11l1l1lll_opy_ = {
          bstack111l11_opy_ (u"ࠩࡤࡧࡹ࡯࡯࡯ࠩ੟"): bstack111l11_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ੠"),
          bstack111l11_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧ੡"): {
              bstack111l11_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ੢"): bstack11l1lll11_opy_
          }
      }
      bstack111l1lll_opy_ = bstack111l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠫ੣").format(json.dumps(bstack11l1l1lll_opy_))
      driver.execute_script(bstack111l1lll_opy_)
  if bstack1lll1llll1_opy_:
      bstack11l11ll11_opy_ = {
          bstack111l11_opy_ (u"ࠧࡢࡥࡷ࡭ࡴࡴࠧ੤"): bstack111l11_opy_ (u"ࠨࡣࡱࡲࡴࡺࡡࡵࡧࠪ੥"),
          bstack111l11_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬ੦"): {
              bstack111l11_opy_ (u"ࠪࡨࡦࡺࡡࠨ੧"): bstack11l1lll11_opy_ + bstack111l11_opy_ (u"ࠫࠥࡶࡡࡴࡵࡨࡨࠦ࠭੨"),
              bstack111l11_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫ੩"): bstack111l11_opy_ (u"࠭ࡩ࡯ࡨࡲࠫ੪")
          }
      }
      if bstack1lll1llll1_opy_.status == bstack111l11_opy_ (u"ࠧࡑࡃࡖࡗࠬ੫"):
          bstack1ll1l11ll1_opy_ = bstack111l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࢂ࠭੬").format(json.dumps(bstack11l11ll11_opy_))
          driver.execute_script(bstack1ll1l11ll1_opy_)
          bstack1l1l11llll_opy_(driver, bstack111l11_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ੭"))
      elif bstack1lll1llll1_opy_.status == bstack111l11_opy_ (u"ࠪࡊࡆࡏࡌࠨ੮"):
          reason = bstack111l11_opy_ (u"ࠦࠧ੯")
          bstack11111111l_opy_ = bstack11l1lll11_opy_ + bstack111l11_opy_ (u"ࠬࠦࡦࡢ࡫࡯ࡩࡩ࠭ੰ")
          if bstack1lll1llll1_opy_.message:
              reason = str(bstack1lll1llll1_opy_.message)
              bstack11111111l_opy_ = bstack11111111l_opy_ + bstack111l11_opy_ (u"࠭ࠠࡸ࡫ࡷ࡬ࠥ࡫ࡲࡳࡱࡵ࠾ࠥ࠭ੱ") + reason
          bstack11l11ll11_opy_[bstack111l11_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪੲ")] = {
              bstack111l11_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧੳ"): bstack111l11_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨੴ"),
              bstack111l11_opy_ (u"ࠪࡨࡦࡺࡡࠨੵ"): bstack11111111l_opy_
          }
          bstack1ll1l11ll1_opy_ = bstack111l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠩ੶").format(json.dumps(bstack11l11ll11_opy_))
          driver.execute_script(bstack1ll1l11ll1_opy_)
          bstack1l1l11llll_opy_(driver, bstack111l11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ੷"), reason)
          bstack11ll11l1l_opy_(reason, str(bstack1lll1llll1_opy_), str(bstack1111111l1_opy_), logger)
def bstack1lll1l111l_opy_(driver, test):
  if CONFIG.get(bstack111l11_opy_ (u"࠭ࡰࡦࡴࡦࡽࠬ੸"), False) and CONFIG.get(bstack111l11_opy_ (u"ࠧࡱࡧࡵࡧࡾࡉࡡࡱࡶࡸࡶࡪࡓ࡯ࡥࡧࠪ੹"), bstack111l11_opy_ (u"ࠣࡣࡸࡸࡴࠨ੺")) == bstack111l11_opy_ (u"ࠤࡷࡩࡸࡺࡣࡢࡵࡨࠦ੻"):
      bstack1l111ll1l_opy_ = bstack1ll111l1ll_opy_(threading.current_thread(), bstack111l11_opy_ (u"ࠪࡴࡪࡸࡣࡺࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭੼"), None)
      bstack1lll11lll1_opy_(driver, bstack1l111ll1l_opy_)
  if bstack1ll111l1ll_opy_(threading.current_thread(), bstack111l11_opy_ (u"ࠫ࡮ࡹࡁ࠲࠳ࡼࡘࡪࡹࡴࠨ੽"), None) and bstack1ll111l1ll_opy_(
          threading.current_thread(), bstack111l11_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫ੾"), None):
      logger.info(bstack111l11_opy_ (u"ࠨࡁࡶࡶࡲࡱࡦࡺࡥࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨࠤࡪࡾࡥࡤࡷࡷ࡭ࡴࡴࠠࡩࡣࡶࠤࡪࡴࡤࡦࡦ࠱ࠤࡕࡸ࡯ࡤࡧࡶࡷ࡮ࡴࡧࠡࡨࡲࡶࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡺࡥࡴࡶ࡬ࡲ࡬ࠦࡩࡴࠢࡸࡲࡩ࡫ࡲࡸࡣࡼ࠲ࠥࠨ੿"))
      bstack1llll11l_opy_.bstack1ll111l1l1_opy_(driver, class_name=test.parent.name, name=test.name, module_name=None,
                              path=test.source, bstack1ll1l1ll1_opy_=bstack1l1lll11l_opy_)
def bstack1ll1111ll_opy_(test, bstack11l1lll11_opy_):
    try:
      data = {}
      if test:
        data[bstack111l11_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ઀")] = bstack11l1lll11_opy_
      if bstack1lll1llll1_opy_:
        if bstack1lll1llll1_opy_.status == bstack111l11_opy_ (u"ࠨࡒࡄࡗࡘ࠭ઁ"):
          data[bstack111l11_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩં")] = bstack111l11_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪઃ")
        elif bstack1lll1llll1_opy_.status == bstack111l11_opy_ (u"ࠫࡋࡇࡉࡍࠩ઄"):
          data[bstack111l11_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬઅ")] = bstack111l11_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭આ")
          if bstack1lll1llll1_opy_.message:
            data[bstack111l11_opy_ (u"ࠧࡳࡧࡤࡷࡴࡴࠧઇ")] = str(bstack1lll1llll1_opy_.message)
      user = CONFIG[bstack111l11_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪઈ")]
      key = CONFIG[bstack111l11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬઉ")]
      url = bstack111l11_opy_ (u"ࠪ࡬ࡹࡺࡰࡴ࠼࠲࠳ࢀࢃ࠺ࡼࡿࡃࡥࡵ࡯࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡥࡺࡺ࡯࡮ࡣࡷࡩ࠴ࡹࡥࡴࡵ࡬ࡳࡳࡹ࠯ࡼࡿ࠱࡮ࡸࡵ࡮ࠨઊ").format(user, key, bstack1ll111l1_opy_)
      headers = {
        bstack111l11_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲ࡺࡹࡱࡧࠪઋ"): bstack111l11_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠨઌ"),
      }
      if bool(data):
        requests.put(url, json=data, headers=headers)
    except Exception as e:
      logger.error(bstack1l1llll11l_opy_.format(str(e)))
def bstack1ll11111_opy_(test, bstack11l1lll11_opy_):
  global CONFIG
  global bstack1l1lll1111_opy_
  global bstack1lll1l11_opy_
  global bstack1ll111l1_opy_
  global bstack1lll1llll1_opy_
  global bstack1l11l11l1_opy_
  global bstack1ll1l1lll1_opy_
  global bstack1ll1l11l_opy_
  global bstack11l1l111l_opy_
  global bstack11lll1l1_opy_
  global bstack1l1l1ll1l1_opy_
  global bstack1l1lll11l_opy_
  try:
    if not bstack1ll111l1_opy_:
      with open(os.path.join(os.path.expanduser(bstack111l11_opy_ (u"࠭ࡾࠨઍ")), bstack111l11_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧ઎"), bstack111l11_opy_ (u"ࠨ࠰ࡶࡩࡸࡹࡩࡰࡰ࡬ࡨࡸ࠴ࡴࡹࡶࠪએ"))) as f:
        bstack1l1l11l111_opy_ = json.loads(bstack111l11_opy_ (u"ࠤࡾࠦઐ") + f.read().strip() + bstack111l11_opy_ (u"ࠪࠦࡽࠨ࠺ࠡࠤࡼࠦࠬઑ") + bstack111l11_opy_ (u"ࠦࢂࠨ઒"))
        bstack1ll111l1_opy_ = bstack1l1l11l111_opy_[str(threading.get_ident())]
  except:
    pass
  if bstack1l1l1ll1l1_opy_:
    for driver in bstack1l1l1ll1l1_opy_:
      if bstack1ll111l1_opy_ == driver.session_id:
        if test:
          bstack1lll1l111l_opy_(driver, test)
        bstack1lll11llll_opy_(driver, bstack11l1lll11_opy_)
  elif bstack1ll111l1_opy_:
    bstack1ll1111ll_opy_(test, bstack11l1lll11_opy_)
  if bstack1l1lll1111_opy_:
    bstack1ll1l11l_opy_(bstack1l1lll1111_opy_)
  if bstack1lll1l11_opy_:
    bstack11l1l111l_opy_(bstack1lll1l11_opy_)
  if bstack1ll1111l1_opy_:
    bstack11lll1l1_opy_()
def bstack11l1lll1l_opy_(self, test, *args, **kwargs):
  bstack11l1lll11_opy_ = None
  if test:
    bstack11l1lll11_opy_ = str(test.name)
  bstack1ll11111_opy_(test, bstack11l1lll11_opy_)
  bstack1ll1l1lll1_opy_(self, test, *args, **kwargs)
def bstack1111lllll_opy_(self, parent, test, skip_on_failure=None, rpa=False):
  global bstack1l11ll11_opy_
  global CONFIG
  global bstack1l1l1ll1l1_opy_
  global bstack1ll111l1_opy_
  bstack1l1l111ll_opy_ = None
  try:
    if bstack1ll111l1ll_opy_(threading.current_thread(), bstack111l11_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫઓ"), None):
      try:
        if not bstack1ll111l1_opy_:
          with open(os.path.join(os.path.expanduser(bstack111l11_opy_ (u"࠭ࡾࠨઔ")), bstack111l11_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧક"), bstack111l11_opy_ (u"ࠨ࠰ࡶࡩࡸࡹࡩࡰࡰ࡬ࡨࡸ࠴ࡴࡹࡶࠪખ"))) as f:
            bstack1l1l11l111_opy_ = json.loads(bstack111l11_opy_ (u"ࠤࡾࠦગ") + f.read().strip() + bstack111l11_opy_ (u"ࠪࠦࡽࠨ࠺ࠡࠤࡼࠦࠬઘ") + bstack111l11_opy_ (u"ࠦࢂࠨઙ"))
            bstack1ll111l1_opy_ = bstack1l1l11l111_opy_[str(threading.get_ident())]
      except:
        pass
      if bstack1l1l1ll1l1_opy_:
        for driver in bstack1l1l1ll1l1_opy_:
          if bstack1ll111l1_opy_ == driver.session_id:
            bstack1l1l111ll_opy_ = driver
    bstack1l11l1111_opy_ = bstack1llll11l_opy_.bstack1l1111l11_opy_(CONFIG, test.tags)
    if bstack1l1l111ll_opy_:
      threading.current_thread().isA11yTest = bstack1llll11l_opy_.bstack1llll1l111_opy_(bstack1l1l111ll_opy_, bstack1l11l1111_opy_)
    else:
      threading.current_thread().isA11yTest = bstack1l11l1111_opy_
  except:
    pass
  bstack1l11ll11_opy_(self, parent, test, skip_on_failure=skip_on_failure, rpa=rpa)
  global bstack1lll1llll1_opy_
  bstack1lll1llll1_opy_ = self._test
def bstack1l1llll1l_opy_():
  global bstack11l11l11_opy_
  try:
    if os.path.exists(bstack11l11l11_opy_):
      os.remove(bstack11l11l11_opy_)
  except Exception as e:
    logger.debug(bstack111l11_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡥࡧ࡯ࡩࡹ࡯࡮ࡨࠢࡵࡳࡧࡵࡴࠡࡴࡨࡴࡴࡸࡴࠡࡨ࡬ࡰࡪࡀࠠࠨચ") + str(e))
def bstack111l1111l_opy_():
  global bstack11l11l11_opy_
  bstack1111ll1l1_opy_ = {}
  try:
    if not os.path.isfile(bstack11l11l11_opy_):
      with open(bstack11l11l11_opy_, bstack111l11_opy_ (u"࠭ࡷࠨછ")):
        pass
      with open(bstack11l11l11_opy_, bstack111l11_opy_ (u"ࠢࡸ࠭ࠥજ")) as outfile:
        json.dump({}, outfile)
    if os.path.exists(bstack11l11l11_opy_):
      bstack1111ll1l1_opy_ = json.load(open(bstack11l11l11_opy_, bstack111l11_opy_ (u"ࠨࡴࡥࠫઝ")))
  except Exception as e:
    logger.debug(bstack111l11_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡷ࡫ࡡࡥ࡫ࡱ࡫ࠥࡸ࡯ࡣࡱࡷࠤࡷ࡫ࡰࡰࡴࡷࠤ࡫࡯࡬ࡦ࠼ࠣࠫઞ") + str(e))
  finally:
    return bstack1111ll1l1_opy_
def bstack1l1l111l11_opy_(platform_index, item_index):
  global bstack11l11l11_opy_
  try:
    bstack1111ll1l1_opy_ = bstack111l1111l_opy_()
    bstack1111ll1l1_opy_[item_index] = platform_index
    with open(bstack11l11l11_opy_, bstack111l11_opy_ (u"ࠥࡻ࠰ࠨટ")) as outfile:
      json.dump(bstack1111ll1l1_opy_, outfile)
  except Exception as e:
    logger.debug(bstack111l11_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡷࡳ࡫ࡷ࡭ࡳ࡭ࠠࡵࡱࠣࡶࡴࡨ࡯ࡵࠢࡵࡩࡵࡵࡲࡵࠢࡩ࡭ࡱ࡫࠺ࠡࠩઠ") + str(e))
def bstack1l1llll11_opy_(bstack11l11111_opy_):
  global CONFIG
  bstack11111lll_opy_ = bstack111l11_opy_ (u"ࠬ࠭ડ")
  if not bstack111l11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩઢ") in CONFIG:
    logger.info(bstack111l11_opy_ (u"ࠧࡏࡱࠣࡴࡱࡧࡴࡧࡱࡵࡱࡸࠦࡰࡢࡵࡶࡩࡩࠦࡵ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡪࡩࡳ࡫ࡲࡢࡶࡨࠤࡷ࡫ࡰࡰࡴࡷࠤ࡫ࡵࡲࠡࡔࡲࡦࡴࡺࠠࡳࡷࡱࠫણ"))
  try:
    platform = CONFIG[bstack111l11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫત")][bstack11l11111_opy_]
    if bstack111l11_opy_ (u"ࠩࡲࡷࠬથ") in platform:
      bstack11111lll_opy_ += str(platform[bstack111l11_opy_ (u"ࠪࡳࡸ࠭દ")]) + bstack111l11_opy_ (u"ࠫ࠱ࠦࠧધ")
    if bstack111l11_opy_ (u"ࠬࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠨન") in platform:
      bstack11111lll_opy_ += str(platform[bstack111l11_opy_ (u"࠭࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩ઩")]) + bstack111l11_opy_ (u"ࠧ࠭ࠢࠪપ")
    if bstack111l11_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠬફ") in platform:
      bstack11111lll_opy_ += str(platform[bstack111l11_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪ࠭બ")]) + bstack111l11_opy_ (u"ࠪ࠰ࠥ࠭ભ")
    if bstack111l11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭મ") in platform:
      bstack11111lll_opy_ += str(platform[bstack111l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠧય")]) + bstack111l11_opy_ (u"࠭ࠬࠡࠩર")
    if bstack111l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬ઱") in platform:
      bstack11111lll_opy_ += str(platform[bstack111l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭લ")]) + bstack111l11_opy_ (u"ࠩ࠯ࠤࠬળ")
    if bstack111l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫ઴") in platform:
      bstack11111lll_opy_ += str(platform[bstack111l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬવ")]) + bstack111l11_opy_ (u"ࠬ࠲ࠠࠨશ")
  except Exception as e:
    logger.debug(bstack111l11_opy_ (u"࠭ࡓࡰ࡯ࡨࠤࡪࡸࡲࡰࡴࠣ࡭ࡳࠦࡧࡦࡰࡨࡶࡦࡺࡩ࡯ࡩࠣࡴࡱࡧࡴࡧࡱࡵࡱࠥࡹࡴࡳ࡫ࡱ࡫ࠥ࡬࡯ࡳࠢࡵࡩࡵࡵࡲࡵࠢࡪࡩࡳ࡫ࡲࡢࡶ࡬ࡳࡳ࠭ષ") + str(e))
  finally:
    if bstack11111lll_opy_[len(bstack11111lll_opy_) - 2:] == bstack111l11_opy_ (u"ࠧ࠭ࠢࠪસ"):
      bstack11111lll_opy_ = bstack11111lll_opy_[:-2]
    return bstack11111lll_opy_
def bstack11l1l1ll1_opy_(path, bstack11111lll_opy_):
  try:
    import xml.etree.ElementTree as ET
    bstack1l11ll11ll_opy_ = ET.parse(path)
    bstack1ll111l11_opy_ = bstack1l11ll11ll_opy_.getroot()
    bstack1111l1ll_opy_ = None
    for suite in bstack1ll111l11_opy_.iter(bstack111l11_opy_ (u"ࠨࡵࡸ࡭ࡹ࡫ࠧહ")):
      if bstack111l11_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩ઺") in suite.attrib:
        suite.attrib[bstack111l11_opy_ (u"ࠪࡲࡦࡳࡥࠨ઻")] += bstack111l11_opy_ (u"઼ࠫࠥ࠭") + bstack11111lll_opy_
        bstack1111l1ll_opy_ = suite
    bstack1ll1l1llll_opy_ = None
    for robot in bstack1ll111l11_opy_.iter(bstack111l11_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫઽ")):
      bstack1ll1l1llll_opy_ = robot
    bstack1l11lll111_opy_ = len(bstack1ll1l1llll_opy_.findall(bstack111l11_opy_ (u"࠭ࡳࡶ࡫ࡷࡩࠬા")))
    if bstack1l11lll111_opy_ == 1:
      bstack1ll1l1llll_opy_.remove(bstack1ll1l1llll_opy_.findall(bstack111l11_opy_ (u"ࠧࡴࡷ࡬ࡸࡪ࠭િ"))[0])
      bstack1ll1lll111_opy_ = ET.Element(bstack111l11_opy_ (u"ࠨࡵࡸ࡭ࡹ࡫ࠧી"), attrib={bstack111l11_opy_ (u"ࠩࡱࡥࡲ࡫ࠧુ"): bstack111l11_opy_ (u"ࠪࡗࡺ࡯ࡴࡦࡵࠪૂ"), bstack111l11_opy_ (u"ࠫ࡮ࡪࠧૃ"): bstack111l11_opy_ (u"ࠬࡹ࠰ࠨૄ")})
      bstack1ll1l1llll_opy_.insert(1, bstack1ll1lll111_opy_)
      bstack1ll1l111ll_opy_ = None
      for suite in bstack1ll1l1llll_opy_.iter(bstack111l11_opy_ (u"࠭ࡳࡶ࡫ࡷࡩࠬૅ")):
        bstack1ll1l111ll_opy_ = suite
      bstack1ll1l111ll_opy_.append(bstack1111l1ll_opy_)
      bstack1111lll1_opy_ = None
      for status in bstack1111l1ll_opy_.iter(bstack111l11_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ૆")):
        bstack1111lll1_opy_ = status
      bstack1ll1l111ll_opy_.append(bstack1111lll1_opy_)
    bstack1l11ll11ll_opy_.write(path)
  except Exception as e:
    logger.debug(bstack111l11_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡴࡦࡸࡳࡪࡰࡪࠤࡼ࡮ࡩ࡭ࡧࠣ࡫ࡪࡴࡥࡳࡣࡷ࡭ࡳ࡭ࠠࡳࡱࡥࡳࡹࠦࡲࡦࡲࡲࡶࡹ࠭ે") + str(e))
def bstack1l1l111ll1_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name):
  global bstack1llll1lll1_opy_
  global CONFIG
  if bstack111l11_opy_ (u"ࠤࡳࡽࡹ࡮࡯࡯ࡲࡤࡸ࡭ࠨૈ") in options:
    del options[bstack111l11_opy_ (u"ࠥࡴࡾࡺࡨࡰࡰࡳࡥࡹ࡮ࠢૉ")]
  bstack1lll1l1l_opy_ = bstack111l1111l_opy_()
  for bstack1l1lll1ll_opy_ in bstack1lll1l1l_opy_.keys():
    path = os.path.join(os.getcwd(), bstack111l11_opy_ (u"ࠫࡵࡧࡢࡰࡶࡢࡶࡪࡹࡵ࡭ࡶࡶࠫ૊"), str(bstack1l1lll1ll_opy_), bstack111l11_opy_ (u"ࠬࡵࡵࡵࡲࡸࡸ࠳ࡾ࡭࡭ࠩો"))
    bstack11l1l1ll1_opy_(path, bstack1l1llll11_opy_(bstack1lll1l1l_opy_[bstack1l1lll1ll_opy_]))
  bstack1l1llll1l_opy_()
  return bstack1llll1lll1_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name)
def bstack1l1111l1_opy_(self, ff_profile_dir):
  global bstack1l1ll1l1_opy_
  if not ff_profile_dir:
    return None
  return bstack1l1ll1l1_opy_(self, ff_profile_dir)
def bstack1111ll1l_opy_(datasources, opts_for_run, outs_dir, pabot_args, suite_group):
  from pabot.pabot import QueueItem
  global CONFIG
  global bstack1l11ll1l_opy_
  bstack111l1lll1_opy_ = []
  if bstack111l11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩૌ") in CONFIG:
    bstack111l1lll1_opy_ = CONFIG[bstack111l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵ્ࠪ")]
  return [
    QueueItem(
      datasources,
      outs_dir,
      opts_for_run,
      suite,
      pabot_args[bstack111l11_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࠤ૎")],
      pabot_args[bstack111l11_opy_ (u"ࠤࡹࡩࡷࡨ࡯ࡴࡧࠥ૏")],
      argfile,
      pabot_args.get(bstack111l11_opy_ (u"ࠥ࡬࡮ࡼࡥࠣૐ")),
      pabot_args[bstack111l11_opy_ (u"ࠦࡵࡸ࡯ࡤࡧࡶࡷࡪࡹࠢ૑")],
      platform[0],
      bstack1l11ll1l_opy_
    )
    for suite in suite_group
    for argfile in pabot_args[bstack111l11_opy_ (u"ࠧࡧࡲࡨࡷࡰࡩࡳࡺࡦࡪ࡮ࡨࡷࠧ૒")] or [(bstack111l11_opy_ (u"ࠨࠢ૓"), None)]
    for platform in enumerate(bstack111l1lll1_opy_)
  ]
def bstack1lll11l111_opy_(self, datasources, outs_dir, options,
                        execution_item, command, verbose, argfile,
                        hive=None, processes=0, platform_index=0, bstack1ll1lll11_opy_=bstack111l11_opy_ (u"ࠧࠨ૔")):
  global bstack1ll1l1ll1l_opy_
  self.platform_index = platform_index
  self.bstack1111llll1_opy_ = bstack1ll1lll11_opy_
  bstack1ll1l1ll1l_opy_(self, datasources, outs_dir, options,
                      execution_item, command, verbose, argfile, hive, processes)
def bstack11lllll11_opy_(caller_id, datasources, is_last, item, outs_dir):
  global bstack1lll1llll_opy_
  global bstack111ll1l11_opy_
  bstack1l1l111l_opy_ = copy.deepcopy(item)
  if not bstack111l11_opy_ (u"ࠨࡸࡤࡶ࡮ࡧࡢ࡭ࡧࠪ૕") in item.options:
    bstack1l1l111l_opy_.options[bstack111l11_opy_ (u"ࠩࡹࡥࡷ࡯ࡡࡣ࡮ࡨࠫ૖")] = []
  bstack11l1ll1ll_opy_ = bstack1l1l111l_opy_.options[bstack111l11_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬ૗")].copy()
  for v in bstack1l1l111l_opy_.options[bstack111l11_opy_ (u"ࠫࡻࡧࡲࡪࡣࡥࡰࡪ࠭૘")]:
    if bstack111l11_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡕࡒࡁࡕࡈࡒࡖࡒࡏࡎࡅࡇ࡛ࠫ૙") in v:
      bstack11l1ll1ll_opy_.remove(v)
    if bstack111l11_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡉࡌࡊࡃࡕࡋࡘ࠭૚") in v:
      bstack11l1ll1ll_opy_.remove(v)
    if bstack111l11_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑࡄࡆࡈࡏࡓࡈࡇࡌࡊࡆࡈࡒ࡙ࡏࡆࡊࡇࡕࠫ૛") in v:
      bstack11l1ll1ll_opy_.remove(v)
  bstack11l1ll1ll_opy_.insert(0, bstack111l11_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡑࡎࡄࡘࡋࡕࡒࡎࡋࡑࡈࡊ࡞࠺ࡼࡿࠪ૜").format(bstack1l1l111l_opy_.platform_index))
  bstack11l1ll1ll_opy_.insert(0, bstack111l11_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡆࡈࡊࡑࡕࡃࡂࡎࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗࡀࡻࡾࠩ૝").format(bstack1l1l111l_opy_.bstack1111llll1_opy_))
  bstack1l1l111l_opy_.options[bstack111l11_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬ૞")] = bstack11l1ll1ll_opy_
  if bstack111ll1l11_opy_:
    bstack1l1l111l_opy_.options[bstack111l11_opy_ (u"ࠫࡻࡧࡲࡪࡣࡥࡰࡪ࠭૟")].insert(0, bstack111l11_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡈࡒࡉࡂࡔࡊࡗ࠿ࢁࡽࠨૠ").format(bstack111ll1l11_opy_))
  return bstack1lll1llll_opy_(caller_id, datasources, is_last, bstack1l1l111l_opy_, outs_dir)
def bstack1ll11ll1_opy_(command, item_index):
  if bstack1l11l111ll_opy_.get_property(bstack111l11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡳࡦࡵࡶ࡭ࡴࡴࠧૡ")):
    os.environ[bstack111l11_opy_ (u"ࠧࡄࡗࡕࡖࡊࡔࡔࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡈࡆ࡚ࡁࠨૢ")] = json.dumps(CONFIG[bstack111l11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫૣ")][item_index % bstack1l1ll1111l_opy_])
  global bstack111ll1l11_opy_
  if bstack111ll1l11_opy_:
    command[0] = command[0].replace(bstack111l11_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ૤"), bstack111l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠯ࡶࡨࡰࠦࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠠ࠮࠯ࡥࡷࡹࡧࡣ࡬ࡡ࡬ࡸࡪࡳ࡟ࡪࡰࡧࡩࡽࠦࠧ૥") + str(
      item_index) + bstack111l11_opy_ (u"ࠫࠥ࠭૦") + bstack111ll1l11_opy_, 1)
  else:
    command[0] = command[0].replace(bstack111l11_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫ૧"),
                                    bstack111l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠲ࡹࡤ࡬ࠢࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠣ࠱࠲ࡨࡳࡵࡣࡦ࡯ࡤ࡯ࡴࡦ࡯ࡢ࡭ࡳࡪࡥࡹࠢࠪ૨") + str(item_index), 1)
def bstack1l1111ll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index):
  global bstack1llll1l1ll_opy_
  bstack1ll11ll1_opy_(command, item_index)
  return bstack1llll1l1ll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
def bstack1l1ll1111_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir):
  global bstack1llll1l1ll_opy_
  bstack1ll11ll1_opy_(command, item_index)
  return bstack1llll1l1ll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir)
def bstack1l1l1lll1l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout):
  global bstack1llll1l1ll_opy_
  bstack1ll11ll1_opy_(command, item_index)
  return bstack1llll1l1ll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
def bstack1llllll1l1_opy_(self, runner, quiet=False, capture=True):
  global bstack11l1ll11_opy_
  bstack111ll1l1_opy_ = bstack11l1ll11_opy_(self, runner, quiet=quiet, capture=capture)
  if self.exception:
    if not hasattr(runner, bstack111l11_opy_ (u"ࠧࡦࡺࡦࡩࡵࡺࡩࡰࡰࡢࡥࡷࡸࠧ૩")):
      runner.exception_arr = []
    if not hasattr(runner, bstack111l11_opy_ (u"ࠨࡧࡻࡧࡤࡺࡲࡢࡥࡨࡦࡦࡩ࡫ࡠࡣࡵࡶࠬ૪")):
      runner.exc_traceback_arr = []
    runner.exception = self.exception
    runner.exc_traceback = self.exc_traceback
    runner.exception_arr.append(self.exception)
    runner.exc_traceback_arr.append(self.exc_traceback)
  return bstack111ll1l1_opy_
def bstack11ll1ll11_opy_(self, name, context, *args):
  os.environ[bstack111l11_opy_ (u"ࠩࡆ࡙ࡗࡘࡅࡏࡖࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡊࡁࡕࡃࠪ૫")] = json.dumps(CONFIG[bstack111l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭૬")][int(threading.current_thread()._name) % bstack1l1ll1111l_opy_])
  global bstack11ll1lll_opy_
  if name == bstack111l11_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࡣ࡫࡫ࡡࡵࡷࡵࡩࠬ૭"):
    bstack11ll1lll_opy_(self, name, context, *args)
    try:
      if not bstack1ll11lll_opy_:
        bstack1l1l111ll_opy_ = threading.current_thread().bstackSessionDriver if bstack111ll1ll1_opy_(bstack111l11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫ૮")) else context.browser
        bstack1l11lll11l_opy_ = str(self.feature.name)
        bstack11111111_opy_(context, bstack1l11lll11l_opy_)
        bstack1l1l111ll_opy_.execute_script(bstack111l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡲࡦࡳࡥࠣ࠼ࠣࠫ૯") + json.dumps(bstack1l11lll11l_opy_) + bstack111l11_opy_ (u"ࠧࡾࡿࠪ૰"))
      self.driver_before_scenario = False
    except Exception as e:
      logger.debug(bstack111l11_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡱࡥࡲ࡫ࠠࡪࡰࠣࡦࡪ࡬࡯ࡳࡧࠣࡪࡪࡧࡴࡶࡴࡨ࠾ࠥࢁࡽࠨ૱").format(str(e)))
  elif name == bstack111l11_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠫ૲"):
    bstack11ll1lll_opy_(self, name, context, *args)
    try:
      if not hasattr(self, bstack111l11_opy_ (u"ࠪࡨࡷ࡯ࡶࡦࡴࡢࡦࡪ࡬࡯ࡳࡧࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬ૳")):
        self.driver_before_scenario = True
      if (not bstack1ll11lll_opy_):
        scenario_name = args[0].name
        feature_name = bstack1l11lll11l_opy_ = str(self.feature.name)
        bstack1l11lll11l_opy_ = feature_name + bstack111l11_opy_ (u"ࠫࠥ࠳ࠠࠨ૴") + scenario_name
        bstack1l1l111ll_opy_ = threading.current_thread().bstackSessionDriver if bstack111ll1ll1_opy_(bstack111l11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫ૵")) else context.browser
        if self.driver_before_scenario:
          bstack11111111_opy_(context, bstack1l11lll11l_opy_)
          bstack1l1l111ll_opy_.execute_script(bstack111l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡲࡦࡳࡥࠣ࠼ࠣࠫ૶") + json.dumps(bstack1l11lll11l_opy_) + bstack111l11_opy_ (u"ࠧࡾࡿࠪ૷"))
    except Exception as e:
      logger.debug(bstack111l11_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡱࡥࡲ࡫ࠠࡪࡰࠣࡦࡪ࡬࡯ࡳࡧࠣࡷࡨ࡫࡮ࡢࡴ࡬ࡳ࠿ࠦࡻࡾࠩ૸").format(str(e)))
  elif name == bstack111l11_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡵࡦࡩࡳࡧࡲࡪࡱࠪૹ"):
    try:
      bstack1l1ll1l1ll_opy_ = args[0].status.name
      bstack1l1l111ll_opy_ = threading.current_thread().bstackSessionDriver if bstack111l11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩૺ") in threading.current_thread().__dict__.keys() else context.browser
      if str(bstack1l1ll1l1ll_opy_).lower() == bstack111l11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫૻ"):
        bstack1lll1lll1_opy_ = bstack111l11_opy_ (u"ࠬ࠭ૼ")
        bstack111111l1l_opy_ = bstack111l11_opy_ (u"࠭ࠧ૽")
        bstack1lll111111_opy_ = bstack111l11_opy_ (u"ࠧࠨ૾")
        try:
          import traceback
          bstack1lll1lll1_opy_ = self.exception.__class__.__name__
          bstack1111l1ll1_opy_ = traceback.format_tb(self.exc_traceback)
          bstack111111l1l_opy_ = bstack111l11_opy_ (u"ࠨࠢࠪ૿").join(bstack1111l1ll1_opy_)
          bstack1lll111111_opy_ = bstack1111l1ll1_opy_[-1]
        except Exception as e:
          logger.debug(bstack11l111lll_opy_.format(str(e)))
        bstack1lll1lll1_opy_ += bstack1lll111111_opy_
        bstack1lll1l1111_opy_(context, json.dumps(str(args[0].name) + bstack111l11_opy_ (u"ࠤࠣ࠱ࠥࡌࡡࡪ࡮ࡨࡨࠦࡢ࡮ࠣ଀") + str(bstack111111l1l_opy_)),
                            bstack111l11_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠤଁ"))
        if self.driver_before_scenario:
          bstack111111l1_opy_(getattr(context, bstack111l11_opy_ (u"ࠫࡵࡧࡧࡦࠩଂ"), None), bstack111l11_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧଃ"), bstack1lll1lll1_opy_)
          bstack1l1l111ll_opy_.execute_script(bstack111l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡩࡧࡴࡢࠤ࠽ࠫ଄") + json.dumps(str(args[0].name) + bstack111l11_opy_ (u"ࠢࠡ࠯ࠣࡊࡦ࡯࡬ࡦࡦࠤࡠࡳࠨଅ") + str(bstack111111l1l_opy_)) + bstack111l11_opy_ (u"ࠨ࠮ࠣࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠥࠨࡥࡳࡴࡲࡶࠧࢃࡽࠨଆ"))
        if self.driver_before_scenario:
          bstack1l1l11llll_opy_(bstack1l1l111ll_opy_, bstack111l11_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩଇ"), bstack111l11_opy_ (u"ࠥࡗࡨ࡫࡮ࡢࡴ࡬ࡳࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡽࡩࡵࡪ࠽ࠤࡡࡴࠢଈ") + str(bstack1lll1lll1_opy_))
      else:
        bstack1lll1l1111_opy_(context, bstack111l11_opy_ (u"ࠦࡕࡧࡳࡴࡧࡧࠥࠧଉ"), bstack111l11_opy_ (u"ࠧ࡯࡮ࡧࡱࠥଊ"))
        if self.driver_before_scenario:
          bstack111111l1_opy_(getattr(context, bstack111l11_opy_ (u"࠭ࡰࡢࡩࡨࠫଋ"), None), bstack111l11_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢଌ"))
        bstack1l1l111ll_opy_.execute_script(bstack111l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡤࡢࡶࡤࠦ࠿࠭଍") + json.dumps(str(args[0].name) + bstack111l11_opy_ (u"ࠤࠣ࠱ࠥࡖࡡࡴࡵࡨࡨࠦࠨ଎")) + bstack111l11_opy_ (u"ࠪ࠰ࠥࠨ࡬ࡦࡸࡨࡰࠧࡀࠠࠣ࡫ࡱࡪࡴࠨࡽࡾࠩଏ"))
        if self.driver_before_scenario:
          bstack1l1l11llll_opy_(bstack1l1l111ll_opy_, bstack111l11_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦଐ"))
    except Exception as e:
      logger.debug(bstack111l11_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡ࡯ࡤࡶࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡴࡶࡤࡸࡺࡹࠠࡪࡰࠣࡥ࡫ࡺࡥࡳࠢࡩࡩࡦࡺࡵࡳࡧ࠽ࠤࢀࢃࠧ଑").format(str(e)))
  elif name == bstack111l11_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤ࡬ࡥࡢࡶࡸࡶࡪ࠭଒"):
    try:
      bstack1l1l111ll_opy_ = threading.current_thread().bstackSessionDriver if bstack111ll1ll1_opy_(bstack111l11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭ଓ")) else context.browser
      if context.failed is True:
        bstack1111l1lll_opy_ = []
        bstack1l1lll1l1_opy_ = []
        bstack1lll1lllll_opy_ = []
        bstack1ll1llllll_opy_ = bstack111l11_opy_ (u"ࠨࠩଔ")
        try:
          import traceback
          for exc in self.exception_arr:
            bstack1111l1lll_opy_.append(exc.__class__.__name__)
          for exc_tb in self.exc_traceback_arr:
            bstack1111l1ll1_opy_ = traceback.format_tb(exc_tb)
            bstack1l1l111l1l_opy_ = bstack111l11_opy_ (u"ࠩࠣࠫକ").join(bstack1111l1ll1_opy_)
            bstack1l1lll1l1_opy_.append(bstack1l1l111l1l_opy_)
            bstack1lll1lllll_opy_.append(bstack1111l1ll1_opy_[-1])
        except Exception as e:
          logger.debug(bstack11l111lll_opy_.format(str(e)))
        bstack1lll1lll1_opy_ = bstack111l11_opy_ (u"ࠪࠫଖ")
        for i in range(len(bstack1111l1lll_opy_)):
          bstack1lll1lll1_opy_ += bstack1111l1lll_opy_[i] + bstack1lll1lllll_opy_[i] + bstack111l11_opy_ (u"ࠫࡡࡴࠧଗ")
        bstack1ll1llllll_opy_ = bstack111l11_opy_ (u"ࠬࠦࠧଘ").join(bstack1l1lll1l1_opy_)
        if not self.driver_before_scenario:
          bstack1lll1l1111_opy_(context, bstack1ll1llllll_opy_, bstack111l11_opy_ (u"ࠨࡥࡳࡴࡲࡶࠧଙ"))
          bstack111111l1_opy_(getattr(context, bstack111l11_opy_ (u"ࠧࡱࡣࡪࡩࠬଚ"), None), bstack111l11_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣଛ"), bstack1lll1lll1_opy_)
          bstack1l1l111ll_opy_.execute_script(bstack111l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡥࡣࡷࡥࠧࡀࠧଜ") + json.dumps(bstack1ll1llllll_opy_) + bstack111l11_opy_ (u"ࠪ࠰ࠥࠨ࡬ࡦࡸࡨࡰࠧࡀࠠࠣࡧࡵࡶࡴࡸࠢࡾࡿࠪଝ"))
          bstack1l1l11llll_opy_(bstack1l1l111ll_opy_, bstack111l11_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦଞ"), bstack111l11_opy_ (u"࡙ࠧ࡯࡮ࡧࠣࡷࡨ࡫࡮ࡢࡴ࡬ࡳࡸࠦࡦࡢ࡫࡯ࡩࡩࡀࠠ࡝ࡰࠥଟ") + str(bstack1lll1lll1_opy_))
          bstack11l1l11l_opy_ = bstack11l1l1l11_opy_(bstack1ll1llllll_opy_, self.feature.name, logger)
          if (bstack11l1l11l_opy_ != None):
            bstack1l11llll1l_opy_.append(bstack11l1l11l_opy_)
      else:
        if not self.driver_before_scenario:
          bstack1lll1l1111_opy_(context, bstack111l11_opy_ (u"ࠨࡆࡦࡣࡷࡹࡷ࡫࠺ࠡࠤଠ") + str(self.feature.name) + bstack111l11_opy_ (u"ࠢࠡࡲࡤࡷࡸ࡫ࡤࠢࠤଡ"), bstack111l11_opy_ (u"ࠣ࡫ࡱࡪࡴࠨଢ"))
          bstack111111l1_opy_(getattr(context, bstack111l11_opy_ (u"ࠩࡳࡥ࡬࡫ࠧଣ"), None), bstack111l11_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥତ"))
          bstack1l1l111ll_opy_.execute_script(bstack111l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡧࡥࡹࡧࠢ࠻ࠩଥ") + json.dumps(bstack111l11_opy_ (u"ࠧࡌࡥࡢࡶࡸࡶࡪࡀࠠࠣଦ") + str(self.feature.name) + bstack111l11_opy_ (u"ࠨࠠࡱࡣࡶࡷࡪࡪࠡࠣଧ")) + bstack111l11_opy_ (u"ࠧ࠭ࠢࠥࡰࡪࡼࡥ࡭ࠤ࠽ࠤࠧ࡯࡮ࡧࡱࠥࢁࢂ࠭ନ"))
          bstack1l1l11llll_opy_(bstack1l1l111ll_opy_, bstack111l11_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨ଩"))
          bstack11l1l11l_opy_ = bstack11l1l1l11_opy_(bstack1ll1llllll_opy_, self.feature.name, logger)
          if (bstack11l1l11l_opy_ != None):
            bstack1l11llll1l_opy_.append(bstack11l1l11l_opy_)
    except Exception as e:
      logger.debug(bstack111l11_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡳࡡࡳ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠤࡸࡺࡡࡵࡷࡶࠤ࡮ࡴࠠࡢࡨࡷࡩࡷࠦࡦࡦࡣࡷࡹࡷ࡫࠺ࠡࡽࢀࠫପ").format(str(e)))
  else:
    bstack11ll1lll_opy_(self, name, context, *args)
  if name in [bstack111l11_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡩࡩࡦࡺࡵࡳࡧࠪଫ"), bstack111l11_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬବ")]:
    bstack11ll1lll_opy_(self, name, context, *args)
    if (name == bstack111l11_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴ࠭ଭ") and self.driver_before_scenario) or (
            name == bstack111l11_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤ࡬ࡥࡢࡶࡸࡶࡪ࠭ମ") and not self.driver_before_scenario):
      try:
        bstack1l1l111ll_opy_ = threading.current_thread().bstackSessionDriver if bstack111ll1ll1_opy_(bstack111l11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭ଯ")) else context.browser
        bstack1l1l111ll_opy_.quit()
      except Exception:
        pass
def bstack11l11lll_opy_(config, startdir):
  return bstack111l11_opy_ (u"ࠣࡦࡵ࡭ࡻ࡫ࡲ࠻ࠢࡾ࠴ࢂࠨର").format(bstack111l11_opy_ (u"ࠤࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠣ଱"))
notset = Notset()
def bstack11l1llll1_opy_(self, name: str, default=notset, skip: bool = False):
  global bstack1llll1ll_opy_
  if str(name).lower() == bstack111l11_opy_ (u"ࠪࡨࡷ࡯ࡶࡦࡴࠪଲ"):
    return bstack111l11_opy_ (u"ࠦࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠥଳ")
  else:
    return bstack1llll1ll_opy_(self, name, default, skip)
def bstack1ll1l11l1l_opy_(item, when):
  global bstack111l1llll_opy_
  try:
    bstack111l1llll_opy_(item, when)
  except Exception as e:
    pass
def bstack1111lll11_opy_():
  return
def bstack1l11l1l111_opy_(type, name, status, reason, bstack1l11l1ll1l_opy_, bstack1lllll11_opy_):
  bstack11l1l1lll_opy_ = {
    bstack111l11_opy_ (u"ࠬࡧࡣࡵ࡫ࡲࡲࠬ଴"): type,
    bstack111l11_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩଵ"): {}
  }
  if type == bstack111l11_opy_ (u"ࠧࡢࡰࡱࡳࡹࡧࡴࡦࠩଶ"):
    bstack11l1l1lll_opy_[bstack111l11_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫଷ")][bstack111l11_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨସ")] = bstack1l11l1ll1l_opy_
    bstack11l1l1lll_opy_[bstack111l11_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ହ")][bstack111l11_opy_ (u"ࠫࡩࡧࡴࡢࠩ଺")] = json.dumps(str(bstack1lllll11_opy_))
  if type == bstack111l11_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭଻"):
    bstack11l1l1lll_opy_[bstack111l11_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴ଼ࠩ")][bstack111l11_opy_ (u"ࠧ࡯ࡣࡰࡩࠬଽ")] = name
  if type == bstack111l11_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫା"):
    bstack11l1l1lll_opy_[bstack111l11_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬି")][bstack111l11_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪୀ")] = status
    if status == bstack111l11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫୁ"):
      bstack11l1l1lll_opy_[bstack111l11_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨୂ")][bstack111l11_opy_ (u"࠭ࡲࡦࡣࡶࡳࡳ࠭ୃ")] = json.dumps(str(reason))
  bstack111l1lll_opy_ = bstack111l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࢁࠬୄ").format(json.dumps(bstack11l1l1lll_opy_))
  return bstack111l1lll_opy_
def bstack1l1llllll1_opy_(driver_command, response):
    if driver_command == bstack111l11_opy_ (u"ࠨࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠬ୅"):
        bstack1lll1ll1l_opy_.bstack1ll11l1ll_opy_({
            bstack111l11_opy_ (u"ࠩ࡬ࡱࡦ࡭ࡥࠨ୆"): response[bstack111l11_opy_ (u"ࠪࡺࡦࡲࡵࡦࠩେ")],
            bstack111l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫୈ"): bstack1lll1ll1l_opy_.current_test_uuid()
        })
def bstack1ll11l111l_opy_(item, call, rep):
  global bstack1lll1ll1ll_opy_
  global bstack1l1l1ll1l1_opy_
  global bstack1ll11lll_opy_
  name = bstack111l11_opy_ (u"ࠬ࠭୉")
  try:
    if rep.when == bstack111l11_opy_ (u"࠭ࡣࡢ࡮࡯ࠫ୊"):
      bstack1ll111l1_opy_ = threading.current_thread().bstackSessionId
      try:
        if not bstack1ll11lll_opy_:
          name = str(rep.nodeid)
          bstack1l11l11ll_opy_ = bstack1l11l1l111_opy_(bstack111l11_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨୋ"), name, bstack111l11_opy_ (u"ࠨࠩୌ"), bstack111l11_opy_ (u"୍ࠩࠪ"), bstack111l11_opy_ (u"ࠪࠫ୎"), bstack111l11_opy_ (u"ࠫࠬ୏"))
          threading.current_thread().bstack1ll11l11l_opy_ = name
          for driver in bstack1l1l1ll1l1_opy_:
            if bstack1ll111l1_opy_ == driver.session_id:
              driver.execute_script(bstack1l11l11ll_opy_)
      except Exception as e:
        logger.debug(bstack111l11_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠦࡦࡰࡴࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡴࡧࡶࡷ࡮ࡵ࡮࠻ࠢࡾࢁࠬ୐").format(str(e)))
      try:
        bstack1l1l11ll11_opy_(rep.outcome.lower())
        if rep.outcome.lower() != bstack111l11_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧ୑"):
          status = bstack111l11_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ୒") if rep.outcome.lower() == bstack111l11_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ୓") else bstack111l11_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ୔")
          reason = bstack111l11_opy_ (u"ࠪࠫ୕")
          if status == bstack111l11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫୖ"):
            reason = rep.longrepr.reprcrash.message
            if (not threading.current_thread().bstackTestErrorMessages):
              threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(reason)
          level = bstack111l11_opy_ (u"ࠬ࡯࡮ࡧࡱࠪୗ") if status == bstack111l11_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭୘") else bstack111l11_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭୙")
          data = name + bstack111l11_opy_ (u"ࠨࠢࡳࡥࡸࡹࡥࡥࠣࠪ୚") if status == bstack111l11_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ୛") else name + bstack111l11_opy_ (u"ࠪࠤ࡫ࡧࡩ࡭ࡧࡧࠥࠥ࠭ଡ଼") + reason
          bstack1l1l1ll1ll_opy_ = bstack1l11l1l111_opy_(bstack111l11_opy_ (u"ࠫࡦࡴ࡮ࡰࡶࡤࡸࡪ࠭ଢ଼"), bstack111l11_opy_ (u"ࠬ࠭୞"), bstack111l11_opy_ (u"࠭ࠧୟ"), bstack111l11_opy_ (u"ࠧࠨୠ"), level, data)
          for driver in bstack1l1l1ll1l1_opy_:
            if bstack1ll111l1_opy_ == driver.session_id:
              driver.execute_script(bstack1l1l1ll1ll_opy_)
      except Exception as e:
        logger.debug(bstack111l11_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡷࡪࡺࡴࡪࡰࡪࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡩ࡯࡯ࡶࡨࡼࡹࠦࡦࡰࡴࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡴࡧࡶࡷ࡮ࡵ࡮࠻ࠢࡾࢁࠬୡ").format(str(e)))
  except Exception as e:
    logger.debug(bstack111l11_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤ࡬࡫ࡴࡵ࡫ࡱ࡫ࠥࡹࡴࡢࡶࡨࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡹ࡫ࡳࡵࠢࡶࡸࡦࡺࡵࡴ࠼ࠣࡿࢂ࠭ୢ").format(str(e)))
  bstack1lll1ll1ll_opy_(item, call, rep)
def bstack1lll11lll1_opy_(driver, bstack11l1l1l1l_opy_):
  PercySDK.screenshot(driver, bstack11l1l1l1l_opy_)
def bstack1l1111111_opy_(driver):
  if bstack1lll1l1l1_opy_.bstack1l1l1111_opy_() is True or bstack1lll1l1l1_opy_.capturing() is True:
    return
  bstack1lll1l1l1_opy_.bstack1lllll111l_opy_()
  while not bstack1lll1l1l1_opy_.bstack1l1l1111_opy_():
    bstack1l11ll1111_opy_ = bstack1lll1l1l1_opy_.bstack1l1l11ll_opy_()
    bstack1lll11lll1_opy_(driver, bstack1l11ll1111_opy_)
  bstack1lll1l1l1_opy_.bstack1l111111l_opy_()
def bstack111ll1l1l_opy_(sequence, driver_command, response = None, bstack1lll11l1_opy_ = None, args = None):
    try:
      if sequence != bstack111l11_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࠪୣ"):
        return
      if not CONFIG.get(bstack111l11_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪ୤"), False):
        return
      bstack1l11ll1111_opy_ = bstack1ll111l1ll_opy_(threading.current_thread(), bstack111l11_opy_ (u"ࠬࡶࡥࡳࡥࡼࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ୥"), None)
      for command in bstack111ll11l1_opy_:
        if command == driver_command:
          for driver in bstack1l1l1ll1l1_opy_:
            bstack1l1111111_opy_(driver)
      bstack11ll1l1l1_opy_ = CONFIG.get(bstack111l11_opy_ (u"࠭ࡰࡦࡴࡦࡽࡈࡧࡰࡵࡷࡵࡩࡒࡵࡤࡦࠩ୦"), bstack111l11_opy_ (u"ࠢࡢࡷࡷࡳࠧ୧"))
      if driver_command in bstack1lll1111_opy_[bstack11ll1l1l1_opy_]:
        bstack1lll1l1l1_opy_.bstack1ll1lllll1_opy_(bstack1l11ll1111_opy_, driver_command)
    except Exception as e:
      pass
def bstack11l11l111_opy_(framework_name):
  global bstack1lll1ll11_opy_
  global bstack1ll1l1ll11_opy_
  global bstack1l1lll11_opy_
  bstack1lll1ll11_opy_ = framework_name
  logger.info(bstack1ll1l111l_opy_.format(bstack1lll1ll11_opy_.split(bstack111l11_opy_ (u"ࠨ࠯ࠪ୨"))[0]))
  try:
    from selenium import webdriver
    from selenium.webdriver.common.service import Service
    from selenium.webdriver.remote.webdriver import WebDriver
    if bstack1ll1l11l1_opy_:
      Service.start = bstack1l11lll1ll_opy_
      Service.stop = bstack1llll1lll_opy_
      webdriver.Remote.get = bstack11111ll1l_opy_
      WebDriver.close = bstack1l11lll1_opy_
      WebDriver.quit = bstack1ll11111ll_opy_
      webdriver.Remote.__init__ = bstack11ll1llll_opy_
      WebDriver.getAccessibilityResults = getAccessibilityResults
      WebDriver.get_accessibility_results = getAccessibilityResults
      WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
      WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
      WebDriver.performScan = perform_scan
      WebDriver.perform_scan = perform_scan
    if not bstack1ll1l11l1_opy_ and bstack1lll1ll1l_opy_.on():
      webdriver.Remote.__init__ = bstack1l1ll1ll11_opy_
    WebDriver.execute = bstack1lll1l11l_opy_
    bstack1ll1l1ll11_opy_ = True
  except Exception as e:
    pass
  try:
    if bstack1ll1l11l1_opy_:
      from QWeb.keywords import browser
      browser.close_browser = bstack1lll1ll1l1_opy_
  except Exception as e:
    pass
  bstack1ll1lllll_opy_()
  if not bstack1ll1l1ll11_opy_:
    bstack1lll11lll_opy_(bstack111l11_opy_ (u"ࠤࡓࡥࡨࡱࡡࡨࡧࡶࠤࡳࡵࡴࠡ࡫ࡱࡷࡹࡧ࡬࡭ࡧࡧࠦ୩"), bstack11llll111_opy_)
  if bstack11l1ll1l1_opy_():
    try:
      from selenium.webdriver.remote.remote_connection import RemoteConnection
      RemoteConnection._get_proxy_url = bstack1l1ll11111_opy_
    except Exception as e:
      logger.error(bstack1l1l1lllll_opy_.format(str(e)))
  if bstack1l1l1lll1_opy_():
    bstack1ll11111l1_opy_(CONFIG, logger)
  if (bstack111l11_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩ୪") in str(framework_name).lower()):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        if CONFIG.get(bstack111l11_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪ୫"), False):
          bstack1ll1lll11l_opy_(bstack111ll1l1l_opy_)
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        WebDriverCreator._get_ff_profile = bstack1l1111l1_opy_
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCache.close = bstack1l1ll1ll1l_opy_
      except Exception as e:
        logger.warn(bstack1ll11ll1l_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import bstack11ll11lll_opy_
        bstack11ll11lll_opy_.close = bstack1111l1l1_opy_
      except Exception as e:
        logger.debug(bstack11111l1l1_opy_ + str(e))
    except Exception as e:
      bstack1lll11lll_opy_(e, bstack1ll11ll1l_opy_)
    Output.start_test = bstack1lll11ll11_opy_
    Output.end_test = bstack11l1lll1l_opy_
    TestStatus.__init__ = bstack1111lllll_opy_
    QueueItem.__init__ = bstack1lll11l111_opy_
    pabot._create_items = bstack1111ll1l_opy_
    try:
      from pabot import __version__ as bstack11ll1l111_opy_
      if version.parse(bstack11ll1l111_opy_) >= version.parse(bstack111l11_opy_ (u"ࠬ࠸࠮࠲࠷࠱࠴ࠬ୬")):
        pabot._run = bstack1l1l1lll1l_opy_
      elif version.parse(bstack11ll1l111_opy_) >= version.parse(bstack111l11_opy_ (u"࠭࠲࠯࠳࠶࠲࠵࠭୭")):
        pabot._run = bstack1l1ll1111_opy_
      else:
        pabot._run = bstack1l1111ll_opy_
    except Exception as e:
      pabot._run = bstack1l1111ll_opy_
    pabot._create_command_for_execution = bstack11lllll11_opy_
    pabot._report_results = bstack1l1l111ll1_opy_
  if bstack111l11_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧ୮") in str(framework_name).lower():
    if not bstack1ll1l11l1_opy_:
      return
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1lll11lll_opy_(e, bstack1ll1ll111l_opy_)
    Runner.run_hook = bstack11ll1ll11_opy_
    Step.run = bstack1llllll1l1_opy_
  if bstack111l11_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ୯") in str(framework_name).lower():
    if not bstack1ll1l11l1_opy_:
      return
    try:
      if CONFIG.get(bstack111l11_opy_ (u"ࠩࡳࡩࡷࡩࡹࠨ୰"), False):
          bstack1ll1lll11l_opy_(bstack111ll1l1l_opy_)
      from pytest_selenium import pytest_selenium
      from _pytest.config import Config
      pytest_selenium.pytest_report_header = bstack11l11lll_opy_
      from pytest_selenium.drivers import browserstack
      browserstack.pytest_selenium_runtest_makereport = bstack1111lll11_opy_
      Config.getoption = bstack11l1llll1_opy_
    except Exception as e:
      pass
    try:
      from pytest_bdd import reporting
      reporting.runtest_makereport = bstack1ll11l111l_opy_
    except Exception as e:
      pass
def bstack1l1l11l1l_opy_():
  global CONFIG
  if bstack111l11_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪୱ") in CONFIG and int(CONFIG[bstack111l11_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫ୲")]) > 1:
    logger.warn(bstack11l1ll11l_opy_)
def bstack1l1llll1ll_opy_(arg, bstack11l11ll1_opy_, bstack1ll11llll_opy_=None):
  global CONFIG
  global bstack1l1l11l11_opy_
  global bstack1lll11l11_opy_
  global bstack1ll1l11l1_opy_
  global bstack1l11l111ll_opy_
  bstack1l11l11l11_opy_ = bstack111l11_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ୳")
  if bstack11l11ll1_opy_ and isinstance(bstack11l11ll1_opy_, str):
    bstack11l11ll1_opy_ = eval(bstack11l11ll1_opy_)
  CONFIG = bstack11l11ll1_opy_[bstack111l11_opy_ (u"࠭ࡃࡐࡐࡉࡍࡌ࠭୴")]
  bstack1l1l11l11_opy_ = bstack11l11ll1_opy_[bstack111l11_opy_ (u"ࠧࡉࡗࡅࡣ࡚ࡘࡌࠨ୵")]
  bstack1lll11l11_opy_ = bstack11l11ll1_opy_[bstack111l11_opy_ (u"ࠨࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪ୶")]
  bstack1ll1l11l1_opy_ = bstack11l11ll1_opy_[bstack111l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡘࡘࡔࡓࡁࡕࡋࡒࡒࠬ୷")]
  bstack1l11l111ll_opy_.bstack1ll1l11ll_opy_(bstack111l11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡷࡪࡹࡳࡪࡱࡱࠫ୸"), bstack1ll1l11l1_opy_)
  os.environ[bstack111l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐ࠭୹")] = bstack1l11l11l11_opy_
  os.environ[bstack111l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡕࡎࡇࡋࡊࠫ୺")] = json.dumps(CONFIG)
  os.environ[bstack111l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡎࡕࡃࡡࡘࡖࡑ࠭୻")] = bstack1l1l11l11_opy_
  os.environ[bstack111l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨ୼")] = str(bstack1lll11l11_opy_)
  os.environ[bstack111l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑ࡛ࡗࡉࡘ࡚࡟ࡑࡎࡘࡋࡎࡔࠧ୽")] = str(True)
  if bstack1l111l11l_opy_(arg, [bstack111l11_opy_ (u"ࠩ࠰ࡲࠬ୾"), bstack111l11_opy_ (u"ࠪ࠱࠲ࡴࡵ࡮ࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠫ୿")]) != -1:
    os.environ[bstack111l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔ࡞࡚ࡅࡔࡖࡢࡔࡆࡘࡁࡍࡎࡈࡐࠬ஀")] = str(True)
  if len(sys.argv) <= 1:
    logger.critical(bstack1ll1l1l11l_opy_)
    return
  bstack1llll11l1_opy_()
  global bstack1l1l1llll1_opy_
  global bstack1111111l1_opy_
  global bstack1l11ll1l_opy_
  global bstack111ll1l11_opy_
  global bstack1l1llll1_opy_
  global bstack1l1lll11_opy_
  global bstack111lll1ll_opy_
  arg.append(bstack111l11_opy_ (u"ࠧ࠳ࡗࠣ஁"))
  arg.append(bstack111l11_opy_ (u"ࠨࡩࡨࡰࡲࡶࡪࡀࡍࡰࡦࡸࡰࡪࠦࡡ࡭ࡴࡨࡥࡩࡿࠠࡪ࡯ࡳࡳࡷࡺࡥࡥ࠼ࡳࡽࡹ࡫ࡳࡵ࠰ࡓࡽࡹ࡫ࡳࡵ࡙ࡤࡶࡳ࡯࡮ࡨࠤஂ"))
  arg.append(bstack111l11_opy_ (u"ࠢ࠮࡙ࠥஃ"))
  arg.append(bstack111l11_opy_ (u"ࠣ࡫ࡪࡲࡴࡸࡥ࠻ࡖ࡫ࡩࠥ࡮࡯ࡰ࡭࡬ࡱࡵࡲࠢ஄"))
  global bstack1ll111l11l_opy_
  global bstack11l1lll1_opy_
  global bstack1l111111_opy_
  global bstack1l11ll11_opy_
  global bstack1l1ll1l1_opy_
  global bstack1ll1l1ll1l_opy_
  global bstack1lll1llll_opy_
  global bstack111l1l1l1_opy_
  global bstack1l1ll1l11l_opy_
  global bstack111l1l11_opy_
  global bstack1llll1ll_opy_
  global bstack111l1llll_opy_
  global bstack1lll1ll1ll_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack1ll111l11l_opy_ = webdriver.Remote.__init__
    bstack11l1lll1_opy_ = WebDriver.quit
    bstack111l1l1l1_opy_ = WebDriver.close
    bstack1l1ll1l11l_opy_ = WebDriver.get
    bstack1l111111_opy_ = WebDriver.execute
  except Exception as e:
    pass
  if bstack111ll1111_opy_(CONFIG) and bstack1ll1l11l11_opy_():
    if bstack1lll1l1ll_opy_() < version.parse(bstack1l111lll_opy_):
      logger.error(bstack1ll11111l_opy_.format(bstack1lll1l1ll_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        bstack111l1l11_opy_ = RemoteConnection._get_proxy_url
      except Exception as e:
        logger.error(bstack1l1l1lllll_opy_.format(str(e)))
  try:
    from _pytest.config import Config
    bstack1llll1ll_opy_ = Config.getoption
    from _pytest import runner
    bstack111l1llll_opy_ = runner._update_current_test_var
  except Exception as e:
    logger.warn(e, bstack1l11l1l1_opy_)
  try:
    from pytest_bdd import reporting
    bstack1lll1ll1ll_opy_ = reporting.runtest_makereport
  except Exception as e:
    logger.debug(bstack111l11_opy_ (u"ࠩࡓࡰࡪࡧࡳࡦࠢ࡬ࡲࡸࡺࡡ࡭࡮ࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡵࡱࠣࡶࡺࡴࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡹ࡫ࡳࡵࡵࠪஅ"))
  bstack1l11ll1l_opy_ = CONFIG.get(bstack111l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧஆ"), {}).get(bstack111l11_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭இ"))
  bstack111lll1ll_opy_ = True
  bstack11l11l111_opy_(bstack1llll1ll1_opy_)
  os.environ[bstack111l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡚࡙ࡅࡓࡐࡄࡑࡊ࠭ஈ")] = CONFIG[bstack111l11_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨஉ")]
  os.environ[bstack111l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡄࡅࡈࡗࡘࡥࡋࡆ࡛ࠪஊ")] = CONFIG[bstack111l11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫ஋")]
  os.environ[bstack111l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡘࡘࡔࡓࡁࡕࡋࡒࡒࠬ஌")] = bstack1ll1l11l1_opy_.__str__()
  from _pytest.config import main as bstack1l1lllll1l_opy_
  bstack1111111l_opy_ = []
  try:
    bstack1ll1l1l111_opy_ = bstack1l1lllll1l_opy_(arg)
    if bstack111l11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡩࡷࡸ࡯ࡳࡡ࡯࡭ࡸࡺࠧ஍") in multiprocessing.current_process().__dict__.keys():
      for bstack1lll1111l1_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack1111111l_opy_.append(bstack1lll1111l1_opy_)
    try:
      bstack1111l11l1_opy_ = (bstack1111111l_opy_, int(bstack1ll1l1l111_opy_))
      bstack1ll11llll_opy_.append(bstack1111l11l1_opy_)
    except:
      bstack1ll11llll_opy_.append((bstack1111111l_opy_, bstack1ll1l1l111_opy_))
  except Exception as e:
    logger.error(traceback.format_exc())
    bstack1111111l_opy_.append({bstack111l11_opy_ (u"ࠫࡳࡧ࡭ࡦࠩஎ"): bstack111l11_opy_ (u"ࠬࡖࡲࡰࡥࡨࡷࡸࠦࠧஏ") + os.environ.get(bstack111l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ஐ")), bstack111l11_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭஑"): traceback.format_exc(), bstack111l11_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧஒ"): int(os.environ.get(bstack111l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩஓ")))})
    bstack1ll11llll_opy_.append((bstack1111111l_opy_, 1))
def bstack11lllll1_opy_(arg):
  global bstack11111llll_opy_
  bstack11l11l111_opy_(bstack11l11l1ll_opy_)
  os.environ[bstack111l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡌࡗࡤࡇࡐࡑࡡࡄ࡙࡙ࡕࡍࡂࡖࡈࠫஔ")] = str(bstack1lll11l11_opy_)
  from behave.__main__ import main as bstack1ll1111111_opy_
  status_code = bstack1ll1111111_opy_(arg)
  if status_code != 0:
    bstack11111llll_opy_ = status_code
def bstack1llll11l11_opy_():
  logger.info(bstack1l1111lll_opy_)
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument(bstack111l11_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪக"), help=bstack111l11_opy_ (u"ࠬࡍࡥ࡯ࡧࡵࡥࡹ࡫ࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡣࡰࡰࡩ࡭࡬࠭஖"))
  parser.add_argument(bstack111l11_opy_ (u"࠭࠭ࡶࠩ஗"), bstack111l11_opy_ (u"ࠧ࠮࠯ࡸࡷࡪࡸ࡮ࡢ࡯ࡨࠫ஘"), help=bstack111l11_opy_ (u"ࠨ࡛ࡲࡹࡷࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡻࡳࡦࡴࡱࡥࡲ࡫ࠧங"))
  parser.add_argument(bstack111l11_opy_ (u"ࠩ࠰࡯ࠬச"), bstack111l11_opy_ (u"ࠪ࠱࠲ࡱࡥࡺࠩ஛"), help=bstack111l11_opy_ (u"ࠫ࡞ࡵࡵࡳࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡣࡦࡧࡪࡹࡳࠡ࡭ࡨࡽࠬஜ"))
  parser.add_argument(bstack111l11_opy_ (u"ࠬ࠳ࡦࠨ஝"), bstack111l11_opy_ (u"࠭࠭࠮ࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫஞ"), help=bstack111l11_opy_ (u"࡚ࠧࡱࡸࡶࠥࡺࡥࡴࡶࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ட"))
  bstack1ll1ll1ll1_opy_ = parser.parse_args()
  try:
    bstack1lllllll1l_opy_ = bstack111l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡨࡧࡱࡩࡷ࡯ࡣ࠯ࡻࡰࡰ࠳ࡹࡡ࡮ࡲ࡯ࡩࠬ஠")
    if bstack1ll1ll1ll1_opy_.framework and bstack1ll1ll1ll1_opy_.framework not in (bstack111l11_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩ஡"), bstack111l11_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰ࠶ࠫ஢")):
      bstack1lllllll1l_opy_ = bstack111l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠴ࡹ࡮࡮࠱ࡷࡦࡳࡰ࡭ࡧࠪண")
    bstack1llll1ll1l_opy_ = os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1lllllll1l_opy_)
    bstack1ll1l1l1l_opy_ = open(bstack1llll1ll1l_opy_, bstack111l11_opy_ (u"ࠬࡸࠧத"))
    bstack1l1l11lll1_opy_ = bstack1ll1l1l1l_opy_.read()
    bstack1ll1l1l1l_opy_.close()
    if bstack1ll1ll1ll1_opy_.username:
      bstack1l1l11lll1_opy_ = bstack1l1l11lll1_opy_.replace(bstack111l11_opy_ (u"࡙࠭ࡐࡗࡕࡣ࡚࡙ࡅࡓࡐࡄࡑࡊ࠭஥"), bstack1ll1ll1ll1_opy_.username)
    if bstack1ll1ll1ll1_opy_.key:
      bstack1l1l11lll1_opy_ = bstack1l1l11lll1_opy_.replace(bstack111l11_opy_ (u"࡚ࠧࡑࡘࡖࡤࡇࡃࡄࡇࡖࡗࡤࡑࡅ࡚ࠩ஦"), bstack1ll1ll1ll1_opy_.key)
    if bstack1ll1ll1ll1_opy_.framework:
      bstack1l1l11lll1_opy_ = bstack1l1l11lll1_opy_.replace(bstack111l11_opy_ (u"ࠨ࡛ࡒ࡙ࡗࡥࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࠩ஧"), bstack1ll1ll1ll1_opy_.framework)
    file_name = bstack111l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡻࡰࡰࠬந")
    file_path = os.path.abspath(file_name)
    bstack111l111ll_opy_ = open(file_path, bstack111l11_opy_ (u"ࠪࡻࠬன"))
    bstack111l111ll_opy_.write(bstack1l1l11lll1_opy_)
    bstack111l111ll_opy_.close()
    logger.info(bstack1lllll1ll1_opy_)
    try:
      os.environ[bstack111l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐ࠭ப")] = bstack1ll1ll1ll1_opy_.framework if bstack1ll1ll1ll1_opy_.framework != None else bstack111l11_opy_ (u"ࠧࠨ஫")
      config = yaml.safe_load(bstack1l1l11lll1_opy_)
      config[bstack111l11_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭஬")] = bstack111l11_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴ࠭ࡴࡧࡷࡹࡵ࠭஭")
      bstack111lll1l1_opy_(bstack1lll1ll1_opy_, config)
    except Exception as e:
      logger.debug(bstack11ll11ll1_opy_.format(str(e)))
  except Exception as e:
    logger.error(bstack11111ll1_opy_.format(str(e)))
def bstack111lll1l1_opy_(bstack1llllll111_opy_, config, bstack1ll11l1ll1_opy_={}):
  global bstack1ll1l11l1_opy_
  global bstack11llllll_opy_
  global bstack1l11l111ll_opy_
  if not config:
    return
  bstack1111ll11l_opy_ = bstack1ll11l11l1_opy_ if not bstack1ll1l11l1_opy_ else (
    bstack1l111l11_opy_ if bstack111l11_opy_ (u"ࠨࡣࡳࡴࠬம") in config else bstack1llll1l11l_opy_)
  bstack1ll111lll_opy_ = False
  bstack111l11l11_opy_ = False
  if bstack1ll1l11l1_opy_ is True:
      if bstack111l11_opy_ (u"ࠩࡤࡴࡵ࠭ய") in config:
          bstack1ll111lll_opy_ = True
      else:
          bstack111l11l11_opy_ = True
  bstack1l11111l_opy_ = {
      bstack111l11_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪர"): bstack1lll1ll1l_opy_.bstack1llllll1l_opy_(bstack11llllll_opy_),
      bstack111l11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫற"): bstack1llll11l_opy_.bstack1l1l1l11l_opy_(config),
      bstack111l11_opy_ (u"ࠬࡶࡥࡳࡥࡼࠫல"): config.get(bstack111l11_opy_ (u"࠭ࡰࡦࡴࡦࡽࠬள"), False),
      bstack111l11_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡦࠩழ"): bstack111l11l11_opy_,
      bstack111l11_opy_ (u"ࠨࡣࡳࡴࡤࡧࡵࡵࡱࡰࡥࡹ࡫ࠧவ"): bstack1ll111lll_opy_
  }
  data = {
    bstack111l11_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫஶ"): config[bstack111l11_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬஷ")],
    bstack111l11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧஸ"): config[bstack111l11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨஹ")],
    bstack111l11_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪ஺"): bstack1llllll111_opy_,
    bstack111l11_opy_ (u"ࠧࡥࡧࡷࡩࡨࡺࡥࡥࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫ஻"): os.environ.get(bstack111l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࠪ஼"), bstack11llllll_opy_),
    bstack111l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫ஽"): bstack1ll11l111_opy_,
    bstack111l11_opy_ (u"ࠪࡳࡵࡺࡩ࡮ࡣ࡯ࡣ࡭ࡻࡢࡠࡷࡵࡰࠬா"): bstack11l1l1ll_opy_(),
    bstack111l11_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡴࡷࡵࡰࡦࡴࡷ࡭ࡪࡹࠧி"): {
      bstack111l11_opy_ (u"ࠬࡲࡡ࡯ࡩࡸࡥ࡬࡫࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪீ"): str(config[bstack111l11_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭ு")]) if bstack111l11_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧூ") in config else bstack111l11_opy_ (u"ࠣࡷࡱ࡯ࡳࡵࡷ࡯ࠤ௃"),
      bstack111l11_opy_ (u"ࠩ࡯ࡥࡳ࡭ࡵࡢࡩࡨ࡚ࡪࡸࡳࡪࡱࡱࠫ௄"): sys.version,
      bstack111l11_opy_ (u"ࠪࡶࡪ࡬ࡥࡳࡴࡨࡶࠬ௅"): bstack111lll11_opy_(os.getenv(bstack111l11_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐࠨெ"), bstack111l11_opy_ (u"ࠧࠨே"))),
      bstack111l11_opy_ (u"࠭࡬ࡢࡰࡪࡹࡦ࡭ࡥࠨை"): bstack111l11_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧ௉"),
      bstack111l11_opy_ (u"ࠨࡲࡵࡳࡩࡻࡣࡵࠩொ"): bstack1111ll11l_opy_,
      bstack111l11_opy_ (u"ࠩࡳࡶࡴࡪࡵࡤࡶࡢࡱࡦࡶࠧோ"): bstack1l11111l_opy_,
      bstack111l11_opy_ (u"ࠪࡸࡪࡹࡴࡩࡷࡥࡣࡺࡻࡩࡥࠩௌ"): os.environ[bstack111l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅ்ࠩ")],
      bstack111l11_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡗࡧࡵࡷ࡮ࡵ࡮ࠨ௎"): bstack1lllll1l1_opy_(os.environ.get(bstack111l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࠨ௏"), bstack11llllll_opy_)),
      bstack111l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪௐ"): config[bstack111l11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ௑")] if config[bstack111l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬ௒")] else bstack111l11_opy_ (u"ࠥࡹࡳࡱ࡮ࡰࡹࡱࠦ௓"),
      bstack111l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭௔"): str(config[bstack111l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ௕")]) if bstack111l11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ௖") in config else bstack111l11_opy_ (u"ࠢࡶࡰ࡮ࡲࡴࡽ࡮ࠣௗ"),
      bstack111l11_opy_ (u"ࠨࡱࡶࠫ௘"): sys.platform,
      bstack111l11_opy_ (u"ࠩ࡫ࡳࡸࡺ࡮ࡢ࡯ࡨࠫ௙"): socket.gethostname(),
      bstack111l11_opy_ (u"ࠪࡷࡩࡱࡒࡶࡰࡌࡨࠬ௚"): bstack1l11l111ll_opy_.get_property(bstack111l11_opy_ (u"ࠫࡸࡪ࡫ࡓࡷࡱࡍࡩ࠭௛"))
    }
  }
  if not bstack1l11l111ll_opy_.get_property(bstack111l11_opy_ (u"ࠬࡹࡤ࡬ࡍ࡬ࡰࡱ࡙ࡩࡨࡰࡤࡰࠬ௜")) is None:
    data[bstack111l11_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡶࡲࡰࡲࡨࡶࡹ࡯ࡥࡴࠩ௝")][bstack111l11_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡏࡨࡸࡦࡪࡡࡵࡣࠪ௞")] = {
      bstack111l11_opy_ (u"ࠨࡴࡨࡥࡸࡵ࡮ࠨ௟"): bstack111l11_opy_ (u"ࠩࡸࡷࡪࡸ࡟࡬࡫࡯ࡰࡪࡪࠧ௠"),
      bstack111l11_opy_ (u"ࠪࡷ࡮࡭࡮ࡢ࡮ࠪ௡"): bstack1l11l111ll_opy_.get_property(bstack111l11_opy_ (u"ࠫࡸࡪ࡫ࡌ࡫࡯ࡰࡘ࡯ࡧ࡯ࡣ࡯ࠫ௢")),
      bstack111l11_opy_ (u"ࠬࡹࡩࡨࡰࡤࡰࡓࡻ࡭ࡣࡧࡵࠫ௣"): bstack1l11l111ll_opy_.get_property(bstack111l11_opy_ (u"࠭ࡳࡥ࡭ࡎ࡭ࡱࡲࡎࡰࠩ௤"))
    }
  update(data[bstack111l11_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡰࡳࡱࡳࡩࡷࡺࡩࡦࡵࠪ௥")], bstack1ll11l1ll1_opy_)
  try:
    response = bstack1lllll1lll_opy_(bstack111l11_opy_ (u"ࠨࡒࡒࡗ࡙࠭௦"), bstack1lllll11l_opy_(bstack1l1lllllll_opy_), data, {
      bstack111l11_opy_ (u"ࠩࡤࡹࡹ࡮ࠧ௧"): (config[bstack111l11_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬ௨")], config[bstack111l11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧ௩")])
    })
    if response:
      logger.debug(bstack1lll1lll_opy_.format(bstack1llllll111_opy_, str(response.json())))
  except Exception as e:
    logger.debug(bstack1ll111111l_opy_.format(str(e)))
def bstack111lll11_opy_(framework):
  return bstack111l11_opy_ (u"ࠧࢁࡽ࠮ࡲࡼࡸ࡭ࡵ࡮ࡢࡩࡨࡲࡹ࠵ࡻࡾࠤ௪").format(str(framework), __version__) if framework else bstack111l11_opy_ (u"ࠨࡰࡺࡶ࡫ࡳࡳࡧࡧࡦࡰࡷ࠳ࢀࢃࠢ௫").format(
    __version__)
def bstack1llll11l1_opy_():
  global CONFIG
  global bstack111llll11_opy_
  if bool(CONFIG):
    return
  try:
    bstack1ll1llll_opy_()
    logger.debug(bstack1ll11l1l1l_opy_.format(str(CONFIG)))
    bstack111llll11_opy_ = bstack1l1l1l1l1_opy_.bstack11ll1ll1l_opy_(CONFIG, bstack111llll11_opy_)
    bstack111111ll1_opy_()
  except Exception as e:
    logger.error(bstack111l11_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡺࡵࡱ࠮ࠣࡩࡷࡸ࡯ࡳ࠼ࠣࠦ௬") + str(e))
    sys.exit(1)
  sys.excepthook = bstack1ll11ll11l_opy_
  atexit.register(bstack1ll11l1111_opy_)
  signal.signal(signal.SIGINT, bstack1l11l1l1l_opy_)
  signal.signal(signal.SIGTERM, bstack1l11l1l1l_opy_)
def bstack1ll11ll11l_opy_(exctype, value, traceback):
  global bstack1l1l1ll1l1_opy_
  try:
    for driver in bstack1l1l1ll1l1_opy_:
      bstack1l1l11llll_opy_(driver, bstack111l11_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ௭"), bstack111l11_opy_ (u"ࠤࡖࡩࡸࡹࡩࡰࡰࠣࡪࡦ࡯࡬ࡦࡦࠣࡻ࡮ࡺࡨ࠻ࠢ࡟ࡲࠧ௮") + str(value))
  except Exception:
    pass
  bstack1l1l11111_opy_(value, True)
  sys.__excepthook__(exctype, value, traceback)
  sys.exit(1)
def bstack1l1l11111_opy_(message=bstack111l11_opy_ (u"ࠪࠫ௯"), bstack1l1l11ll1l_opy_ = False):
  global CONFIG
  bstack1lllll1l1l_opy_ = bstack111l11_opy_ (u"ࠫ࡬ࡲ࡯ࡣࡣ࡯ࡉࡽࡩࡥࡱࡶ࡬ࡳࡳ࠭௰") if bstack1l1l11ll1l_opy_ else bstack111l11_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫ௱")
  try:
    if message:
      bstack1ll11l1ll1_opy_ = {
        bstack1lllll1l1l_opy_ : str(message)
      }
      bstack111lll1l1_opy_(bstack1l1l1l11ll_opy_, CONFIG, bstack1ll11l1ll1_opy_)
    else:
      bstack111lll1l1_opy_(bstack1l1l1l11ll_opy_, CONFIG)
  except Exception as e:
    logger.debug(bstack1llll111_opy_.format(str(e)))
def bstack1lll1lll1l_opy_(bstack1ll1ll11ll_opy_, size):
  bstack11l1llll_opy_ = []
  while len(bstack1ll1ll11ll_opy_) > size:
    bstack1l1ll1l11_opy_ = bstack1ll1ll11ll_opy_[:size]
    bstack11l1llll_opy_.append(bstack1l1ll1l11_opy_)
    bstack1ll1ll11ll_opy_ = bstack1ll1ll11ll_opy_[size:]
  bstack11l1llll_opy_.append(bstack1ll1ll11ll_opy_)
  return bstack11l1llll_opy_
def bstack1ll1l111_opy_(args):
  if bstack111l11_opy_ (u"࠭࠭࡮ࠩ௲") in args and bstack111l11_opy_ (u"ࠧࡱࡦࡥࠫ௳") in args:
    return True
  return False
def run_on_browserstack(bstack1l1l1lll_opy_=None, bstack1ll11llll_opy_=None, bstack1l11111ll_opy_=False):
  global CONFIG
  global bstack1l1l11l11_opy_
  global bstack1lll11l11_opy_
  global bstack11llllll_opy_
  global bstack1l11l111ll_opy_
  bstack1l11l11l11_opy_ = bstack111l11_opy_ (u"ࠨࠩ௴")
  bstack1l1l1l11_opy_(bstack1ll1llll11_opy_, logger)
  if bstack1l1l1lll_opy_ and isinstance(bstack1l1l1lll_opy_, str):
    bstack1l1l1lll_opy_ = eval(bstack1l1l1lll_opy_)
  if bstack1l1l1lll_opy_:
    CONFIG = bstack1l1l1lll_opy_[bstack111l11_opy_ (u"ࠩࡆࡓࡓࡌࡉࡈࠩ௵")]
    bstack1l1l11l11_opy_ = bstack1l1l1lll_opy_[bstack111l11_opy_ (u"ࠪࡌ࡚ࡈ࡟ࡖࡔࡏࠫ௶")]
    bstack1lll11l11_opy_ = bstack1l1l1lll_opy_[bstack111l11_opy_ (u"ࠫࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭௷")]
    bstack1l11l111ll_opy_.bstack1ll1l11ll_opy_(bstack111l11_opy_ (u"ࠬࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧ௸"), bstack1lll11l11_opy_)
    bstack1l11l11l11_opy_ = bstack111l11_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭௹")
  bstack1l11l111ll_opy_.bstack1ll1l11ll_opy_(bstack111l11_opy_ (u"ࠧࡴࡦ࡮ࡖࡺࡴࡉࡥࠩ௺"), uuid4().__str__())
  logger.debug(bstack111l11_opy_ (u"ࠨࡵࡧ࡯ࡗࡻ࡮ࡊࡦࡀࠫ௻") + bstack1l11l111ll_opy_.get_property(bstack111l11_opy_ (u"ࠩࡶࡨࡰࡘࡵ࡯ࡋࡧࠫ௼")))
  if not bstack1l11111ll_opy_:
    if len(sys.argv) <= 1:
      logger.critical(bstack1ll1l1l11l_opy_)
      return
    if sys.argv[1] == bstack111l11_opy_ (u"ࠪ࠱࠲ࡼࡥࡳࡵ࡬ࡳࡳ࠭௽") or sys.argv[1] == bstack111l11_opy_ (u"ࠫ࠲ࡼࠧ௾"):
      logger.info(bstack111l11_opy_ (u"ࠬࡈࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡕࡿࡴࡩࡱࡱࠤࡘࡊࡋࠡࡸࡾࢁࠬ௿").format(__version__))
      return
    if sys.argv[1] == bstack111l11_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬఀ"):
      bstack1llll11l11_opy_()
      return
  args = sys.argv
  bstack1llll11l1_opy_()
  global bstack1l1l1llll1_opy_
  global bstack1l1ll1111l_opy_
  global bstack111lll1ll_opy_
  global bstack111111111_opy_
  global bstack1111111l1_opy_
  global bstack1l11ll1l_opy_
  global bstack111ll1l11_opy_
  global bstack1ll11l1l_opy_
  global bstack1l1llll1_opy_
  global bstack1l1lll11_opy_
  global bstack1l1l1ll11_opy_
  bstack1l1ll1111l_opy_ = len(CONFIG.get(bstack111l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪఁ"), []))
  if not bstack1l11l11l11_opy_:
    if args[1] == bstack111l11_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨం") or args[1] == bstack111l11_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯࠵ࠪః"):
      bstack1l11l11l11_opy_ = bstack111l11_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪఄ")
      args = args[2:]
    elif args[1] == bstack111l11_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪఅ"):
      bstack1l11l11l11_opy_ = bstack111l11_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫఆ")
      args = args[2:]
    elif args[1] == bstack111l11_opy_ (u"࠭ࡰࡢࡤࡲࡸࠬఇ"):
      bstack1l11l11l11_opy_ = bstack111l11_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭ఈ")
      args = args[2:]
    elif args[1] == bstack111l11_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠩఉ"):
      bstack1l11l11l11_opy_ = bstack111l11_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠪఊ")
      args = args[2:]
    elif args[1] == bstack111l11_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪఋ"):
      bstack1l11l11l11_opy_ = bstack111l11_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫఌ")
      args = args[2:]
    elif args[1] == bstack111l11_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬ఍"):
      bstack1l11l11l11_opy_ = bstack111l11_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭ఎ")
      args = args[2:]
    else:
      if not bstack111l11_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪఏ") in CONFIG or str(CONFIG[bstack111l11_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫఐ")]).lower() in [bstack111l11_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩ఑"), bstack111l11_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰ࠶ࠫఒ")]:
        bstack1l11l11l11_opy_ = bstack111l11_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫఓ")
        args = args[1:]
      elif str(CONFIG[bstack111l11_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨఔ")]).lower() == bstack111l11_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬక"):
        bstack1l11l11l11_opy_ = bstack111l11_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ఖ")
        args = args[1:]
      elif str(CONFIG[bstack111l11_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫగ")]).lower() == bstack111l11_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨఘ"):
        bstack1l11l11l11_opy_ = bstack111l11_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩఙ")
        args = args[1:]
      elif str(CONFIG[bstack111l11_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧచ")]).lower() == bstack111l11_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬఛ"):
        bstack1l11l11l11_opy_ = bstack111l11_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭జ")
        args = args[1:]
      elif str(CONFIG[bstack111l11_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪఝ")]).lower() == bstack111l11_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨఞ"):
        bstack1l11l11l11_opy_ = bstack111l11_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩట")
        args = args[1:]
      else:
        os.environ[bstack111l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡉࡖࡆࡓࡅࡘࡑࡕࡏࠬఠ")] = bstack1l11l11l11_opy_
        bstack11ll1lll1_opy_(bstack1l1l1l1lll_opy_)
  os.environ[bstack111l11_opy_ (u"ࠫࡋࡘࡁࡎࡇ࡚ࡓࡗࡑ࡟ࡖࡕࡈࡈࠬడ")] = bstack1l11l11l11_opy_
  bstack11llllll_opy_ = bstack1l11l11l11_opy_
  global bstack1llll111l_opy_
  if bstack1l1l1lll_opy_:
    try:
      os.environ[bstack111l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑࠧఢ")] = bstack1l11l11l11_opy_
      bstack111lll1l1_opy_(bstack11l1111l1_opy_, CONFIG)
    except Exception as e:
      logger.debug(bstack1ll1ll1l_opy_.format(str(e)))
  global bstack1ll111l11l_opy_
  global bstack11l1lll1_opy_
  global bstack111l1l11l_opy_
  global bstack1ll1l1lll1_opy_
  global bstack11l1l111l_opy_
  global bstack1ll1l11l_opy_
  global bstack1l11ll11_opy_
  global bstack1l1ll1l1_opy_
  global bstack1llll1l1ll_opy_
  global bstack1ll1l1ll1l_opy_
  global bstack1lll1llll_opy_
  global bstack111l1l1l1_opy_
  global bstack11ll1lll_opy_
  global bstack11l1ll11_opy_
  global bstack1l1ll1l11l_opy_
  global bstack111l1l11_opy_
  global bstack1llll1ll_opy_
  global bstack111l1llll_opy_
  global bstack1llll1lll1_opy_
  global bstack1lll1ll1ll_opy_
  global bstack1l111111_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack1ll111l11l_opy_ = webdriver.Remote.__init__
    bstack11l1lll1_opy_ = WebDriver.quit
    bstack111l1l1l1_opy_ = WebDriver.close
    bstack1l1ll1l11l_opy_ = WebDriver.get
    bstack1l111111_opy_ = WebDriver.execute
  except Exception as e:
    pass
  try:
    import Browser
    from subprocess import Popen
    bstack1llll111l_opy_ = Popen.__init__
  except Exception as e:
    pass
  try:
    global bstack11lll1l1_opy_
    from QWeb.keywords import browser
    bstack11lll1l1_opy_ = browser.close_browser
  except Exception as e:
    pass
  if bstack111ll1111_opy_(CONFIG) and bstack1ll1l11l11_opy_():
    if bstack1lll1l1ll_opy_() < version.parse(bstack1l111lll_opy_):
      logger.error(bstack1ll11111l_opy_.format(bstack1lll1l1ll_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        bstack111l1l11_opy_ = RemoteConnection._get_proxy_url
      except Exception as e:
        logger.error(bstack1l1l1lllll_opy_.format(str(e)))
  if not CONFIG.get(bstack111l11_opy_ (u"࠭ࡤࡪࡵࡤࡦࡱ࡫ࡁࡶࡶࡲࡇࡦࡶࡴࡶࡴࡨࡐࡴ࡭ࡳࠨణ"), False) and not bstack1l1l1lll_opy_:
    logger.info(bstack111lllll_opy_)
  if bstack1l11l11l11_opy_ != bstack111l11_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧత") or (bstack1l11l11l11_opy_ == bstack111l11_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨథ") and not bstack1l1l1lll_opy_):
    bstack1l1l11l1l1_opy_()
  if (bstack1l11l11l11_opy_ in [bstack111l11_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨద"), bstack111l11_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩధ"), bstack111l11_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬన")]):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCreator._get_ff_profile = bstack1l1111l1_opy_
        bstack1ll1l11l_opy_ = WebDriverCache.close
      except Exception as e:
        logger.warn(bstack1ll11ll1l_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import bstack11ll11lll_opy_
        bstack11l1l111l_opy_ = bstack11ll11lll_opy_.close
      except Exception as e:
        logger.debug(bstack11111l1l1_opy_ + str(e))
    except Exception as e:
      bstack1lll11lll_opy_(e, bstack1ll11ll1l_opy_)
    if bstack1l11l11l11_opy_ != bstack111l11_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ࠭఩"):
      bstack1l1llll1l_opy_()
    bstack111l1l11l_opy_ = Output.start_test
    bstack1ll1l1lll1_opy_ = Output.end_test
    bstack1l11ll11_opy_ = TestStatus.__init__
    bstack1llll1l1ll_opy_ = pabot._run
    bstack1ll1l1ll1l_opy_ = QueueItem.__init__
    bstack1lll1llll_opy_ = pabot._create_command_for_execution
    bstack1llll1lll1_opy_ = pabot._report_results
  if bstack1l11l11l11_opy_ == bstack111l11_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭ప"):
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1lll11lll_opy_(e, bstack1ll1ll111l_opy_)
    bstack11ll1lll_opy_ = Runner.run_hook
    bstack11l1ll11_opy_ = Step.run
  if bstack1l11l11l11_opy_ == bstack111l11_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧఫ"):
    try:
      from _pytest.config import Config
      bstack1llll1ll_opy_ = Config.getoption
      from _pytest import runner
      bstack111l1llll_opy_ = runner._update_current_test_var
    except Exception as e:
      logger.warn(e, bstack1l11l1l1_opy_)
    try:
      from pytest_bdd import reporting
      bstack1lll1ll1ll_opy_ = reporting.runtest_makereport
    except Exception as e:
      logger.debug(bstack111l11_opy_ (u"ࠨࡒ࡯ࡩࡦࡹࡥࠡ࡫ࡱࡷࡹࡧ࡬࡭ࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡴࡰࠢࡵࡹࡳࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡸࡪࡹࡴࡴࠩబ"))
  try:
    framework_name = bstack111l11_opy_ (u"ࠩࡕࡳࡧࡵࡴࠨభ") if bstack1l11l11l11_opy_ in [bstack111l11_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩమ"), bstack111l11_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪయ"), bstack111l11_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ࠭ర")] else bstack1l1ll111l1_opy_(bstack1l11l11l11_opy_)
    bstack1lll1ll1l_opy_.launch(CONFIG, {
      bstack111l11_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫ࠧఱ"): bstack111l11_opy_ (u"ࠧࡼ࠲ࢀ࠱ࡨࡻࡣࡶ࡯ࡥࡩࡷ࠭ల").format(framework_name) if bstack1l11l11l11_opy_ == bstack111l11_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨళ") and bstack11l1l111_opy_() else framework_name,
      bstack111l11_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ఴ"): bstack1lllll1l1_opy_(framework_name),
      bstack111l11_opy_ (u"ࠪࡷࡩࡱ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨవ"): __version__,
      bstack111l11_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡶࡵࡨࡨࠬశ"): bstack1l11l11l11_opy_
    })
  except Exception as e:
    logger.debug(bstack11111ll11_opy_.format(bstack111l11_opy_ (u"ࠬࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬష"), str(e)))
  if bstack1l11l11l11_opy_ in bstack1lll11ll_opy_:
    try:
      framework_name = bstack111l11_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬస") if bstack1l11l11l11_opy_ in [bstack111l11_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭హ"), bstack111l11_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧ఺")] else bstack1l11l11l11_opy_
      if bstack1ll1l11l1_opy_ and bstack111l11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ఻") in CONFIG and CONFIG[bstack111l11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻ఼ࠪ")] == True:
        if bstack111l11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫఽ") in CONFIG:
          os.environ[bstack111l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭ా")] = os.getenv(bstack111l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧి"), json.dumps(CONFIG[bstack111l11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧీ")]))
          CONFIG[bstack111l11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨు")].pop(bstack111l11_opy_ (u"ࠩ࡬ࡲࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧూ"), None)
          CONFIG[bstack111l11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪృ")].pop(bstack111l11_opy_ (u"ࠫࡪࡾࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩౄ"), None)
        bstack1111ll1ll_opy_, bstack1ll1llll1_opy_ = bstack1llll11l_opy_.bstack1l1lllll1_opy_(CONFIG, bstack1l11l11l11_opy_, bstack1lllll1l1_opy_(framework_name), str(bstack1lll1l1ll_opy_()))
        if not bstack1111ll1ll_opy_ is None:
          os.environ[bstack111l11_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪ౅")] = bstack1111ll1ll_opy_
          os.environ[bstack111l11_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡕࡇࡖࡘࡤࡘࡕࡏࡡࡌࡈࠬె")] = str(bstack1ll1llll1_opy_)
    except Exception as e:
      logger.debug(bstack11111ll11_opy_.format(bstack111l11_opy_ (u"ࠧࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧే"), str(e)))
  if bstack1l11l11l11_opy_ == bstack111l11_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨై"):
    bstack111lll1ll_opy_ = True
    if bstack1l1l1lll_opy_ and bstack1l11111ll_opy_:
      bstack1l11ll1l_opy_ = CONFIG.get(bstack111l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭౉"), {}).get(bstack111l11_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬొ"))
      bstack11l11l111_opy_(bstack11l1l1l1_opy_)
    elif bstack1l1l1lll_opy_:
      bstack1l11ll1l_opy_ = CONFIG.get(bstack111l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨో"), {}).get(bstack111l11_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧౌ"))
      global bstack1l1l1ll1l1_opy_
      try:
        if bstack1ll1l111_opy_(bstack1l1l1lll_opy_[bstack111l11_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦ్ࠩ")]) and multiprocessing.current_process().name == bstack111l11_opy_ (u"ࠧ࠱ࠩ౎"):
          bstack1l1l1lll_opy_[bstack111l11_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫ౏")].remove(bstack111l11_opy_ (u"ࠩ࠰ࡱࠬ౐"))
          bstack1l1l1lll_opy_[bstack111l11_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭౑")].remove(bstack111l11_opy_ (u"ࠫࡵࡪࡢࠨ౒"))
          bstack1l1l1lll_opy_[bstack111l11_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨ౓")] = bstack1l1l1lll_opy_[bstack111l11_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩ౔")][0]
          with open(bstack1l1l1lll_opy_[bstack111l11_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧౕࠪ")], bstack111l11_opy_ (u"ࠨࡴౖࠪ")) as f:
            bstack11l111l1l_opy_ = f.read()
          bstack1lll1lll11_opy_ = bstack111l11_opy_ (u"ࠤࠥࠦ࡫ࡸ࡯࡮ࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡵࡧ࡯ࠥ࡯࡭ࡱࡱࡵࡸࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣ࡮ࡴࡩࡵ࡫ࡤࡰ࡮ࢀࡥ࠼ࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠ࡫ࡱ࡭ࡹ࡯ࡡ࡭࡫ࡽࡩ࠭ࢁࡽࠪ࠽ࠣࡪࡷࡵ࡭ࠡࡲࡧࡦࠥ࡯࡭ࡱࡱࡵࡸࠥࡖࡤࡣ࠽ࠣࡳ࡬ࡥࡤࡣࠢࡀࠤࡕࡪࡢ࠯ࡦࡲࡣࡧࡸࡥࡢ࡭࠾ࠎࡩ࡫ࡦࠡ࡯ࡲࡨࡤࡨࡲࡦࡣ࡮ࠬࡸ࡫࡬ࡧ࠮ࠣࡥࡷ࡭ࠬࠡࡶࡨࡱࡵࡵࡲࡢࡴࡼࠤࡂࠦ࠰ࠪ࠼ࠍࠤࠥࡺࡲࡺ࠼ࠍࠤࠥࠦࠠࡢࡴࡪࠤࡂࠦࡳࡵࡴࠫ࡭ࡳࡺࠨࡢࡴࡪ࠭࠰࠷࠰ࠪࠌࠣࠤࡪࡾࡣࡦࡲࡷࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡢࡵࠣࡩ࠿ࠐࠠࠡࠢࠣࡴࡦࡹࡳࠋࠢࠣࡳ࡬ࡥࡤࡣࠪࡶࡩࡱ࡬ࠬࡢࡴࡪ࠰ࡹ࡫࡭ࡱࡱࡵࡥࡷࡿࠩࠋࡒࡧࡦ࠳ࡪ࡯ࡠࡤࠣࡁࠥࡳ࡯ࡥࡡࡥࡶࡪࡧ࡫ࠋࡒࡧࡦ࠳ࡪ࡯ࡠࡤࡵࡩࡦࡱࠠ࠾ࠢࡰࡳࡩࡥࡢࡳࡧࡤ࡯ࠏࡖࡤࡣࠪࠬ࠲ࡸ࡫ࡴࡠࡶࡵࡥࡨ࡫ࠨࠪ࡞ࡱࠦࠧࠨ౗").format(str(bstack1l1l1lll_opy_))
          bstack1lll1l1lll_opy_ = bstack1lll1lll11_opy_ + bstack11l111l1l_opy_
          bstack1lll111lll_opy_ = bstack1l1l1lll_opy_[bstack111l11_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ౘ")] + bstack111l11_opy_ (u"ࠫࡤࡨࡳࡵࡣࡦ࡯ࡤࡺࡥ࡮ࡲ࠱ࡴࡾ࠭ౙ")
          with open(bstack1lll111lll_opy_, bstack111l11_opy_ (u"ࠬࡽࠧౚ")):
            pass
          with open(bstack1lll111lll_opy_, bstack111l11_opy_ (u"ࠨࡷࠬࠤ౛")) as f:
            f.write(bstack1lll1l1lll_opy_)
          import subprocess
          bstack1l111l111_opy_ = subprocess.run([bstack111l11_opy_ (u"ࠢࡱࡻࡷ࡬ࡴࡴࠢ౜"), bstack1lll111lll_opy_])
          if os.path.exists(bstack1lll111lll_opy_):
            os.unlink(bstack1lll111lll_opy_)
          os._exit(bstack1l111l111_opy_.returncode)
        else:
          if bstack1ll1l111_opy_(bstack1l1l1lll_opy_[bstack111l11_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫౝ")]):
            bstack1l1l1lll_opy_[bstack111l11_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬ౞")].remove(bstack111l11_opy_ (u"ࠪ࠱ࡲ࠭౟"))
            bstack1l1l1lll_opy_[bstack111l11_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧౠ")].remove(bstack111l11_opy_ (u"ࠬࡶࡤࡣࠩౡ"))
            bstack1l1l1lll_opy_[bstack111l11_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩౢ")] = bstack1l1l1lll_opy_[bstack111l11_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪౣ")][0]
          bstack11l11l111_opy_(bstack11l1l1l1_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(bstack1l1l1lll_opy_[bstack111l11_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫ౤")])))
          sys.argv = sys.argv[2:]
          mod_globals = globals()
          mod_globals[bstack111l11_opy_ (u"ࠩࡢࡣࡳࡧ࡭ࡦࡡࡢࠫ౥")] = bstack111l11_opy_ (u"ࠪࡣࡤࡳࡡࡪࡰࡢࡣࠬ౦")
          mod_globals[bstack111l11_opy_ (u"ࠫࡤࡥࡦࡪ࡮ࡨࡣࡤ࠭౧")] = os.path.abspath(bstack1l1l1lll_opy_[bstack111l11_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨ౨")])
          exec(open(bstack1l1l1lll_opy_[bstack111l11_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩ౩")]).read(), mod_globals)
      except BaseException as e:
        try:
          traceback.print_exc()
          logger.error(bstack111l11_opy_ (u"ࠧࡄࡣࡸ࡫࡭ࡺࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰ࠽ࠤࢀࢃࠧ౪").format(str(e)))
          for driver in bstack1l1l1ll1l1_opy_:
            bstack1ll11llll_opy_.append({
              bstack111l11_opy_ (u"ࠨࡰࡤࡱࡪ࠭౫"): bstack1l1l1lll_opy_[bstack111l11_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬ౬")],
              bstack111l11_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩ౭"): str(e),
              bstack111l11_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪ౮"): multiprocessing.current_process().name
            })
            bstack1l1l11llll_opy_(driver, bstack111l11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ౯"), bstack111l11_opy_ (u"ࠨࡓࡦࡵࡶ࡭ࡴࡴࠠࡧࡣ࡬ࡰࡪࡪࠠࡸ࡫ࡷ࡬࠿ࠦ࡜࡯ࠤ౰") + str(e))
        except Exception:
          pass
      finally:
        try:
          for driver in bstack1l1l1ll1l1_opy_:
            driver.quit()
        except Exception as e:
          pass
    else:
      percy.init(bstack1lll11l11_opy_, CONFIG, logger)
      bstack111l11lll_opy_()
      bstack1l1l11l1l_opy_()
      bstack11l11ll1_opy_ = {
        bstack111l11_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪ౱"): args[0],
        bstack111l11_opy_ (u"ࠨࡅࡒࡒࡋࡏࡇࠨ౲"): CONFIG,
        bstack111l11_opy_ (u"ࠩࡋ࡙ࡇࡥࡕࡓࡎࠪ౳"): bstack1l1l11l11_opy_,
        bstack111l11_opy_ (u"ࠪࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬ౴"): bstack1lll11l11_opy_
      }
      percy.bstack11l1l11l1_opy_()
      if bstack111l11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ౵") in CONFIG:
        bstack1ll1111l_opy_ = []
        manager = multiprocessing.Manager()
        bstack1ll1ll111_opy_ = manager.list()
        if bstack1ll1l111_opy_(args):
          for index, platform in enumerate(CONFIG[bstack111l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ౶")]):
            if index == 0:
              bstack11l11ll1_opy_[bstack111l11_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩ౷")] = args
            bstack1ll1111l_opy_.append(multiprocessing.Process(name=str(index),
                                                       target=run_on_browserstack,
                                                       args=(bstack11l11ll1_opy_, bstack1ll1ll111_opy_)))
        else:
          for index, platform in enumerate(CONFIG[bstack111l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ౸")]):
            bstack1ll1111l_opy_.append(multiprocessing.Process(name=str(index),
                                                       target=run_on_browserstack,
                                                       args=(bstack11l11ll1_opy_, bstack1ll1ll111_opy_)))
        for t in bstack1ll1111l_opy_:
          t.start()
        for t in bstack1ll1111l_opy_:
          t.join()
        bstack1ll11l1l_opy_ = list(bstack1ll1ll111_opy_)
      else:
        if bstack1ll1l111_opy_(args):
          bstack11l11ll1_opy_[bstack111l11_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫ౹")] = args
          test = multiprocessing.Process(name=str(0),
                                         target=run_on_browserstack, args=(bstack11l11ll1_opy_,))
          test.start()
          test.join()
        else:
          bstack11l11l111_opy_(bstack11l1l1l1_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(args[0])))
          mod_globals = globals()
          mod_globals[bstack111l11_opy_ (u"ࠩࡢࡣࡳࡧ࡭ࡦࡡࡢࠫ౺")] = bstack111l11_opy_ (u"ࠪࡣࡤࡳࡡࡪࡰࡢࡣࠬ౻")
          mod_globals[bstack111l11_opy_ (u"ࠫࡤࡥࡦࡪ࡮ࡨࡣࡤ࠭౼")] = os.path.abspath(args[0])
          sys.argv = sys.argv[2:]
          exec(open(args[0]).read(), mod_globals)
  elif bstack1l11l11l11_opy_ == bstack111l11_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫ౽") or bstack1l11l11l11_opy_ == bstack111l11_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬ౾"):
    percy.init(bstack1lll11l11_opy_, CONFIG, logger)
    percy.bstack11l1l11l1_opy_()
    try:
      from pabot import pabot
    except Exception as e:
      bstack1lll11lll_opy_(e, bstack1ll11ll1l_opy_)
    bstack111l11lll_opy_()
    bstack11l11l111_opy_(bstack1ll111ll1l_opy_)
    if bstack1ll1l11l1_opy_ and bstack111l11_opy_ (u"ࠧ࠮࠯ࡳࡶࡴࡩࡥࡴࡵࡨࡷࠬ౿") in args:
      i = args.index(bstack111l11_opy_ (u"ࠨ࠯࠰ࡴࡷࡵࡣࡦࡵࡶࡩࡸ࠭ಀ"))
      args.pop(i)
      args.pop(i)
    if bstack1ll1l11l1_opy_:
      args.insert(0, str(bstack1l1l1llll1_opy_))
      args.insert(0, str(bstack111l11_opy_ (u"ࠩ࠰࠱ࡵࡸ࡯ࡤࡧࡶࡷࡪࡹࠧಁ")))
    if bstack1lll1ll1l_opy_.on():
      try:
        from robot.run import USAGE
        from robot.utils import ArgumentParser
        from pabot.arguments import _parse_pabot_args
        bstack1l1lllll_opy_, pabot_args = _parse_pabot_args(args)
        opts, bstack1ll1l1l1l1_opy_ = ArgumentParser(
            USAGE,
            auto_pythonpath=False,
            auto_argumentfile=True,
            env_options=bstack111l11_opy_ (u"ࠥࡖࡔࡈࡏࡕࡡࡒࡔ࡙ࡏࡏࡏࡕࠥಂ"),
        ).parse_args(bstack1l1lllll_opy_)
        bstack1l11l1l11_opy_ = args.index(bstack1l1lllll_opy_[0]) if len(bstack1l1lllll_opy_) > 0 else len(args)
        args.insert(bstack1l11l1l11_opy_, str(bstack111l11_opy_ (u"ࠫ࠲࠳࡬ࡪࡵࡷࡩࡳ࡫ࡲࠨಃ")))
        args.insert(bstack1l11l1l11_opy_ + 1, str(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack111l11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡸ࡯ࡣࡱࡷࡣࡱ࡯ࡳࡵࡧࡱࡩࡷ࠴ࡰࡺࠩ಄"))))
        if bstack1ll11l1l11_opy_(os.environ.get(bstack111l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡘࡅࡓࡗࡑࠫಅ"))) and str(os.environ.get(bstack111l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡒࡆࡔࡘࡒࡤ࡚ࡅࡔࡖࡖࠫಆ"), bstack111l11_opy_ (u"ࠨࡰࡸࡰࡱ࠭ಇ"))) != bstack111l11_opy_ (u"ࠩࡱࡹࡱࡲࠧಈ"):
          for bstack11l1111ll_opy_ in bstack1ll1l1l1l1_opy_:
            args.remove(bstack11l1111ll_opy_)
          bstack1lllllllll_opy_ = os.environ.get(bstack111l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡕࡉࡗ࡛ࡎࡠࡖࡈࡗ࡙࡙ࠧಉ")).split(bstack111l11_opy_ (u"ࠫ࠱࠭ಊ"))
          for bstack1ll1l1ll_opy_ in bstack1lllllllll_opy_:
            args.append(bstack1ll1l1ll_opy_)
      except Exception as e:
        logger.error(bstack111l11_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡥࡹࡺࡡࡤࡪ࡬ࡲ࡬ࠦ࡬ࡪࡵࡷࡩࡳ࡫ࡲࠡࡨࡲࡶࠥࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽ࠳ࠦࡅࡳࡴࡲࡶࠥ࠳ࠠࠣಋ").format(e))
    pabot.main(args)
  elif bstack1l11l11l11_opy_ == bstack111l11_opy_ (u"࠭ࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠧಌ"):
    try:
      from robot import run_cli
    except Exception as e:
      bstack1lll11lll_opy_(e, bstack1ll11ll1l_opy_)
    for a in args:
      if bstack111l11_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑࡐࡍࡃࡗࡊࡔࡘࡍࡊࡐࡇࡉ࡝࠭಍") in a:
        bstack1111111l1_opy_ = int(a.split(bstack111l11_opy_ (u"ࠨ࠼ࠪಎ"))[1])
      if bstack111l11_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡆࡈࡊࡑࡕࡃࡂࡎࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗ࠭ಏ") in a:
        bstack1l11ll1l_opy_ = str(a.split(bstack111l11_opy_ (u"ࠪ࠾ࠬಐ"))[1])
      if bstack111l11_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡇࡑࡏࡁࡓࡉࡖࠫ಑") in a:
        bstack111ll1l11_opy_ = str(a.split(bstack111l11_opy_ (u"ࠬࡀࠧಒ"))[1])
    bstack1ll1ll11_opy_ = None
    if bstack111l11_opy_ (u"࠭࠭࠮ࡤࡶࡸࡦࡩ࡫ࡠ࡫ࡷࡩࡲࡥࡩ࡯ࡦࡨࡼࠬಓ") in args:
      i = args.index(bstack111l11_opy_ (u"ࠧ࠮࠯ࡥࡷࡹࡧࡣ࡬ࡡ࡬ࡸࡪࡳ࡟ࡪࡰࡧࡩࡽ࠭ಔ"))
      args.pop(i)
      bstack1ll1ll11_opy_ = args.pop(i)
    if bstack1ll1ll11_opy_ is not None:
      global bstack1ll1ll1l1_opy_
      bstack1ll1ll1l1_opy_ = bstack1ll1ll11_opy_
    bstack11l11l111_opy_(bstack1ll111ll1l_opy_)
    run_cli(args)
    if bstack111l11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸࠬಕ") in multiprocessing.current_process().__dict__.keys():
      for bstack1lll1111l1_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack1ll11llll_opy_.append(bstack1lll1111l1_opy_)
  elif bstack1l11l11l11_opy_ == bstack111l11_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩಖ"):
    percy.init(bstack1lll11l11_opy_, CONFIG, logger)
    percy.bstack11l1l11l1_opy_()
    bstack1ll1ll1ll_opy_ = bstack1l11l111l_opy_(args, logger, CONFIG, bstack1ll1l11l1_opy_)
    bstack1ll1ll1ll_opy_.bstack111l11l1_opy_()
    bstack111l11lll_opy_()
    bstack111111111_opy_ = True
    bstack1l1lll11_opy_ = bstack1ll1ll1ll_opy_.bstack1l1lll11ll_opy_()
    bstack1ll1ll1ll_opy_.bstack11l11ll1_opy_(bstack1ll11lll_opy_)
    bstack1l1lll1ll1_opy_ = bstack1ll1ll1ll_opy_.bstack11l11ll1l_opy_(bstack1l1llll1ll_opy_, {
      bstack111l11_opy_ (u"ࠪࡌ࡚ࡈ࡟ࡖࡔࡏࠫಗ"): bstack1l1l11l11_opy_,
      bstack111l11_opy_ (u"ࠫࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭ಘ"): bstack1lll11l11_opy_,
      bstack111l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࠨಙ"): bstack1ll1l11l1_opy_
    })
    try:
      bstack1111111l_opy_, bstack1111l11l_opy_ = map(list, zip(*bstack1l1lll1ll1_opy_))
      bstack1l1llll1_opy_ = bstack1111111l_opy_[0]
      for status_code in bstack1111l11l_opy_:
        if status_code != 0:
          bstack1l1l1ll11_opy_ = status_code
          break
    except Exception as e:
      logger.debug(bstack111l11_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡶࡥࡻ࡫ࠠࡦࡴࡵࡳࡷࡹࠠࡢࡰࡧࠤࡸࡺࡡࡵࡷࡶࠤࡨࡵࡤࡦ࠰ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦ࠺ࠡࡽࢀࠦಚ").format(str(e)))
  elif bstack1l11l11l11_opy_ == bstack111l11_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧಛ"):
    try:
      from behave.__main__ import main as bstack1ll1111111_opy_
      from behave.configuration import Configuration
    except Exception as e:
      bstack1lll11lll_opy_(e, bstack1ll1ll111l_opy_)
    bstack111l11lll_opy_()
    bstack111111111_opy_ = True
    bstack1lll11111_opy_ = 1
    if bstack111l11_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨಜ") in CONFIG:
      bstack1lll11111_opy_ = CONFIG[bstack111l11_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩಝ")]
    bstack1111111ll_opy_ = int(bstack1lll11111_opy_) * int(len(CONFIG[bstack111l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ಞ")]))
    config = Configuration(args)
    bstack1l11l1ll1_opy_ = config.paths
    if len(bstack1l11l1ll1_opy_) == 0:
      import glob
      pattern = bstack111l11_opy_ (u"ࠫ࠯࠰࠯ࠫ࠰ࡩࡩࡦࡺࡵࡳࡧࠪಟ")
      bstack1111l1l1l_opy_ = glob.glob(pattern, recursive=True)
      args.extend(bstack1111l1l1l_opy_)
      config = Configuration(args)
      bstack1l11l1ll1_opy_ = config.paths
    bstack1ll1111ll1_opy_ = [os.path.normpath(item) for item in bstack1l11l1ll1_opy_]
    bstack1l1ll1l1l1_opy_ = [os.path.normpath(item) for item in args]
    bstack11ll1l11l_opy_ = [item for item in bstack1l1ll1l1l1_opy_ if item not in bstack1ll1111ll1_opy_]
    import platform as pf
    if pf.system().lower() == bstack111l11_opy_ (u"ࠬࡽࡩ࡯ࡦࡲࡻࡸ࠭ಠ"):
      from pathlib import PureWindowsPath, PurePosixPath
      bstack1ll1111ll1_opy_ = [str(PurePosixPath(PureWindowsPath(bstack11ll111l_opy_)))
                    for bstack11ll111l_opy_ in bstack1ll1111ll1_opy_]
    bstack1llll11l1l_opy_ = []
    for spec in bstack1ll1111ll1_opy_:
      bstack1111l1l11_opy_ = []
      bstack1111l1l11_opy_ += bstack11ll1l11l_opy_
      bstack1111l1l11_opy_.append(spec)
      bstack1llll11l1l_opy_.append(bstack1111l1l11_opy_)
    execution_items = []
    for bstack1111l1l11_opy_ in bstack1llll11l1l_opy_:
      for index, _ in enumerate(CONFIG[bstack111l11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩಡ")]):
        item = {}
        item[bstack111l11_opy_ (u"ࠧࡢࡴࡪࠫಢ")] = bstack111l11_opy_ (u"ࠨࠢࠪಣ").join(bstack1111l1l11_opy_)
        item[bstack111l11_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨತ")] = index
        execution_items.append(item)
    bstack1111ll111_opy_ = bstack1lll1lll1l_opy_(execution_items, bstack1111111ll_opy_)
    for execution_item in bstack1111ll111_opy_:
      bstack1ll1111l_opy_ = []
      for item in execution_item:
        bstack1ll1111l_opy_.append(bstack1l111ll11_opy_(name=str(item[bstack111l11_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩಥ")]),
                                             target=bstack11lllll1_opy_,
                                             args=(item[bstack111l11_opy_ (u"ࠫࡦࡸࡧࠨದ")],)))
      for t in bstack1ll1111l_opy_:
        t.start()
      for t in bstack1ll1111l_opy_:
        t.join()
  else:
    bstack11ll1lll1_opy_(bstack1l1l1l1lll_opy_)
  if not bstack1l1l1lll_opy_:
    bstack1l1lll111_opy_()
  bstack1l1l1l1l1_opy_.bstack1111l111l_opy_()
def browserstack_initialize(bstack111l1ll1l_opy_=None):
  run_on_browserstack(bstack111l1ll1l_opy_, None, True)
def bstack1l1lll111_opy_():
  global CONFIG
  global bstack11llllll_opy_
  global bstack1l1l1ll11_opy_
  global bstack11111llll_opy_
  global bstack1l11l111ll_opy_
  bstack1lll1ll1l_opy_.stop(bstack1l11l111ll_opy_.get_property(bstack111l11_opy_ (u"ࠬࡹࡤ࡬ࡍ࡬ࡰࡱ࡙ࡩࡨࡰࡤࡰࠬಧ")))
  bstack1lll1ll1l_opy_.bstack1l1l1ll1_opy_()
  if bstack1llll11l_opy_.bstack1l1l1l11l_opy_(CONFIG):
    bstack1llll11l_opy_.bstack1l111l1ll_opy_()
  [bstack11lll11ll_opy_, bstack1l11l11lll_opy_] = get_build_link()
  if bstack11lll11ll_opy_ is not None and bstack1l1ll1ll1_opy_() != -1:
    sessions = bstack1l1l1ll111_opy_(bstack11lll11ll_opy_)
    bstack1l1ll11l1_opy_(sessions, bstack1l11l11lll_opy_)
  if bstack11llllll_opy_ == bstack111l11_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ನ") and bstack1l1l1ll11_opy_ != 0:
    sys.exit(bstack1l1l1ll11_opy_)
  if bstack11llllll_opy_ == bstack111l11_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧ಩") and bstack11111llll_opy_ != 0:
    sys.exit(bstack11111llll_opy_)
def bstack1l1ll111l1_opy_(bstack111lll111_opy_):
  if bstack111lll111_opy_:
    return bstack111lll111_opy_.capitalize()
  else:
    return bstack111l11_opy_ (u"ࠨࠩಪ")
def bstack111l11l1l_opy_(bstack111lllll1_opy_):
  if bstack111l11_opy_ (u"ࠩࡱࡥࡲ࡫ࠧಫ") in bstack111lllll1_opy_ and bstack111lllll1_opy_[bstack111l11_opy_ (u"ࠪࡲࡦࡳࡥࠨಬ")] != bstack111l11_opy_ (u"ࠫࠬಭ"):
    return bstack111lllll1_opy_[bstack111l11_opy_ (u"ࠬࡴࡡ࡮ࡧࠪಮ")]
  else:
    bstack11l1lll11_opy_ = bstack111l11_opy_ (u"ࠨࠢಯ")
    if bstack111l11_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࠧರ") in bstack111lllll1_opy_ and bstack111lllll1_opy_[bstack111l11_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࠨಱ")] != None:
      bstack11l1lll11_opy_ += bstack111lllll1_opy_[bstack111l11_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࠩಲ")] + bstack111l11_opy_ (u"ࠥ࠰ࠥࠨಳ")
      if bstack111lllll1_opy_[bstack111l11_opy_ (u"ࠫࡴࡹࠧ಴")] == bstack111l11_opy_ (u"ࠧ࡯࡯ࡴࠤವ"):
        bstack11l1lll11_opy_ += bstack111l11_opy_ (u"ࠨࡩࡐࡕࠣࠦಶ")
      bstack11l1lll11_opy_ += (bstack111lllll1_opy_[bstack111l11_opy_ (u"ࠧࡰࡵࡢࡺࡪࡸࡳࡪࡱࡱࠫಷ")] or bstack111l11_opy_ (u"ࠨࠩಸ"))
      return bstack11l1lll11_opy_
    else:
      bstack11l1lll11_opy_ += bstack1l1ll111l1_opy_(bstack111lllll1_opy_[bstack111l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪಹ")]) + bstack111l11_opy_ (u"ࠥࠤࠧ಺") + (
              bstack111lllll1_opy_[bstack111l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭಻")] or bstack111l11_opy_ (u"಼ࠬ࠭")) + bstack111l11_opy_ (u"ࠨࠬࠡࠤಽ")
      if bstack111lllll1_opy_[bstack111l11_opy_ (u"ࠧࡰࡵࠪಾ")] == bstack111l11_opy_ (u"࡙ࠣ࡬ࡲࡩࡵࡷࡴࠤಿ"):
        bstack11l1lll11_opy_ += bstack111l11_opy_ (u"ࠤ࡚࡭ࡳࠦࠢೀ")
      bstack11l1lll11_opy_ += bstack111lllll1_opy_[bstack111l11_opy_ (u"ࠪࡳࡸࡥࡶࡦࡴࡶ࡭ࡴࡴࠧು")] or bstack111l11_opy_ (u"ࠫࠬೂ")
      return bstack11l1lll11_opy_
def bstack11lll1lll_opy_(bstack111111ll_opy_):
  if bstack111111ll_opy_ == bstack111l11_opy_ (u"ࠧࡪ࡯࡯ࡧࠥೃ"):
    return bstack111l11_opy_ (u"࠭࠼ࡵࡦࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࠢࡶࡸࡾࡲࡥ࠾ࠤࡦࡳࡱࡵࡲ࠻ࡩࡵࡩࡪࡴ࠻ࠣࡀ࠿ࡪࡴࡴࡴࠡࡥࡲࡰࡴࡸ࠽ࠣࡩࡵࡩࡪࡴࠢ࠿ࡅࡲࡱࡵࡲࡥࡵࡧࡧࡀ࠴࡬࡯࡯ࡶࡁࡀ࠴ࡺࡤ࠿ࠩೄ")
  elif bstack111111ll_opy_ == bstack111l11_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢ೅"):
    return bstack111l11_opy_ (u"ࠨ࠾ࡷࡨࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࠤࡸࡺࡹ࡭ࡧࡀࠦࡨࡵ࡬ࡰࡴ࠽ࡶࡪࡪ࠻ࠣࡀ࠿ࡪࡴࡴࡴࠡࡥࡲࡰࡴࡸ࠽ࠣࡴࡨࡨࠧࡄࡆࡢ࡫࡯ࡩࡩࡂ࠯ࡧࡱࡱࡸࡃࡂ࠯ࡵࡦࡁࠫೆ")
  elif bstack111111ll_opy_ == bstack111l11_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤೇ"):
    return bstack111l11_opy_ (u"ࠪࡀࡹࡪࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࠦࡳࡵࡻ࡯ࡩࡂࠨࡣࡰ࡮ࡲࡶ࠿࡭ࡲࡦࡧࡱ࠿ࠧࡄ࠼ࡧࡱࡱࡸࠥࡩ࡯࡭ࡱࡵࡁࠧ࡭ࡲࡦࡧࡱࠦࡃࡖࡡࡴࡵࡨࡨࡁ࠵ࡦࡰࡰࡷࡂࡁ࠵ࡴࡥࡀࠪೈ")
  elif bstack111111ll_opy_ == bstack111l11_opy_ (u"ࠦࡪࡸࡲࡰࡴࠥ೉"):
    return bstack111l11_opy_ (u"ࠬࡂࡴࡥࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢࠡࡵࡷࡽࡱ࡫࠽ࠣࡥࡲࡰࡴࡸ࠺ࡳࡧࡧ࠿ࠧࡄ࠼ࡧࡱࡱࡸࠥࡩ࡯࡭ࡱࡵࡁࠧࡸࡥࡥࠤࡁࡉࡷࡸ࡯ࡳ࠾࠲ࡪࡴࡴࡴ࠿࠾࠲ࡸࡩࡄࠧೊ")
  elif bstack111111ll_opy_ == bstack111l11_opy_ (u"ࠨࡴࡪ࡯ࡨࡳࡺࡺࠢೋ"):
    return bstack111l11_opy_ (u"ࠧ࠽ࡶࡧࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࠣࡷࡹࡿ࡬ࡦ࠿ࠥࡧࡴࡲ࡯ࡳ࠼ࠦࡩࡪࡧ࠳࠳࠸࠾ࠦࡃࡂࡦࡰࡰࡷࠤࡨࡵ࡬ࡰࡴࡀࠦࠨ࡫ࡥࡢ࠵࠵࠺ࠧࡄࡔࡪ࡯ࡨࡳࡺࡺ࠼࠰ࡨࡲࡲࡹࡄ࠼࠰ࡶࡧࡂࠬೌ")
  elif bstack111111ll_opy_ == bstack111l11_opy_ (u"ࠣࡴࡸࡲࡳ࡯࡮ࡨࠤ್"):
    return bstack111l11_opy_ (u"ࠩ࠿ࡸࡩࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࠥࡹࡴࡺ࡮ࡨࡁࠧࡩ࡯࡭ࡱࡵ࠾ࡧࡲࡡࡤ࡭࠾ࠦࡃࡂࡦࡰࡰࡷࠤࡨࡵ࡬ࡰࡴࡀࠦࡧࡲࡡࡤ࡭ࠥࡂࡗࡻ࡮࡯࡫ࡱ࡫ࡁ࠵ࡦࡰࡰࡷࡂࡁ࠵ࡴࡥࡀࠪ೎")
  else:
    return bstack111l11_opy_ (u"ࠪࡀࡹࡪࠠࡢ࡮࡬࡫ࡳࡃࠢࡤࡧࡱࡸࡪࡸࠢࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨࠠࡴࡶࡼࡰࡪࡃࠢࡤࡱ࡯ࡳࡷࡀࡢ࡭ࡣࡦ࡯ࡀࠨ࠾࠽ࡨࡲࡲࡹࠦࡣࡰ࡮ࡲࡶࡂࠨࡢ࡭ࡣࡦ࡯ࠧࡄࠧ೏") + bstack1l1ll111l1_opy_(
      bstack111111ll_opy_) + bstack111l11_opy_ (u"ࠫࡁ࠵ࡦࡰࡰࡷࡂࡁ࠵ࡴࡥࡀࠪ೐")
def bstack1ll1llll1l_opy_(session):
  return bstack111l11_opy_ (u"ࠬࡂࡴࡳࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡵࡳࡼࠨ࠾࠽ࡶࡧࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠢࡶࡩࡸࡹࡩࡰࡰ࠰ࡲࡦࡳࡥࠣࡀ࠿ࡥࠥ࡮ࡲࡦࡨࡀࠦࢀࢃࠢࠡࡶࡤࡶ࡬࡫ࡴ࠾ࠤࡢࡦࡱࡧ࡮࡬ࠤࡁࡿࢂࡂ࠯ࡢࡀ࠿࠳ࡹࡪ࠾ࡼࡿࡾࢁࡁࡺࡤࠡࡣ࡯࡭࡬ࡴ࠽ࠣࡥࡨࡲࡹ࡫ࡲࠣࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢ࠿ࡽࢀࡀ࠴ࡺࡤ࠿࠾ࡷࡨࠥࡧ࡬ࡪࡩࡱࡁࠧࡩࡥ࡯ࡶࡨࡶࠧࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࡃࢁࡽ࠽࠱ࡷࡨࡃࡂࡴࡥࠢࡤࡰ࡮࡭࡮࠾ࠤࡦࡩࡳࡺࡥࡳࠤࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࡀࡾࢁࡁ࠵ࡴࡥࡀ࠿ࡸࡩࠦࡡ࡭࡫ࡪࡲࡂࠨࡣࡦࡰࡷࡩࡷࠨࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࡄࡻࡾ࠾࠲ࡸࡩࡄ࠼࠰ࡶࡵࡂࠬ೑").format(
    session[bstack111l11_opy_ (u"࠭ࡰࡶࡤ࡯࡭ࡨࡥࡵࡳ࡮ࠪ೒")], bstack111l11l1l_opy_(session), bstack11lll1lll_opy_(session[bstack111l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡳࡵࡣࡷࡹࡸ࠭೓")]),
    bstack11lll1lll_opy_(session[bstack111l11_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ೔")]),
    bstack1l1ll111l1_opy_(session[bstack111l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪೕ")] or session[bstack111l11_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࠪೖ")] or bstack111l11_opy_ (u"ࠫࠬ೗")) + bstack111l11_opy_ (u"ࠧࠦࠢ೘") + (session[bstack111l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ೙")] or bstack111l11_opy_ (u"ࠧࠨ೚")),
    session[bstack111l11_opy_ (u"ࠨࡱࡶࠫ೛")] + bstack111l11_opy_ (u"ࠤࠣࠦ೜") + session[bstack111l11_opy_ (u"ࠪࡳࡸࡥࡶࡦࡴࡶ࡭ࡴࡴࠧೝ")], session[bstack111l11_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳ࠭ೞ")] or bstack111l11_opy_ (u"ࠬ࠭೟"),
    session[bstack111l11_opy_ (u"࠭ࡣࡳࡧࡤࡸࡪࡪ࡟ࡢࡶࠪೠ")] if session[bstack111l11_opy_ (u"ࠧࡤࡴࡨࡥࡹ࡫ࡤࡠࡣࡷࠫೡ")] else bstack111l11_opy_ (u"ࠨࠩೢ"))
def bstack1l1ll11l1_opy_(sessions, bstack1l11l11lll_opy_):
  try:
    bstack1lll111ll_opy_ = bstack111l11_opy_ (u"ࠤࠥೣ")
    if not os.path.exists(bstack11llll1l_opy_):
      os.mkdir(bstack11llll1l_opy_)
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack111l11_opy_ (u"ࠪࡥࡸࡹࡥࡵࡵ࠲ࡶࡪࡶ࡯ࡳࡶ࠱࡬ࡹࡳ࡬ࠨ೤")), bstack111l11_opy_ (u"ࠫࡷ࠭೥")) as f:
      bstack1lll111ll_opy_ = f.read()
    bstack1lll111ll_opy_ = bstack1lll111ll_opy_.replace(bstack111l11_opy_ (u"ࠬࢁࠥࡓࡇࡖ࡙ࡑ࡚ࡓࡠࡅࡒ࡙ࡓ࡚ࠥࡾࠩ೦"), str(len(sessions)))
    bstack1lll111ll_opy_ = bstack1lll111ll_opy_.replace(bstack111l11_opy_ (u"࠭ࡻࠦࡄࡘࡍࡑࡊ࡟ࡖࡔࡏࠩࢂ࠭೧"), bstack1l11l11lll_opy_)
    bstack1lll111ll_opy_ = bstack1lll111ll_opy_.replace(bstack111l11_opy_ (u"ࠧࡼࠧࡅ࡙ࡎࡒࡄࡠࡐࡄࡑࡊࠫࡽࠨ೨"),
                                              sessions[0].get(bstack111l11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟࡯ࡣࡰࡩࠬ೩")) if sessions[0] else bstack111l11_opy_ (u"ࠩࠪ೪"))
    with open(os.path.join(bstack11llll1l_opy_, bstack111l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠯ࡵࡩࡵࡵࡲࡵ࠰࡫ࡸࡲࡲࠧ೫")), bstack111l11_opy_ (u"ࠫࡼ࠭೬")) as stream:
      stream.write(bstack1lll111ll_opy_.split(bstack111l11_opy_ (u"ࠬࢁࠥࡔࡇࡖࡗࡎࡕࡎࡔࡡࡇࡅ࡙ࡇࠥࡾࠩ೭"))[0])
      for session in sessions:
        stream.write(bstack1ll1llll1l_opy_(session))
      stream.write(bstack1lll111ll_opy_.split(bstack111l11_opy_ (u"࠭ࡻࠦࡕࡈࡗࡘࡏࡏࡏࡕࡢࡈࡆ࡚ࡁࠦࡿࠪ೮"))[1])
    logger.info(bstack111l11_opy_ (u"ࠧࡈࡧࡱࡩࡷࡧࡴࡦࡦࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡥࡹ࡮ࡲࡤࠡࡣࡵࡸ࡮࡬ࡡࡤࡶࡶࠤࡦࡺࠠࡼࡿࠪ೯").format(bstack11llll1l_opy_));
  except Exception as e:
    logger.debug(bstack1l1l11ll1_opy_.format(str(e)))
def bstack1l1l1ll111_opy_(bstack11lll11ll_opy_):
  global CONFIG
  try:
    host = bstack111l11_opy_ (u"ࠨࡣࡳ࡭࠲ࡩ࡬ࡰࡷࡧࠫ೰") if bstack111l11_opy_ (u"ࠩࡤࡴࡵ࠭ೱ") in CONFIG else bstack111l11_opy_ (u"ࠪࡥࡵ࡯ࠧೲ")
    user = CONFIG[bstack111l11_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ೳ")]
    key = CONFIG[bstack111l11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ೴")]
    bstack11l1lllll_opy_ = bstack111l11_opy_ (u"࠭ࡡࡱࡲ࠰ࡥࡺࡺ࡯࡮ࡣࡷࡩࠬ೵") if bstack111l11_opy_ (u"ࠧࡢࡲࡳࠫ೶") in CONFIG else bstack111l11_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵࡧࠪ೷")
    url = bstack111l11_opy_ (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡿࢂࡀࡻࡾࡂࡾࢁ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡽࢀ࠳ࡧࡻࡩ࡭ࡦࡶ࠳ࢀࢃ࠯ࡴࡧࡶࡷ࡮ࡵ࡮ࡴ࠰࡭ࡷࡴࡴࠧ೸").format(user, key, host, bstack11l1lllll_opy_,
                                                                                bstack11lll11ll_opy_)
    headers = {
      bstack111l11_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩ೹"): bstack111l11_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧ೺"),
    }
    proxies = bstack1l11ll11l1_opy_(CONFIG, url)
    response = requests.get(url, headers=headers, proxies=proxies)
    if response.json():
      return list(map(lambda session: session[bstack111l11_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡࡶࡩࡸࡹࡩࡰࡰࠪ೻")], response.json()))
  except Exception as e:
    logger.debug(bstack1ll11lll1_opy_.format(str(e)))
def get_build_link():
  global CONFIG
  global bstack1ll11l111_opy_
  try:
    if bstack111l11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ೼") in CONFIG:
      host = bstack111l11_opy_ (u"ࠧࡢࡲ࡬࠱ࡨࡲ࡯ࡶࡦࠪ೽") if bstack111l11_opy_ (u"ࠨࡣࡳࡴࠬ೾") in CONFIG else bstack111l11_opy_ (u"ࠩࡤࡴ࡮࠭೿")
      user = CONFIG[bstack111l11_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬഀ")]
      key = CONFIG[bstack111l11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧഁ")]
      bstack11l1lllll_opy_ = bstack111l11_opy_ (u"ࠬࡧࡰࡱ࠯ࡤࡹࡹࡵ࡭ࡢࡶࡨࠫം") if bstack111l11_opy_ (u"࠭ࡡࡱࡲࠪഃ") in CONFIG else bstack111l11_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡦࠩഄ")
      url = bstack111l11_opy_ (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱ࡾࢁ࠿ࢁࡽࡁࡽࢀ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡼࡿ࠲ࡦࡺ࡯࡬ࡥࡵ࠱࡮ࡸࡵ࡮ࠨഅ").format(user, key, host, bstack11l1lllll_opy_)
      headers = {
        bstack111l11_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡸࡾࡶࡥࠨആ"): bstack111l11_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ഇ"),
      }
      if bstack111l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ഈ") in CONFIG:
        params = {bstack111l11_opy_ (u"ࠬࡴࡡ࡮ࡧࠪഉ"): CONFIG[bstack111l11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩഊ")], bstack111l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪഋ"): CONFIG[bstack111l11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪഌ")]}
      else:
        params = {bstack111l11_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ഍"): CONFIG[bstack111l11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭എ")]}
      proxies = bstack1l11ll11l1_opy_(CONFIG, url)
      response = requests.get(url, params=params, headers=headers, proxies=proxies)
      if response.json():
        bstack11lll1l11_opy_ = response.json()[0][bstack111l11_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠࡤࡸ࡭ࡱࡪࠧഏ")]
        if bstack11lll1l11_opy_:
          bstack1l11l11lll_opy_ = bstack11lll1l11_opy_[bstack111l11_opy_ (u"ࠬࡶࡵࡣ࡮࡬ࡧࡤࡻࡲ࡭ࠩഐ")].split(bstack111l11_opy_ (u"࠭ࡰࡶࡤ࡯࡭ࡨ࠳ࡢࡶ࡫࡯ࡨࠬ഑"))[0] + bstack111l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡹ࠯ࠨഒ") + bstack11lll1l11_opy_[
            bstack111l11_opy_ (u"ࠨࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫഓ")]
          logger.info(bstack1ll111ll_opy_.format(bstack1l11l11lll_opy_))
          bstack1ll11l111_opy_ = bstack11lll1l11_opy_[bstack111l11_opy_ (u"ࠩ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬഔ")]
          bstack1llllllll1_opy_ = CONFIG[bstack111l11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ക")]
          if bstack111l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ഖ") in CONFIG:
            bstack1llllllll1_opy_ += bstack111l11_opy_ (u"ࠬࠦࠧഗ") + CONFIG[bstack111l11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨഘ")]
          if bstack1llllllll1_opy_ != bstack11lll1l11_opy_[bstack111l11_opy_ (u"ࠧ࡯ࡣࡰࡩࠬങ")]:
            logger.debug(bstack11111l111_opy_.format(bstack11lll1l11_opy_[bstack111l11_opy_ (u"ࠨࡰࡤࡱࡪ࠭ച")], bstack1llllllll1_opy_))
          return [bstack11lll1l11_opy_[bstack111l11_opy_ (u"ࠩ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬഛ")], bstack1l11l11lll_opy_]
    else:
      logger.warn(bstack1lll1l1l1l_opy_)
  except Exception as e:
    logger.debug(bstack1l1l11l1ll_opy_.format(str(e)))
  return [None, None]
def bstack11l111ll1_opy_(url, bstack111l111l1_opy_=False):
  global CONFIG
  global bstack11111l11l_opy_
  if not bstack11111l11l_opy_:
    hostname = bstack1lll11ll1l_opy_(url)
    is_private = bstack1l1ll1lll1_opy_(hostname)
    if (bstack111l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧജ") in CONFIG and not bstack1ll11l1l11_opy_(CONFIG[bstack111l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨഝ")])) and (is_private or bstack111l111l1_opy_):
      bstack11111l11l_opy_ = hostname
def bstack1lll11ll1l_opy_(url):
  return urlparse(url).hostname
def bstack1l1ll1lll1_opy_(hostname):
  for bstack1llllll11l_opy_ in bstack1lllllll11_opy_:
    regex = re.compile(bstack1llllll11l_opy_)
    if regex.match(hostname):
      return True
  return False
def bstack111ll1ll1_opy_(key_name):
  return True if key_name in threading.current_thread().__dict__.keys() else False
def getAccessibilityResults(driver):
  global CONFIG
  global bstack1111111l1_opy_
  bstack1l111llll_opy_ = not (bstack1ll111l1ll_opy_(threading.current_thread(), bstack111l11_opy_ (u"ࠬ࡯ࡳࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠩഞ"), None) and bstack1ll111l1ll_opy_(
          threading.current_thread(), bstack111l11_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬട"), None))
  bstack1lll11l1l_opy_ = getattr(driver, bstack111l11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡁ࠲࠳ࡼࡗ࡭ࡵࡵ࡭ࡦࡖࡧࡦࡴࠧഠ"), None) != True
  if not bstack1llll11l_opy_.bstack1l1l1ll1l_opy_(CONFIG, bstack1111111l1_opy_) or (bstack1lll11l1l_opy_ and bstack1l111llll_opy_):
    logger.warning(bstack111l11_opy_ (u"ࠣࡐࡲࡸࠥࡧ࡮ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡹࡥࡴࡵ࡬ࡳࡳ࠲ࠠࡤࡣࡱࡲࡴࡺࠠࡳࡧࡷࡶ࡮࡫ࡶࡦࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡵࡩࡸࡻ࡬ࡵࡵ࠱ࠦഡ"))
    return {}
  try:
    logger.debug(bstack111l11_opy_ (u"ࠩࡓࡩࡷ࡬࡯ࡳ࡯࡬ࡲ࡬ࠦࡳࡤࡣࡱࠤࡧ࡫ࡦࡰࡴࡨࠤ࡬࡫ࡴࡵ࡫ࡱ࡫ࠥࡸࡥࡴࡷ࡯ࡸࡸ࠭ഢ"))
    logger.debug(perform_scan(driver))
    results = driver.execute_async_script(bstack1l1lll1lll_opy_.bstack1llll111ll_opy_)
    return results
  except Exception:
    logger.error(bstack111l11_opy_ (u"ࠥࡒࡴࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡲࡦࡵࡸࡰࡹࡹࠠࡸࡧࡵࡩࠥ࡬࡯ࡶࡰࡧ࠲ࠧണ"))
    return {}
def getAccessibilityResultsSummary(driver):
  global CONFIG
  global bstack1111111l1_opy_
  bstack1l111llll_opy_ = not (bstack1ll111l1ll_opy_(threading.current_thread(), bstack111l11_opy_ (u"ࠫ࡮ࡹࡁ࠲࠳ࡼࡘࡪࡹࡴࠨത"), None) and bstack1ll111l1ll_opy_(
          threading.current_thread(), bstack111l11_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫഥ"), None))
  bstack1lll11l1l_opy_ = getattr(driver, bstack111l11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡇ࠱࠲ࡻࡖ࡬ࡴࡻ࡬ࡥࡕࡦࡥࡳ࠭ദ"), None) != True
  if not bstack1llll11l_opy_.bstack1l1l1ll1l_opy_(CONFIG, bstack1111111l1_opy_) or (bstack1lll11l1l_opy_ and bstack1l111llll_opy_):
    logger.warning(bstack111l11_opy_ (u"ࠢࡏࡱࡷࠤࡦࡴࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠱ࠦࡣࡢࡰࡱࡳࡹࠦࡲࡦࡶࡵ࡭ࡪࡼࡥࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡴࡨࡷࡺࡲࡴࡴࠢࡶࡹࡲࡳࡡࡳࡻ࠱ࠦധ"))
    return {}
  try:
    logger.debug(bstack111l11_opy_ (u"ࠨࡒࡨࡶ࡫ࡵࡲ࡮࡫ࡱ࡫ࠥࡹࡣࡢࡰࠣࡦࡪ࡬࡯ࡳࡧࠣ࡫ࡪࡺࡴࡪࡰࡪࠤࡷ࡫ࡳࡶ࡮ࡷࡷࠥࡹࡵ࡮࡯ࡤࡶࡾ࠭ന"))
    logger.debug(perform_scan(driver))
    bstack1l11l1lll1_opy_ = driver.execute_async_script(bstack1l1lll1lll_opy_.bstack1111lll1l_opy_)
    return bstack1l11l1lll1_opy_
  except Exception:
    logger.error(bstack111l11_opy_ (u"ࠤࡑࡳࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡹࡵ࡮࡯ࡤࡶࡾࠦࡷࡢࡵࠣࡪࡴࡻ࡮ࡥ࠰ࠥഩ"))
    return {}
def perform_scan(driver, *args, **kwargs):
  global CONFIG
  global bstack1111111l1_opy_
  bstack1l111llll_opy_ = not (bstack1ll111l1ll_opy_(threading.current_thread(), bstack111l11_opy_ (u"ࠪ࡭ࡸࡇ࠱࠲ࡻࡗࡩࡸࡺࠧപ"), None) and bstack1ll111l1ll_opy_(
          threading.current_thread(), bstack111l11_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪഫ"), None))
  bstack1lll11l1l_opy_ = getattr(driver, bstack111l11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡆ࠷࠱ࡺࡕ࡫ࡳࡺࡲࡤࡔࡥࡤࡲࠬബ"), None) != True
  if not bstack1llll11l_opy_.bstack1l1l1ll1l_opy_(CONFIG, bstack1111111l1_opy_) or (bstack1lll11l1l_opy_ and bstack1l111llll_opy_):
    logger.warning(bstack111l11_opy_ (u"ࠨࡎࡰࡶࠣࡥࡳࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡷࡪࡹࡳࡪࡱࡱ࠰ࠥࡩࡡ࡯ࡰࡲࡸࠥࡸࡵ࡯ࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡶࡧࡦࡴ࠮ࠣഭ"))
    return {}
  try:
    bstack11lll111_opy_ = driver.execute_async_script(bstack1l1lll1lll_opy_.perform_scan, {bstack111l11_opy_ (u"ࠧ࡮ࡧࡷ࡬ࡴࡪࠧമ"): kwargs.get(bstack111l11_opy_ (u"ࠨࡦࡵ࡭ࡻ࡫ࡲࡠࡥࡲࡱࡲࡧ࡮ࡥࠩയ"), None) or bstack111l11_opy_ (u"ࠩࠪര")})
    return bstack11lll111_opy_
  except Exception:
    logger.error(bstack111l11_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡲࡶࡰࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡷࡨࡧ࡮࠯ࠤറ"))
    return {}
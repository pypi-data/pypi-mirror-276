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
import os
import json
import requests
import logging
from urllib.parse import urlparse
from bstack_utils.constants import bstack11ll11l11l_opy_ as bstack11ll111l11_opy_
from bstack_utils.bstack1l1lll1lll_opy_ import bstack1l1lll1lll_opy_
from bstack_utils.helper import bstack11ll1l1ll_opy_, bstack1l111llll1_opy_, bstack1l11lll11_opy_, bstack11ll11l1ll_opy_, bstack11l1llll11_opy_, bstack1l111ll1_opy_, get_host_info, bstack11ll11111l_opy_, bstack1lllll1lll_opy_, bstack1l1111ll11_opy_
from browserstack_sdk._version import __version__
logger = logging.getLogger(__name__)
@bstack1l1111ll11_opy_(class_method=False)
def _11l1llllll_opy_(driver, bstack1ll1l1ll1_opy_):
  response = {}
  try:
    caps = driver.capabilities
    response = {
        bstack111l11_opy_ (u"ࠪࡳࡸࡥ࡮ࡢ࡯ࡨ้ࠫ"): caps.get(bstack111l11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡔࡡ࡮ࡧ๊ࠪ"), None),
        bstack111l11_opy_ (u"ࠬࡵࡳࡠࡸࡨࡶࡸ࡯࡯࡯๋ࠩ"): bstack1ll1l1ll1_opy_.get(bstack111l11_opy_ (u"࠭࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩ์"), None),
        bstack111l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡰࡤࡱࡪ࠭ํ"): caps.get(bstack111l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭๎"), None),
        bstack111l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠫ๏"): caps.get(bstack111l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫ๐"), None)
    }
  except Exception as error:
    logger.debug(bstack111l11_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡪࡪࡺࡣࡩ࡫ࡱ࡫ࠥࡶ࡬ࡢࡶࡩࡳࡷࡳࠠࡥࡧࡷࡥ࡮ࡲࡳࠡࡹ࡬ࡸ࡭ࠦࡥࡳࡴࡲࡶࠥࡀࠠࠨ๑") + str(error))
  return response
def bstack1l1l1l11l_opy_(config):
  return config.get(bstack111l11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ๒"), False) or any([p.get(bstack111l11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭๓"), False) == True for p in config.get(bstack111l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ๔"), [])])
def bstack1l1l1ll1l_opy_(config, bstack1ll11lllll_opy_):
  try:
    if not bstack1l11lll11_opy_(config):
      return False
    bstack11ll1111ll_opy_ = config.get(bstack111l11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ๕"), False)
    bstack11l1lll1l1_opy_ = config[bstack111l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ๖")][bstack1ll11lllll_opy_].get(bstack111l11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ๗"), None)
    if bstack11l1lll1l1_opy_ != None:
      bstack11ll1111ll_opy_ = bstack11l1lll1l1_opy_
    bstack11l1lll111_opy_ = os.getenv(bstack111l11_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩ๘")) is not None and len(os.getenv(bstack111l11_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪ๙"))) > 0 and os.getenv(bstack111l11_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫ๚")) != bstack111l11_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬ๛")
    return bstack11ll1111ll_opy_ and bstack11l1lll111_opy_
  except Exception as error:
    logger.debug(bstack111l11_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡷࡧࡵ࡭࡫ࡿࡩ࡯ࡩࠣࡸ࡭࡫ࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡹ࡬ࡸ࡭ࠦࡥࡳࡴࡲࡶࠥࡀࠠࠨ๜") + str(error))
  return False
def bstack1l1111l11_opy_(bstack11l1ll1l1l_opy_, test_tags):
  bstack11l1ll1l1l_opy_ = os.getenv(bstack111l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪ๝"))
  if bstack11l1ll1l1l_opy_ is None:
    return True
  bstack11l1ll1l1l_opy_ = json.loads(bstack11l1ll1l1l_opy_)
  try:
    include_tags = bstack11l1ll1l1l_opy_[bstack111l11_opy_ (u"ࠪ࡭ࡳࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨ๞")] if bstack111l11_opy_ (u"ࠫ࡮ࡴࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩ๟") in bstack11l1ll1l1l_opy_ and isinstance(bstack11l1ll1l1l_opy_[bstack111l11_opy_ (u"ࠬ࡯࡮ࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪ๠")], list) else []
    exclude_tags = bstack11l1ll1l1l_opy_[bstack111l11_opy_ (u"࠭ࡥࡹࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫ๡")] if bstack111l11_opy_ (u"ࠧࡦࡺࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬ๢") in bstack11l1ll1l1l_opy_ and isinstance(bstack11l1ll1l1l_opy_[bstack111l11_opy_ (u"ࠨࡧࡻࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭๣")], list) else []
    excluded = any(tag in exclude_tags for tag in test_tags)
    included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
    return not excluded and included
  except Exception as error:
    logger.debug(bstack111l11_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡷࡣ࡯࡭ࡩࡧࡴࡪࡰࡪࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫ࠠࡧࡱࡵࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡧ࡫ࡦࡰࡴࡨࠤࡸࡩࡡ࡯ࡰ࡬ࡲ࡬࠴ࠠࡆࡴࡵࡳࡷࠦ࠺ࠡࠤ๤") + str(error))
  return False
def bstack1l1lllll1_opy_(config, bstack11ll1111l1_opy_, bstack11ll111111_opy_, bstack11l1lll1ll_opy_):
  bstack11l1ll1111_opy_ = bstack11ll11l1ll_opy_(config)
  bstack11l1lllll1_opy_ = bstack11l1llll11_opy_(config)
  if bstack11l1ll1111_opy_ is None or bstack11l1lllll1_opy_ is None:
    logger.error(bstack111l11_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥࡩࡲࡦࡣࡷ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥࡸࡵ࡯ࠢࡩࡳࡷࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯࠼ࠣࡑ࡮ࡹࡳࡪࡰࡪࠤࡦࡻࡴࡩࡧࡱࡸ࡮ࡩࡡࡵ࡫ࡲࡲࠥࡺ࡯࡬ࡧࡱࠫ๥"))
    return [None, None]
  try:
    settings = json.loads(os.getenv(bstack111l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬ๦"), bstack111l11_opy_ (u"ࠬࢁࡽࠨ๧")))
    data = {
        bstack111l11_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫ๨"): config[bstack111l11_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬ๩")],
        bstack111l11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ๪"): config.get(bstack111l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬ๫"), os.path.basename(os.getcwd())),
        bstack111l11_opy_ (u"ࠪࡷࡹࡧࡲࡵࡖ࡬ࡱࡪ࠭๬"): bstack11ll1l1ll_opy_(),
        bstack111l11_opy_ (u"ࠫࡩ࡫ࡳࡤࡴ࡬ࡴࡹ࡯࡯࡯ࠩ๭"): config.get(bstack111l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡈࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠨ๮"), bstack111l11_opy_ (u"࠭ࠧ๯")),
        bstack111l11_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧ๰"): {
            bstack111l11_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡒࡦࡳࡥࠨ๱"): bstack11ll1111l1_opy_,
            bstack111l11_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯࡛࡫ࡲࡴ࡫ࡲࡲࠬ๲"): bstack11ll111111_opy_,
            bstack111l11_opy_ (u"ࠪࡷࡩࡱࡖࡦࡴࡶ࡭ࡴࡴࠧ๳"): __version__,
            bstack111l11_opy_ (u"ࠫࡱࡧ࡮ࡨࡷࡤ࡫ࡪ࠭๴"): bstack111l11_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬ๵"),
            bstack111l11_opy_ (u"࠭ࡴࡦࡵࡷࡊࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭๶"): bstack111l11_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠩ๷"),
            bstack111l11_opy_ (u"ࠨࡶࡨࡷࡹࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡗࡧࡵࡷ࡮ࡵ࡮ࠨ๸"): bstack11l1lll1ll_opy_
        },
        bstack111l11_opy_ (u"ࠩࡶࡩࡹࡺࡩ࡯ࡩࡶࠫ๹"): settings,
        bstack111l11_opy_ (u"ࠪࡺࡪࡸࡳࡪࡱࡱࡇࡴࡴࡴࡳࡱ࡯ࠫ๺"): bstack11ll11111l_opy_(),
        bstack111l11_opy_ (u"ࠫࡨ࡯ࡉ࡯ࡨࡲࠫ๻"): bstack1l111ll1_opy_(),
        bstack111l11_opy_ (u"ࠬ࡮࡯ࡴࡶࡌࡲ࡫ࡵࠧ๼"): get_host_info(),
        bstack111l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨ๽"): bstack1l11lll11_opy_(config)
    }
    headers = {
        bstack111l11_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪ࠭๾"): bstack111l11_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠫ๿"),
    }
    config = {
        bstack111l11_opy_ (u"ࠩࡤࡹࡹ࡮ࠧ຀"): (bstack11l1ll1111_opy_, bstack11l1lllll1_opy_),
        bstack111l11_opy_ (u"ࠪ࡬ࡪࡧࡤࡦࡴࡶࠫກ"): headers
    }
    response = bstack1lllll1lll_opy_(bstack111l11_opy_ (u"ࠫࡕࡕࡓࡕࠩຂ"), bstack11ll111l11_opy_ + bstack111l11_opy_ (u"ࠬ࠵ࡶ࠳࠱ࡷࡩࡸࡺ࡟ࡳࡷࡱࡷࠬ຃"), data, config)
    bstack11l1ll11l1_opy_ = response.json()
    if bstack11l1ll11l1_opy_[bstack111l11_opy_ (u"࠭ࡳࡶࡥࡦࡩࡸࡹࠧຄ")]:
      parsed = json.loads(os.getenv(bstack111l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨ຅"), bstack111l11_opy_ (u"ࠨࡽࢀࠫຆ")))
      parsed[bstack111l11_opy_ (u"ࠩࡶࡧࡦࡴ࡮ࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪງ")] = bstack11l1ll11l1_opy_[bstack111l11_opy_ (u"ࠪࡨࡦࡺࡡࠨຈ")][bstack111l11_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬຉ")]
      os.environ[bstack111l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭ຊ")] = json.dumps(parsed)
      bstack1l1lll1lll_opy_.bstack11l1ll1l11_opy_(bstack11l1ll11l1_opy_[bstack111l11_opy_ (u"࠭ࡤࡢࡶࡤࠫ຋")][bstack111l11_opy_ (u"ࠧࡴࡥࡵ࡭ࡵࡺࡳࠨຌ")])
      bstack1l1lll1lll_opy_.bstack11l1ll1ll1_opy_(bstack11l1ll11l1_opy_[bstack111l11_opy_ (u"ࠨࡦࡤࡸࡦ࠭ຍ")][bstack111l11_opy_ (u"ࠩࡦࡳࡲࡳࡡ࡯ࡦࡶࠫຎ")])
      bstack1l1lll1lll_opy_.store()
      return bstack11l1ll11l1_opy_[bstack111l11_opy_ (u"ࠪࡨࡦࡺࡡࠨຏ")][bstack111l11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡘࡴࡱࡥ࡯ࠩຐ")], bstack11l1ll11l1_opy_[bstack111l11_opy_ (u"ࠬࡪࡡࡵࡣࠪຑ")][bstack111l11_opy_ (u"࠭ࡩࡥࠩຒ")]
    else:
      logger.error(bstack111l11_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡵࡹࡳࡴࡩ࡯ࡩࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡀࠠࠨຓ") + bstack11l1ll11l1_opy_[bstack111l11_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩດ")])
      if bstack11l1ll11l1_opy_[bstack111l11_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪຕ")] == bstack111l11_opy_ (u"ࠪࡍࡳࡼࡡ࡭࡫ࡧࠤࡨࡵ࡮ࡧ࡫ࡪࡹࡷࡧࡴࡪࡱࡱࠤࡵࡧࡳࡴࡧࡧ࠲ࠬຖ"):
        for bstack11l1ll111l_opy_ in bstack11l1ll11l1_opy_[bstack111l11_opy_ (u"ࠫࡪࡸࡲࡰࡴࡶࠫທ")]:
          logger.error(bstack11l1ll111l_opy_[bstack111l11_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ຘ")])
      return None, None
  except Exception as error:
    logger.error(bstack111l11_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡥࡵࡩࡦࡺࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡴࡸࡲࠥ࡬࡯ࡳࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࠿ࠦࠢນ") +  str(error))
    return None, None
def bstack1l111l1ll_opy_():
  if os.getenv(bstack111l11_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬບ")) is None:
    return {
        bstack111l11_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨປ"): bstack111l11_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨຜ"),
        bstack111l11_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫຝ"): bstack111l11_opy_ (u"ࠫࡇࡻࡩ࡭ࡦࠣࡧࡷ࡫ࡡࡵ࡫ࡲࡲࠥ࡮ࡡࡥࠢࡩࡥ࡮ࡲࡥࡥ࠰ࠪພ")
    }
  data = {bstack111l11_opy_ (u"ࠬ࡫࡮ࡥࡖ࡬ࡱࡪ࠭ຟ"): bstack11ll1l1ll_opy_()}
  headers = {
      bstack111l11_opy_ (u"࠭ࡁࡶࡶ࡫ࡳࡷ࡯ࡺࡢࡶ࡬ࡳࡳ࠭ຠ"): bstack111l11_opy_ (u"ࠧࡃࡧࡤࡶࡪࡸࠠࠨມ") + os.getenv(bstack111l11_opy_ (u"ࠣࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙ࠨຢ")),
      bstack111l11_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡘࡾࡶࡥࠨຣ"): bstack111l11_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭຤")
  }
  response = bstack1lllll1lll_opy_(bstack111l11_opy_ (u"ࠫࡕ࡛ࡔࠨລ"), bstack11ll111l11_opy_ + bstack111l11_opy_ (u"ࠬ࠵ࡴࡦࡵࡷࡣࡷࡻ࡮ࡴ࠱ࡶࡸࡴࡶࠧ຦"), data, { bstack111l11_opy_ (u"࠭ࡨࡦࡣࡧࡩࡷࡹࠧວ"): headers })
  try:
    if response.status_code == 200:
      logger.info(bstack111l11_opy_ (u"ࠢࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡘࡪࡹࡴࠡࡔࡸࡲࠥࡳࡡࡳ࡭ࡨࡨࠥࡧࡳࠡࡥࡲࡱࡵࡲࡥࡵࡧࡧࠤࡦࡺࠠࠣຨ") + bstack1l111llll1_opy_().isoformat() + bstack111l11_opy_ (u"ࠨ࡜ࠪຩ"))
      return {bstack111l11_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩສ"): bstack111l11_opy_ (u"ࠪࡷࡺࡩࡣࡦࡵࡶࠫຫ"), bstack111l11_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬຬ"): bstack111l11_opy_ (u"ࠬ࠭ອ")}
    else:
      response.raise_for_status()
  except requests.RequestException as error:
    logger.error(bstack111l11_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡ࡯ࡤࡶࡰ࡯࡮ࡨࠢࡦࡳࡲࡶ࡬ࡦࡶ࡬ࡳࡳࠦ࡯ࡧࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࡚ࠥࡥࡴࡶࠣࡖࡺࡴ࠺ࠡࠤຮ") + str(error))
    return {
        bstack111l11_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧຯ"): bstack111l11_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧະ"),
        bstack111l11_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪັ"): str(error)
    }
def bstack1llllllll_opy_(caps, options):
  try:
    bstack11l1ll1lll_opy_ = caps.get(bstack111l11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫາ"), {}).get(bstack111l11_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨຳ"), caps.get(bstack111l11_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࠬິ"), bstack111l11_opy_ (u"࠭ࠧີ")))
    if bstack11l1ll1lll_opy_:
      logger.warn(bstack111l11_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡵࡹࡳࠦ࡯࡯࡮ࡼࠤࡴࡴࠠࡅࡧࡶ࡯ࡹࡵࡰࠡࡤࡵࡳࡼࡹࡥࡳࡵ࠱ࠦຶ"))
      return False
    browser = caps.get(bstack111l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ື"), bstack111l11_opy_ (u"ຸࠩࠪ")).lower()
    if browser != bstack111l11_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧູࠪ"):
      logger.warn(bstack111l11_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦࡲࡶࡰࠣࡳࡳࡲࡹࠡࡱࡱࠤࡈ࡮ࡲࡰ࡯ࡨࠤࡧࡸ࡯ࡸࡵࡨࡶࡸ࠴຺ࠢ"))
      return False
    browser_version = caps.get(bstack111l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ົ"), caps.get(bstack111l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨຼ")))
    if browser_version and browser_version != bstack111l11_opy_ (u"ࠧ࡭ࡣࡷࡩࡸࡺࠧຽ") and int(browser_version.split(bstack111l11_opy_ (u"ࠨ࠰ࠪ຾"))[0]) <= 94:
      logger.warn(bstack111l11_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡷࡪ࡮࡯ࠤࡷࡻ࡮ࠡࡱࡱࡰࡾࠦ࡯࡯ࠢࡆ࡬ࡷࡵ࡭ࡦࠢࡥࡶࡴࡽࡳࡦࡴࠣࡺࡪࡸࡳࡪࡱࡱࠤ࡬ࡸࡥࡢࡶࡨࡶࠥࡺࡨࡢࡰࠣ࠽࠹࠴ࠢ຿"))
      return False
    if not options is None:
      bstack11ll111l1l_opy_ = options.to_capabilities().get(bstack111l11_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨເ"), {})
      if bstack111l11_opy_ (u"ࠫ࠲࠳ࡨࡦࡣࡧࡰࡪࡹࡳࠨແ") in bstack11ll111l1l_opy_.get(bstack111l11_opy_ (u"ࠬࡧࡲࡨࡵࠪໂ"), []):
        logger.warn(bstack111l11_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡰࡲࡸࠥࡸࡵ࡯ࠢࡲࡲࠥࡲࡥࡨࡣࡦࡽࠥ࡮ࡥࡢࡦ࡯ࡩࡸࡹࠠ࡮ࡱࡧࡩ࠳ࠦࡓࡸ࡫ࡷࡧ࡭ࠦࡴࡰࠢࡱࡩࡼࠦࡨࡦࡣࡧࡰࡪࡹࡳࠡ࡯ࡲࡨࡪࠦ࡯ࡳࠢࡤࡺࡴ࡯ࡤࠡࡷࡶ࡭ࡳ࡭ࠠࡩࡧࡤࡨࡱ࡫ࡳࡴࠢࡰࡳࡩ࡫࠮ࠣໃ"))
        return False
    return True
  except Exception as error:
    logger.debug(bstack111l11_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡶࡢ࡮࡬ࡨࡦࡺࡥࠡࡣ࠴࠵ࡾࠦࡳࡶࡲࡳࡳࡷࡺࠠ࠻ࠤໄ") + str(error))
    return False
def set_capabilities(caps, config):
  try:
    bstack11l1llll1l_opy_ = config.get(bstack111l11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨ໅"), {})
    bstack11l1llll1l_opy_[bstack111l11_opy_ (u"ࠩࡤࡹࡹ࡮ࡔࡰ࡭ࡨࡲࠬໆ")] = os.getenv(bstack111l11_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨ໇"))
    bstack11ll11l111_opy_ = json.loads(os.getenv(bstack111l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐ່ࠬ"), bstack111l11_opy_ (u"ࠬࢁࡽࠨ້"))).get(bstack111l11_opy_ (u"࠭ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴ໊ࠧ"))
    caps[bstack111l11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ໋ࠧ")] = True
    if bstack111l11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩ໌") in caps:
      caps[bstack111l11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪໍ")][bstack111l11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪ໎")] = bstack11l1llll1l_opy_
      caps[bstack111l11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬ໏")][bstack111l11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬ໐")][bstack111l11_opy_ (u"࠭ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧ໑")] = bstack11ll11l111_opy_
    else:
      caps[bstack111l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭໒")] = bstack11l1llll1l_opy_
      caps[bstack111l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧ໓")][bstack111l11_opy_ (u"ࠩࡶࡧࡦࡴ࡮ࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪ໔")] = bstack11ll11l111_opy_
  except Exception as error:
    logger.debug(bstack111l11_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴ࠰ࠣࡉࡷࡸ࡯ࡳ࠼ࠣࠦ໕") +  str(error))
def bstack1llll1l111_opy_(driver, bstack11ll111ll1_opy_):
  try:
    setattr(driver, bstack111l11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡅ࠶࠷ࡹࡔࡪࡲࡹࡱࡪࡓࡤࡣࡱࠫ໖"), True)
    session = driver.session_id
    if session:
      bstack11l1lll11l_opy_ = True
      current_url = driver.current_url
      try:
        url = urlparse(current_url)
      except Exception as e:
        bstack11l1lll11l_opy_ = False
      bstack11l1lll11l_opy_ = url.scheme in [bstack111l11_opy_ (u"ࠧ࡮ࡴࡵࡲࠥ໗"), bstack111l11_opy_ (u"ࠨࡨࡵࡶࡳࡷࠧ໘")]
      if bstack11l1lll11l_opy_:
        if bstack11ll111ll1_opy_:
          logger.info(bstack111l11_opy_ (u"ࠢࡔࡧࡷࡹࡵࠦࡦࡰࡴࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡸࡪࡹࡴࡪࡰࡪࠤ࡭ࡧࡳࠡࡵࡷࡥࡷࡺࡥࡥ࠰ࠣࡅࡺࡺ࡯࡮ࡣࡷࡩࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥࠡࡧࡻࡩࡨࡻࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡥࡩ࡬࡯࡮ࠡ࡯ࡲࡱࡪࡴࡴࡢࡴ࡬ࡰࡾ࠴ࠢ໙"))
      return bstack11ll111ll1_opy_
  except Exception as e:
    logger.error(bstack111l11_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡴࡶࡤࡶࡹ࡯࡮ࡨࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡳࡤࡣࡱࠤ࡫ࡵࡲࠡࡶ࡫࡭ࡸࠦࡴࡦࡵࡷࠤࡨࡧࡳࡦ࠼ࠣࠦ໚") + str(e))
    return False
def bstack1ll111l1l1_opy_(driver, class_name, name, module_name, path, bstack1ll1l1ll1_opy_):
  try:
    bstack11ll1l111l_opy_ = [class_name] if not class_name is None else []
    bstack11l1ll11ll_opy_ = {
        bstack111l11_opy_ (u"ࠤࡶࡥࡻ࡫ࡒࡦࡵࡸࡰࡹࡹࠢ໛"): True,
        bstack111l11_opy_ (u"ࠥࡸࡪࡹࡴࡅࡧࡷࡥ࡮ࡲࡳࠣໜ"): {
            bstack111l11_opy_ (u"ࠦࡳࡧ࡭ࡦࠤໝ"): name,
            bstack111l11_opy_ (u"ࠧࡺࡥࡴࡶࡕࡹࡳࡏࡤࠣໞ"): os.environ.get(bstack111l11_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡕࡇࡖࡘࡤࡘࡕࡏࡡࡌࡈࠬໟ")),
            bstack111l11_opy_ (u"ࠢࡧ࡫࡯ࡩࡕࡧࡴࡩࠤ໠"): str(path),
            bstack111l11_opy_ (u"ࠣࡵࡦࡳࡵ࡫ࡌࡪࡵࡷࠦ໡"): [module_name, *bstack11ll1l111l_opy_, name],
        },
        bstack111l11_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࠦ໢"): _11l1llllll_opy_(driver, bstack1ll1l1ll1_opy_)
    }
    logger.debug(bstack111l11_opy_ (u"ࠪࡔࡪࡸࡦࡰࡴࡰ࡭ࡳ࡭ࠠࡴࡥࡤࡲࠥࡨࡥࡧࡱࡵࡩࠥࡹࡡࡷ࡫ࡱ࡫ࠥࡸࡥࡴࡷ࡯ࡸࡸ࠭໣"))
    logger.debug(driver.execute_async_script(bstack1l1lll1lll_opy_.perform_scan, {bstack111l11_opy_ (u"ࠦࡲ࡫ࡴࡩࡱࡧࠦ໤"): name}))
    logger.debug(driver.execute_async_script(bstack1l1lll1lll_opy_.bstack11ll11l1l1_opy_, bstack11l1ll11ll_opy_))
    logger.info(bstack111l11_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡺࡥࡴࡶ࡬ࡲ࡬ࠦࡦࡰࡴࠣࡸ࡭࡯ࡳࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨࠤ࡭ࡧࡳࠡࡧࡱࡨࡪࡪ࠮ࠣ໥"))
  except Exception as bstack11ll111lll_opy_:
    logger.error(bstack111l11_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡲࡦࡵࡸࡰࡹࡹࠠࡤࡱࡸࡰࡩࠦ࡮ࡰࡶࠣࡦࡪࠦࡰࡳࡱࡦࡩࡸࡹࡥࡥࠢࡩࡳࡷࠦࡴࡩࡧࠣࡸࡪࡹࡴࠡࡥࡤࡷࡪࡀࠠࠣ໦") + str(path) + bstack111l11_opy_ (u"ࠢࠡࡇࡵࡶࡴࡸࠠ࠻ࠤ໧") + str(bstack11ll111lll_opy_))
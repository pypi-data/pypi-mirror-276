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
import json
import os
import threading
from bstack_utils.config import Config
from bstack_utils.helper import bstack111l1ll1ll_opy_, bstack1lll11ll1l_opy_, bstack1ll111l1ll_opy_, bstack1l1ll1lll1_opy_, \
    bstack111lll11ll_opy_
def bstack1ll11l1111_opy_(bstack1llll111111_opy_):
    for driver in bstack1llll111111_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1l1l11llll_opy_(driver, status, reason=bstack111l11_opy_ (u"ࠪࠫᒡ")):
    bstack1l11l111ll_opy_ = Config.bstack1l1l1l1111_opy_()
    if bstack1l11l111ll_opy_.bstack11ll1l11l1_opy_():
        return
    bstack1l11l11ll_opy_ = bstack1l11l1l111_opy_(bstack111l11_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠧᒢ"), bstack111l11_opy_ (u"ࠬ࠭ᒣ"), status, reason, bstack111l11_opy_ (u"࠭ࠧᒤ"), bstack111l11_opy_ (u"ࠧࠨᒥ"))
    driver.execute_script(bstack1l11l11ll_opy_)
def bstack111111l1_opy_(page, status, reason=bstack111l11_opy_ (u"ࠨࠩᒦ")):
    try:
        if page is None:
            return
        bstack1l11l111ll_opy_ = Config.bstack1l1l1l1111_opy_()
        if bstack1l11l111ll_opy_.bstack11ll1l11l1_opy_():
            return
        bstack1l11l11ll_opy_ = bstack1l11l1l111_opy_(bstack111l11_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠬᒧ"), bstack111l11_opy_ (u"ࠪࠫᒨ"), status, reason, bstack111l11_opy_ (u"ࠫࠬᒩ"), bstack111l11_opy_ (u"ࠬ࠭ᒪ"))
        page.evaluate(bstack111l11_opy_ (u"ࠨ࡟ࠡ࠿ࡁࠤࢀࢃࠢᒫ"), bstack1l11l11ll_opy_)
    except Exception as e:
        print(bstack111l11_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡵࡷࡥࡹࡻࡳࠡࡨࡲࡶࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡾࢁࠧᒬ"), e)
def bstack1l11l1l111_opy_(type, name, status, reason, bstack1l11l1ll1l_opy_, bstack1lllll11_opy_):
    bstack11l1l1lll_opy_ = {
        bstack111l11_opy_ (u"ࠨࡣࡦࡸ࡮ࡵ࡮ࠨᒭ"): type,
        bstack111l11_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬᒮ"): {}
    }
    if type == bstack111l11_opy_ (u"ࠪࡥࡳࡴ࡯ࡵࡣࡷࡩࠬᒯ"):
        bstack11l1l1lll_opy_[bstack111l11_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧᒰ")][bstack111l11_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫᒱ")] = bstack1l11l1ll1l_opy_
        bstack11l1l1lll_opy_[bstack111l11_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩᒲ")][bstack111l11_opy_ (u"ࠧࡥࡣࡷࡥࠬᒳ")] = json.dumps(str(bstack1lllll11_opy_))
    if type == bstack111l11_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩᒴ"):
        bstack11l1l1lll_opy_[bstack111l11_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬᒵ")][bstack111l11_opy_ (u"ࠪࡲࡦࡳࡥࠨᒶ")] = name
    if type == bstack111l11_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠧᒷ"):
        bstack11l1l1lll_opy_[bstack111l11_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨᒸ")][bstack111l11_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ᒹ")] = status
        if status == bstack111l11_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᒺ") and str(reason) != bstack111l11_opy_ (u"ࠣࠤᒻ"):
            bstack11l1l1lll_opy_[bstack111l11_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬᒼ")][bstack111l11_opy_ (u"ࠪࡶࡪࡧࡳࡰࡰࠪᒽ")] = json.dumps(str(reason))
    bstack111l1lll_opy_ = bstack111l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠩᒾ").format(json.dumps(bstack11l1l1lll_opy_))
    return bstack111l1lll_opy_
def bstack11l111ll1_opy_(url, config, logger, bstack111l111l1_opy_=False):
    hostname = bstack1lll11ll1l_opy_(url)
    is_private = bstack1l1ll1lll1_opy_(hostname)
    try:
        if is_private or bstack111l111l1_opy_:
            file_path = bstack111l1ll1ll_opy_(bstack111l11_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬᒿ"), bstack111l11_opy_ (u"࠭࠮ࡣࡵࡷࡥࡨࡱ࠭ࡤࡱࡱࡪ࡮࡭࠮࡫ࡵࡲࡲࠬᓀ"), logger)
            if os.environ.get(bstack111l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࡤࡔࡏࡕࡡࡖࡉ࡙ࡥࡅࡓࡔࡒࡖࠬᓁ")) and eval(
                    os.environ.get(bstack111l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡍࡑࡆࡅࡑࡥࡎࡐࡖࡢࡗࡊ࡚࡟ࡆࡔࡕࡓࡗ࠭ᓂ"))):
                return
            if (bstack111l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ᓃ") in config and not config[bstack111l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧᓄ")]):
                os.environ[bstack111l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡉࡁࡍࡡࡑࡓ࡙ࡥࡓࡆࡖࡢࡉࡗࡘࡏࡓࠩᓅ")] = str(True)
                bstack1llll11111l_opy_ = {bstack111l11_opy_ (u"ࠬ࡮࡯ࡴࡶࡱࡥࡲ࡫ࠧᓆ"): hostname}
                bstack111lll11ll_opy_(bstack111l11_opy_ (u"࠭࠮ࡣࡵࡷࡥࡨࡱ࠭ࡤࡱࡱࡪ࡮࡭࠮࡫ࡵࡲࡲࠬᓇ"), bstack111l11_opy_ (u"ࠧ࡯ࡷࡧ࡫ࡪࡥ࡬ࡰࡥࡤࡰࠬᓈ"), bstack1llll11111l_opy_, logger)
    except Exception as e:
        pass
def bstack111llll1l_opy_(caps, bstack1llll1111l1_opy_):
    if bstack111l11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩᓉ") in caps:
        caps[bstack111l11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪᓊ")][bstack111l11_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࠩᓋ")] = True
        if bstack1llll1111l1_opy_:
            caps[bstack111l11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬᓌ")][bstack111l11_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧᓍ")] = bstack1llll1111l1_opy_
    else:
        caps[bstack111l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡲ࡯ࡤࡣ࡯ࠫᓎ")] = True
        if bstack1llll1111l1_opy_:
            caps[bstack111l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨᓏ")] = bstack1llll1111l1_opy_
def bstack1llll1ll1l1_opy_(bstack1l111ll1ll_opy_):
    bstack1lll1llllll_opy_ = bstack1ll111l1ll_opy_(threading.current_thread(), bstack111l11_opy_ (u"ࠨࡶࡨࡷࡹ࡙ࡴࡢࡶࡸࡷࠬᓐ"), bstack111l11_opy_ (u"ࠩࠪᓑ"))
    if bstack1lll1llllll_opy_ == bstack111l11_opy_ (u"ࠪࠫᓒ") or bstack1lll1llllll_opy_ == bstack111l11_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬᓓ"):
        threading.current_thread().testStatus = bstack1l111ll1ll_opy_
    else:
        if bstack1l111ll1ll_opy_ == bstack111l11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᓔ"):
            threading.current_thread().testStatus = bstack1l111ll1ll_opy_
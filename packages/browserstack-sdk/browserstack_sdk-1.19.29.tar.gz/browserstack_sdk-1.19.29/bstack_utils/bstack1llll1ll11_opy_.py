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
import re
from bstack_utils.bstack1ll11ll111_opy_ import bstack1llll1ll1l1_opy_
def bstack1llll1l1ll1_opy_(fixture_name):
    if fixture_name.startswith(bstack111l11_opy_ (u"࠭࡟ࡹࡷࡱ࡭ࡹࡥࡳࡦࡶࡸࡴࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᑬ")):
        return bstack111l11_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠳ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨᑭ")
    elif fixture_name.startswith(bstack111l11_opy_ (u"ࠨࡡࡻࡹࡳ࡯ࡴࡠࡵࡨࡸࡺࡶ࡟࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᑮ")):
        return bstack111l11_opy_ (u"ࠩࡶࡩࡹࡻࡰ࠮࡯ࡲࡨࡺࡲࡥࠨᑯ")
    elif fixture_name.startswith(bstack111l11_opy_ (u"ࠪࡣࡽࡻ࡮ࡪࡶࡢࡸࡪࡧࡲࡥࡱࡺࡲࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᑰ")):
        return bstack111l11_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠳ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨᑱ")
    elif fixture_name.startswith(bstack111l11_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᑲ")):
        return bstack111l11_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮࠮࡯ࡲࡨࡺࡲࡥࠨᑳ")
def bstack1llll1lll11_opy_(fixture_name):
    return bool(re.match(bstack111l11_opy_ (u"ࠧ࡟ࡡࡻࡹࡳ࡯ࡴࡠࠪࡶࡩࡹࡻࡰࡽࡶࡨࡥࡷࡪ࡯ࡸࡰࠬࡣ࠭࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࡼ࡮ࡱࡧࡹࡱ࡫ࠩࡠࡨ࡬ࡼࡹࡻࡲࡦࡡ࠱࠮ࠬᑴ"), fixture_name))
def bstack1llll1l1lll_opy_(fixture_name):
    return bool(re.match(bstack111l11_opy_ (u"ࠨࡠࡢࡼࡺࡴࡩࡵࡡࠫࡷࡪࡺࡵࡱࡾࡷࡩࡦࡸࡤࡰࡹࡱ࠭ࡤࡳ࡯ࡥࡷ࡯ࡩࡤ࡬ࡩࡹࡶࡸࡶࡪࡥ࠮ࠫࠩᑵ"), fixture_name))
def bstack1lllll11111_opy_(fixture_name):
    return bool(re.match(bstack111l11_opy_ (u"ࠩࡡࡣࡽࡻ࡮ࡪࡶࡢࠬࡸ࡫ࡴࡶࡲࡿࡸࡪࡧࡲࡥࡱࡺࡲ࠮ࡥࡣ࡭ࡣࡶࡷࡤ࡬ࡩࡹࡶࡸࡶࡪࡥ࠮ࠫࠩᑶ"), fixture_name))
def bstack1llll1l1l1l_opy_(fixture_name):
    if fixture_name.startswith(bstack111l11_opy_ (u"ࠪࡣࡽࡻ࡮ࡪࡶࡢࡷࡪࡺࡵࡱࡡࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᑷ")):
        return bstack111l11_opy_ (u"ࠫࡸ࡫ࡴࡶࡲ࠰ࡪࡺࡴࡣࡵ࡫ࡲࡲࠬᑸ"), bstack111l11_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡋࡁࡄࡊࠪᑹ")
    elif fixture_name.startswith(bstack111l11_opy_ (u"࠭࡟ࡹࡷࡱ࡭ࡹࡥࡳࡦࡶࡸࡴࡤࡳ࡯ࡥࡷ࡯ࡩࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᑺ")):
        return bstack111l11_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠳࡭ࡰࡦࡸࡰࡪ࠭ᑻ"), bstack111l11_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡃࡏࡐࠬᑼ")
    elif fixture_name.startswith(bstack111l11_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡷࡩࡦࡸࡤࡰࡹࡱࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᑽ")):
        return bstack111l11_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲ࠲࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧᑾ"), bstack111l11_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡉࡆࡉࡈࠨᑿ")
    elif fixture_name.startswith(bstack111l11_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᒀ")):
        return bstack111l11_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮࠮࡯ࡲࡨࡺࡲࡥࠨᒁ"), bstack111l11_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡁࡍࡎࠪᒂ")
    return None, None
def bstack1llll1l1l11_opy_(hook_name):
    if hook_name in [bstack111l11_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧᒃ"), bstack111l11_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫᒄ")]:
        return hook_name.capitalize()
    return hook_name
def bstack1llll1ll11l_opy_(hook_name):
    if hook_name in [bstack111l11_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡩࡹࡳࡩࡴࡪࡱࡱࠫᒅ"), bstack111l11_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡱࡪࡺࡨࡰࡦࠪᒆ")]:
        return bstack111l11_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡋࡁࡄࡊࠪᒇ")
    elif hook_name in [bstack111l11_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡳ࡯ࡥࡷ࡯ࡩࠬᒈ"), bstack111l11_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥࡣ࡭ࡣࡶࡷࠬᒉ")]:
        return bstack111l11_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡃࡏࡐࠬᒊ")
    elif hook_name in [bstack111l11_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠭ᒋ"), bstack111l11_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳࡥࡵࡪࡲࡨࠬᒌ")]:
        return bstack111l11_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡉࡆࡉࡈࠨᒍ")
    elif hook_name in [bstack111l11_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡱࡧࡹࡱ࡫ࠧᒎ"), bstack111l11_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡥ࡯ࡥࡸࡹࠧᒏ")]:
        return bstack111l11_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡁࡍࡎࠪᒐ")
    return hook_name
def bstack1llll1l11ll_opy_(node, scenario):
    if hasattr(node, bstack111l11_opy_ (u"ࠨࡥࡤࡰࡱࡹࡰࡦࡥࠪᒑ")):
        parts = node.nodeid.rsplit(bstack111l11_opy_ (u"ࠤ࡞ࠦᒒ"))
        params = parts[-1]
        return bstack111l11_opy_ (u"ࠥࡿࢂ࡛ࠦࡼࡿࠥᒓ").format(scenario.name, params)
    return scenario.name
def bstack1llll1ll111_opy_(node):
    try:
        examples = []
        if hasattr(node, bstack111l11_opy_ (u"ࠫࡨࡧ࡬࡭ࡵࡳࡩࡨ࠭ᒔ")):
            examples = list(node.callspec.params[bstack111l11_opy_ (u"ࠬࡥࡰࡺࡶࡨࡷࡹࡥࡢࡥࡦࡢࡩࡽࡧ࡭ࡱ࡮ࡨࠫᒕ")].values())
        return examples
    except:
        return []
def bstack1llll1llll1_opy_(feature, scenario):
    return list(feature.tags) + list(scenario.tags)
def bstack1llll1lllll_opy_(report):
    try:
        status = bstack111l11_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᒖ")
        if report.passed or (report.failed and hasattr(report, bstack111l11_opy_ (u"ࠢࡸࡣࡶࡼ࡫ࡧࡩ࡭ࠤᒗ"))):
            status = bstack111l11_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨᒘ")
        elif report.skipped:
            status = bstack111l11_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪᒙ")
        bstack1llll1ll1l1_opy_(status)
    except:
        pass
def bstack1l1l11ll11_opy_(status):
    try:
        bstack1llll1lll1l_opy_ = bstack111l11_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᒚ")
        if status == bstack111l11_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫᒛ"):
            bstack1llll1lll1l_opy_ = bstack111l11_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬᒜ")
        elif status == bstack111l11_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧᒝ"):
            bstack1llll1lll1l_opy_ = bstack111l11_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨᒞ")
        bstack1llll1ll1l1_opy_(bstack1llll1lll1l_opy_)
    except:
        pass
def bstack1llll1ll1ll_opy_(item=None, report=None, summary=None, extra=None):
    return
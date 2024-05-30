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
import logging
logger = logging.getLogger(__name__)
class BrowserStackSdk:
    def get_current_platform():
        bstack11l1ll111_opy_ = {}
        bstack1l11l111l1_opy_ = os.environ.get(bstack111l11_opy_ (u"ࠫࡈ࡛ࡒࡓࡇࡑࡘࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡅࡃࡗࡅࠬല"), bstack111l11_opy_ (u"ࠬ࠭ള"))
        if not bstack1l11l111l1_opy_:
            return bstack11l1ll111_opy_
        try:
            bstack1l11l1111l_opy_ = json.loads(bstack1l11l111l1_opy_)
            if bstack111l11_opy_ (u"ࠨ࡯ࡴࠤഴ") in bstack1l11l1111l_opy_:
                bstack11l1ll111_opy_[bstack111l11_opy_ (u"ࠢࡰࡵࠥവ")] = bstack1l11l1111l_opy_[bstack111l11_opy_ (u"ࠣࡱࡶࠦശ")]
            if bstack111l11_opy_ (u"ࠤࡲࡷࡤࡼࡥࡳࡵ࡬ࡳࡳࠨഷ") in bstack1l11l1111l_opy_ or bstack111l11_opy_ (u"ࠥࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳࠨസ") in bstack1l11l1111l_opy_:
                bstack11l1ll111_opy_[bstack111l11_opy_ (u"ࠦࡴࡹࡖࡦࡴࡶ࡭ࡴࡴࠢഹ")] = bstack1l11l1111l_opy_.get(bstack111l11_opy_ (u"ࠧࡵࡳࡠࡸࡨࡶࡸ࡯࡯࡯ࠤഺ"), bstack1l11l1111l_opy_.get(bstack111l11_opy_ (u"ࠨ࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠤ഻")))
            if bstack111l11_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲ഼ࠣ") in bstack1l11l1111l_opy_ or bstack111l11_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪࠨഽ") in bstack1l11l1111l_opy_:
                bstack11l1ll111_opy_[bstack111l11_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠢാ")] = bstack1l11l1111l_opy_.get(bstack111l11_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࠦി"), bstack1l11l1111l_opy_.get(bstack111l11_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠤീ")))
            if bstack111l11_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠢു") in bstack1l11l1111l_opy_ or bstack111l11_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠢൂ") in bstack1l11l1111l_opy_:
                bstack11l1ll111_opy_[bstack111l11_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠣൃ")] = bstack1l11l1111l_opy_.get(bstack111l11_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠥൄ"), bstack1l11l1111l_opy_.get(bstack111l11_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠥ൅")))
            if bstack111l11_opy_ (u"ࠥࡨࡪࡼࡩࡤࡧࠥെ") in bstack1l11l1111l_opy_ or bstack111l11_opy_ (u"ࠦࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠣേ") in bstack1l11l1111l_opy_:
                bstack11l1ll111_opy_[bstack111l11_opy_ (u"ࠧࡪࡥࡷ࡫ࡦࡩࡓࡧ࡭ࡦࠤൈ")] = bstack1l11l1111l_opy_.get(bstack111l11_opy_ (u"ࠨࡤࡦࡸ࡬ࡧࡪࠨ൉"), bstack1l11l1111l_opy_.get(bstack111l11_opy_ (u"ࠢࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠦൊ")))
            if bstack111l11_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠥോ") in bstack1l11l1111l_opy_ or bstack111l11_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠣൌ") in bstack1l11l1111l_opy_:
                bstack11l1ll111_opy_[bstack111l11_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠤ്")] = bstack1l11l1111l_opy_.get(bstack111l11_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࠨൎ"), bstack1l11l1111l_opy_.get(bstack111l11_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࡎࡢ࡯ࡨࠦ൏")))
            if bstack111l11_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠࡸࡨࡶࡸ࡯࡯࡯ࠤ൐") in bstack1l11l1111l_opy_ or bstack111l11_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠤ൑") in bstack1l11l1111l_opy_:
                bstack11l1ll111_opy_[bstack111l11_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠥ൒")] = bstack1l11l1111l_opy_.get(bstack111l11_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠧ൓"), bstack1l11l1111l_opy_.get(bstack111l11_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠧൔ")))
            if bstack111l11_opy_ (u"ࠦࡨࡻࡳࡵࡱࡰ࡚ࡦࡸࡩࡢࡤ࡯ࡩࡸࠨൕ") in bstack1l11l1111l_opy_:
                bstack11l1ll111_opy_[bstack111l11_opy_ (u"ࠧࡩࡵࡴࡶࡲࡱ࡛ࡧࡲࡪࡣࡥࡰࡪࡹࠢൖ")] = bstack1l11l1111l_opy_[bstack111l11_opy_ (u"ࠨࡣࡶࡵࡷࡳࡲ࡜ࡡࡳ࡫ࡤࡦࡱ࡫ࡳࠣൗ")]
        except Exception as error:
            logger.error(bstack111l11_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡪࡩࡹࡺࡩ࡯ࡩࠣࡧࡺࡸࡲࡦࡰࡷࠤࡵࡲࡡࡵࡨࡲࡶࡲࠦࡤࡢࡶࡤ࠾ࠥࠨ൘") +  str(error))
        return bstack11l1ll111_opy_
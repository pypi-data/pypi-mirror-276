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
import datetime
import json
import logging
import os
import threading
from bstack_utils.helper import bstack11ll11111l_opy_, bstack1l111ll1_opy_, get_host_info, bstack11ll11l1ll_opy_, bstack11l1llll11_opy_, bstack11l11l1111_opy_, bstack1l111llll1_opy_, \
    bstack111l1llll1_opy_, bstack111l1l1lll_opy_, bstack1lllll1lll_opy_, bstack111ll11111_opy_, bstack1ll11l1l11_opy_, bstack1l1111ll11_opy_, bstack111l1l1ll_opy_, bstack11ll1l1ll_opy_
from bstack_utils.bstack1llll11l1l1_opy_ import bstack1llll11ll11_opy_
from bstack_utils.bstack1l111l1ll1_opy_ import bstack1l111l111l_opy_
import bstack_utils.bstack1111llll_opy_ as bstack1llll11l_opy_
from bstack_utils.constants import bstack11l11lll11_opy_
bstack1lll11lllll_opy_ = [
    bstack111l11_opy_ (u"ࠬࡒ࡯ࡨࡅࡵࡩࡦࡺࡥࡥࠩᔓ"), bstack111l11_opy_ (u"࠭ࡃࡃࡖࡖࡩࡸࡹࡩࡰࡰࡆࡶࡪࡧࡴࡦࡦࠪᔔ"), bstack111l11_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩᔕ"), bstack111l11_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕ࡮࡭ࡵࡶࡥࡥࠩᔖ"),
    bstack111l11_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫᔗ"), bstack111l11_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫᔘ"), bstack111l11_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬᔙ")
]
bstack1lll1l1111l_opy_ = bstack111l11_opy_ (u"ࠬ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡣࡰ࡮࡯ࡩࡨࡺ࡯ࡳ࠯ࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱࠬᔚ")
logger = logging.getLogger(__name__)
class bstack1lll1ll1l_opy_:
    bstack1llll11l1l1_opy_ = None
    bs_config = None
    @classmethod
    @bstack1l1111ll11_opy_(class_method=True)
    def launch(cls, bs_config, bstack1lll1l11l1l_opy_):
        cls.bs_config = bs_config
        cls.bstack1lll11ll1l1_opy_()
        bstack11l1ll1111_opy_ = bstack11ll11l1ll_opy_(bs_config)
        bstack11l1lllll1_opy_ = bstack11l1llll11_opy_(bs_config)
        bstack1ll111lll_opy_ = False
        bstack111l11l11_opy_ = False
        if bstack111l11_opy_ (u"࠭ࡡࡱࡲࠪᔛ") in bs_config:
            bstack1ll111lll_opy_ = True
        else:
            bstack111l11l11_opy_ = True
        bstack1l11111l_opy_ = {
            bstack111l11_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧᔜ"): cls.bstack1llllll1l_opy_(bstack1lll1l11l1l_opy_.get(bstack111l11_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡺࡹࡥࡥࠩᔝ"), bstack111l11_opy_ (u"ࠩࠪᔞ"))),
            bstack111l11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᔟ"): bstack1llll11l_opy_.bstack1l1l1l11l_opy_(bs_config),
            bstack111l11_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪᔠ"): bs_config.get(bstack111l11_opy_ (u"ࠬࡶࡥࡳࡥࡼࠫᔡ"), False),
            bstack111l11_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡥࠨᔢ"): bstack111l11l11_opy_,
            bstack111l11_opy_ (u"ࠧࡢࡲࡳࡣࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭ᔣ"): bstack1ll111lll_opy_
        }
        data = {
            bstack111l11_opy_ (u"ࠨࡨࡲࡶࡲࡧࡴࠨᔤ"): bstack111l11_opy_ (u"ࠩ࡭ࡷࡴࡴࠧᔥ"),
            bstack111l11_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡣࡳࡧ࡭ࡦࠩᔦ"): bs_config.get(bstack111l11_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠩᔧ"), bstack111l11_opy_ (u"ࠬ࠭ᔨ")),
            bstack111l11_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᔩ"): bs_config.get(bstack111l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪᔪ"), os.path.basename(os.path.abspath(os.getcwd()))),
            bstack111l11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡪࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫᔫ"): bs_config.get(bstack111l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫᔬ")),
            bstack111l11_opy_ (u"ࠪࡨࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠨᔭ"): bs_config.get(bstack111l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡇࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴࠧᔮ"), bstack111l11_opy_ (u"ࠬ࠭ᔯ")),
            bstack111l11_opy_ (u"࠭ࡳࡵࡣࡵࡸࡤࡺࡩ࡮ࡧࠪᔰ"): datetime.datetime.now().isoformat(),
            bstack111l11_opy_ (u"ࠧࡵࡣࡪࡷࠬᔱ"): bstack11l11l1111_opy_(bs_config),
            bstack111l11_opy_ (u"ࠨࡪࡲࡷࡹࡥࡩ࡯ࡨࡲࠫᔲ"): get_host_info(),
            bstack111l11_opy_ (u"ࠩࡦ࡭ࡤ࡯࡮ࡧࡱࠪᔳ"): bstack1l111ll1_opy_(),
            bstack111l11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡࡵࡹࡳࡥࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪᔴ"): os.environ.get(bstack111l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡆ࡚ࡏࡌࡅࡡࡕ࡙ࡓࡥࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔࠪᔵ")),
            bstack111l11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࡤࡺࡥࡴࡶࡶࡣࡷ࡫ࡲࡶࡰࠪᔶ"): os.environ.get(bstack111l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡘࡅࡓࡗࡑࠫᔷ"), False),
            bstack111l11_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࡠࡥࡲࡲࡹࡸ࡯࡭ࠩᔸ"): bstack11ll11111l_opy_(),
            bstack111l11_opy_ (u"ࠨࡲࡵࡳࡩࡻࡣࡵࡡࡰࡥࡵ࠭ᔹ"): bstack1l11111l_opy_,
            bstack111l11_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࡡࡹࡩࡷࡹࡩࡰࡰࠪᔺ"): {
                bstack111l11_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡔࡡ࡮ࡧࠪᔻ"): bstack1lll1l11l1l_opy_.get(bstack111l11_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࠬᔼ"), bstack111l11_opy_ (u"ࠬࡖࡹࡵࡧࡶࡸࠬᔽ")),
                bstack111l11_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡘࡨࡶࡸ࡯࡯࡯ࠩᔾ"): bstack1lll1l11l1l_opy_.get(bstack111l11_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࠫᔿ")),
                bstack111l11_opy_ (u"ࠨࡵࡧ࡯࡛࡫ࡲࡴ࡫ࡲࡲࠬᕀ"): bstack1lll1l11l1l_opy_.get(bstack111l11_opy_ (u"ࠩࡶࡨࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠧᕁ"))
            }
        }
        config = {
            bstack111l11_opy_ (u"ࠪࡥࡺࡺࡨࠨᕂ"): (bstack11l1ll1111_opy_, bstack11l1lllll1_opy_),
            bstack111l11_opy_ (u"ࠫ࡭࡫ࡡࡥࡧࡵࡷࠬᕃ"): cls.default_headers()
        }
        response = bstack1lllll1lll_opy_(bstack111l11_opy_ (u"ࠬࡖࡏࡔࡖࠪᕄ"), cls.request_url(bstack111l11_opy_ (u"࠭ࡡࡱ࡫࠲ࡺ࠶࠵ࡢࡶ࡫࡯ࡨࡸ࠭ᕅ")), data, config)
        if response.status_code != 200:
            os.environ[bstack111l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬᕆ")] = bstack111l11_opy_ (u"ࠨࡰࡸࡰࡱ࠭ᕇ")
            os.environ[bstack111l11_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡂࡖࡋࡏࡈࡤࡉࡏࡎࡒࡏࡉ࡙ࡋࡄࠨᕈ")] = bstack111l11_opy_ (u"ࠪࡪࡦࡲࡳࡦࠩᕉ")
            os.environ[bstack111l11_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡌ࡚ࡘࠬᕊ")] = bstack111l11_opy_ (u"ࠬࡴࡵ࡭࡮ࠪᕋ")
            os.environ[bstack111l11_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡆ࡚ࡏࡌࡅࡡࡋࡅࡘࡎࡅࡅࡡࡌࡈࠬᕌ")] = bstack111l11_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧᕍ")
            os.environ[bstack111l11_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡇࡌࡍࡑ࡚ࡣࡘࡉࡒࡆࡇࡑࡗࡍࡕࡔࡔࠩᕎ")] = bstack111l11_opy_ (u"ࠤࡱࡹࡱࡲࠢᕏ")
            bstack1lll11ll1ll_opy_ = response.json()
            if bstack1lll11ll1ll_opy_ and bstack1lll11ll1ll_opy_[bstack111l11_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᕐ")]:
                error_message = bstack1lll11ll1ll_opy_[bstack111l11_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᕑ")]
                if bstack1lll11ll1ll_opy_[bstack111l11_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࡘࡾࡶࡥࠨᕒ")] == bstack111l11_opy_ (u"࠭ࡅࡓࡔࡒࡖࡤࡏࡎࡗࡃࡏࡍࡉࡥࡃࡓࡇࡇࡉࡓ࡚ࡉࡂࡎࡖࠫᕓ"):
                    logger.error(error_message)
                elif bstack1lll11ll1ll_opy_[bstack111l11_opy_ (u"ࠧࡦࡴࡵࡳࡷ࡚ࡹࡱࡧࠪᕔ")] == bstack111l11_opy_ (u"ࠨࡇࡕࡖࡔࡘ࡟ࡂࡅࡆࡉࡘ࡙࡟ࡅࡇࡑࡍࡊࡊࠧᕕ"):
                    logger.info(error_message)
                elif bstack1lll11ll1ll_opy_[bstack111l11_opy_ (u"ࠩࡨࡶࡷࡵࡲࡕࡻࡳࡩࠬᕖ")] == bstack111l11_opy_ (u"ࠪࡉࡗࡘࡏࡓࡡࡖࡈࡐࡥࡄࡆࡒࡕࡉࡈࡇࡔࡆࡆࠪᕗ"):
                    logger.error(error_message)
                else:
                    logger.error(error_message)
            else:
                logger.error(bstack111l11_opy_ (u"ࠦࡉࡧࡴࡢࠢࡸࡴࡱࡵࡡࡥࠢࡷࡳࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤ࡙࡫ࡳࡵࠢࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠢࡩࡥ࡮ࡲࡥࡥࠢࡧࡹࡪࠦࡴࡰࠢࡶࡳࡲ࡫ࠠࡦࡴࡵࡳࡷࠨᕘ"))
            return [None, None, None]
        bstack1lll11ll1ll_opy_ = response.json()
        os.environ[bstack111l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪᕙ")] = bstack1lll11ll1ll_opy_[bstack111l11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨᕚ")]
        if cls.bstack1llllll1l_opy_(bstack1lll1l11l1l_opy_.get(bstack111l11_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡹࡸ࡫ࡤࠨᕛ"), bstack111l11_opy_ (u"ࠨࠩᕜ"))) is True:
            logger.debug(bstack111l11_opy_ (u"ࠩࡗࡩࡸࡺࠠࡐࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠠࡃࡷ࡬ࡰࡩࠦࡣࡳࡧࡤࡸ࡮ࡵ࡮ࠡࡕࡸࡧࡨ࡫ࡳࡴࡨࡸࡰࠦ࠭ᕝ"))
            os.environ[bstack111l11_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡃࡗࡌࡐࡉࡥࡃࡐࡏࡓࡐࡊ࡚ࡅࡅࠩᕞ")] = bstack111l11_opy_ (u"ࠫࡹࡸࡵࡦࠩᕟ")
            if bstack1lll11ll1ll_opy_.get(bstack111l11_opy_ (u"ࠬࡰࡷࡵࠩᕠ")):
                os.environ[bstack111l11_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡎ࡜࡚ࠧᕡ")] = bstack1lll11ll1ll_opy_[bstack111l11_opy_ (u"ࠧ࡫ࡹࡷࠫᕢ")]
                os.environ[bstack111l11_opy_ (u"ࠨࡅࡕࡉࡉࡋࡎࡕࡋࡄࡐࡘࡥࡆࡐࡔࡢࡇࡗࡇࡓࡉࡡࡕࡉࡕࡕࡒࡕࡋࡑࡋࠬᕣ")] = json.dumps({
                    bstack111l11_opy_ (u"ࠩࡸࡷࡪࡸ࡮ࡢ࡯ࡨࠫᕤ"): bstack11l1ll1111_opy_,
                    bstack111l11_opy_ (u"ࠪࡴࡦࡹࡳࡸࡱࡵࡨࠬᕥ"): bstack11l1lllll1_opy_
                })
            if bstack1lll11ll1ll_opy_.get(bstack111l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭ᕦ")):
                os.environ[bstack111l11_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡅ࡙ࡎࡒࡄࡠࡊࡄࡗࡍࡋࡄࡠࡋࡇࠫᕧ")] = bstack1lll11ll1ll_opy_[bstack111l11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨᕨ")]
            if bstack1lll11ll1ll_opy_.get(bstack111l11_opy_ (u"ࠧࡢ࡮࡯ࡳࡼࡥࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࡶࠫᕩ")):
                os.environ[bstack111l11_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡇࡌࡍࡑ࡚ࡣࡘࡉࡒࡆࡇࡑࡗࡍࡕࡔࡔࠩᕪ")] = str(bstack1lll11ll1ll_opy_[bstack111l11_opy_ (u"ࠩࡤࡰࡱࡵࡷࡠࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࡸ࠭ᕫ")])
        return [bstack1lll11ll1ll_opy_[bstack111l11_opy_ (u"ࠪ࡮ࡼࡺࠧᕬ")], bstack1lll11ll1ll_opy_[bstack111l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭ᕭ")], bstack1lll11ll1ll_opy_[bstack111l11_opy_ (u"ࠬࡧ࡬࡭ࡱࡺࡣࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࡴࠩᕮ")]]
    @classmethod
    @bstack1l1111ll11_opy_(class_method=True)
    def stop(cls, bstack1lll1l1l1l1_opy_ = None):
        if not cls.on():
            return
        if os.environ[bstack111l11_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡎ࡜࡚ࠧᕯ")] == bstack111l11_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧᕰ") or os.environ[bstack111l11_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡈࡕࡊࡎࡇࡣࡍࡇࡓࡉࡇࡇࡣࡎࡊࠧᕱ")] == bstack111l11_opy_ (u"ࠤࡱࡹࡱࡲࠢᕲ"):
            print(bstack111l11_opy_ (u"ࠪࡉ࡝ࡉࡅࡑࡖࡌࡓࡓࠦࡉࡏࠢࡶࡸࡴࡶࡂࡶ࡫࡯ࡨ࡚ࡶࡳࡵࡴࡨࡥࡲࠦࡒࡆࡓࡘࡉࡘ࡚ࠠࡕࡑࠣࡘࡊ࡙ࡔࠡࡑࡅࡗࡊࡘࡖࡂࡄࡌࡐࡎ࡚࡙ࠡ࠼ࠣࡑ࡮ࡹࡳࡪࡰࡪࠤࡦࡻࡴࡩࡧࡱࡸ࡮ࡩࡡࡵ࡫ࡲࡲࠥࡺ࡯࡬ࡧࡱࠫᕳ"))
            return {
                bstack111l11_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫᕴ"): bstack111l11_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫᕵ"),
                bstack111l11_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᕶ"): bstack111l11_opy_ (u"ࠧࡕࡱ࡮ࡩࡳ࠵ࡢࡶ࡫࡯ࡨࡎࡊࠠࡪࡵࠣࡹࡳࡪࡥࡧ࡫ࡱࡩࡩ࠲ࠠࡣࡷ࡬ࡰࡩࠦࡣࡳࡧࡤࡸ࡮ࡵ࡮ࠡ࡯࡬࡫࡭ࡺࠠࡩࡣࡹࡩࠥ࡬ࡡࡪ࡮ࡨࡨࠬᕷ")
            }
        else:
            cls.bstack1llll11l1l1_opy_.shutdown()
            data = {
                bstack111l11_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ᕸ"): bstack11ll1l1ll_opy_()
            }
            if not bstack1lll1l1l1l1_opy_ is None:
                data[bstack111l11_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡲ࡫ࡴࡢࡦࡤࡸࡦ࠭ᕹ")] = [{
                    bstack111l11_opy_ (u"ࠪࡶࡪࡧࡳࡰࡰࠪᕺ"): bstack111l11_opy_ (u"ࠫࡺࡹࡥࡳࡡ࡮࡭ࡱࡲࡥࡥࠩᕻ"),
                    bstack111l11_opy_ (u"ࠬࡹࡩࡨࡰࡤࡰࠬᕼ"): bstack1lll1l1l1l1_opy_
                }]
            config = {
                bstack111l11_opy_ (u"࠭ࡨࡦࡣࡧࡩࡷࡹࠧᕽ"): cls.default_headers()
            }
            bstack11l11111l1_opy_ = bstack111l11_opy_ (u"ࠧࡢࡲ࡬࠳ࡻ࠷࠯ࡣࡷ࡬ࡰࡩࡹ࠯ࡼࡿ࠲ࡷࡹࡵࡰࠨᕾ").format(os.environ[bstack111l11_opy_ (u"ࠣࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡈࡕࡊࡎࡇࡣࡍࡇࡓࡉࡇࡇࡣࡎࡊࠢᕿ")])
            bstack1lll11l1lll_opy_ = cls.request_url(bstack11l11111l1_opy_)
            response = bstack1lllll1lll_opy_(bstack111l11_opy_ (u"ࠩࡓ࡙࡙࠭ᖀ"), bstack1lll11l1lll_opy_, data, config)
            if not response.ok:
                raise Exception(bstack111l11_opy_ (u"ࠥࡗࡹࡵࡰࠡࡴࡨࡵࡺ࡫ࡳࡵࠢࡱࡳࡹࠦ࡯࡬ࠤᖁ"))
    @classmethod
    def bstack11lll1l1l1_opy_(cls):
        if cls.bstack1llll11l1l1_opy_ is None:
            return
        cls.bstack1llll11l1l1_opy_.shutdown()
    @classmethod
    def bstack1l1l1ll1_opy_(cls):
        if cls.on():
            print(
                bstack111l11_opy_ (u"࡛ࠫ࡯ࡳࡪࡶࠣ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡣࡷ࡬ࡰࡩࡹ࠯ࡼࡿࠣࡸࡴࠦࡶࡪࡧࡺࠤࡧࡻࡩ࡭ࡦࠣࡶࡪࡶ࡯ࡳࡶ࠯ࠤ࡮ࡴࡳࡪࡩ࡫ࡸࡸ࠲ࠠࡢࡰࡧࠤࡲࡧ࡮ࡺࠢࡰࡳࡷ࡫ࠠࡥࡧࡥࡹ࡬࡭ࡩ࡯ࡩࠣ࡭ࡳ࡬࡯ࡳ࡯ࡤࡸ࡮ࡵ࡮ࠡࡣ࡯ࡰࠥࡧࡴࠡࡱࡱࡩࠥࡶ࡬ࡢࡥࡨࠥࡡࡴࠧᖂ").format(os.environ[bstack111l11_opy_ (u"ࠧࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡅ࡙ࡎࡒࡄࡠࡊࡄࡗࡍࡋࡄࡠࡋࡇࠦᖃ")]))
    @classmethod
    def bstack1lll11ll1l1_opy_(cls):
        if cls.bstack1llll11l1l1_opy_ is not None:
            return
        cls.bstack1llll11l1l1_opy_ = bstack1llll11ll11_opy_(cls.bstack1lll11ll11l_opy_)
        cls.bstack1llll11l1l1_opy_.start()
    @classmethod
    def bstack1l11l11111_opy_(cls, bstack1l111lll1l_opy_, bstack1lll1l11111_opy_=bstack111l11_opy_ (u"࠭ࡡࡱ࡫࠲ࡺ࠶࠵ࡢࡢࡶࡦ࡬ࠬᖄ")):
        if not cls.on():
            return
        bstack1llllll111_opy_ = bstack1l111lll1l_opy_[bstack111l11_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫᖅ")]
        bstack1lll1l1l111_opy_ = {
            bstack111l11_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩᖆ"): bstack111l11_opy_ (u"ࠩࡗࡩࡸࡺ࡟ࡔࡶࡤࡶࡹࡥࡕࡱ࡮ࡲࡥࡩ࠭ᖇ"),
            bstack111l11_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬᖈ"): bstack111l11_opy_ (u"࡙ࠫ࡫ࡳࡵࡡࡈࡲࡩࡥࡕࡱ࡮ࡲࡥࡩ࠭ᖉ"),
            bstack111l11_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙࡫ࡪࡲࡳࡩࡩ࠭ᖊ"): bstack111l11_opy_ (u"࠭ࡔࡦࡵࡷࡣࡘࡱࡩࡱࡲࡨࡨࡤ࡛ࡰ࡭ࡱࡤࡨࠬᖋ"),
            bstack111l11_opy_ (u"ࠧࡍࡱࡪࡇࡷ࡫ࡡࡵࡧࡧࠫᖌ"): bstack111l11_opy_ (u"ࠨࡎࡲ࡫ࡤ࡛ࡰ࡭ࡱࡤࡨࠬᖍ"),
            bstack111l11_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪᖎ"): bstack111l11_opy_ (u"ࠪࡌࡴࡵ࡫ࡠࡕࡷࡥࡷࡺ࡟ࡖࡲ࡯ࡳࡦࡪࠧᖏ"),
            bstack111l11_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ᖐ"): bstack111l11_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡢࡉࡳࡪ࡟ࡖࡲ࡯ࡳࡦࡪࠧᖑ"),
            bstack111l11_opy_ (u"࠭ࡃࡃࡖࡖࡩࡸࡹࡩࡰࡰࡆࡶࡪࡧࡴࡦࡦࠪᖒ"): bstack111l11_opy_ (u"ࠧࡄࡄࡗࡣ࡚ࡶ࡬ࡰࡣࡧࠫᖓ")
        }.get(bstack1llllll111_opy_)
        if bstack1lll1l11111_opy_ == bstack111l11_opy_ (u"ࠨࡣࡳ࡭࠴ࡼ࠱࠰ࡤࡤࡸࡨ࡮ࠧᖔ"):
            cls.bstack1lll11ll1l1_opy_()
            cls.bstack1llll11l1l1_opy_.add(bstack1l111lll1l_opy_)
        elif bstack1lll1l11111_opy_ == bstack111l11_opy_ (u"ࠩࡤࡴ࡮࠵ࡶ࠲࠱ࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࡹࠧᖕ"):
            cls.bstack1lll11ll11l_opy_([bstack1l111lll1l_opy_], bstack1lll1l11111_opy_)
    @classmethod
    @bstack1l1111ll11_opy_(class_method=True)
    def bstack1lll11ll11l_opy_(cls, bstack1l111lll1l_opy_, bstack1lll1l11111_opy_=bstack111l11_opy_ (u"ࠪࡥࡵ࡯࠯ࡷ࠳࠲ࡦࡦࡺࡣࡩࠩᖖ")):
        config = {
            bstack111l11_opy_ (u"ࠫ࡭࡫ࡡࡥࡧࡵࡷࠬᖗ"): cls.default_headers()
        }
        response = bstack1lllll1lll_opy_(bstack111l11_opy_ (u"ࠬࡖࡏࡔࡖࠪᖘ"), cls.request_url(bstack1lll1l11111_opy_), bstack1l111lll1l_opy_, config)
        bstack11l1ll11l1_opy_ = response.json()
    @classmethod
    @bstack1l1111ll11_opy_(class_method=True)
    def bstack1l11111l1_opy_(cls, bstack1l111ll1l1_opy_):
        bstack1lll11llll1_opy_ = []
        for log in bstack1l111ll1l1_opy_:
            bstack1lll1l1l11l_opy_ = {
                bstack111l11_opy_ (u"࠭࡫ࡪࡰࡧࠫᖙ"): bstack111l11_opy_ (u"ࠧࡕࡇࡖࡘࡤࡒࡏࡈࠩᖚ"),
                bstack111l11_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧᖛ"): log[bstack111l11_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨᖜ")],
                bstack111l11_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭ᖝ"): log[bstack111l11_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧᖞ")],
                bstack111l11_opy_ (u"ࠬ࡮ࡴࡵࡲࡢࡶࡪࡹࡰࡰࡰࡶࡩࠬᖟ"): {},
                bstack111l11_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᖠ"): log[bstack111l11_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᖡ")],
            }
            if bstack111l11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᖢ") in log:
                bstack1lll1l1l11l_opy_[bstack111l11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᖣ")] = log[bstack111l11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᖤ")]
            elif bstack111l11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᖥ") in log:
                bstack1lll1l1l11l_opy_[bstack111l11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᖦ")] = log[bstack111l11_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᖧ")]
            bstack1lll11llll1_opy_.append(bstack1lll1l1l11l_opy_)
        cls.bstack1l11l11111_opy_({
            bstack111l11_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫᖨ"): bstack111l11_opy_ (u"ࠨࡎࡲ࡫ࡈࡸࡥࡢࡶࡨࡨࠬᖩ"),
            bstack111l11_opy_ (u"ࠩ࡯ࡳ࡬ࡹࠧᖪ"): bstack1lll11llll1_opy_
        })
    @classmethod
    @bstack1l1111ll11_opy_(class_method=True)
    def bstack1lll11ll111_opy_(cls, steps):
        bstack1lll1l11lll_opy_ = []
        for step in steps:
            bstack1lll1l11l11_opy_ = {
                bstack111l11_opy_ (u"ࠪ࡯࡮ࡴࡤࠨᖫ"): bstack111l11_opy_ (u"࡙ࠫࡋࡓࡕࡡࡖࡘࡊࡖࠧᖬ"),
                bstack111l11_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫᖭ"): step[bstack111l11_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬᖮ")],
                bstack111l11_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪᖯ"): step[bstack111l11_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫᖰ")],
                bstack111l11_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᖱ"): step[bstack111l11_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᖲ")],
                bstack111l11_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳ࠭ᖳ"): step[bstack111l11_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴࠧᖴ")]
            }
            if bstack111l11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᖵ") in step:
                bstack1lll1l11l11_opy_[bstack111l11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᖶ")] = step[bstack111l11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᖷ")]
            elif bstack111l11_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᖸ") in step:
                bstack1lll1l11l11_opy_[bstack111l11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᖹ")] = step[bstack111l11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᖺ")]
            bstack1lll1l11lll_opy_.append(bstack1lll1l11l11_opy_)
        cls.bstack1l11l11111_opy_({
            bstack111l11_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩᖻ"): bstack111l11_opy_ (u"࠭ࡌࡰࡩࡆࡶࡪࡧࡴࡦࡦࠪᖼ"),
            bstack111l11_opy_ (u"ࠧ࡭ࡱࡪࡷࠬᖽ"): bstack1lll1l11lll_opy_
        })
    @classmethod
    @bstack1l1111ll11_opy_(class_method=True)
    def bstack1ll11l1ll_opy_(cls, screenshot):
        cls.bstack1l11l11111_opy_({
            bstack111l11_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬᖾ"): bstack111l11_opy_ (u"ࠩࡏࡳ࡬ࡉࡲࡦࡣࡷࡩࡩ࠭ᖿ"),
            bstack111l11_opy_ (u"ࠪࡰࡴ࡭ࡳࠨᗀ"): [{
                bstack111l11_opy_ (u"ࠫࡰ࡯࡮ࡥࠩᗁ"): bstack111l11_opy_ (u"࡚ࠬࡅࡔࡖࡢࡗࡈࡘࡅࡆࡐࡖࡌࡔ࡚ࠧᗂ"),
                bstack111l11_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩᗃ"): bstack1l111llll1_opy_().isoformat() + bstack111l11_opy_ (u"࡛ࠧࠩᗄ"),
                bstack111l11_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᗅ"): screenshot[bstack111l11_opy_ (u"ࠩ࡬ࡱࡦ࡭ࡥࠨᗆ")],
                bstack111l11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᗇ"): screenshot[bstack111l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᗈ")]
            }]
        }, bstack1lll1l11111_opy_=bstack111l11_opy_ (u"ࠬࡧࡰࡪ࠱ࡹ࠵࠴ࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࡵࠪᗉ"))
    @classmethod
    @bstack1l1111ll11_opy_(class_method=True)
    def bstack1l1ll11l11_opy_(cls, driver):
        current_test_uuid = cls.current_test_uuid()
        if not current_test_uuid:
            return
        cls.bstack1l11l11111_opy_({
            bstack111l11_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪᗊ"): bstack111l11_opy_ (u"ࠧࡄࡄࡗࡗࡪࡹࡳࡪࡱࡱࡇࡷ࡫ࡡࡵࡧࡧࠫᗋ"),
            bstack111l11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࠪᗌ"): {
                bstack111l11_opy_ (u"ࠤࡸࡹ࡮ࡪࠢᗍ"): cls.current_test_uuid(),
                bstack111l11_opy_ (u"ࠥ࡭ࡳࡺࡥࡨࡴࡤࡸ࡮ࡵ࡮ࡴࠤᗎ"): cls.bstack1l111l11l1_opy_(driver)
            }
        })
    @classmethod
    def on(cls):
        if os.environ.get(bstack111l11_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡌ࡚ࡘࠬᗏ"), None) is None or os.environ[bstack111l11_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡍ࡛࡙࠭ᗐ")] == bstack111l11_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦᗑ"):
            return False
        return True
    @classmethod
    def bstack1llllll1l_opy_(cls, framework=bstack111l11_opy_ (u"ࠢࠣᗒ")):
        if framework not in bstack11l11lll11_opy_:
            return False
        bstack1lll11lll11_opy_ = not bstack111l1l1ll_opy_()
        return bstack1ll11l1l11_opy_(cls.bs_config.get(bstack111l11_opy_ (u"ࠨࡶࡨࡷࡹࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬᗓ"), bstack1lll11lll11_opy_))
    @staticmethod
    def request_url(url):
        return bstack111l11_opy_ (u"ࠩࡾࢁ࠴ࢁࡽࠨᗔ").format(bstack1lll1l1111l_opy_, url)
    @staticmethod
    def default_headers():
        headers = {
            bstack111l11_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱࡙ࡿࡰࡦࠩᗕ"): bstack111l11_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧᗖ"),
            bstack111l11_opy_ (u"ࠬ࡞࠭ࡃࡕࡗࡅࡈࡑ࠭ࡕࡇࡖࡘࡔࡖࡓࠨᗗ"): bstack111l11_opy_ (u"࠭ࡴࡳࡷࡨࠫᗘ")
        }
        if os.environ.get(bstack111l11_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡏ࡝ࡔࠨᗙ"), None):
            headers[bstack111l11_opy_ (u"ࠨࡃࡸࡸ࡭ࡵࡲࡪࡼࡤࡸ࡮ࡵ࡮ࠨᗚ")] = bstack111l11_opy_ (u"ࠩࡅࡩࡦࡸࡥࡳࠢࡾࢁࠬᗛ").format(os.environ[bstack111l11_opy_ (u"ࠥࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡋ࡙ࡗࠦᗜ")])
        return headers
    @staticmethod
    def current_test_uuid():
        return getattr(threading.current_thread(), bstack111l11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨᗝ"), None)
    @staticmethod
    def current_hook_uuid():
        return getattr(threading.current_thread(), bstack111l11_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩᗞ"), None)
    @staticmethod
    def bstack11llll1ll1_opy_():
        if getattr(threading.current_thread(), bstack111l11_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪᗟ"), None):
            return {
                bstack111l11_opy_ (u"ࠧࡵࡻࡳࡩࠬᗠ"): bstack111l11_opy_ (u"ࠨࡶࡨࡷࡹ࠭ᗡ"),
                bstack111l11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᗢ"): getattr(threading.current_thread(), bstack111l11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧᗣ"), None)
            }
        if getattr(threading.current_thread(), bstack111l11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨᗤ"), None):
            return {
                bstack111l11_opy_ (u"ࠬࡺࡹࡱࡧࠪᗥ"): bstack111l11_opy_ (u"࠭ࡨࡰࡱ࡮ࠫᗦ"),
                bstack111l11_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᗧ"): getattr(threading.current_thread(), bstack111l11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬᗨ"), None)
            }
        return None
    @staticmethod
    def bstack1l111l11l1_opy_(driver):
        return {
            bstack111l1l1lll_opy_(): bstack111l1llll1_opy_(driver)
        }
    @staticmethod
    def bstack1lll11lll1l_opy_(exception_info, report):
        return [{bstack111l11_opy_ (u"ࠩࡥࡥࡨࡱࡴࡳࡣࡦࡩࠬᗩ"): [exception_info.exconly(), report.longreprtext]}]
    @staticmethod
    def bstack11ll11llll_opy_(typename):
        if bstack111l11_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࠨᗪ") in typename:
            return bstack111l11_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࡅࡳࡴࡲࡶࠧᗫ")
        return bstack111l11_opy_ (u"࡛ࠧ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡆࡴࡵࡳࡷࠨᗬ")
    @staticmethod
    def bstack1lll1l111ll_opy_(func):
        def wrap(*args, **kwargs):
            if bstack1lll1ll1l_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def bstack1l1111111l_opy_(test, hook_name=None):
        bstack1lll1l111l1_opy_ = test.parent
        if hook_name in [bstack111l11_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡩ࡬ࡢࡵࡶࠫᗭ"), bstack111l11_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡦࡰࡦࡹࡳࠨᗮ"), bstack111l11_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟࡮ࡱࡧࡹࡱ࡫ࠧᗯ"), bstack111l11_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲࡵࡤࡶ࡮ࡨࠫᗰ")]:
            bstack1lll1l111l1_opy_ = test
        scope = []
        while bstack1lll1l111l1_opy_ is not None:
            scope.append(bstack1lll1l111l1_opy_.name)
            bstack1lll1l111l1_opy_ = bstack1lll1l111l1_opy_.parent
        scope.reverse()
        return scope[2:]
    @staticmethod
    def bstack1lll1l1l1ll_opy_(hook_type):
        if hook_type == bstack111l11_opy_ (u"ࠥࡆࡊࡌࡏࡓࡇࡢࡉࡆࡉࡈࠣᗱ"):
            return bstack111l11_opy_ (u"ࠦࡘ࡫ࡴࡶࡲࠣ࡬ࡴࡵ࡫ࠣᗲ")
        elif hook_type == bstack111l11_opy_ (u"ࠧࡇࡆࡕࡇࡕࡣࡊࡇࡃࡉࠤᗳ"):
            return bstack111l11_opy_ (u"ࠨࡔࡦࡣࡵࡨࡴࡽ࡮ࠡࡪࡲࡳࡰࠨᗴ")
    @staticmethod
    def bstack1lll1l11ll1_opy_(bstack1ll1111ll1_opy_):
        try:
            if not bstack1lll1ll1l_opy_.on():
                return bstack1ll1111ll1_opy_
            if os.environ.get(bstack111l11_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡒࡆࡔࡘࡒࠧᗵ"), None) == bstack111l11_opy_ (u"ࠣࡶࡵࡹࡪࠨᗶ"):
                tests = os.environ.get(bstack111l11_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡔࡈࡖ࡚ࡔ࡟ࡕࡇࡖࡘࡘࠨᗷ"), None)
                if tests is None or tests == bstack111l11_opy_ (u"ࠥࡲࡺࡲ࡬ࠣᗸ"):
                    return bstack1ll1111ll1_opy_
                bstack1ll1111ll1_opy_ = tests.split(bstack111l11_opy_ (u"ࠫ࠱࠭ᗹ"))
                return bstack1ll1111ll1_opy_
        except Exception as exc:
            print(bstack111l11_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡷ࡫ࡲࡶࡰࠣ࡬ࡦࡴࡤ࡭ࡧࡵ࠾ࠥࠨᗺ"), str(exc))
        return bstack1ll1111ll1_opy_
    @classmethod
    def bstack1l111l1l11_opy_(cls, event: str, bstack1l111lll1l_opy_: bstack1l111l111l_opy_):
        bstack1l1111l1ll_opy_ = {
            bstack111l11_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪᗻ"): event,
            bstack1l111lll1l_opy_.bstack11llll1111_opy_(): bstack1l111lll1l_opy_.bstack11lllllll1_opy_(event)
        }
        bstack1lll1ll1l_opy_.bstack1l11l11111_opy_(bstack1l1111l1ll_opy_)
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
from browserstack_sdk.bstack11111lll1_opy_ import bstack1l11l111l_opy_
from browserstack_sdk.bstack11llll1lll_opy_ import RobotHandler
def bstack1lllll1l1_opy_(framework):
    if framework.lower() == bstack111l11_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪᆘ"):
        return bstack1l11l111l_opy_.version()
    elif framework.lower() == bstack111l11_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪᆙ"):
        return RobotHandler.version()
    elif framework.lower() == bstack111l11_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬᆚ"):
        import behave
        return behave.__version__
    else:
        return bstack111l11_opy_ (u"࠭ࡵ࡯࡭ࡱࡳࡼࡴࠧᆛ")
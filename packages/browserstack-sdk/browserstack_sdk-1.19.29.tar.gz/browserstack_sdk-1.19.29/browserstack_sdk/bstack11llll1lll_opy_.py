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
class RobotHandler():
    def __init__(self, args, logger, bstack11ll1lll1l_opy_, bstack11ll1lllll_opy_):
        self.args = args
        self.logger = logger
        self.bstack11ll1lll1l_opy_ = bstack11ll1lll1l_opy_
        self.bstack11ll1lllll_opy_ = bstack11ll1lllll_opy_
    @staticmethod
    def version():
        import robot
        return robot.__version__
    @staticmethod
    def bstack1l1111111l_opy_(bstack11ll11lll1_opy_):
        bstack11ll11ll11_opy_ = []
        if bstack11ll11lll1_opy_:
            tokens = str(os.path.basename(bstack11ll11lll1_opy_)).split(bstack111l11_opy_ (u"ࠧࡥࠢไ"))
            camelcase_name = bstack111l11_opy_ (u"ࠨࠠࠣๅ").join(t.title() for t in tokens)
            suite_name, bstack11ll11ll1l_opy_ = os.path.splitext(camelcase_name)
            bstack11ll11ll11_opy_.append(suite_name)
        return bstack11ll11ll11_opy_
    @staticmethod
    def bstack11ll11llll_opy_(typename):
        if bstack111l11_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࠥๆ") in typename:
            return bstack111l11_opy_ (u"ࠣࡃࡶࡷࡪࡸࡴࡪࡱࡱࡉࡷࡸ࡯ࡳࠤ็")
        return bstack111l11_opy_ (u"ࠤࡘࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࡊࡸࡲࡰࡴ่ࠥ")
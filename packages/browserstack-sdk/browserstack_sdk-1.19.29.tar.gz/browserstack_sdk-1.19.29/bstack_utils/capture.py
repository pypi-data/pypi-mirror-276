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
import sys
class bstack1l111111l1_opy_:
    def __init__(self, handler):
        self._11l1l1l111_opy_ = sys.stdout.write
        self._11l1l11lll_opy_ = sys.stderr.write
        self.handler = handler
        self._started = False
    def start(self):
        if self._started:
            return
        self._started = True
        sys.stdout.write = self.bstack11l1l1l11l_opy_
        sys.stdout.error = self.bstack11l1l11ll1_opy_
    def bstack11l1l1l11l_opy_(self, _str):
        self._11l1l1l111_opy_(_str)
        if self.handler:
            self.handler({bstack111l11_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧ໽"): bstack111l11_opy_ (u"ࠩࡌࡒࡋࡕࠧ໾"), bstack111l11_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ໿"): _str})
    def bstack11l1l11ll1_opy_(self, _str):
        self._11l1l11lll_opy_(_str)
        if self.handler:
            self.handler({bstack111l11_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪༀ"): bstack111l11_opy_ (u"ࠬࡋࡒࡓࡑࡕࠫ༁"), bstack111l11_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ༂"): _str})
    def reset(self):
        if not self._started:
            return
        self._started = False
        sys.stdout.write = self._11l1l1l111_opy_
        sys.stderr.write = self._11l1l11lll_opy_
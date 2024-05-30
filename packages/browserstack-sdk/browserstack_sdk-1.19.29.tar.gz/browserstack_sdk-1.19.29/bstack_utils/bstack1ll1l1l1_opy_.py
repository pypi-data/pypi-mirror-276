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
from collections import deque
from bstack_utils.constants import *
class bstack1l11ll1lll_opy_:
    def __init__(self):
        self._1lllll1l11l_opy_ = deque()
        self._1lllll1lll1_opy_ = {}
        self._1llllll1ll1_opy_ = False
    def bstack1llllll11l1_opy_(self, test_name, bstack1lllll1l1l1_opy_):
        bstack1llllll1111_opy_ = self._1lllll1lll1_opy_.get(test_name, {})
        return bstack1llllll1111_opy_.get(bstack1lllll1l1l1_opy_, 0)
    def bstack1lllll1l1ll_opy_(self, test_name, bstack1lllll1l1l1_opy_):
        bstack1lllll1llll_opy_ = self.bstack1llllll11l1_opy_(test_name, bstack1lllll1l1l1_opy_)
        self.bstack1llllll1l1l_opy_(test_name, bstack1lllll1l1l1_opy_)
        return bstack1lllll1llll_opy_
    def bstack1llllll1l1l_opy_(self, test_name, bstack1lllll1l1l1_opy_):
        if test_name not in self._1lllll1lll1_opy_:
            self._1lllll1lll1_opy_[test_name] = {}
        bstack1llllll1111_opy_ = self._1lllll1lll1_opy_[test_name]
        bstack1lllll1llll_opy_ = bstack1llllll1111_opy_.get(bstack1lllll1l1l1_opy_, 0)
        bstack1llllll1111_opy_[bstack1lllll1l1l1_opy_] = bstack1lllll1llll_opy_ + 1
    def bstack1ll1lllll1_opy_(self, bstack1llllll1l11_opy_, bstack1llllll11ll_opy_):
        bstack1lllll1ll1l_opy_ = self.bstack1lllll1l1ll_opy_(bstack1llllll1l11_opy_, bstack1llllll11ll_opy_)
        bstack1lllll1l111_opy_ = bstack11l1l111ll_opy_[bstack1llllll11ll_opy_]
        bstack1llllll111l_opy_ = bstack111l11_opy_ (u"ࠥࡿࢂ࠳ࡻࡾ࠯ࡾࢁࠧᑆ").format(bstack1llllll1l11_opy_, bstack1lllll1l111_opy_, bstack1lllll1ll1l_opy_)
        self._1lllll1l11l_opy_.append(bstack1llllll111l_opy_)
    def bstack1l1l1111_opy_(self):
        return len(self._1lllll1l11l_opy_) == 0
    def bstack1l1l11ll_opy_(self):
        bstack1lllll1ll11_opy_ = self._1lllll1l11l_opy_.popleft()
        return bstack1lllll1ll11_opy_
    def capturing(self):
        return self._1llllll1ll1_opy_
    def bstack1lllll111l_opy_(self):
        self._1llllll1ll1_opy_ = True
    def bstack1l111111l_opy_(self):
        self._1llllll1ll1_opy_ = False
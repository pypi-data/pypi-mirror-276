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
class bstack1ll1lll11l_opy_:
    def __init__(self, handler):
        self._1llll1111ll_opy_ = None
        self.handler = handler
        self._1llll111l1l_opy_ = self.bstack1llll111ll1_opy_()
        self.patch()
    def patch(self):
        self._1llll1111ll_opy_ = self._1llll111l1l_opy_.execute
        self._1llll111l1l_opy_.execute = self.bstack1llll111l11_opy_()
    def bstack1llll111l11_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            self.handler(bstack111l11_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࠣᒟ"), driver_command, None, this, args)
            response = self._1llll1111ll_opy_(this, driver_command, *args, **kwargs)
            self.handler(bstack111l11_opy_ (u"ࠤࡤࡪࡹ࡫ࡲࠣᒠ"), driver_command, response)
            return response
        return execute
    def reset(self):
        self._1llll111l1l_opy_.execute = self._1llll1111ll_opy_
    @staticmethod
    def bstack1llll111ll1_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver
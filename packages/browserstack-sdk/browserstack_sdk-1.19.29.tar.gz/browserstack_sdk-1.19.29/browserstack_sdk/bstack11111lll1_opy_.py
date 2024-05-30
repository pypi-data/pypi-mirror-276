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
import multiprocessing
import os
import json
from time import sleep
import bstack_utils.bstack1111llll_opy_ as bstack1llll11l_opy_
from browserstack_sdk.bstack111111lll_opy_ import *
from bstack_utils.config import Config
from bstack_utils.messages import bstack1l11l1l1_opy_
class bstack1l11l111l_opy_:
    def __init__(self, args, logger, bstack11ll1lll1l_opy_, bstack11ll1lllll_opy_):
        self.args = args
        self.logger = logger
        self.bstack11ll1lll1l_opy_ = bstack11ll1lll1l_opy_
        self.bstack11ll1lllll_opy_ = bstack11ll1lllll_opy_
        self._prepareconfig = None
        self.Config = None
        self.runner = None
        self.bstack1ll1111ll1_opy_ = []
        self.bstack11ll1l1lll_opy_ = None
        self.bstack1llll11l1l_opy_ = []
        self.bstack11ll1l1ll1_opy_ = self.bstack1l1lll11ll_opy_()
        self.bstack1lll11111_opy_ = -1
    def bstack11l11ll1_opy_(self, bstack11ll1l11ll_opy_):
        self.parse_args()
        self.bstack11ll1lll11_opy_()
        self.bstack11ll1ll11l_opy_(bstack11ll1l11ll_opy_)
    @staticmethod
    def version():
        import pytest
        return pytest.__version__
    @staticmethod
    def bstack11ll1llll1_opy_():
        import importlib
        if getattr(importlib, bstack111l11_opy_ (u"ࠩࡩ࡭ࡳࡪ࡟࡭ࡱࡤࡨࡪࡸࠧล"), False):
            bstack11ll1l1l1l_opy_ = importlib.find_loader(bstack111l11_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡷࡪࡲࡥ࡯࡫ࡸࡱࠬฦ"))
        else:
            bstack11ll1l1l1l_opy_ = importlib.util.find_spec(bstack111l11_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡣࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࠭ว"))
    def bstack11ll1ll1l1_opy_(self, arg):
        if arg in self.args:
            i = self.args.index(arg)
            self.args.pop(i + 1)
            self.args.pop(i)
    def parse_args(self):
        self.bstack1lll11111_opy_ = -1
        if bstack111l11_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬศ") in self.bstack11ll1lll1l_opy_:
            self.bstack1lll11111_opy_ = int(self.bstack11ll1lll1l_opy_[bstack111l11_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭ษ")])
        try:
            bstack11ll1ll111_opy_ = [bstack111l11_opy_ (u"ࠧ࠮࠯ࡧࡶ࡮ࡼࡥࡳࠩส"), bstack111l11_opy_ (u"ࠨ࠯࠰ࡴࡱࡻࡧࡪࡰࡶࠫห"), bstack111l11_opy_ (u"ࠩ࠰ࡴࠬฬ")]
            if self.bstack1lll11111_opy_ >= 0:
                bstack11ll1ll111_opy_.extend([bstack111l11_opy_ (u"ࠪ࠱࠲ࡴࡵ࡮ࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠫอ"), bstack111l11_opy_ (u"ࠫ࠲ࡴࠧฮ")])
            for arg in bstack11ll1ll111_opy_:
                self.bstack11ll1ll1l1_opy_(arg)
        except Exception as exc:
            self.logger.error(str(exc))
    def get_args(self):
        return self.args
    def bstack11ll1lll11_opy_(self):
        bstack11ll1l1lll_opy_ = [os.path.normpath(item) for item in self.args]
        self.bstack11ll1l1lll_opy_ = bstack11ll1l1lll_opy_
        return bstack11ll1l1lll_opy_
    def bstack111l11l1_opy_(self):
        try:
            from _pytest.config import _prepareconfig
            from _pytest.config import Config
            from _pytest import runner
            self.bstack11ll1llll1_opy_()
            self._prepareconfig = _prepareconfig
            self.Config = Config
            self.runner = runner
        except Exception as e:
            self.logger.warn(e, bstack1l11l1l1_opy_)
    def bstack11ll1ll11l_opy_(self, bstack11ll1l11ll_opy_):
        bstack1l11l111ll_opy_ = Config.bstack1l1l1l1111_opy_()
        if bstack11ll1l11ll_opy_:
            self.bstack11ll1l1lll_opy_.append(bstack111l11_opy_ (u"ࠬ࠳࠭ࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩฯ"))
            self.bstack11ll1l1lll_opy_.append(bstack111l11_opy_ (u"࠭ࡔࡳࡷࡨࠫะ"))
        if bstack1l11l111ll_opy_.bstack11ll1l11l1_opy_():
            self.bstack11ll1l1lll_opy_.append(bstack111l11_opy_ (u"ࠧ࠮࠯ࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸ࠭ั"))
            self.bstack11ll1l1lll_opy_.append(bstack111l11_opy_ (u"ࠨࡖࡵࡹࡪ࠭า"))
        self.bstack11ll1l1lll_opy_.append(bstack111l11_opy_ (u"ࠩ࠰ࡴࠬำ"))
        self.bstack11ll1l1lll_opy_.append(bstack111l11_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡲ࡯ࡹ࡬࡯࡮ࠨิ"))
        self.bstack11ll1l1lll_opy_.append(bstack111l11_opy_ (u"ࠫ࠲࠳ࡤࡳ࡫ࡹࡩࡷ࠭ี"))
        self.bstack11ll1l1lll_opy_.append(bstack111l11_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࠬึ"))
        if self.bstack1lll11111_opy_ > 1:
            self.bstack11ll1l1lll_opy_.append(bstack111l11_opy_ (u"࠭࠭࡯ࠩื"))
            self.bstack11ll1l1lll_opy_.append(str(self.bstack1lll11111_opy_))
    def bstack11ll1l1l11_opy_(self):
        bstack1llll11l1l_opy_ = []
        for spec in self.bstack1ll1111ll1_opy_:
            bstack1111l1l11_opy_ = [spec]
            bstack1111l1l11_opy_ += self.bstack11ll1l1lll_opy_
            bstack1llll11l1l_opy_.append(bstack1111l1l11_opy_)
        self.bstack1llll11l1l_opy_ = bstack1llll11l1l_opy_
        return bstack1llll11l1l_opy_
    def bstack1l1lll11ll_opy_(self):
        try:
            from pytest_bdd import reporting
            self.bstack11ll1l1ll1_opy_ = True
            return True
        except Exception as e:
            self.bstack11ll1l1ll1_opy_ = False
        return self.bstack11ll1l1ll1_opy_
    def bstack11l11ll1l_opy_(self, bstack11ll1ll1ll_opy_, bstack11l11ll1_opy_):
        bstack11l11ll1_opy_[bstack111l11_opy_ (u"ࠧࡄࡑࡑࡊࡎࡍุࠧ")] = self.bstack11ll1lll1l_opy_
        multiprocessing.set_start_method(bstack111l11_opy_ (u"ࠨࡵࡳࡥࡼࡴูࠧ"))
        if bstack111l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷฺࠬ") in self.bstack11ll1lll1l_opy_:
            bstack1ll1111l_opy_ = []
            manager = multiprocessing.Manager()
            bstack1ll1ll111_opy_ = manager.list()
            for index, platform in enumerate(self.bstack11ll1lll1l_opy_[bstack111l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭฻")]):
                bstack1ll1111l_opy_.append(multiprocessing.Process(name=str(index),
                                                           target=bstack11ll1ll1ll_opy_,
                                                           args=(self.bstack11ll1l1lll_opy_, bstack11l11ll1_opy_, bstack1ll1ll111_opy_)))
            i = 0
            bstack11ll1l1111_opy_ = len(self.bstack11ll1lll1l_opy_[bstack111l11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ฼")])
            for t in bstack1ll1111l_opy_:
                os.environ[bstack111l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬ฽")] = str(i)
                os.environ[bstack111l11_opy_ (u"࠭ࡃࡖࡔࡕࡉࡓ࡚࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡇࡅ࡙ࡇࠧ฾")] = json.dumps(self.bstack11ll1lll1l_opy_[bstack111l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ฿")][i % bstack11ll1l1111_opy_])
                i += 1
                t.start()
            for t in bstack1ll1111l_opy_:
                t.join()
            return list(bstack1ll1ll111_opy_)
    @staticmethod
    def bstack1l1lllll11_opy_(driver, bstack1ll1l1ll1_opy_, logger, item=None, wait=False):
        item = item or getattr(threading.current_thread(), bstack111l11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡶࡨࡱࠬเ"), None)
        if item and getattr(item, bstack111l11_opy_ (u"ࠩࡢࡥ࠶࠷ࡹࡠࡶࡨࡷࡹࡥࡣࡢࡵࡨࠫแ"), None) and not getattr(item, bstack111l11_opy_ (u"ࠪࡣࡦ࠷࠱ࡺࡡࡶࡸࡴࡶ࡟ࡥࡱࡱࡩࠬโ"), False):
            logger.info(
                bstack111l11_opy_ (u"ࠦࡆࡻࡴࡰ࡯ࡤࡸࡪࠦࡴࡦࡵࡷࠤࡨࡧࡳࡦࠢࡨࡼࡪࡩࡵࡵ࡫ࡲࡲࠥ࡮ࡡࡴࠢࡨࡲࡩ࡫ࡤ࠯ࠢࡓࡶࡴࡩࡥࡴࡵ࡬ࡲ࡬ࠦࡦࡰࡴࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡸࡪࡹࡴࡪࡰࡪࠤ࡮ࡹࠠࡶࡰࡧࡩࡷࡽࡡࡺ࠰ࠥใ"))
            bstack11ll1l111l_opy_ = item.cls.__name__ if not item.cls is None else None
            bstack1llll11l_opy_.bstack1ll111l1l1_opy_(driver, bstack11ll1l111l_opy_, item.name, item.module.__name__, item.path, bstack1ll1l1ll1_opy_)
            item._a11y_stop_done = True
            if wait:
                sleep(2)
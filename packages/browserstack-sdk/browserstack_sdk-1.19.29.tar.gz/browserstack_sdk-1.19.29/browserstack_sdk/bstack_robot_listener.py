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
import threading
from uuid import uuid4
from itertools import zip_longest
from collections import OrderedDict
from robot.libraries.BuiltIn import BuiltIn
from browserstack_sdk.bstack11llll1lll_opy_ import RobotHandler
from bstack_utils.capture import bstack1l111111l1_opy_
from bstack_utils.bstack1l111l1ll1_opy_ import bstack1l111l111l_opy_, bstack11lll11111_opy_, bstack11lll1ll11_opy_
from bstack_utils.bstack1l1l1l1l1l_opy_ import bstack1lll1ll1l_opy_
from bstack_utils.constants import *
from bstack_utils.helper import bstack1ll111l1ll_opy_, bstack11ll1l1ll_opy_, Result, \
    bstack1l1111ll11_opy_, bstack1l111llll1_opy_
class bstack_robot_listener:
    ROBOT_LISTENER_API_VERSION = 2
    store = {
        bstack111l11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬ൙"): [],
        bstack111l11_opy_ (u"ࠩࡪࡰࡴࡨࡡ࡭ࡡ࡫ࡳࡴࡱࡳࠨ൚"): [],
        bstack111l11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡪࡲࡳࡰࡹࠧ൛"): []
    }
    bstack1l111l1lll_opy_ = []
    bstack1l11111111_opy_ = []
    @staticmethod
    def bstack11lll1l1ll_opy_(log):
        if not (log[bstack111l11_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ൜")] and log[bstack111l11_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭൝")].strip()):
            return
        active = bstack1lll1ll1l_opy_.bstack11llll1ll1_opy_()
        log = {
            bstack111l11_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬ൞"): log[bstack111l11_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ൟ")],
            bstack111l11_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫൠ"): bstack1l111llll1_opy_().isoformat() + bstack111l11_opy_ (u"ࠩ࡝ࠫൡ"),
            bstack111l11_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫൢ"): log[bstack111l11_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬൣ")],
        }
        if active:
            if active[bstack111l11_opy_ (u"ࠬࡺࡹࡱࡧࠪ൤")] == bstack111l11_opy_ (u"࠭ࡨࡰࡱ࡮ࠫ൥"):
                log[bstack111l11_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ൦")] = active[bstack111l11_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ൧")]
            elif active[bstack111l11_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ൨")] == bstack111l11_opy_ (u"ࠪࡸࡪࡹࡴࠨ൩"):
                log[bstack111l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ൪")] = active[bstack111l11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ൫")]
        bstack1lll1ll1l_opy_.bstack1l11111l1_opy_([log])
    def __init__(self):
        self.messages = Messages()
        self._1l111lllll_opy_ = None
        self._1l111lll11_opy_ = None
        self._11lll1lll1_opy_ = OrderedDict()
        self.bstack1l11111l11_opy_ = bstack1l111111l1_opy_(self.bstack11lll1l1ll_opy_)
    @bstack1l1111ll11_opy_(class_method=True)
    def start_suite(self, name, attrs):
        self.messages.bstack11llll1l1l_opy_()
        if not self._11lll1lll1_opy_.get(attrs.get(bstack111l11_opy_ (u"࠭ࡩࡥࠩ൬")), None):
            self._11lll1lll1_opy_[attrs.get(bstack111l11_opy_ (u"ࠧࡪࡦࠪ൭"))] = {}
        bstack11lll1llll_opy_ = bstack11lll1ll11_opy_(
                bstack1l11111l1l_opy_=attrs.get(bstack111l11_opy_ (u"ࠨ࡫ࡧࠫ൮")),
                name=name,
                bstack11llllll11_opy_=bstack11ll1l1ll_opy_(),
                file_path=os.path.relpath(attrs[bstack111l11_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩ൯")], start=os.getcwd()) if attrs.get(bstack111l11_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪ൰")) != bstack111l11_opy_ (u"ࠫࠬ൱") else bstack111l11_opy_ (u"ࠬ࠭൲"),
                framework=bstack111l11_opy_ (u"࠭ࡒࡰࡤࡲࡸࠬ൳")
            )
        threading.current_thread().current_suite_id = attrs.get(bstack111l11_opy_ (u"ࠧࡪࡦࠪ൴"), None)
        self._11lll1lll1_opy_[attrs.get(bstack111l11_opy_ (u"ࠨ࡫ࡧࠫ൵"))][bstack111l11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ൶")] = bstack11lll1llll_opy_
    @bstack1l1111ll11_opy_(class_method=True)
    def end_suite(self, name, attrs):
        messages = self.messages.bstack11lll111l1_opy_()
        self._1l1111l11l_opy_(messages)
        for bstack11lll1111l_opy_ in self.bstack1l111l1lll_opy_:
            bstack11lll1111l_opy_[bstack111l11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࠬ൷")][bstack111l11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪ൸")].extend(self.store[bstack111l11_opy_ (u"ࠬ࡭࡬ࡰࡤࡤࡰࡤ࡮࡯ࡰ࡭ࡶࠫ൹")])
            bstack1lll1ll1l_opy_.bstack1l11l11111_opy_(bstack11lll1111l_opy_)
        self.bstack1l111l1lll_opy_ = []
        self.store[bstack111l11_opy_ (u"࠭ࡧ࡭ࡱࡥࡥࡱࡥࡨࡰࡱ࡮ࡷࠬൺ")] = []
    @bstack1l1111ll11_opy_(class_method=True)
    def start_test(self, name, attrs):
        self.bstack1l11111l11_opy_.start()
        if not self._11lll1lll1_opy_.get(attrs.get(bstack111l11_opy_ (u"ࠧࡪࡦࠪൻ")), None):
            self._11lll1lll1_opy_[attrs.get(bstack111l11_opy_ (u"ࠨ࡫ࡧࠫർ"))] = {}
        driver = bstack1ll111l1ll_opy_(threading.current_thread(), bstack111l11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨൽ"), None)
        bstack1l111l1ll1_opy_ = bstack11lll1ll11_opy_(
            bstack1l11111l1l_opy_=attrs.get(bstack111l11_opy_ (u"ࠪ࡭ࡩ࠭ൾ")),
            name=name,
            bstack11llllll11_opy_=bstack11ll1l1ll_opy_(),
            file_path=os.path.relpath(attrs[bstack111l11_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫൿ")], start=os.getcwd()),
            scope=RobotHandler.bstack1l1111111l_opy_(attrs.get(bstack111l11_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬ඀"), None)),
            framework=bstack111l11_opy_ (u"࠭ࡒࡰࡤࡲࡸࠬඁ"),
            tags=attrs[bstack111l11_opy_ (u"ࠧࡵࡣࡪࡷࠬං")],
            hooks=self.store[bstack111l11_opy_ (u"ࠨࡩ࡯ࡳࡧࡧ࡬ࡠࡪࡲࡳࡰࡹࠧඃ")],
            bstack1l111ll111_opy_=bstack1lll1ll1l_opy_.bstack1l111l11l1_opy_(driver) if driver and driver.session_id else {},
            meta={},
            code=bstack111l11_opy_ (u"ࠤࡾࢁࠥࡢ࡮ࠡࡽࢀࠦ඄").format(bstack111l11_opy_ (u"ࠥࠤࠧඅ").join(attrs[bstack111l11_opy_ (u"ࠫࡹࡧࡧࡴࠩආ")]), name) if attrs[bstack111l11_opy_ (u"ࠬࡺࡡࡨࡵࠪඇ")] else name
        )
        self._11lll1lll1_opy_[attrs.get(bstack111l11_opy_ (u"࠭ࡩࡥࠩඈ"))][bstack111l11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪඉ")] = bstack1l111l1ll1_opy_
        threading.current_thread().current_test_uuid = bstack1l111l1ll1_opy_.bstack11lll11ll1_opy_()
        threading.current_thread().current_test_id = attrs.get(bstack111l11_opy_ (u"ࠨ࡫ࡧࠫඊ"), None)
        self.bstack1l111l1l11_opy_(bstack111l11_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪඋ"), bstack1l111l1ll1_opy_)
    @bstack1l1111ll11_opy_(class_method=True)
    def end_test(self, name, attrs):
        self.bstack1l11111l11_opy_.reset()
        bstack1l111ll1ll_opy_ = bstack11llll11ll_opy_.get(attrs.get(bstack111l11_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪඌ")), bstack111l11_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬඍ"))
        self._11lll1lll1_opy_[attrs.get(bstack111l11_opy_ (u"ࠬ࡯ࡤࠨඎ"))][bstack111l11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩඏ")].stop(time=bstack11ll1l1ll_opy_(), duration=int(attrs.get(bstack111l11_opy_ (u"ࠧࡦ࡮ࡤࡴࡸ࡫ࡤࡵ࡫ࡰࡩࠬඐ"), bstack111l11_opy_ (u"ࠨ࠲ࠪඑ"))), result=Result(result=bstack1l111ll1ll_opy_, exception=attrs.get(bstack111l11_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪඒ")), bstack11llllll1l_opy_=[attrs.get(bstack111l11_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫඓ"))]))
        self.bstack1l111l1l11_opy_(bstack111l11_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ඔ"), self._11lll1lll1_opy_[attrs.get(bstack111l11_opy_ (u"ࠬ࡯ࡤࠨඕ"))][bstack111l11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩඖ")], True)
        self.store[bstack111l11_opy_ (u"ࠧࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡶࠫ඗")] = []
        threading.current_thread().current_test_uuid = None
        threading.current_thread().current_test_id = None
    @bstack1l1111ll11_opy_(class_method=True)
    def start_keyword(self, name, attrs):
        self.messages.bstack11llll1l1l_opy_()
        current_test_id = bstack1ll111l1ll_opy_(threading.current_thread(), bstack111l11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡦࠪ඘"), None)
        bstack11llll111l_opy_ = current_test_id if bstack1ll111l1ll_opy_(threading.current_thread(), bstack111l11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡧࠫ඙"), None) else bstack1ll111l1ll_opy_(threading.current_thread(), bstack111l11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡸࡻࡩࡵࡧࡢ࡭ࡩ࠭ක"), None)
        if attrs.get(bstack111l11_opy_ (u"ࠫࡹࡿࡰࡦࠩඛ"), bstack111l11_opy_ (u"ࠬ࠭ග")).lower() in [bstack111l11_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬඝ"), bstack111l11_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࠩඞ")]:
            hook_type = bstack1l111l1111_opy_(attrs.get(bstack111l11_opy_ (u"ࠨࡶࡼࡴࡪ࠭ඟ")), bstack1ll111l1ll_opy_(threading.current_thread(), bstack111l11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭ච"), None))
            hook_name = bstack111l11_opy_ (u"ࠪࡿࢂ࠭ඡ").format(attrs.get(bstack111l11_opy_ (u"ࠫࡰࡽ࡮ࡢ࡯ࡨࠫජ"), bstack111l11_opy_ (u"ࠬ࠭ඣ")))
            if hook_type in [bstack111l11_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡁࡍࡎࠪඤ"), bstack111l11_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡁࡍࡎࠪඥ")]:
                hook_name = bstack111l11_opy_ (u"ࠨ࡝ࡾࢁࡢࠦࡻࡾࠩඦ").format(bstack11lllll11l_opy_.get(hook_type), attrs.get(bstack111l11_opy_ (u"ࠩ࡮ࡻࡳࡧ࡭ࡦࠩට"), bstack111l11_opy_ (u"ࠪࠫඨ")))
            bstack1l1111lll1_opy_ = bstack11lll11111_opy_(
                bstack1l11111l1l_opy_=bstack11llll111l_opy_ + bstack111l11_opy_ (u"ࠫ࠲࠭ඩ") + attrs.get(bstack111l11_opy_ (u"ࠬࡺࡹࡱࡧࠪඪ"), bstack111l11_opy_ (u"࠭ࠧණ")).lower(),
                name=hook_name,
                bstack11llllll11_opy_=bstack11ll1l1ll_opy_(),
                file_path=os.path.relpath(attrs.get(bstack111l11_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧඬ")), start=os.getcwd()),
                framework=bstack111l11_opy_ (u"ࠨࡔࡲࡦࡴࡺࠧත"),
                tags=attrs[bstack111l11_opy_ (u"ࠩࡷࡥ࡬ࡹࠧථ")],
                scope=RobotHandler.bstack1l1111111l_opy_(attrs.get(bstack111l11_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪද"), None)),
                hook_type=hook_type,
                meta={}
            )
            threading.current_thread().current_hook_uuid = bstack1l1111lll1_opy_.bstack11lll11ll1_opy_()
            threading.current_thread().current_hook_id = bstack11llll111l_opy_ + bstack111l11_opy_ (u"ࠫ࠲࠭ධ") + attrs.get(bstack111l11_opy_ (u"ࠬࡺࡹࡱࡧࠪන"), bstack111l11_opy_ (u"࠭ࠧ඲")).lower()
            self.store[bstack111l11_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫඳ")] = [bstack1l1111lll1_opy_.bstack11lll11ll1_opy_()]
            if bstack1ll111l1ll_opy_(threading.current_thread(), bstack111l11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬප"), None):
                self.store[bstack111l11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡸ࠭ඵ")].append(bstack1l1111lll1_opy_.bstack11lll11ll1_opy_())
            else:
                self.store[bstack111l11_opy_ (u"ࠪ࡫ࡱࡵࡢࡢ࡮ࡢ࡬ࡴࡵ࡫ࡴࠩබ")].append(bstack1l1111lll1_opy_.bstack11lll11ll1_opy_())
            if bstack11llll111l_opy_:
                self._11lll1lll1_opy_[bstack11llll111l_opy_ + bstack111l11_opy_ (u"ࠫ࠲࠭භ") + attrs.get(bstack111l11_opy_ (u"ࠬࡺࡹࡱࡧࠪම"), bstack111l11_opy_ (u"࠭ࠧඹ")).lower()] = { bstack111l11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪය"): bstack1l1111lll1_opy_ }
            bstack1lll1ll1l_opy_.bstack1l111l1l11_opy_(bstack111l11_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩර"), bstack1l1111lll1_opy_)
        else:
            bstack11lll111ll_opy_ = {
                bstack111l11_opy_ (u"ࠩ࡬ࡨࠬ඼"): uuid4().__str__(),
                bstack111l11_opy_ (u"ࠪࡸࡪࡾࡴࠨල"): bstack111l11_opy_ (u"ࠫࢀࢃࠠࡼࡿࠪ඾").format(attrs.get(bstack111l11_opy_ (u"ࠬࡱࡷ࡯ࡣࡰࡩࠬ඿")), attrs.get(bstack111l11_opy_ (u"࠭ࡡࡳࡩࡶࠫව"), bstack111l11_opy_ (u"ࠧࠨශ"))) if attrs.get(bstack111l11_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ෂ"), []) else attrs.get(bstack111l11_opy_ (u"ࠩ࡮ࡻࡳࡧ࡭ࡦࠩස")),
                bstack111l11_opy_ (u"ࠪࡷࡹ࡫ࡰࡠࡣࡵ࡫ࡺࡳࡥ࡯ࡶࠪහ"): attrs.get(bstack111l11_opy_ (u"ࠫࡦࡸࡧࡴࠩළ"), []),
                bstack111l11_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩෆ"): bstack11ll1l1ll_opy_(),
                bstack111l11_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭෇"): bstack111l11_opy_ (u"ࠧࡱࡧࡱࡨ࡮ࡴࡧࠨ෈"),
                bstack111l11_opy_ (u"ࠨࡦࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳ࠭෉"): attrs.get(bstack111l11_opy_ (u"ࠩࡧࡳࡨ්࠭"), bstack111l11_opy_ (u"ࠪࠫ෋"))
            }
            if attrs.get(bstack111l11_opy_ (u"ࠫࡱ࡯ࡢ࡯ࡣࡰࡩࠬ෌"), bstack111l11_opy_ (u"ࠬ࠭෍")) != bstack111l11_opy_ (u"࠭ࠧ෎"):
                bstack11lll111ll_opy_[bstack111l11_opy_ (u"ࠧ࡬ࡧࡼࡻࡴࡸࡤࠨා")] = attrs.get(bstack111l11_opy_ (u"ࠨ࡮࡬ࡦࡳࡧ࡭ࡦࠩැ"))
            if not self.bstack1l11111111_opy_:
                self._11lll1lll1_opy_[self._11lll1ll1l_opy_()][bstack111l11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬෑ")].add_step(bstack11lll111ll_opy_)
                threading.current_thread().current_step_uuid = bstack11lll111ll_opy_[bstack111l11_opy_ (u"ࠪ࡭ࡩ࠭ි")]
            self.bstack1l11111111_opy_.append(bstack11lll111ll_opy_)
    @bstack1l1111ll11_opy_(class_method=True)
    def end_keyword(self, name, attrs):
        messages = self.messages.bstack11lll111l1_opy_()
        self._1l1111l11l_opy_(messages)
        current_test_id = bstack1ll111l1ll_opy_(threading.current_thread(), bstack111l11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡩ࠭ී"), None)
        bstack11llll111l_opy_ = current_test_id if current_test_id else bstack1ll111l1ll_opy_(threading.current_thread(), bstack111l11_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡳࡶ࡫ࡷࡩࡤ࡯ࡤࠨු"), None)
        bstack11lll11l1l_opy_ = bstack11llll11ll_opy_.get(attrs.get(bstack111l11_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭෕")), bstack111l11_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨූ"))
        bstack1l111l11ll_opy_ = attrs.get(bstack111l11_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ෗"))
        if bstack11lll11l1l_opy_ != bstack111l11_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪෘ") and not attrs.get(bstack111l11_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫෙ")) and self._1l111lllll_opy_:
            bstack1l111l11ll_opy_ = self._1l111lllll_opy_
        bstack1l111l1l1l_opy_ = Result(result=bstack11lll11l1l_opy_, exception=bstack1l111l11ll_opy_, bstack11llllll1l_opy_=[bstack1l111l11ll_opy_])
        if attrs.get(bstack111l11_opy_ (u"ࠫࡹࡿࡰࡦࠩේ"), bstack111l11_opy_ (u"ࠬ࠭ෛ")).lower() in [bstack111l11_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬො"), bstack111l11_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࠩෝ")]:
            bstack11llll111l_opy_ = current_test_id if current_test_id else bstack1ll111l1ll_opy_(threading.current_thread(), bstack111l11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡶࡹ࡮ࡺࡥࡠ࡫ࡧࠫෞ"), None)
            if bstack11llll111l_opy_:
                bstack11llll11l1_opy_ = bstack11llll111l_opy_ + bstack111l11_opy_ (u"ࠤ࠰ࠦෟ") + attrs.get(bstack111l11_opy_ (u"ࠪࡸࡾࡶࡥࠨ෠"), bstack111l11_opy_ (u"ࠫࠬ෡")).lower()
                self._11lll1lll1_opy_[bstack11llll11l1_opy_][bstack111l11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ෢")].stop(time=bstack11ll1l1ll_opy_(), duration=int(attrs.get(bstack111l11_opy_ (u"࠭ࡥ࡭ࡣࡳࡷࡪࡪࡴࡪ࡯ࡨࠫ෣"), bstack111l11_opy_ (u"ࠧ࠱ࠩ෤"))), result=bstack1l111l1l1l_opy_)
                bstack1lll1ll1l_opy_.bstack1l111l1l11_opy_(bstack111l11_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪ෥"), self._11lll1lll1_opy_[bstack11llll11l1_opy_][bstack111l11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ෦")])
        else:
            bstack11llll111l_opy_ = current_test_id if current_test_id else bstack1ll111l1ll_opy_(threading.current_thread(), bstack111l11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡ࡬ࡨࠬ෧"), None)
            if bstack11llll111l_opy_ and len(self.bstack1l11111111_opy_) == 1:
                current_step_uuid = bstack1ll111l1ll_opy_(threading.current_thread(), bstack111l11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡹࡴࡦࡲࡢࡹࡺ࡯ࡤࠨ෨"), None)
                self._11lll1lll1_opy_[bstack11llll111l_opy_][bstack111l11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ෩")].bstack1l1111l111_opy_(current_step_uuid, duration=int(attrs.get(bstack111l11_opy_ (u"࠭ࡥ࡭ࡣࡳࡷࡪࡪࡴࡪ࡯ࡨࠫ෪"), bstack111l11_opy_ (u"ࠧ࠱ࠩ෫"))), result=bstack1l111l1l1l_opy_)
            else:
                self.bstack11lllll1l1_opy_(attrs)
            self.bstack1l11111111_opy_.pop()
    def log_message(self, message):
        try:
            if message.get(bstack111l11_opy_ (u"ࠨࡪࡷࡱࡱ࠭෬"), bstack111l11_opy_ (u"ࠩࡱࡳࠬ෭")) == bstack111l11_opy_ (u"ࠪࡽࡪࡹࠧ෮"):
                return
            self.messages.push(message)
            bstack1l111ll1l1_opy_ = []
            if bstack1lll1ll1l_opy_.bstack11llll1ll1_opy_():
                bstack1l111ll1l1_opy_.append({
                    bstack111l11_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧ෯"): bstack11ll1l1ll_opy_(),
                    bstack111l11_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭෰"): message.get(bstack111l11_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ෱")),
                    bstack111l11_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ෲ"): message.get(bstack111l11_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧෳ")),
                    **bstack1lll1ll1l_opy_.bstack11llll1ll1_opy_()
                })
                if len(bstack1l111ll1l1_opy_) > 0:
                    bstack1lll1ll1l_opy_.bstack1l11111l1_opy_(bstack1l111ll1l1_opy_)
        except Exception as err:
            pass
    def close(self):
        bstack1lll1ll1l_opy_.bstack11lll1l1l1_opy_()
    def bstack11lllll1l1_opy_(self, bstack1l1111ll1l_opy_):
        if not bstack1lll1ll1l_opy_.bstack11llll1ll1_opy_():
            return
        kwname = bstack111l11_opy_ (u"ࠩࡾࢁࠥࢁࡽࠨ෴").format(bstack1l1111ll1l_opy_.get(bstack111l11_opy_ (u"ࠪ࡯ࡼࡴࡡ࡮ࡧࠪ෵")), bstack1l1111ll1l_opy_.get(bstack111l11_opy_ (u"ࠫࡦࡸࡧࡴࠩ෶"), bstack111l11_opy_ (u"ࠬ࠭෷"))) if bstack1l1111ll1l_opy_.get(bstack111l11_opy_ (u"࠭ࡡࡳࡩࡶࠫ෸"), []) else bstack1l1111ll1l_opy_.get(bstack111l11_opy_ (u"ࠧ࡬ࡹࡱࡥࡲ࡫ࠧ෹"))
        error_message = bstack111l11_opy_ (u"ࠣ࡭ࡺࡲࡦࡳࡥ࠻ࠢ࡟ࠦࢀ࠶ࡽ࡝ࠤࠣࢀࠥࡹࡴࡢࡶࡸࡷ࠿ࠦ࡜ࠣࡽ࠴ࢁࡡࠨࠠࡽࠢࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲ࠿ࠦ࡜ࠣࡽ࠵ࢁࡡࠨࠢ෺").format(kwname, bstack1l1111ll1l_opy_.get(bstack111l11_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩ෻")), str(bstack1l1111ll1l_opy_.get(bstack111l11_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ෼"))))
        bstack11lll1l11l_opy_ = bstack111l11_opy_ (u"ࠦࡰࡽ࡮ࡢ࡯ࡨ࠾ࠥࡢࠢࡼ࠲ࢀࡠࠧࠦࡼࠡࡵࡷࡥࡹࡻࡳ࠻ࠢ࡟ࠦࢀ࠷ࡽ࡝ࠤࠥ෽").format(kwname, bstack1l1111ll1l_opy_.get(bstack111l11_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬ෾")))
        bstack1l1111l1l1_opy_ = error_message if bstack1l1111ll1l_opy_.get(bstack111l11_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ෿")) else bstack11lll1l11l_opy_
        bstack1l111111ll_opy_ = {
            bstack111l11_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪ฀"): self.bstack1l11111111_opy_[-1].get(bstack111l11_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬก"), bstack11ll1l1ll_opy_()),
            bstack111l11_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪข"): bstack1l1111l1l1_opy_,
            bstack111l11_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩฃ"): bstack111l11_opy_ (u"ࠫࡊࡘࡒࡐࡔࠪค") if bstack1l1111ll1l_opy_.get(bstack111l11_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬฅ")) == bstack111l11_opy_ (u"࠭ࡆࡂࡋࡏࠫฆ") else bstack111l11_opy_ (u"ࠧࡊࡐࡉࡓࠬง"),
            **bstack1lll1ll1l_opy_.bstack11llll1ll1_opy_()
        }
        bstack1lll1ll1l_opy_.bstack1l11111l1_opy_([bstack1l111111ll_opy_])
    def _11lll1ll1l_opy_(self):
        for bstack1l11111l1l_opy_ in reversed(self._11lll1lll1_opy_):
            bstack11llllllll_opy_ = bstack1l11111l1l_opy_
            data = self._11lll1lll1_opy_[bstack1l11111l1l_opy_][bstack111l11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫจ")]
            if isinstance(data, bstack11lll11111_opy_):
                if not bstack111l11_opy_ (u"ࠩࡈࡅࡈࡎࠧฉ") in data.bstack11lllll111_opy_():
                    return bstack11llllllll_opy_
            else:
                return bstack11llllllll_opy_
    def _1l1111l11l_opy_(self, messages):
        try:
            bstack1l1111llll_opy_ = BuiltIn().get_variable_value(bstack111l11_opy_ (u"ࠥࠨࢀࡒࡏࡈࠢࡏࡉ࡛ࡋࡌࡾࠤช")) in (bstack11lll1l111_opy_.DEBUG, bstack11lll1l111_opy_.TRACE)
            for message, bstack11lllll1ll_opy_ in zip_longest(messages, messages[1:]):
                name = message.get(bstack111l11_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬซ"))
                level = message.get(bstack111l11_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫฌ"))
                if level == bstack11lll1l111_opy_.FAIL:
                    self._1l111lllll_opy_ = name or self._1l111lllll_opy_
                    self._1l111lll11_opy_ = bstack11lllll1ll_opy_.get(bstack111l11_opy_ (u"ࠨ࡭ࡦࡵࡶࡥ࡬࡫ࠢญ")) if bstack1l1111llll_opy_ and bstack11lllll1ll_opy_ else self._1l111lll11_opy_
        except:
            pass
    @classmethod
    def bstack1l111l1l11_opy_(self, event: str, bstack1l111lll1l_opy_: bstack1l111l111l_opy_, bstack1l111ll11l_opy_=False):
        if event == bstack111l11_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩฎ"):
            bstack1l111lll1l_opy_.set(hooks=self.store[bstack111l11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡷࠬฏ")])
        if event == bstack111l11_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖ࡯࡮ࡶࡰࡦࡦࠪฐ"):
            event = bstack111l11_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬฑ")
        if bstack1l111ll11l_opy_:
            bstack1l1111l1ll_opy_ = {
                bstack111l11_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨฒ"): event,
                bstack1l111lll1l_opy_.bstack11llll1111_opy_(): bstack1l111lll1l_opy_.bstack11lllllll1_opy_(event)
            }
            self.bstack1l111l1lll_opy_.append(bstack1l1111l1ll_opy_)
        else:
            bstack1lll1ll1l_opy_.bstack1l111l1l11_opy_(event, bstack1l111lll1l_opy_)
class Messages:
    def __init__(self):
        self._11lll11lll_opy_ = []
    def bstack11llll1l1l_opy_(self):
        self._11lll11lll_opy_.append([])
    def bstack11lll111l1_opy_(self):
        return self._11lll11lll_opy_.pop() if self._11lll11lll_opy_ else list()
    def push(self, message):
        self._11lll11lll_opy_[-1].append(message) if self._11lll11lll_opy_ else self._11lll11lll_opy_.append([message])
class bstack11lll1l111_opy_:
    FAIL = bstack111l11_opy_ (u"ࠬࡌࡁࡊࡎࠪณ")
    ERROR = bstack111l11_opy_ (u"࠭ࡅࡓࡔࡒࡖࠬด")
    WARNING = bstack111l11_opy_ (u"ࠧࡘࡃࡕࡒࠬต")
    bstack1l11111ll1_opy_ = bstack111l11_opy_ (u"ࠨࡋࡑࡊࡔ࠭ถ")
    DEBUG = bstack111l11_opy_ (u"ࠩࡇࡉࡇ࡛ࡇࠨท")
    TRACE = bstack111l11_opy_ (u"ࠪࡘࡗࡇࡃࡆࠩธ")
    bstack11lll11l11_opy_ = [FAIL, ERROR]
def bstack1l11111lll_opy_(bstack11llll1l11_opy_):
    if not bstack11llll1l11_opy_:
        return None
    if bstack11llll1l11_opy_.get(bstack111l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧน"), None):
        return getattr(bstack11llll1l11_opy_[bstack111l11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨบ")], bstack111l11_opy_ (u"࠭ࡵࡶ࡫ࡧࠫป"), None)
    return bstack11llll1l11_opy_.get(bstack111l11_opy_ (u"ࠧࡶࡷ࡬ࡨࠬผ"), None)
def bstack1l111l1111_opy_(hook_type, current_test_uuid):
    if hook_type.lower() not in [bstack111l11_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧฝ"), bstack111l11_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫพ")]:
        return
    if hook_type.lower() == bstack111l11_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩฟ"):
        if current_test_uuid is None:
            return bstack111l11_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡆࡒࡌࠨภ")
        else:
            return bstack111l11_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡋࡁࡄࡊࠪม")
    elif hook_type.lower() == bstack111l11_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࠨย"):
        if current_test_uuid is None:
            return bstack111l11_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡁࡍࡎࠪร")
        else:
            return bstack111l11_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡆࡃࡆࡌࠬฤ")
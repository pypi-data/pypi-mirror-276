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
import atexit
import datetime
import inspect
import logging
import os
import signal
import sys
import threading
from uuid import uuid4
from bstack_utils.percy_sdk import PercySDK
import tempfile
import pytest
from packaging import version
from browserstack_sdk.__init__ import (bstack111ll11ll_opy_, bstack111ll1ll_opy_, update, bstack1l1llll1l1_opy_,
                                       bstack11l11lll_opy_, bstack1111lll11_opy_, bstack1l11lll1ll_opy_, bstack1llll1lll_opy_,
                                       bstack1l11lll1_opy_, bstack1l11lllll1_opy_, bstack1lll11lll_opy_, bstack1l1ll1ll_opy_,
                                       bstack11ll11111_opy_, getAccessibilityResults, getAccessibilityResultsSummary, perform_scan, bstack1l1111l1l_opy_)
from browserstack_sdk.bstack11111lll1_opy_ import bstack1l11l111l_opy_
from browserstack_sdk._version import __version__
from bstack_utils import bstack1l1l1l1l1_opy_
from bstack_utils.capture import bstack1l111111l1_opy_
from bstack_utils.config import Config
from bstack_utils.constants import bstack111lll1l_opy_, bstack1l111lll_opy_, bstack11l11lll1_opy_, \
    bstack1llll1ll1_opy_
from bstack_utils.helper import bstack1ll111l1ll_opy_, bstack111l11llll_opy_, bstack1l111llll1_opy_, bstack1ll1l11l11_opy_, bstack111ll1ll1l_opy_, bstack11ll1l1ll_opy_, \
    bstack11l11l1ll1_opy_, \
    bstack111lll11l1_opy_, bstack1lll1l1ll_opy_, bstack1l1l1l111_opy_, bstack111l1l1l1l_opy_, bstack11l1l111_opy_, Notset, \
    bstack11ll111ll_opy_, bstack11l11l11l1_opy_, bstack11l1111ll1_opy_, Result, bstack111ll1111l_opy_, bstack111l1lll11_opy_, bstack1l1111ll11_opy_, \
    bstack111llllll_opy_, bstack1l1l1lll11_opy_, bstack1ll11l1l11_opy_, bstack11l111111l_opy_
from bstack_utils.bstack111l111111_opy_ import bstack1111llllll_opy_
from bstack_utils.messages import bstack1lllll1l11_opy_, bstack1ll1l111l1_opy_, bstack1ll11l1l1_opy_, bstack1lll111l1l_opy_, bstack1l11l1l1_opy_, \
    bstack1l1l1lllll_opy_, bstack1ll11111l_opy_, bstack111l11111_opy_, bstack1l1l111l1_opy_, bstack11lll11l1_opy_, \
    bstack11llll111_opy_, bstack1ll1l111l_opy_
from bstack_utils.proxy import bstack1llll1l11_opy_, bstack1l1l11l11l_opy_
from bstack_utils.bstack1llll1ll11_opy_ import bstack1llll1ll1ll_opy_, bstack1llll1l1l11_opy_, bstack1llll1ll11l_opy_, bstack1llll1l1lll_opy_, \
    bstack1lllll11111_opy_, bstack1llll1l11ll_opy_, bstack1llll1llll1_opy_, bstack1l1l11ll11_opy_, bstack1llll1lllll_opy_
from bstack_utils.bstack1ll1lll1l_opy_ import bstack1ll1lll11l_opy_
from bstack_utils.bstack1ll11ll111_opy_ import bstack1l11l1l111_opy_, bstack11l111ll1_opy_, bstack111llll1l_opy_, \
    bstack1l1l11llll_opy_, bstack111111l1_opy_
from bstack_utils.bstack1l111l1ll1_opy_ import bstack11lll1ll11_opy_
from bstack_utils.bstack1l1l1l1l1l_opy_ import bstack1lll1ll1l_opy_
import bstack_utils.bstack1111llll_opy_ as bstack1llll11l_opy_
from bstack_utils.bstack1l1lll1lll_opy_ import bstack1l1lll1lll_opy_
bstack1ll111l11l_opy_ = None
bstack11l1lll1_opy_ = None
bstack1l11ll11_opy_ = None
bstack1l1ll1l1_opy_ = None
bstack1ll1l1ll1l_opy_ = None
bstack1lll1llll_opy_ = None
bstack111l1l11_opy_ = None
bstack111l1l1l1_opy_ = None
bstack1l1ll1l11l_opy_ = None
bstack1llll111l_opy_ = None
bstack1llll1ll_opy_ = None
bstack111l1llll_opy_ = None
bstack1lll1ll1ll_opy_ = None
bstack1lll1ll11_opy_ = bstack111l11_opy_ (u"ࠧࠨᗼ")
CONFIG = {}
bstack1lll11l11_opy_ = False
bstack1l1l11l11_opy_ = bstack111l11_opy_ (u"ࠨࠩᗽ")
bstack1l11ll1l_opy_ = bstack111l11_opy_ (u"ࠩࠪᗾ")
bstack111lll1ll_opy_ = False
bstack1l1l1ll1l1_opy_ = []
bstack111llll11_opy_ = bstack111lll1l_opy_
bstack1lll11l111l_opy_ = bstack111l11_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪᗿ")
bstack1lll111l111_opy_ = False
bstack1l1lll11l_opy_ = {}
bstack1l1ll11l_opy_ = False
logger = bstack1l1l1l1l1_opy_.get_logger(__name__, bstack111llll11_opy_)
store = {
    bstack111l11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨᘀ"): []
}
bstack1lll11l11l1_opy_ = False
try:
    from playwright.sync_api import (
        BrowserContext,
        Page
    )
except:
    pass
import json
_11lll1lll1_opy_ = {}
current_test_uuid = None
def bstack11111111_opy_(page, bstack1l11lll11l_opy_):
    try:
        page.evaluate(bstack111l11_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨᘁ"),
                      bstack111l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡲࡦࡳࡥࠣ࠼ࠪᘂ") + json.dumps(
                          bstack1l11lll11l_opy_) + bstack111l11_opy_ (u"ࠢࡾࡿࠥᘃ"))
    except Exception as e:
        print(bstack111l11_opy_ (u"ࠣࡧࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧࠣࡿࢂࠨᘄ"), e)
def bstack1lll1l1111_opy_(page, message, level):
    try:
        page.evaluate(bstack111l11_opy_ (u"ࠤࡢࠤࡂࡄࠠࡼࡿࠥᘅ"), bstack111l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡦࡤࡸࡦࠨ࠺ࠨᘆ") + json.dumps(
            message) + bstack111l11_opy_ (u"ࠫ࠱ࠨ࡬ࡦࡸࡨࡰࠧࡀࠧᘇ") + json.dumps(level) + bstack111l11_opy_ (u"ࠬࢃࡽࠨᘈ"))
    except Exception as e:
        print(bstack111l11_opy_ (u"ࠨࡥࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡤࡲࡳࡵࡴࡢࡶ࡬ࡳࡳࠦࡻࡾࠤᘉ"), e)
def pytest_configure(config):
    bstack1l11l111ll_opy_ = Config.bstack1l1l1l1111_opy_()
    config.args = bstack1lll1ll1l_opy_.bstack1lll1l11ll1_opy_(config.args)
    bstack1l11l111ll_opy_.bstack1l1lll11l1_opy_(bstack1ll11l1l11_opy_(config.getoption(bstack111l11_opy_ (u"ࠧࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫᘊ"))))
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    bstack1ll1lll1l11_opy_ = item.config.getoption(bstack111l11_opy_ (u"ࠨࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪᘋ"))
    plugins = item.config.getoption(bstack111l11_opy_ (u"ࠤࡳࡰࡺ࡭ࡩ࡯ࡵࠥᘌ"))
    report = outcome.get_result()
    bstack1ll1lll1l1l_opy_(item, call, report)
    if bstack111l11_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶࡢࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡲ࡯ࡹ࡬࡯࡮ࠣᘍ") not in plugins or bstack11l1l111_opy_():
        return
    summary = []
    driver = getattr(item, bstack111l11_opy_ (u"ࠦࡤࡪࡲࡪࡸࡨࡶࠧᘎ"), None)
    page = getattr(item, bstack111l11_opy_ (u"ࠧࡥࡰࡢࡩࡨࠦᘏ"), None)
    try:
        if (driver == None):
            driver = threading.current_thread().bstackSessionDriver
    except:
        pass
    item._driver = driver
    if (driver is not None):
        bstack1ll1llll111_opy_(item, report, summary, bstack1ll1lll1l11_opy_)
    if (page is not None):
        bstack1lll111llll_opy_(item, report, summary, bstack1ll1lll1l11_opy_)
def bstack1ll1llll111_opy_(item, report, summary, bstack1ll1lll1l11_opy_):
    if report.when == bstack111l11_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬᘐ") and report.skipped:
        bstack1llll1lllll_opy_(report)
    if report.when in [bstack111l11_opy_ (u"ࠢࡴࡧࡷࡹࡵࠨᘑ"), bstack111l11_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࠥᘒ")]:
        return
    if not bstack111ll1ll1l_opy_():
        return
    try:
        if (str(bstack1ll1lll1l11_opy_).lower() != bstack111l11_opy_ (u"ࠩࡷࡶࡺ࡫ࠧᘓ")):
            item._driver.execute_script(
                bstack111l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢ࡯ࡣࡰࡩࠧࡀࠠࠨᘔ") + json.dumps(
                    report.nodeid) + bstack111l11_opy_ (u"ࠫࢂࢃࠧᘕ"))
        os.environ[bstack111l11_opy_ (u"ࠬࡖ࡙ࡕࡇࡖࡘࡤ࡚ࡅࡔࡖࡢࡒࡆࡓࡅࠨᘖ")] = report.nodeid
    except Exception as e:
        summary.append(
            bstack111l11_opy_ (u"ࠨࡗࡂࡔࡑࡍࡓࡍ࠺ࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡲࡧࡲ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠣࡲࡦࡳࡥ࠻ࠢࡾ࠴ࢂࠨᘗ").format(e)
        )
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack111l11_opy_ (u"ࠢࡸࡣࡶࡼ࡫ࡧࡩ࡭ࠤᘘ")))
    bstack1lll1lll1_opy_ = bstack111l11_opy_ (u"ࠣࠤᘙ")
    bstack1llll1lllll_opy_(report)
    if not passed:
        try:
            bstack1lll1lll1_opy_ = report.longrepr.reprcrash
        except Exception as e:
            summary.append(
                bstack111l11_opy_ (u"ࠤ࡚ࡅࡗࡔࡉࡏࡉ࠽ࠤࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡥࡧࡷࡩࡷࡳࡩ࡯ࡧࠣࡪࡦ࡯࡬ࡶࡴࡨࠤࡷ࡫ࡡࡴࡱࡱ࠾ࠥࢁ࠰ࡾࠤᘚ").format(e)
            )
        try:
            if (threading.current_thread().bstackTestErrorMessages == None):
                threading.current_thread().bstackTestErrorMessages = []
        except Exception as e:
            threading.current_thread().bstackTestErrorMessages = []
        threading.current_thread().bstackTestErrorMessages.append(str(bstack1lll1lll1_opy_))
    if not report.skipped:
        passed = report.passed or (report.failed and hasattr(report, bstack111l11_opy_ (u"ࠥࡻࡦࡹࡸࡧࡣ࡬ࡰࠧᘛ")))
        bstack1lll1lll1_opy_ = bstack111l11_opy_ (u"ࠦࠧᘜ")
        if not passed:
            try:
                bstack1lll1lll1_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack111l11_opy_ (u"ࠧ࡝ࡁࡓࡐࡌࡒࡌࡀࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡨࡪࡺࡥࡳ࡯࡬ࡲࡪࠦࡦࡢ࡫࡯ࡹࡷ࡫ࠠࡳࡧࡤࡷࡴࡴ࠺ࠡࡽ࠳ࢁࠧᘝ").format(e)
                )
            try:
                if (threading.current_thread().bstackTestErrorMessages == None):
                    threading.current_thread().bstackTestErrorMessages = []
            except Exception as e:
                threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(str(bstack1lll1lll1_opy_))
        try:
            if passed:
                item._driver.execute_script(
                    bstack111l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢ࡭ࡧࡹࡩࡱࠨ࠺ࠡࠤ࡬ࡲ࡫ࡵࠢ࠭ࠢ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤࡧࡥࡹࡧࠢ࠻ࠢࠪᘞ")
                    + json.dumps(bstack111l11_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠡࠣᘟ"))
                    + bstack111l11_opy_ (u"ࠣ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࢁࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࢀࠦᘠ")
                )
            else:
                item._driver.execute_script(
                    bstack111l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡰࡪࡼࡥ࡭ࠤ࠽ࠤࠧ࡫ࡲࡳࡱࡵࠦ࠱ࠦ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠨࡤࡢࡶࡤࠦ࠿ࠦࠧᘡ")
                    + json.dumps(str(bstack1lll1lll1_opy_))
                    + bstack111l11_opy_ (u"ࠥࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࢃ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࢂࠨᘢ")
                )
        except Exception as e:
            summary.append(bstack111l11_opy_ (u"ࠦ࡜ࡇࡒࡏࡋࡑࡋ࠿ࠦࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡤࡲࡳࡵࡴࡢࡶࡨ࠾ࠥࢁ࠰ࡾࠤᘣ").format(e))
def bstack1lll11111ll_opy_(test_name, error_message):
    try:
        bstack1ll1lllll11_opy_ = []
        bstack1ll11lllll_opy_ = os.environ.get(bstack111l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬᘤ"), bstack111l11_opy_ (u"࠭࠰ࠨᘥ"))
        bstack11l1l11l_opy_ = {bstack111l11_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᘦ"): test_name, bstack111l11_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧᘧ"): error_message, bstack111l11_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨᘨ"): bstack1ll11lllll_opy_}
        bstack1lll111l11l_opy_ = os.path.join(tempfile.gettempdir(), bstack111l11_opy_ (u"ࠪࡴࡼࡥࡰࡺࡶࡨࡷࡹࡥࡥࡳࡴࡲࡶࡤࡲࡩࡴࡶ࠱࡮ࡸࡵ࡮ࠨᘩ"))
        if os.path.exists(bstack1lll111l11l_opy_):
            with open(bstack1lll111l11l_opy_) as f:
                bstack1ll1lllll11_opy_ = json.load(f)
        bstack1ll1lllll11_opy_.append(bstack11l1l11l_opy_)
        with open(bstack1lll111l11l_opy_, bstack111l11_opy_ (u"ࠫࡼ࠭ᘪ")) as f:
            json.dump(bstack1ll1lllll11_opy_, f)
    except Exception as e:
        logger.debug(bstack111l11_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡱࡧࡵࡷ࡮ࡹࡴࡪࡰࡪࠤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡲࡼࡸࡪࡹࡴࠡࡧࡵࡶࡴࡸࡳ࠻ࠢࠪᘫ") + str(e))
def bstack1lll111llll_opy_(item, report, summary, bstack1ll1lll1l11_opy_):
    if report.when in [bstack111l11_opy_ (u"ࠨࡳࡦࡶࡸࡴࠧᘬ"), bstack111l11_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࠤᘭ")]:
        return
    if (str(bstack1ll1lll1l11_opy_).lower() != bstack111l11_opy_ (u"ࠨࡶࡵࡹࡪ࠭ᘮ")):
        bstack11111111_opy_(item._page, report.nodeid)
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack111l11_opy_ (u"ࠤࡺࡥࡸࡾࡦࡢ࡫࡯ࠦᘯ")))
    bstack1lll1lll1_opy_ = bstack111l11_opy_ (u"ࠥࠦᘰ")
    bstack1llll1lllll_opy_(report)
    if not report.skipped:
        if not passed:
            try:
                bstack1lll1lll1_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack111l11_opy_ (u"ࠦ࡜ࡇࡒࡏࡋࡑࡋ࠿ࠦࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡧࡩࡹ࡫ࡲ࡮࡫ࡱࡩࠥ࡬ࡡࡪ࡮ࡸࡶࡪࠦࡲࡦࡣࡶࡳࡳࡀࠠࡼ࠲ࢀࠦᘱ").format(e)
                )
        try:
            if passed:
                bstack111111l1_opy_(getattr(item, bstack111l11_opy_ (u"ࠬࡥࡰࡢࡩࡨࠫᘲ"), None), bstack111l11_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠨᘳ"))
            else:
                error_message = bstack111l11_opy_ (u"ࠧࠨᘴ")
                if bstack1lll1lll1_opy_:
                    bstack1lll1l1111_opy_(item._page, str(bstack1lll1lll1_opy_), bstack111l11_opy_ (u"ࠣࡧࡵࡶࡴࡸࠢᘵ"))
                    bstack111111l1_opy_(getattr(item, bstack111l11_opy_ (u"ࠩࡢࡴࡦ࡭ࡥࠨᘶ"), None), bstack111l11_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥᘷ"), str(bstack1lll1lll1_opy_))
                    error_message = str(bstack1lll1lll1_opy_)
                else:
                    bstack111111l1_opy_(getattr(item, bstack111l11_opy_ (u"ࠫࡤࡶࡡࡨࡧࠪᘸ"), None), bstack111l11_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧᘹ"))
                bstack1lll11111ll_opy_(report.nodeid, error_message)
        except Exception as e:
            summary.append(bstack111l11_opy_ (u"ࠨࡗࡂࡔࡑࡍࡓࡍ࠺ࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡺࡶࡤࡢࡶࡨࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡹࡴࡢࡶࡸࡷ࠿ࠦࡻ࠱ࡿࠥᘺ").format(e))
try:
    from typing import Generator
    import pytest_playwright.pytest_playwright as p
    @pytest.fixture
    def page(context: BrowserContext, request: pytest.FixtureRequest) -> Generator[Page, None, None]:
        page = context.new_page()
        request.node._page = page
        yield page
except:
    pass
def pytest_addoption(parser):
    parser.addoption(bstack111l11_opy_ (u"ࠢ࠮࠯ࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠦᘻ"), default=bstack111l11_opy_ (u"ࠣࡈࡤࡰࡸ࡫ࠢᘼ"), help=bstack111l11_opy_ (u"ࠤࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡧࠥࡹࡥࡵࠢࡶࡩࡸࡹࡩࡰࡰࠣࡲࡦࡳࡥࠣᘽ"))
    parser.addoption(bstack111l11_opy_ (u"ࠥ࠱࠲ࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠤᘾ"), default=bstack111l11_opy_ (u"ࠦࡋࡧ࡬ࡴࡧࠥᘿ"), help=bstack111l11_opy_ (u"ࠧࡇࡵࡵࡱࡰࡥࡹ࡯ࡣࠡࡵࡨࡸࠥࡹࡥࡴࡵ࡬ࡳࡳࠦ࡮ࡢ࡯ࡨࠦᙀ"))
    try:
        import pytest_selenium.pytest_selenium
    except:
        parser.addoption(bstack111l11_opy_ (u"ࠨ࠭࠮ࡦࡵ࡭ࡻ࡫ࡲࠣᙁ"), action=bstack111l11_opy_ (u"ࠢࡴࡶࡲࡶࡪࠨᙂ"), default=bstack111l11_opy_ (u"ࠣࡥ࡫ࡶࡴࡳࡥࠣᙃ"),
                         help=bstack111l11_opy_ (u"ࠤࡇࡶ࡮ࡼࡥࡳࠢࡷࡳࠥࡸࡵ࡯ࠢࡷࡩࡸࡺࡳࠣᙄ"))
def bstack11lll1l1ll_opy_(log):
    if not (log[bstack111l11_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᙅ")] and log[bstack111l11_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᙆ")].strip()):
        return
    active = bstack11llll1ll1_opy_()
    log = {
        bstack111l11_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫᙇ"): log[bstack111l11_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬᙈ")],
        bstack111l11_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪᙉ"): bstack1l111llll1_opy_().isoformat() + bstack111l11_opy_ (u"ࠨ࡜ࠪᙊ"),
        bstack111l11_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᙋ"): log[bstack111l11_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᙌ")],
    }
    if active:
        if active[bstack111l11_opy_ (u"ࠫࡹࡿࡰࡦࠩᙍ")] == bstack111l11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪᙎ"):
            log[bstack111l11_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᙏ")] = active[bstack111l11_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᙐ")]
        elif active[bstack111l11_opy_ (u"ࠨࡶࡼࡴࡪ࠭ᙑ")] == bstack111l11_opy_ (u"ࠩࡷࡩࡸࡺࠧᙒ"):
            log[bstack111l11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᙓ")] = active[bstack111l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᙔ")]
    bstack1lll1ll1l_opy_.bstack1l11111l1_opy_([log])
def bstack11llll1ll1_opy_():
    if len(store[bstack111l11_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩᙕ")]) > 0 and store[bstack111l11_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪᙖ")][-1]:
        return {
            bstack111l11_opy_ (u"ࠧࡵࡻࡳࡩࠬᙗ"): bstack111l11_opy_ (u"ࠨࡪࡲࡳࡰ࠭ᙘ"),
            bstack111l11_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᙙ"): store[bstack111l11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧᙚ")][-1]
        }
    if store.get(bstack111l11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨᙛ"), None):
        return {
            bstack111l11_opy_ (u"ࠬࡺࡹࡱࡧࠪᙜ"): bstack111l11_opy_ (u"࠭ࡴࡦࡵࡷࠫᙝ"),
            bstack111l11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᙞ"): store[bstack111l11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬᙟ")]
        }
    return None
bstack1l11111l11_opy_ = bstack1l111111l1_opy_(bstack11lll1l1ll_opy_)
def pytest_runtest_call(item):
    try:
        global CONFIG
        global bstack1lll111l111_opy_
        item._1lll111111l_opy_ = True
        bstack1l11l1111_opy_ = bstack1llll11l_opy_.bstack1l1111l11_opy_(CONFIG, bstack111lll11l1_opy_(item.own_markers))
        item._a11y_test_case = bstack1l11l1111_opy_
        if bstack1lll111l111_opy_:
            driver = getattr(item, bstack111l11_opy_ (u"ࠩࡢࡨࡷ࡯ࡶࡦࡴࠪᙠ"), None)
            item._a11y_started = bstack1llll11l_opy_.bstack1llll1l111_opy_(driver, bstack1l11l1111_opy_)
        if not bstack1lll1ll1l_opy_.on() or bstack1lll11l111l_opy_ != bstack111l11_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪᙡ"):
            return
        global current_test_uuid, bstack1l11111l11_opy_
        bstack1l11111l11_opy_.start()
        bstack11llll1l11_opy_ = {
            bstack111l11_opy_ (u"ࠫࡺࡻࡩࡥࠩᙢ"): uuid4().__str__(),
            bstack111l11_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩᙣ"): bstack1l111llll1_opy_().isoformat() + bstack111l11_opy_ (u"࡚࠭ࠨᙤ")
        }
        current_test_uuid = bstack11llll1l11_opy_[bstack111l11_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᙥ")]
        store[bstack111l11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬᙦ")] = bstack11llll1l11_opy_[bstack111l11_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᙧ")]
        threading.current_thread().current_test_uuid = current_test_uuid
        _11lll1lll1_opy_[item.nodeid] = {**_11lll1lll1_opy_[item.nodeid], **bstack11llll1l11_opy_}
        bstack1lll111l1ll_opy_(item, _11lll1lll1_opy_[item.nodeid], bstack111l11_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫᙨ"))
    except Exception as err:
        print(bstack111l11_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶࡢࡶࡺࡴࡴࡦࡵࡷࡣࡨࡧ࡬࡭࠼ࠣࡿࢂ࠭ᙩ"), str(err))
def pytest_runtest_setup(item):
    global bstack1lll11l11l1_opy_
    threading.current_thread().percySessionName = item.nodeid
    if bstack111l1l1l1l_opy_():
        atexit.register(bstack1ll11l1111_opy_)
        if not bstack1lll11l11l1_opy_:
            try:
                bstack1lll1111l1l_opy_ = [signal.SIGINT, signal.SIGTERM]
                if not bstack11l111111l_opy_():
                    bstack1lll1111l1l_opy_.extend([signal.SIGHUP, signal.SIGQUIT])
                for s in bstack1lll1111l1l_opy_:
                    signal.signal(s, bstack1ll1lllll1l_opy_)
                bstack1lll11l11l1_opy_ = True
            except Exception as e:
                logger.debug(
                    bstack111l11_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡳࡧࡪ࡭ࡸࡺࡥࡳࠢࡶ࡭࡬ࡴࡡ࡭ࠢ࡫ࡥࡳࡪ࡬ࡦࡴࡶ࠾ࠥࠨᙪ") + str(e))
        try:
            item.config.hook.pytest_selenium_runtest_makereport = bstack1llll1ll1ll_opy_
        except Exception as err:
            threading.current_thread().testStatus = bstack111l11_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ᙫ")
    try:
        if not bstack1lll1ll1l_opy_.on():
            return
        bstack1l11111l11_opy_.start()
        uuid = uuid4().__str__()
        bstack11llll1l11_opy_ = {
            bstack111l11_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᙬ"): uuid,
            bstack111l11_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬ᙭"): bstack1l111llll1_opy_().isoformat() + bstack111l11_opy_ (u"ࠩ࡝ࠫ᙮"),
            bstack111l11_opy_ (u"ࠪࡸࡾࡶࡥࠨᙯ"): bstack111l11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩᙰ"),
            bstack111l11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡸࡾࡶࡥࠨᙱ"): bstack111l11_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡅࡂࡅࡋࠫᙲ"),
            bstack111l11_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡴࡡ࡮ࡧࠪᙳ"): bstack111l11_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧᙴ")
        }
        threading.current_thread().current_hook_uuid = uuid
        threading.current_thread().current_test_item = item
        store[bstack111l11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡷࡩࡲ࠭ᙵ")] = item
        store[bstack111l11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧᙶ")] = [uuid]
        if not _11lll1lll1_opy_.get(item.nodeid, None):
            _11lll1lll1_opy_[item.nodeid] = {bstack111l11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪᙷ"): [], bstack111l11_opy_ (u"ࠬ࡬ࡩࡹࡶࡸࡶࡪࡹࠧᙸ"): []}
        _11lll1lll1_opy_[item.nodeid][bstack111l11_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬᙹ")].append(bstack11llll1l11_opy_[bstack111l11_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᙺ")])
        _11lll1lll1_opy_[item.nodeid + bstack111l11_opy_ (u"ࠨ࠯ࡶࡩࡹࡻࡰࠨᙻ")] = bstack11llll1l11_opy_
        bstack1lll11l1l1l_opy_(item, bstack11llll1l11_opy_, bstack111l11_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪᙼ"))
    except Exception as err:
        print(bstack111l11_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵࡡࡵࡹࡳࡺࡥࡴࡶࡢࡷࡪࡺࡵࡱ࠼ࠣࡿࢂ࠭ᙽ"), str(err))
def pytest_runtest_teardown(item):
    try:
        global bstack1l1lll11l_opy_
        if CONFIG.get(bstack111l11_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪᙾ"), False):
            if CONFIG.get(bstack111l11_opy_ (u"ࠬࡶࡥࡳࡥࡼࡇࡦࡶࡴࡶࡴࡨࡑࡴࡪࡥࠨᙿ"), bstack111l11_opy_ (u"ࠨࡡࡶࡶࡲࠦ ")) == bstack111l11_opy_ (u"ࠢࡵࡧࡶࡸࡨࡧࡳࡦࠤᚁ"):
                bstack1lll11l1111_opy_ = bstack1ll111l1ll_opy_(threading.current_thread(), bstack111l11_opy_ (u"ࠨࡲࡨࡶࡨࡿࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫᚂ"), None)
                bstack1l111ll1l_opy_ = bstack1lll11l1111_opy_ + bstack111l11_opy_ (u"ࠤ࠰ࡸࡪࡹࡴࡤࡣࡶࡩࠧᚃ")
                driver = getattr(item, bstack111l11_opy_ (u"ࠪࡣࡩࡸࡩࡷࡧࡵࠫᚄ"), None)
                PercySDK.screenshot(driver, bstack1l111ll1l_opy_)
        if getattr(item, bstack111l11_opy_ (u"ࠫࡤࡧ࠱࠲ࡻࡢࡷࡹࡧࡲࡵࡧࡧࠫᚅ"), False):
            bstack1l11l111l_opy_.bstack1l1lllll11_opy_(getattr(item, bstack111l11_opy_ (u"ࠬࡥࡤࡳ࡫ࡹࡩࡷ࠭ᚆ"), None), bstack1l1lll11l_opy_, logger, item)
        if not bstack1lll1ll1l_opy_.on():
            return
        bstack11llll1l11_opy_ = {
            bstack111l11_opy_ (u"࠭ࡵࡶ࡫ࡧࠫᚇ"): uuid4().__str__(),
            bstack111l11_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫᚈ"): bstack1l111llll1_opy_().isoformat() + bstack111l11_opy_ (u"ࠨ࡜ࠪᚉ"),
            bstack111l11_opy_ (u"ࠩࡷࡽࡵ࡫ࠧᚊ"): bstack111l11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࠨᚋ"),
            bstack111l11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡷࡽࡵ࡫ࠧᚌ"): bstack111l11_opy_ (u"ࠬࡇࡆࡕࡇࡕࡣࡊࡇࡃࡉࠩᚍ"),
            bstack111l11_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡳࡧ࡭ࡦࠩᚎ"): bstack111l11_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࠩᚏ")
        }
        _11lll1lll1_opy_[item.nodeid + bstack111l11_opy_ (u"ࠨ࠯ࡷࡩࡦࡸࡤࡰࡹࡱࠫᚐ")] = bstack11llll1l11_opy_
        bstack1lll11l1l1l_opy_(item, bstack11llll1l11_opy_, bstack111l11_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪᚑ"))
    except Exception as err:
        print(bstack111l11_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵࡡࡵࡹࡳࡺࡥࡴࡶࡢࡸࡪࡧࡲࡥࡱࡺࡲ࠿ࠦࡻࡾࠩᚒ"), str(err))
@pytest.hookimpl(hookwrapper=True)
def pytest_fixture_setup(fixturedef, request):
    if not bstack1lll1ll1l_opy_.on():
        yield
        return
    start_time = datetime.datetime.now()
    if bstack1llll1l1lll_opy_(fixturedef.argname):
        store[bstack111l11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡳ࡯ࡥࡷ࡯ࡩࡤ࡯ࡴࡦ࡯ࠪᚓ")] = request.node
    elif bstack1lllll11111_opy_(fixturedef.argname):
        store[bstack111l11_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡣ࡭ࡣࡶࡷࡤ࡯ࡴࡦ࡯ࠪᚔ")] = request.node
    outcome = yield
    try:
        fixture = {
            bstack111l11_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᚕ"): fixturedef.argname,
            bstack111l11_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧᚖ"): bstack11l11l1ll1_opy_(outcome),
            bstack111l11_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࠪᚗ"): (datetime.datetime.now() - start_time).total_seconds() * 1000
        }
        current_test_item = store[bstack111l11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡷࡩࡲ࠭ᚘ")]
        if not _11lll1lll1_opy_.get(current_test_item.nodeid, None):
            _11lll1lll1_opy_[current_test_item.nodeid] = {bstack111l11_opy_ (u"ࠪࡪ࡮ࡾࡴࡶࡴࡨࡷࠬᚙ"): []}
        _11lll1lll1_opy_[current_test_item.nodeid][bstack111l11_opy_ (u"ࠫ࡫࡯ࡸࡵࡷࡵࡩࡸ࠭ᚚ")].append(fixture)
    except Exception as err:
        logger.debug(bstack111l11_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷࡣ࡫࡯ࡸࡵࡷࡵࡩࡤࡹࡥࡵࡷࡳ࠾ࠥࢁࡽࠨ᚛"), str(err))
if bstack11l1l111_opy_() and bstack1lll1ll1l_opy_.on():
    def pytest_bdd_before_step(request, step):
        try:
            _11lll1lll1_opy_[request.node.nodeid][bstack111l11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ᚜")].bstack1lll1ll111l_opy_(id(step))
        except Exception as err:
            print(bstack111l11_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹࡥࡢࡥࡦࡢࡦࡪ࡬࡯ࡳࡧࡢࡷࡹ࡫ࡰ࠻ࠢࡾࢁࠬ᚝"), str(err))
    def pytest_bdd_step_error(request, step, exception):
        try:
            _11lll1lll1_opy_[request.node.nodeid][bstack111l11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫ᚞")].bstack1l1111l111_opy_(id(step), Result.failed(exception=exception))
        except Exception as err:
            print(bstack111l11_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡼࡸࡪࡹࡴࡠࡤࡧࡨࡤࡹࡴࡦࡲࡢࡩࡷࡸ࡯ࡳ࠼ࠣࡿࢂ࠭᚟"), str(err))
    def pytest_bdd_after_step(request, step):
        try:
            bstack1l111l1ll1_opy_: bstack11lll1ll11_opy_ = _11lll1lll1_opy_[request.node.nodeid][bstack111l11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ᚠ")]
            bstack1l111l1ll1_opy_.bstack1l1111l111_opy_(id(step), Result.passed())
        except Exception as err:
            print(bstack111l11_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶࡢࡦࡩࡪ࡟ࡴࡶࡨࡴࡤ࡫ࡲࡳࡱࡵ࠾ࠥࢁࡽࠨᚡ"), str(err))
    def pytest_bdd_before_scenario(request, feature, scenario):
        global bstack1lll11l111l_opy_
        try:
            if not bstack1lll1ll1l_opy_.on() or bstack1lll11l111l_opy_ != bstack111l11_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠩᚢ"):
                return
            global bstack1l11111l11_opy_
            bstack1l11111l11_opy_.start()
            driver = bstack1ll111l1ll_opy_(threading.current_thread(), bstack111l11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬᚣ"), None)
            if not _11lll1lll1_opy_.get(request.node.nodeid, None):
                _11lll1lll1_opy_[request.node.nodeid] = {}
            bstack1l111l1ll1_opy_ = bstack11lll1ll11_opy_.bstack1lll1l1lll1_opy_(
                scenario, feature, request.node,
                name=bstack1llll1l11ll_opy_(request.node, scenario),
                bstack11llllll11_opy_=bstack11ll1l1ll_opy_(),
                file_path=feature.filename,
                scope=[feature.name],
                framework=bstack111l11_opy_ (u"ࠧࡑࡻࡷࡩࡸࡺ࠭ࡤࡷࡦࡹࡲࡨࡥࡳࠩᚤ"),
                tags=bstack1llll1llll1_opy_(feature, scenario),
                bstack1l111ll111_opy_=bstack1lll1ll1l_opy_.bstack1l111l11l1_opy_(driver) if driver and driver.session_id else {}
            )
            _11lll1lll1_opy_[request.node.nodeid][bstack111l11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫᚥ")] = bstack1l111l1ll1_opy_
            bstack1ll1llll1l1_opy_(bstack1l111l1ll1_opy_.uuid)
            bstack1lll1ll1l_opy_.bstack1l111l1l11_opy_(bstack111l11_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪᚦ"), bstack1l111l1ll1_opy_)
        except Exception as err:
            print(bstack111l11_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵࡡࡥࡨࡩࡥࡢࡦࡨࡲࡶࡪࡥࡳࡤࡧࡱࡥࡷ࡯࡯࠻ࠢࡾࢁࠬᚧ"), str(err))
def bstack1lll111l1l1_opy_(bstack1ll1llll1ll_opy_):
    if bstack1ll1llll1ll_opy_ in store[bstack111l11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨᚨ")]:
        store[bstack111l11_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩᚩ")].remove(bstack1ll1llll1ll_opy_)
def bstack1ll1llll1l1_opy_(bstack1lll111ll1l_opy_):
    store[bstack111l11_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪᚪ")] = bstack1lll111ll1l_opy_
    threading.current_thread().current_test_uuid = bstack1lll111ll1l_opy_
@bstack1lll1ll1l_opy_.bstack1lll1l111ll_opy_
def bstack1ll1lll1l1l_opy_(item, call, report):
    global bstack1lll11l111l_opy_
    bstack1ll1lll1ll_opy_ = bstack11ll1l1ll_opy_()
    if hasattr(report, bstack111l11_opy_ (u"ࠧࡴࡶࡲࡴࠬᚫ")):
        bstack1ll1lll1ll_opy_ = bstack111ll1111l_opy_(report.stop)
    elif hasattr(report, bstack111l11_opy_ (u"ࠨࡵࡷࡥࡷࡺࠧᚬ")):
        bstack1ll1lll1ll_opy_ = bstack111ll1111l_opy_(report.start)
    try:
        if getattr(report, bstack111l11_opy_ (u"ࠩࡺ࡬ࡪࡴࠧᚭ"), bstack111l11_opy_ (u"ࠪࠫᚮ")) == bstack111l11_opy_ (u"ࠫࡨࡧ࡬࡭ࠩᚯ"):
            bstack1l11111l11_opy_.reset()
        if getattr(report, bstack111l11_opy_ (u"ࠬࡽࡨࡦࡰࠪᚰ"), bstack111l11_opy_ (u"࠭ࠧᚱ")) == bstack111l11_opy_ (u"ࠧࡤࡣ࡯ࡰࠬᚲ"):
            if bstack1lll11l111l_opy_ == bstack111l11_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨᚳ"):
                _11lll1lll1_opy_[item.nodeid][bstack111l11_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧᚴ")] = bstack1ll1lll1ll_opy_
                bstack1lll111l1ll_opy_(item, _11lll1lll1_opy_[item.nodeid], bstack111l11_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬᚵ"), report, call)
                store[bstack111l11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨᚶ")] = None
            elif bstack1lll11l111l_opy_ == bstack111l11_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠤᚷ"):
                bstack1l111l1ll1_opy_ = _11lll1lll1_opy_[item.nodeid][bstack111l11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩᚸ")]
                bstack1l111l1ll1_opy_.set(hooks=_11lll1lll1_opy_[item.nodeid].get(bstack111l11_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭ᚹ"), []))
                exception, bstack11llllll1l_opy_ = None, None
                if call.excinfo:
                    exception = call.excinfo.value
                    bstack11llllll1l_opy_ = [call.excinfo.exconly(), getattr(report, bstack111l11_opy_ (u"ࠨ࡮ࡲࡲ࡬ࡸࡥࡱࡴࡷࡩࡽࡺࠧᚺ"), bstack111l11_opy_ (u"ࠩࠪᚻ"))]
                bstack1l111l1ll1_opy_.stop(time=bstack1ll1lll1ll_opy_, result=Result(result=getattr(report, bstack111l11_opy_ (u"ࠪࡳࡺࡺࡣࡰ࡯ࡨࠫᚼ"), bstack111l11_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫᚽ")), exception=exception, bstack11llllll1l_opy_=bstack11llllll1l_opy_))
                bstack1lll1ll1l_opy_.bstack1l111l1l11_opy_(bstack111l11_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧᚾ"), _11lll1lll1_opy_[item.nodeid][bstack111l11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩᚿ")])
        elif getattr(report, bstack111l11_opy_ (u"ࠧࡸࡪࡨࡲࠬᛀ"), bstack111l11_opy_ (u"ࠨࠩᛁ")) in [bstack111l11_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨᛂ"), bstack111l11_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࠬᛃ")]:
            bstack11llll11l1_opy_ = item.nodeid + bstack111l11_opy_ (u"ࠫ࠲࠭ᛄ") + getattr(report, bstack111l11_opy_ (u"ࠬࡽࡨࡦࡰࠪᛅ"), bstack111l11_opy_ (u"࠭ࠧᛆ"))
            if getattr(report, bstack111l11_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨᛇ"), False):
                hook_type = bstack111l11_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡇࡄࡇࡍ࠭ᛈ") if getattr(report, bstack111l11_opy_ (u"ࠩࡺ࡬ࡪࡴࠧᛉ"), bstack111l11_opy_ (u"ࠪࠫᛊ")) == bstack111l11_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪᛋ") else bstack111l11_opy_ (u"ࠬࡇࡆࡕࡇࡕࡣࡊࡇࡃࡉࠩᛌ")
                _11lll1lll1_opy_[bstack11llll11l1_opy_] = {
                    bstack111l11_opy_ (u"࠭ࡵࡶ࡫ࡧࠫᛍ"): uuid4().__str__(),
                    bstack111l11_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫᛎ"): bstack1ll1lll1ll_opy_,
                    bstack111l11_opy_ (u"ࠨࡪࡲࡳࡰࡥࡴࡺࡲࡨࠫᛏ"): hook_type
                }
            _11lll1lll1_opy_[bstack11llll11l1_opy_][bstack111l11_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧᛐ")] = bstack1ll1lll1ll_opy_
            bstack1lll111l1l1_opy_(_11lll1lll1_opy_[bstack11llll11l1_opy_][bstack111l11_opy_ (u"ࠪࡹࡺ࡯ࡤࠨᛑ")])
            bstack1lll11l1l1l_opy_(item, _11lll1lll1_opy_[bstack11llll11l1_opy_], bstack111l11_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ᛒ"), report, call)
            if getattr(report, bstack111l11_opy_ (u"ࠬࡽࡨࡦࡰࠪᛓ"), bstack111l11_opy_ (u"࠭ࠧᛔ")) == bstack111l11_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭ᛕ"):
                if getattr(report, bstack111l11_opy_ (u"ࠨࡱࡸࡸࡨࡵ࡭ࡦࠩᛖ"), bstack111l11_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩᛗ")) == bstack111l11_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᛘ"):
                    bstack11llll1l11_opy_ = {
                        bstack111l11_opy_ (u"ࠫࡺࡻࡩࡥࠩᛙ"): uuid4().__str__(),
                        bstack111l11_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩᛚ"): bstack11ll1l1ll_opy_(),
                        bstack111l11_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫᛛ"): bstack11ll1l1ll_opy_()
                    }
                    _11lll1lll1_opy_[item.nodeid] = {**_11lll1lll1_opy_[item.nodeid], **bstack11llll1l11_opy_}
                    bstack1lll111l1ll_opy_(item, _11lll1lll1_opy_[item.nodeid], bstack111l11_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨᛜ"))
                    bstack1lll111l1ll_opy_(item, _11lll1lll1_opy_[item.nodeid], bstack111l11_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪᛝ"), report, call)
    except Exception as err:
        print(bstack111l11_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡪࡤࡲࡩࡲࡥࡠࡱ࠴࠵ࡾࡥࡴࡦࡵࡷࡣࡪࡼࡥ࡯ࡶ࠽ࠤࢀࢃࠧᛞ"), str(err))
def bstack1lll11111l1_opy_(test, bstack11llll1l11_opy_, result=None, call=None, bstack1llllll111_opy_=None, outcome=None):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    bstack1l111l1ll1_opy_ = {
        bstack111l11_opy_ (u"ࠪࡹࡺ࡯ࡤࠨᛟ"): bstack11llll1l11_opy_[bstack111l11_opy_ (u"ࠫࡺࡻࡩࡥࠩᛠ")],
        bstack111l11_opy_ (u"ࠬࡺࡹࡱࡧࠪᛡ"): bstack111l11_opy_ (u"࠭ࡴࡦࡵࡷࠫᛢ"),
        bstack111l11_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᛣ"): test.name,
        bstack111l11_opy_ (u"ࠨࡤࡲࡨࡾ࠭ᛤ"): {
            bstack111l11_opy_ (u"ࠩ࡯ࡥࡳ࡭ࠧᛥ"): bstack111l11_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪᛦ"),
            bstack111l11_opy_ (u"ࠫࡨࡵࡤࡦࠩᛧ"): inspect.getsource(test.obj)
        },
        bstack111l11_opy_ (u"ࠬ࡯ࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩᛨ"): test.name,
        bstack111l11_opy_ (u"࠭ࡳࡤࡱࡳࡩࠬᛩ"): test.name,
        bstack111l11_opy_ (u"ࠧࡴࡥࡲࡴࡪࡹࠧᛪ"): bstack1lll1ll1l_opy_.bstack1l1111111l_opy_(test),
        bstack111l11_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫ᛫"): file_path,
        bstack111l11_opy_ (u"ࠩ࡯ࡳࡨࡧࡴࡪࡱࡱࠫ᛬"): file_path,
        bstack111l11_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪ᛭"): bstack111l11_opy_ (u"ࠫࡵ࡫࡮ࡥ࡫ࡱ࡫ࠬᛮ"),
        bstack111l11_opy_ (u"ࠬࡼࡣࡠࡨ࡬ࡰࡪࡶࡡࡵࡪࠪᛯ"): file_path,
        bstack111l11_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪᛰ"): bstack11llll1l11_opy_[bstack111l11_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫᛱ")],
        bstack111l11_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫᛲ"): bstack111l11_opy_ (u"ࠩࡓࡽࡹ࡫ࡳࡵࠩᛳ"),
        bstack111l11_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡕࡩࡷࡻ࡮ࡑࡣࡵࡥࡲ࠭ᛴ"): {
            bstack111l11_opy_ (u"ࠫࡷ࡫ࡲࡶࡰࡢࡲࡦࡳࡥࠨᛵ"): test.nodeid
        },
        bstack111l11_opy_ (u"ࠬࡺࡡࡨࡵࠪᛶ"): bstack111lll11l1_opy_(test.own_markers)
    }
    if bstack1llllll111_opy_ in [bstack111l11_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓ࡬࡫ࡳࡴࡪࡪࠧᛷ"), bstack111l11_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩᛸ")]:
        bstack1l111l1ll1_opy_[bstack111l11_opy_ (u"ࠨ࡯ࡨࡸࡦ࠭᛹")] = {
            bstack111l11_opy_ (u"ࠩࡩ࡭ࡽࡺࡵࡳࡧࡶࠫ᛺"): bstack11llll1l11_opy_.get(bstack111l11_opy_ (u"ࠪࡪ࡮ࡾࡴࡶࡴࡨࡷࠬ᛻"), [])
        }
    if bstack1llllll111_opy_ == bstack111l11_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡱࡩࡱࡲࡨࡨࠬ᛼"):
        bstack1l111l1ll1_opy_[bstack111l11_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬ᛽")] = bstack111l11_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧ᛾")
        bstack1l111l1ll1_opy_[bstack111l11_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭᛿")] = bstack11llll1l11_opy_[bstack111l11_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧᜀ")]
        bstack1l111l1ll1_opy_[bstack111l11_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧᜁ")] = bstack11llll1l11_opy_[bstack111l11_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᜂ")]
    if result:
        bstack1l111l1ll1_opy_[bstack111l11_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫᜃ")] = result.outcome
        bstack1l111l1ll1_opy_[bstack111l11_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴ࡟ࡪࡰࡢࡱࡸ࠭ᜄ")] = result.duration * 1000
        bstack1l111l1ll1_opy_[bstack111l11_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫᜅ")] = bstack11llll1l11_opy_[bstack111l11_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬᜆ")]
        if result.failed:
            bstack1l111l1ll1_opy_[bstack111l11_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࡡࡷࡽࡵ࡫ࠧᜇ")] = bstack1lll1ll1l_opy_.bstack11ll11llll_opy_(call.excinfo.typename)
            bstack1l111l1ll1_opy_[bstack111l11_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࠪᜈ")] = bstack1lll1ll1l_opy_.bstack1lll11lll1l_opy_(call.excinfo, result)
        bstack1l111l1ll1_opy_[bstack111l11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩᜉ")] = bstack11llll1l11_opy_[bstack111l11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪᜊ")]
    if outcome:
        bstack1l111l1ll1_opy_[bstack111l11_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬᜋ")] = bstack11l11l1ll1_opy_(outcome)
        bstack1l111l1ll1_opy_[bstack111l11_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࡠ࡫ࡱࡣࡲࡹࠧᜌ")] = 0
        bstack1l111l1ll1_opy_[bstack111l11_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬᜍ")] = bstack11llll1l11_opy_[bstack111l11_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ᜎ")]
        if bstack1l111l1ll1_opy_[bstack111l11_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩᜏ")] == bstack111l11_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᜐ"):
            bstack1l111l1ll1_opy_[bstack111l11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࡤࡺࡹࡱࡧࠪᜑ")] = bstack111l11_opy_ (u"࡛ࠬ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡆࡴࡵࡳࡷ࠭ᜒ")  # bstack1ll1lll1lll_opy_
            bstack1l111l1ll1_opy_[bstack111l11_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫ࠧᜓ")] = [{bstack111l11_opy_ (u"ࠧࡣࡣࡦ࡯ࡹࡸࡡࡤࡧ᜔ࠪ"): [bstack111l11_opy_ (u"ࠨࡵࡲࡱࡪࠦࡥࡳࡴࡲࡶ᜕ࠬ")]}]
        bstack1l111l1ll1_opy_[bstack111l11_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨ᜖")] = bstack11llll1l11_opy_[bstack111l11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩ᜗")]
    return bstack1l111l1ll1_opy_
def bstack1lll111lll1_opy_(test, bstack1l1111lll1_opy_, bstack1llllll111_opy_, result, call, outcome, bstack1lll1111ll1_opy_):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    hook_type = bstack1l1111lll1_opy_[bstack111l11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡷࡽࡵ࡫ࠧ᜘")]
    hook_name = bstack1l1111lll1_opy_[bstack111l11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡲࡦࡳࡥࠨ᜙")]
    hook_data = {
        bstack111l11_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ᜚"): bstack1l1111lll1_opy_[bstack111l11_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ᜛")],
        bstack111l11_opy_ (u"ࠨࡶࡼࡴࡪ࠭᜜"): bstack111l11_opy_ (u"ࠩ࡫ࡳࡴࡱࠧ᜝"),
        bstack111l11_opy_ (u"ࠪࡲࡦࡳࡥࠨ᜞"): bstack111l11_opy_ (u"ࠫࢀࢃࠧᜟ").format(bstack1llll1l1l11_opy_(hook_name)),
        bstack111l11_opy_ (u"ࠬࡨ࡯ࡥࡻࠪᜠ"): {
            bstack111l11_opy_ (u"࠭࡬ࡢࡰࡪࠫᜡ"): bstack111l11_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧᜢ"),
            bstack111l11_opy_ (u"ࠨࡥࡲࡨࡪ࠭ᜣ"): None
        },
        bstack111l11_opy_ (u"ࠩࡶࡧࡴࡶࡥࠨᜤ"): test.name,
        bstack111l11_opy_ (u"ࠪࡷࡨࡵࡰࡦࡵࠪᜥ"): bstack1lll1ll1l_opy_.bstack1l1111111l_opy_(test, hook_name),
        bstack111l11_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧᜦ"): file_path,
        bstack111l11_opy_ (u"ࠬࡲ࡯ࡤࡣࡷ࡭ࡴࡴࠧᜧ"): file_path,
        bstack111l11_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ᜨ"): bstack111l11_opy_ (u"ࠧࡱࡧࡱࡨ࡮ࡴࡧࠨᜩ"),
        bstack111l11_opy_ (u"ࠨࡸࡦࡣ࡫࡯࡬ࡦࡲࡤࡸ࡭࠭ᜪ"): file_path,
        bstack111l11_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭ᜫ"): bstack1l1111lll1_opy_[bstack111l11_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧᜬ")],
        bstack111l11_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧᜭ"): bstack111l11_opy_ (u"ࠬࡖࡹࡵࡧࡶࡸ࠲ࡩࡵࡤࡷࡰࡦࡪࡸࠧᜮ") if bstack1lll11l111l_opy_ == bstack111l11_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠪᜯ") else bstack111l11_opy_ (u"ࠧࡑࡻࡷࡩࡸࡺࠧᜰ"),
        bstack111l11_opy_ (u"ࠨࡪࡲࡳࡰࡥࡴࡺࡲࡨࠫᜱ"): hook_type
    }
    bstack1lll1111111_opy_ = bstack1l11111lll_opy_(_11lll1lll1_opy_.get(test.nodeid, None))
    if bstack1lll1111111_opy_:
        hook_data[bstack111l11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣ࡮ࡪࠧᜲ")] = bstack1lll1111111_opy_
    if result:
        hook_data[bstack111l11_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪᜳ")] = result.outcome
        hook_data[bstack111l11_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳࡥࡩ࡯ࡡࡰࡷ᜴ࠬ")] = result.duration * 1000
        hook_data[bstack111l11_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ᜵")] = bstack1l1111lll1_opy_[bstack111l11_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ᜶")]
        if result.failed:
            hook_data[bstack111l11_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࡠࡶࡼࡴࡪ࠭᜷")] = bstack1lll1ll1l_opy_.bstack11ll11llll_opy_(call.excinfo.typename)
            hook_data[bstack111l11_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࠩ᜸")] = bstack1lll1ll1l_opy_.bstack1lll11lll1l_opy_(call.excinfo, result)
    if outcome:
        hook_data[bstack111l11_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ᜹")] = bstack11l11l1ll1_opy_(outcome)
        hook_data[bstack111l11_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࡤ࡯࡮ࡠ࡯ࡶࠫ᜺")] = 100
        hook_data[bstack111l11_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ᜻")] = bstack1l1111lll1_opy_[bstack111l11_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ᜼")]
        if hook_data[bstack111l11_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭᜽")] == bstack111l11_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ᜾"):
            hook_data[bstack111l11_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࡡࡷࡽࡵ࡫ࠧ᜿")] = bstack111l11_opy_ (u"ࠩࡘࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࡊࡸࡲࡰࡴࠪᝀ")  # bstack1ll1lll1lll_opy_
            hook_data[bstack111l11_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࠫᝁ")] = [{bstack111l11_opy_ (u"ࠫࡧࡧࡣ࡬ࡶࡵࡥࡨ࡫ࠧᝂ"): [bstack111l11_opy_ (u"ࠬࡹ࡯࡮ࡧࠣࡩࡷࡸ࡯ࡳࠩᝃ")]}]
    if bstack1lll1111ll1_opy_:
        hook_data[bstack111l11_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ᝄ")] = bstack1lll1111ll1_opy_.result
        hook_data[bstack111l11_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࡡ࡬ࡲࡤࡳࡳࠨᝅ")] = bstack11l11l11l1_opy_(bstack1l1111lll1_opy_[bstack111l11_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬᝆ")], bstack1l1111lll1_opy_[bstack111l11_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧᝇ")])
        hook_data[bstack111l11_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᝈ")] = bstack1l1111lll1_opy_[bstack111l11_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩᝉ")]
        if hook_data[bstack111l11_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬᝊ")] == bstack111l11_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᝋ"):
            hook_data[bstack111l11_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࡠࡶࡼࡴࡪ࠭ᝌ")] = bstack1lll1ll1l_opy_.bstack11ll11llll_opy_(bstack1lll1111ll1_opy_.exception_type)
            hook_data[bstack111l11_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࠩᝍ")] = [{bstack111l11_opy_ (u"ࠩࡥࡥࡨࡱࡴࡳࡣࡦࡩࠬᝎ"): bstack11l1111ll1_opy_(bstack1lll1111ll1_opy_.exception)}]
    return hook_data
def bstack1lll111l1ll_opy_(test, bstack11llll1l11_opy_, bstack1llllll111_opy_, result=None, call=None, outcome=None):
    bstack1l111l1ll1_opy_ = bstack1lll11111l1_opy_(test, bstack11llll1l11_opy_, result, call, bstack1llllll111_opy_, outcome)
    driver = getattr(test, bstack111l11_opy_ (u"ࠪࡣࡩࡸࡩࡷࡧࡵࠫᝏ"), None)
    if bstack1llllll111_opy_ == bstack111l11_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬᝐ") and driver:
        bstack1l111l1ll1_opy_[bstack111l11_opy_ (u"ࠬ࡯࡮ࡵࡧࡪࡶࡦࡺࡩࡰࡰࡶࠫᝑ")] = bstack1lll1ll1l_opy_.bstack1l111l11l1_opy_(driver)
    if bstack1llllll111_opy_ == bstack111l11_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓ࡬࡫ࡳࡴࡪࡪࠧᝒ"):
        bstack1llllll111_opy_ = bstack111l11_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩᝓ")
    bstack1l1111l1ll_opy_ = {
        bstack111l11_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬ᝔"): bstack1llllll111_opy_,
        bstack111l11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࠫ᝕"): bstack1l111l1ll1_opy_
    }
    bstack1lll1ll1l_opy_.bstack1l11l11111_opy_(bstack1l1111l1ll_opy_)
def bstack1lll11l1l1l_opy_(test, bstack11llll1l11_opy_, bstack1llllll111_opy_, result=None, call=None, outcome=None, bstack1lll1111ll1_opy_=None):
    hook_data = bstack1lll111lll1_opy_(test, bstack11llll1l11_opy_, bstack1llllll111_opy_, result, call, outcome, bstack1lll1111ll1_opy_)
    bstack1l1111l1ll_opy_ = {
        bstack111l11_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧ᝖"): bstack1llllll111_opy_,
        bstack111l11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳ࠭᝗"): hook_data
    }
    bstack1lll1ll1l_opy_.bstack1l11l11111_opy_(bstack1l1111l1ll_opy_)
def bstack1l11111lll_opy_(bstack11llll1l11_opy_):
    if not bstack11llll1l11_opy_:
        return None
    if bstack11llll1l11_opy_.get(bstack111l11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ᝘"), None):
        return getattr(bstack11llll1l11_opy_[bstack111l11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ᝙")], bstack111l11_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ᝚"), None)
    return bstack11llll1l11_opy_.get(bstack111l11_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭᝛"), None)
@pytest.fixture(autouse=True)
def second_fixture(caplog, request):
    yield
    try:
        if not bstack1lll1ll1l_opy_.on():
            return
        places = [bstack111l11_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨ᝜"), bstack111l11_opy_ (u"ࠪࡧࡦࡲ࡬ࠨ᝝"), bstack111l11_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭᝞")]
        bstack1l111ll1l1_opy_ = []
        for bstack1ll1lll1ll1_opy_ in places:
            records = caplog.get_records(bstack1ll1lll1ll1_opy_)
            bstack1lll1111lll_opy_ = bstack111l11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ᝟") if bstack1ll1lll1ll1_opy_ == bstack111l11_opy_ (u"࠭ࡣࡢ࡮࡯ࠫᝠ") else bstack111l11_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᝡ")
            bstack1lll11l11ll_opy_ = request.node.nodeid + (bstack111l11_opy_ (u"ࠨࠩᝢ") if bstack1ll1lll1ll1_opy_ == bstack111l11_opy_ (u"ࠩࡦࡥࡱࡲࠧᝣ") else bstack111l11_opy_ (u"ࠪ࠱ࠬᝤ") + bstack1ll1lll1ll1_opy_)
            bstack1lll111ll1l_opy_ = bstack1l11111lll_opy_(_11lll1lll1_opy_.get(bstack1lll11l11ll_opy_, None))
            if not bstack1lll111ll1l_opy_:
                continue
            for record in records:
                if bstack111l1lll11_opy_(record.message):
                    continue
                bstack1l111ll1l1_opy_.append({
                    bstack111l11_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧᝥ"): bstack111l11llll_opy_(record.created).isoformat() + bstack111l11_opy_ (u"ࠬࡠࠧᝦ"),
                    bstack111l11_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬᝧ"): record.levelname,
                    bstack111l11_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᝨ"): record.message,
                    bstack1lll1111lll_opy_: bstack1lll111ll1l_opy_
                })
        if len(bstack1l111ll1l1_opy_) > 0:
            bstack1lll1ll1l_opy_.bstack1l11111l1_opy_(bstack1l111ll1l1_opy_)
    except Exception as err:
        print(bstack111l11_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡴࡧࡦࡳࡳࡪ࡟ࡧ࡫ࡻࡸࡺࡸࡥ࠻ࠢࡾࢁࠬᝩ"), str(err))
def bstack1l1llllll1_opy_(sequence, driver_command, response=None, driver = None, args = None):
    global bstack1l1ll11l_opy_
    bstack11llll11l_opy_ = bstack1ll111l1ll_opy_(threading.current_thread(), bstack111l11_opy_ (u"ࠩ࡬ࡷࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭ᝪ"), None) and bstack1ll111l1ll_opy_(
            threading.current_thread(), bstack111l11_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩᝫ"), None)
    bstack1l11l1ll_opy_ = getattr(driver, bstack111l11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡅ࠶࠷ࡹࡔࡪࡲࡹࡱࡪࡓࡤࡣࡱࠫᝬ"), None) != None and getattr(driver, bstack111l11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡆ࠷࠱ࡺࡕ࡫ࡳࡺࡲࡤࡔࡥࡤࡲࠬ᝭"), None) == True
    if sequence == bstack111l11_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪ࠭ᝮ") and driver != None:
      if not bstack1l1ll11l_opy_ and bstack111ll1ll1l_opy_() and bstack111l11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᝯ") in CONFIG and CONFIG[bstack111l11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᝰ")] == True and bstack1l1lll1lll_opy_.bstack1lll1l1ll1_opy_(driver_command) and (bstack1l11l1ll_opy_ or bstack11llll11l_opy_) and not bstack1l1111l1l_opy_(args):
        try:
          bstack1l1ll11l_opy_ = True
          logger.debug(bstack111l11_opy_ (u"ࠩࡓࡩࡷ࡬࡯ࡳ࡯࡬ࡲ࡬ࠦࡳࡤࡣࡱࠤ࡫ࡵࡲࠡࡽࢀࠫ᝱").format(driver_command))
          logger.debug(perform_scan(driver, driver_command=driver_command))
        except Exception as err:
          logger.debug(bstack111l11_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡰࡦࡴࡩࡳࡷࡳࠠࡴࡥࡤࡲࠥࢁࡽࠨᝲ").format(str(err)))
        bstack1l1ll11l_opy_ = False
    if sequence == bstack111l11_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࠪᝳ"):
        if driver_command == bstack111l11_opy_ (u"ࠬࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࠩ᝴"):
            bstack1lll1ll1l_opy_.bstack1ll11l1ll_opy_({
                bstack111l11_opy_ (u"࠭ࡩ࡮ࡣࡪࡩࠬ᝵"): response[bstack111l11_opy_ (u"ࠧࡷࡣ࡯ࡹࡪ࠭᝶")],
                bstack111l11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ᝷"): store[bstack111l11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭᝸")]
            })
def bstack1ll11l1111_opy_():
    global bstack1l1l1ll1l1_opy_
    bstack1l1l1l1l1_opy_.bstack1111l111l_opy_()
    logging.shutdown()
    bstack1lll1ll1l_opy_.bstack11lll1l1l1_opy_()
    for driver in bstack1l1l1ll1l1_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1ll1lllll1l_opy_(*args):
    global bstack1l1l1ll1l1_opy_
    bstack1lll1ll1l_opy_.bstack11lll1l1l1_opy_()
    for driver in bstack1l1l1ll1l1_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1l1ll1ll11_opy_(self, *args, **kwargs):
    bstack1l1lll1l_opy_ = bstack1ll111l11l_opy_(self, *args, **kwargs)
    bstack1lll1ll1l_opy_.bstack1l1ll11l11_opy_(self)
    return bstack1l1lll1l_opy_
def bstack11l11l111_opy_(framework_name):
    global bstack1lll1ll11_opy_
    global bstack1ll1l1ll11_opy_
    bstack1lll1ll11_opy_ = framework_name
    logger.info(bstack1ll1l111l_opy_.format(bstack1lll1ll11_opy_.split(bstack111l11_opy_ (u"ࠪ࠱ࠬ᝹"))[0]))
    try:
        from selenium import webdriver
        from selenium.webdriver.common.service import Service
        from selenium.webdriver.remote.webdriver import WebDriver
        if bstack111ll1ll1l_opy_():
            Service.start = bstack1l11lll1ll_opy_
            Service.stop = bstack1llll1lll_opy_
            webdriver.Remote.__init__ = bstack11ll1llll_opy_
            webdriver.Remote.get = bstack11111ll1l_opy_
            if not isinstance(os.getenv(bstack111l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔ࡞࡚ࡅࡔࡖࡢࡔࡆࡘࡁࡍࡎࡈࡐࠬ᝺")), str):
                return
            WebDriver.close = bstack1l11lll1_opy_
            WebDriver.quit = bstack1ll11111ll_opy_
            WebDriver.getAccessibilityResults = getAccessibilityResults
            WebDriver.get_accessibility_results = getAccessibilityResults
            WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
            WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
            WebDriver.performScan = perform_scan
            WebDriver.perform_scan = perform_scan
        if not bstack111ll1ll1l_opy_() and bstack1lll1ll1l_opy_.on():
            webdriver.Remote.__init__ = bstack1l1ll1ll11_opy_
        bstack1ll1l1ll11_opy_ = True
    except Exception as e:
        pass
    bstack1ll1lllll_opy_()
    if os.environ.get(bstack111l11_opy_ (u"࡙ࠬࡅࡍࡇࡑࡍ࡚ࡓ࡟ࡐࡔࡢࡔࡑࡇ࡙ࡘࡔࡌࡋࡍ࡚࡟ࡊࡐࡖࡘࡆࡒࡌࡆࡆࠪ᝻")):
        bstack1ll1l1ll11_opy_ = eval(os.environ.get(bstack111l11_opy_ (u"࠭ࡓࡆࡎࡈࡒࡎ࡛ࡍࡠࡑࡕࡣࡕࡒࡁ࡚࡙ࡕࡍࡌࡎࡔࡠࡋࡑࡗ࡙ࡇࡌࡍࡇࡇࠫ᝼")))
    if not bstack1ll1l1ll11_opy_:
        bstack1lll11lll_opy_(bstack111l11_opy_ (u"ࠢࡑࡣࡦ࡯ࡦ࡭ࡥࡴࠢࡱࡳࡹࠦࡩ࡯ࡵࡷࡥࡱࡲࡥࡥࠤ᝽"), bstack11llll111_opy_)
    if bstack11l1ll1l1_opy_():
        try:
            from selenium.webdriver.remote.remote_connection import RemoteConnection
            RemoteConnection._get_proxy_url = bstack1l1ll11111_opy_
        except Exception as e:
            logger.error(bstack1l1l1lllll_opy_.format(str(e)))
    if bstack111l11_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ᝾") in str(framework_name).lower():
        if not bstack111ll1ll1l_opy_():
            return
        try:
            from pytest_selenium import pytest_selenium
            from _pytest.config import Config
            pytest_selenium.pytest_report_header = bstack11l11lll_opy_
            from pytest_selenium.drivers import browserstack
            browserstack.pytest_selenium_runtest_makereport = bstack1111lll11_opy_
            Config.getoption = bstack11l1llll1_opy_
        except Exception as e:
            pass
        try:
            from pytest_bdd import reporting
            reporting.runtest_makereport = bstack1ll11l111l_opy_
        except Exception as e:
            pass
def bstack1ll11111ll_opy_(self):
    global bstack1lll1ll11_opy_
    global bstack1ll111l1_opy_
    global bstack11l1lll1_opy_
    try:
        if bstack111l11_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ᝿") in bstack1lll1ll11_opy_ and self.session_id != None and bstack1ll111l1ll_opy_(threading.current_thread(), bstack111l11_opy_ (u"ࠪࡸࡪࡹࡴࡔࡶࡤࡸࡺࡹࠧក"), bstack111l11_opy_ (u"ࠫࠬខ")) != bstack111l11_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭គ"):
            bstack1lll11l1ll_opy_ = bstack111l11_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ឃ") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack111l11_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧង")
            bstack1l1l1lll11_opy_(logger, True)
            if self != None:
                bstack1l1l11llll_opy_(self, bstack1lll11l1ll_opy_, bstack111l11_opy_ (u"ࠨ࠮ࠣࠫច").join(threading.current_thread().bstackTestErrorMessages))
        item = store.get(bstack111l11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡷࡩࡲ࠭ឆ"), None)
        if item is not None and bstack1lll111l111_opy_:
            bstack1l11l111l_opy_.bstack1l1lllll11_opy_(self, bstack1l1lll11l_opy_, logger, item)
        threading.current_thread().testStatus = bstack111l11_opy_ (u"ࠪࠫជ")
    except Exception as e:
        logger.debug(bstack111l11_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡰࡥࡷࡱࡩ࡯ࡩࠣࡷࡹࡧࡴࡶࡵ࠽ࠤࠧឈ") + str(e))
    bstack11l1lll1_opy_(self)
    self.session_id = None
def bstack11ll1llll_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
    global CONFIG
    global bstack1ll111l1_opy_
    global bstack1l11l11l1_opy_
    global bstack111lll1ll_opy_
    global bstack1lll1ll11_opy_
    global bstack1ll111l11l_opy_
    global bstack1l1l1ll1l1_opy_
    global bstack1l1l11l11_opy_
    global bstack1l11ll1l_opy_
    global bstack1lll111l111_opy_
    global bstack1l1lll11l_opy_
    CONFIG[bstack111l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧញ")] = str(bstack1lll1ll11_opy_) + str(__version__)
    command_executor = bstack1l1l1l111_opy_(bstack1l1l11l11_opy_)
    logger.debug(bstack1lll111l1l_opy_.format(command_executor))
    proxy = bstack11ll11111_opy_(CONFIG, proxy)
    bstack1ll11lllll_opy_ = 0
    try:
        if bstack111lll1ll_opy_ is True:
            bstack1ll11lllll_opy_ = int(os.environ.get(bstack111l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ដ")))
    except:
        bstack1ll11lllll_opy_ = 0
    bstack1ll1ll1111_opy_ = bstack111ll11ll_opy_(CONFIG, bstack1ll11lllll_opy_)
    logger.debug(bstack111l11111_opy_.format(str(bstack1ll1ll1111_opy_)))
    bstack1l1lll11l_opy_ = CONFIG.get(bstack111l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪឋ"))[bstack1ll11lllll_opy_]
    if bstack111l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬឌ") in CONFIG and CONFIG[bstack111l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ឍ")]:
        bstack111llll1l_opy_(bstack1ll1ll1111_opy_, bstack1l11ll1l_opy_)
    if bstack1llll11l_opy_.bstack1l1l1ll1l_opy_(CONFIG, bstack1ll11lllll_opy_) and bstack1llll11l_opy_.bstack1llllllll_opy_(bstack1ll1ll1111_opy_, options):
        bstack1lll111l111_opy_ = True
        bstack1llll11l_opy_.set_capabilities(bstack1ll1ll1111_opy_, CONFIG)
    if desired_capabilities:
        bstack1l11l1ll11_opy_ = bstack111ll1ll_opy_(desired_capabilities)
        bstack1l11l1ll11_opy_[bstack111l11_opy_ (u"ࠪࡹࡸ࡫ࡗ࠴ࡅࠪណ")] = bstack11ll111ll_opy_(CONFIG)
        bstack11lll1ll1_opy_ = bstack111ll11ll_opy_(bstack1l11l1ll11_opy_)
        if bstack11lll1ll1_opy_:
            bstack1ll1ll1111_opy_ = update(bstack11lll1ll1_opy_, bstack1ll1ll1111_opy_)
        desired_capabilities = None
    if options:
        bstack1l11lllll1_opy_(options, bstack1ll1ll1111_opy_)
    if not options:
        options = bstack1l1llll1l1_opy_(bstack1ll1ll1111_opy_)
    if proxy and bstack1lll1l1ll_opy_() >= version.parse(bstack111l11_opy_ (u"ࠫ࠹࠴࠱࠱࠰࠳ࠫត")):
        options.proxy(proxy)
    if options and bstack1lll1l1ll_opy_() >= version.parse(bstack111l11_opy_ (u"ࠬ࠹࠮࠹࠰࠳ࠫថ")):
        desired_capabilities = None
    if (
            not options and not desired_capabilities
    ) or (
            bstack1lll1l1ll_opy_() < version.parse(bstack111l11_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬទ")) and not desired_capabilities
    ):
        desired_capabilities = {}
        desired_capabilities.update(bstack1ll1ll1111_opy_)
    logger.info(bstack1ll11l1l1_opy_)
    if bstack1lll1l1ll_opy_() >= version.parse(bstack111l11_opy_ (u"ࠧ࠵࠰࠴࠴࠳࠶ࠧធ")):
        bstack1ll111l11l_opy_(self, command_executor=command_executor,
                  options=options, keep_alive=keep_alive, file_detector=file_detector)
    elif bstack1lll1l1ll_opy_() >= version.parse(bstack111l11_opy_ (u"ࠨ࠵࠱࠼࠳࠶ࠧន")):
        bstack1ll111l11l_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities, options=options,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    elif bstack1lll1l1ll_opy_() >= version.parse(bstack111l11_opy_ (u"ࠩ࠵࠲࠺࠹࠮࠱ࠩប")):
        bstack1ll111l11l_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    else:
        bstack1ll111l11l_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive)
    try:
        bstack1llll1l1_opy_ = bstack111l11_opy_ (u"ࠪࠫផ")
        if bstack1lll1l1ll_opy_() >= version.parse(bstack111l11_opy_ (u"ࠫ࠹࠴࠰࠯࠲ࡥ࠵ࠬព")):
            bstack1llll1l1_opy_ = self.caps.get(bstack111l11_opy_ (u"ࠧࡵࡰࡵ࡫ࡰࡥࡱࡎࡵࡣࡗࡵࡰࠧភ"))
        else:
            bstack1llll1l1_opy_ = self.capabilities.get(bstack111l11_opy_ (u"ࠨ࡯ࡱࡶ࡬ࡱࡦࡲࡈࡶࡤࡘࡶࡱࠨម"))
        if bstack1llll1l1_opy_:
            bstack111llllll_opy_(bstack1llll1l1_opy_)
            if bstack1lll1l1ll_opy_() <= version.parse(bstack111l11_opy_ (u"ࠧ࠴࠰࠴࠷࠳࠶ࠧយ")):
                self.command_executor._url = bstack111l11_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤរ") + bstack1l1l11l11_opy_ + bstack111l11_opy_ (u"ࠤ࠽࠼࠵࠵ࡷࡥ࠱࡫ࡹࡧࠨល")
            else:
                self.command_executor._url = bstack111l11_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࠧវ") + bstack1llll1l1_opy_ + bstack111l11_opy_ (u"ࠦ࠴ࡽࡤ࠰ࡪࡸࡦࠧឝ")
            logger.debug(bstack1ll1l111l1_opy_.format(bstack1llll1l1_opy_))
        else:
            logger.debug(bstack1lllll1l11_opy_.format(bstack111l11_opy_ (u"ࠧࡕࡰࡵ࡫ࡰࡥࡱࠦࡈࡶࡤࠣࡲࡴࡺࠠࡧࡱࡸࡲࡩࠨឞ")))
    except Exception as e:
        logger.debug(bstack1lllll1l11_opy_.format(e))
    bstack1ll111l1_opy_ = self.session_id
    if bstack111l11_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ស") in bstack1lll1ll11_opy_:
        threading.current_thread().bstackSessionId = self.session_id
        threading.current_thread().bstackSessionDriver = self
        threading.current_thread().bstackTestErrorMessages = []
        item = store.get(bstack111l11_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡩࡵࡧࡰࠫហ"), None)
        if item:
            bstack1lll111ll11_opy_ = getattr(item, bstack111l11_opy_ (u"ࠨࡡࡷࡩࡸࡺ࡟ࡤࡣࡶࡩࡤࡹࡴࡢࡴࡷࡩࡩ࠭ឡ"), False)
            if not getattr(item, bstack111l11_opy_ (u"ࠩࡢࡨࡷ࡯ࡶࡦࡴࠪអ"), None) and bstack1lll111ll11_opy_:
                setattr(store[bstack111l11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡸࡪࡳࠧឣ")], bstack111l11_opy_ (u"ࠫࡤࡪࡲࡪࡸࡨࡶࠬឤ"), self)
        bstack1lll1ll1l_opy_.bstack1l1ll11l11_opy_(self)
    bstack1l1l1ll1l1_opy_.append(self)
    if bstack111l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨឥ") in CONFIG and bstack111l11_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫឦ") in CONFIG[bstack111l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪឧ")][bstack1ll11lllll_opy_]:
        bstack1l11l11l1_opy_ = CONFIG[bstack111l11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫឨ")][bstack1ll11lllll_opy_][bstack111l11_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧឩ")]
    logger.debug(bstack11lll11l1_opy_.format(bstack1ll111l1_opy_))
def bstack11111ll1l_opy_(self, url):
    global bstack1l1ll1l11l_opy_
    global CONFIG
    try:
        bstack11l111ll1_opy_(url, CONFIG, logger)
    except Exception as err:
        logger.debug(bstack1l1l111l1_opy_.format(str(err)))
    try:
        bstack1l1ll1l11l_opy_(self, url)
    except Exception as e:
        try:
            bstack1l1l11lll_opy_ = str(e)
            if any(err_msg in bstack1l1l11lll_opy_ for err_msg in bstack11l11lll1_opy_):
                bstack11l111ll1_opy_(url, CONFIG, logger, True)
        except Exception as err:
            logger.debug(bstack1l1l111l1_opy_.format(str(err)))
        raise e
def bstack1ll1l11l1l_opy_(item, when):
    global bstack111l1llll_opy_
    try:
        bstack111l1llll_opy_(item, when)
    except Exception as e:
        pass
def bstack1ll11l111l_opy_(item, call, rep):
    global bstack1lll1ll1ll_opy_
    global bstack1l1l1ll1l1_opy_
    name = bstack111l11_opy_ (u"ࠪࠫឪ")
    try:
        if rep.when == bstack111l11_opy_ (u"ࠫࡨࡧ࡬࡭ࠩឫ"):
            bstack1ll111l1_opy_ = threading.current_thread().bstackSessionId
            bstack1ll1lll1l11_opy_ = item.config.getoption(bstack111l11_opy_ (u"ࠬࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧឬ"))
            try:
                if (str(bstack1ll1lll1l11_opy_).lower() != bstack111l11_opy_ (u"࠭ࡴࡳࡷࡨࠫឭ")):
                    name = str(rep.nodeid)
                    bstack1l11l11ll_opy_ = bstack1l11l1l111_opy_(bstack111l11_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨឮ"), name, bstack111l11_opy_ (u"ࠨࠩឯ"), bstack111l11_opy_ (u"ࠩࠪឰ"), bstack111l11_opy_ (u"ࠪࠫឱ"), bstack111l11_opy_ (u"ࠫࠬឲ"))
                    os.environ[bstack111l11_opy_ (u"ࠬࡖ࡙ࡕࡇࡖࡘࡤ࡚ࡅࡔࡖࡢࡒࡆࡓࡅࠨឳ")] = name
                    for driver in bstack1l1l1ll1l1_opy_:
                        if bstack1ll111l1_opy_ == driver.session_id:
                            driver.execute_script(bstack1l11l11ll_opy_)
            except Exception as e:
                logger.debug(bstack111l11_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡵࡨࡸࡹ࡯࡮ࡨࠢࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠠࡧࡱࡵࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡵࡨࡷࡸ࡯࡯࡯࠼ࠣࡿࢂ࠭឴").format(str(e)))
            try:
                bstack1l1l11ll11_opy_(rep.outcome.lower())
                if rep.outcome.lower() != bstack111l11_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨ឵"):
                    status = bstack111l11_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨា") if rep.outcome.lower() == bstack111l11_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩិ") else bstack111l11_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪី")
                    reason = bstack111l11_opy_ (u"ࠫࠬឹ")
                    if status == bstack111l11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬឺ"):
                        reason = rep.longrepr.reprcrash.message
                        if (not threading.current_thread().bstackTestErrorMessages):
                            threading.current_thread().bstackTestErrorMessages = []
                        threading.current_thread().bstackTestErrorMessages.append(reason)
                    level = bstack111l11_opy_ (u"࠭ࡩ࡯ࡨࡲࠫុ") if status == bstack111l11_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧូ") else bstack111l11_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧួ")
                    data = name + bstack111l11_opy_ (u"ࠩࠣࡴࡦࡹࡳࡦࡦࠤࠫើ") if status == bstack111l11_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪឿ") else name + bstack111l11_opy_ (u"ࠫࠥ࡬ࡡࡪ࡮ࡨࡨࠦࠦࠧៀ") + reason
                    bstack1l1l1ll1ll_opy_ = bstack1l11l1l111_opy_(bstack111l11_opy_ (u"ࠬࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠧេ"), bstack111l11_opy_ (u"࠭ࠧែ"), bstack111l11_opy_ (u"ࠧࠨៃ"), bstack111l11_opy_ (u"ࠨࠩោ"), level, data)
                    for driver in bstack1l1l1ll1l1_opy_:
                        if bstack1ll111l1_opy_ == driver.session_id:
                            driver.execute_script(bstack1l1l1ll1ll_opy_)
            except Exception as e:
                logger.debug(bstack111l11_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡣࡰࡰࡷࡩࡽࡺࠠࡧࡱࡵࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡵࡨࡷࡸ࡯࡯࡯࠼ࠣࡿࢂ࠭ៅ").format(str(e)))
    except Exception as e:
        logger.debug(bstack111l11_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥ࡭ࡥࡵࡶ࡬ࡲ࡬ࠦࡳࡵࡣࡷࡩࠥ࡯࡮ࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡺࡥࡴࡶࠣࡷࡹࡧࡴࡶࡵ࠽ࠤࢀࢃࠧំ").format(str(e)))
    bstack1lll1ll1ll_opy_(item, call, rep)
notset = Notset()
def bstack11l1llll1_opy_(self, name: str, default=notset, skip: bool = False):
    global bstack1llll1ll_opy_
    if str(name).lower() == bstack111l11_opy_ (u"ࠫࡩࡸࡩࡷࡧࡵࠫះ"):
        return bstack111l11_opy_ (u"ࠧࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠦៈ")
    else:
        return bstack1llll1ll_opy_(self, name, default, skip)
def bstack1l1ll11111_opy_(self):
    global CONFIG
    global bstack111l1l11_opy_
    try:
        proxy = bstack1llll1l11_opy_(CONFIG)
        if proxy:
            if proxy.endswith(bstack111l11_opy_ (u"࠭࠮ࡱࡣࡦࠫ៉")):
                proxies = bstack1l1l11l11l_opy_(proxy, bstack1l1l1l111_opy_())
                if len(proxies) > 0:
                    protocol, bstack1l111l1l1_opy_ = proxies.popitem()
                    if bstack111l11_opy_ (u"ࠢ࠻࠱࠲ࠦ៊") in bstack1l111l1l1_opy_:
                        return bstack1l111l1l1_opy_
                    else:
                        return bstack111l11_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤ់") + bstack1l111l1l1_opy_
            else:
                return proxy
    except Exception as e:
        logger.error(bstack111l11_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡶࡲࡰࡺࡼࠤࡺࡸ࡬ࠡ࠼ࠣࡿࢂࠨ៌").format(str(e)))
    return bstack111l1l11_opy_(self)
def bstack11l1ll1l1_opy_():
    return (bstack111l11_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭៍") in CONFIG or bstack111l11_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨ៎") in CONFIG) and bstack1ll1l11l11_opy_() and bstack1lll1l1ll_opy_() >= version.parse(
        bstack1l111lll_opy_)
def bstack1ll11ll1l1_opy_(self,
               executablePath=None,
               channel=None,
               args=None,
               ignoreDefaultArgs=None,
               handleSIGINT=None,
               handleSIGTERM=None,
               handleSIGHUP=None,
               timeout=None,
               env=None,
               headless=None,
               devtools=None,
               proxy=None,
               downloadsPath=None,
               slowMo=None,
               tracesDir=None,
               chromiumSandbox=None,
               firefoxUserPrefs=None
               ):
    global CONFIG
    global bstack1l11l11l1_opy_
    global bstack111lll1ll_opy_
    global bstack1lll1ll11_opy_
    CONFIG[bstack111l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧ៏")] = str(bstack1lll1ll11_opy_) + str(__version__)
    bstack1ll11lllll_opy_ = 0
    try:
        if bstack111lll1ll_opy_ is True:
            bstack1ll11lllll_opy_ = int(os.environ.get(bstack111l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭័")))
    except:
        bstack1ll11lllll_opy_ = 0
    CONFIG[bstack111l11_opy_ (u"ࠢࡪࡵࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨ៑")] = True
    bstack1ll1ll1111_opy_ = bstack111ll11ll_opy_(CONFIG, bstack1ll11lllll_opy_)
    logger.debug(bstack111l11111_opy_.format(str(bstack1ll1ll1111_opy_)))
    if CONFIG.get(bstack111l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰ្ࠬ")):
        bstack111llll1l_opy_(bstack1ll1ll1111_opy_, bstack1l11ll1l_opy_)
    if bstack111l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ៓") in CONFIG and bstack111l11_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ។") in CONFIG[bstack111l11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ៕")][bstack1ll11lllll_opy_]:
        bstack1l11l11l1_opy_ = CONFIG[bstack111l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ៖")][bstack1ll11lllll_opy_][bstack111l11_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫៗ")]
    import urllib
    import json
    bstack11l1111l_opy_ = bstack111l11_opy_ (u"ࠧࡸࡵࡶ࠾࠴࠵ࡣࡥࡲ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࡂࡧࡦࡶࡳ࠾ࠩ៘") + urllib.parse.quote(json.dumps(bstack1ll1ll1111_opy_))
    browser = self.connect(bstack11l1111l_opy_)
    return browser
def bstack1ll1lllll_opy_():
    global bstack1ll1l1ll11_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        BrowserType.launch = bstack1ll11ll1l1_opy_
        bstack1ll1l1ll11_opy_ = True
    except Exception as e:
        pass
def bstack1lll11l1ll1_opy_():
    global CONFIG
    global bstack1lll11l11_opy_
    global bstack1l1l11l11_opy_
    global bstack1l11ll1l_opy_
    global bstack111lll1ll_opy_
    global bstack111llll11_opy_
    CONFIG = json.loads(os.environ.get(bstack111l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡑࡑࡊࡎࡍࠧ៙")))
    bstack1lll11l11_opy_ = eval(os.environ.get(bstack111l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪ៚")))
    bstack1l1l11l11_opy_ = os.environ.get(bstack111l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡋ࡙ࡇࡥࡕࡓࡎࠪ៛"))
    bstack1l1ll1ll_opy_(CONFIG, bstack1lll11l11_opy_)
    bstack111llll11_opy_ = bstack1l1l1l1l1_opy_.bstack11ll1ll1l_opy_(CONFIG, bstack111llll11_opy_)
    global bstack1ll111l11l_opy_
    global bstack11l1lll1_opy_
    global bstack1l11ll11_opy_
    global bstack1l1ll1l1_opy_
    global bstack1ll1l1ll1l_opy_
    global bstack1lll1llll_opy_
    global bstack111l1l1l1_opy_
    global bstack1l1ll1l11l_opy_
    global bstack111l1l11_opy_
    global bstack1llll1ll_opy_
    global bstack111l1llll_opy_
    global bstack1lll1ll1ll_opy_
    try:
        from selenium import webdriver
        from selenium.webdriver.remote.webdriver import WebDriver
        bstack1ll111l11l_opy_ = webdriver.Remote.__init__
        bstack11l1lll1_opy_ = WebDriver.quit
        bstack111l1l1l1_opy_ = WebDriver.close
        bstack1l1ll1l11l_opy_ = WebDriver.get
    except Exception as e:
        pass
    if (bstack111l11_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧៜ") in CONFIG or bstack111l11_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩ៝") in CONFIG) and bstack1ll1l11l11_opy_():
        if bstack1lll1l1ll_opy_() < version.parse(bstack1l111lll_opy_):
            logger.error(bstack1ll11111l_opy_.format(bstack1lll1l1ll_opy_()))
        else:
            try:
                from selenium.webdriver.remote.remote_connection import RemoteConnection
                bstack111l1l11_opy_ = RemoteConnection._get_proxy_url
            except Exception as e:
                logger.error(bstack1l1l1lllll_opy_.format(str(e)))
    try:
        from _pytest.config import Config
        bstack1llll1ll_opy_ = Config.getoption
        from _pytest import runner
        bstack111l1llll_opy_ = runner._update_current_test_var
    except Exception as e:
        logger.warn(e, bstack1l11l1l1_opy_)
    try:
        from pytest_bdd import reporting
        bstack1lll1ll1ll_opy_ = reporting.runtest_makereport
    except Exception as e:
        logger.debug(bstack111l11_opy_ (u"࠭ࡐ࡭ࡧࡤࡷࡪࠦࡩ࡯ࡵࡷࡥࡱࡲࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡹࡵࠠࡳࡷࡱࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡶࡨࡷࡹࡹࠧ៞"))
    bstack1l11ll1l_opy_ = CONFIG.get(bstack111l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫ៟"), {}).get(bstack111l11_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ០"))
    bstack111lll1ll_opy_ = True
    bstack11l11l111_opy_(bstack1llll1ll1_opy_)
if (bstack111l1l1l1l_opy_()):
    bstack1lll11l1ll1_opy_()
@bstack1l1111ll11_opy_(class_method=False)
def bstack1lll1111l11_opy_(hook_name, event, bstack1ll1lllllll_opy_=None):
    if hook_name not in [bstack111l11_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠࡨࡸࡲࡨࡺࡩࡰࡰࠪ១"), bstack111l11_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧ២"), bstack111l11_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡱࡴࡪࡵ࡭ࡧࠪ៣"), bstack111l11_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡱࡧࡹࡱ࡫ࠧ៤"), bstack111l11_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡩ࡬ࡢࡵࡶࠫ៥"), bstack111l11_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡦࡰࡦࡹࡳࠨ៦"), bstack111l11_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟࡮ࡧࡷ࡬ࡴࡪࠧ៧"), bstack111l11_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲ࡫ࡴࡩࡱࡧࠫ៨")]:
        return
    node = store[bstack111l11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡸࡪࡳࠧ៩")]
    if hook_name in [bstack111l11_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡱࡴࡪࡵ࡭ࡧࠪ៪"), bstack111l11_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡱࡧࡹࡱ࡫ࠧ៫")]:
        node = store[bstack111l11_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟࡮ࡱࡧࡹࡱ࡫࡟ࡪࡶࡨࡱࠬ៬")]
    elif hook_name in [bstack111l11_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥࡣ࡭ࡣࡶࡷࠬ៭"), bstack111l11_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡧࡱࡧࡳࡴࠩ៮")]:
        node = store[bstack111l11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡧࡱࡧࡳࡴࡡ࡬ࡸࡪࡳࠧ៯")]
    if event == bstack111l11_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࠪ៰"):
        hook_type = bstack1llll1ll11l_opy_(hook_name)
        uuid = uuid4().__str__()
        bstack1l1111lll1_opy_ = {
            bstack111l11_opy_ (u"ࠫࡺࡻࡩࡥࠩ៱"): uuid,
            bstack111l11_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩ៲"): bstack11ll1l1ll_opy_(),
            bstack111l11_opy_ (u"࠭ࡴࡺࡲࡨࠫ៳"): bstack111l11_opy_ (u"ࠧࡩࡱࡲ࡯ࠬ៴"),
            bstack111l11_opy_ (u"ࠨࡪࡲࡳࡰࡥࡴࡺࡲࡨࠫ៵"): hook_type,
            bstack111l11_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟࡯ࡣࡰࡩࠬ៶"): hook_name
        }
        store[bstack111l11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧ៷")].append(uuid)
        bstack1lll11l1l11_opy_ = node.nodeid
        if hook_type == bstack111l11_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡊࡇࡃࡉࠩ៸"):
            if not _11lll1lll1_opy_.get(bstack1lll11l1l11_opy_, None):
                _11lll1lll1_opy_[bstack1lll11l1l11_opy_] = {bstack111l11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫ៹"): []}
            _11lll1lll1_opy_[bstack1lll11l1l11_opy_][bstack111l11_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬ៺")].append(bstack1l1111lll1_opy_[bstack111l11_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ៻")])
        _11lll1lll1_opy_[bstack1lll11l1l11_opy_ + bstack111l11_opy_ (u"ࠨ࠯ࠪ៼") + hook_name] = bstack1l1111lll1_opy_
        bstack1lll11l1l1l_opy_(node, bstack1l1111lll1_opy_, bstack111l11_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪ៽"))
    elif event == bstack111l11_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࠩ៾"):
        bstack11llll11l1_opy_ = node.nodeid + bstack111l11_opy_ (u"ࠫ࠲࠭៿") + hook_name
        _11lll1lll1_opy_[bstack11llll11l1_opy_][bstack111l11_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ᠀")] = bstack11ll1l1ll_opy_()
        bstack1lll111l1l1_opy_(_11lll1lll1_opy_[bstack11llll11l1_opy_][bstack111l11_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ᠁")])
        bstack1lll11l1l1l_opy_(node, _11lll1lll1_opy_[bstack11llll11l1_opy_], bstack111l11_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩ᠂"), bstack1lll1111ll1_opy_=bstack1ll1lllllll_opy_)
def bstack1ll1llll11l_opy_():
    global bstack1lll11l111l_opy_
    if bstack11l1l111_opy_():
        bstack1lll11l111l_opy_ = bstack111l11_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠬ᠃")
    else:
        bstack1lll11l111l_opy_ = bstack111l11_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ᠄")
@bstack1lll1ll1l_opy_.bstack1lll1l111ll_opy_
def bstack1ll1llllll1_opy_():
    bstack1ll1llll11l_opy_()
    if bstack1ll1l11l11_opy_():
        bstack1ll1lll11l_opy_(bstack1l1llllll1_opy_)
    try:
        bstack1111llllll_opy_(bstack1lll1111l11_opy_)
    except Exception as e:
        logger.debug(bstack111l11_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢ࡫ࡳࡴࡱࡳࠡࡲࡤࡸࡨ࡮࠺ࠡࡽࢀࠦ᠅").format(e))
bstack1ll1llllll1_opy_()
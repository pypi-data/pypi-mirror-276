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
from _pytest import fixtures
from _pytest.python import _call_with_optional_argument
from pytest import Module, Class
from bstack_utils.helper import Result, bstack111l11lll1_opy_
from browserstack_sdk.bstack11111lll1_opy_ import bstack1l11l111l_opy_
def _1111lllll1_opy_(method, this, arg):
    arg_count = method.__code__.co_argcount
    if arg_count > 1:
        method(this, arg)
    else:
        method(this)
class bstack1111llllll_opy_:
    def __init__(self, handler):
        self._111l111l11_opy_ = {}
        self._111l11l1l1_opy_ = {}
        self.handler = handler
        self.patch()
        pass
    def patch(self):
        pytest_version = bstack1l11l111l_opy_.version()
        if bstack111l11lll1_opy_(pytest_version, bstack111l11_opy_ (u"ࠨ࠸࠯࠳࠱࠵ࠧጿ")) >= 0:
            self._111l111l11_opy_[bstack111l11_opy_ (u"ࠧࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠪፀ")] = Module._register_setup_function_fixture
            self._111l111l11_opy_[bstack111l11_opy_ (u"ࠨ࡯ࡲࡨࡺࡲࡥࡠࡨ࡬ࡼࡹࡻࡲࡦࠩፁ")] = Module._register_setup_module_fixture
            self._111l111l11_opy_[bstack111l11_opy_ (u"ࠩࡦࡰࡦࡹࡳࡠࡨ࡬ࡼࡹࡻࡲࡦࠩፂ")] = Class._register_setup_class_fixture
            self._111l111l11_opy_[bstack111l11_opy_ (u"ࠪࡱࡪࡺࡨࡰࡦࡢࡪ࡮ࡾࡴࡶࡴࡨࠫፃ")] = Class._register_setup_method_fixture
            Module._register_setup_function_fixture = self.bstack111l111ll1_opy_(bstack111l11_opy_ (u"ࠫ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧፄ"))
            Module._register_setup_module_fixture = self.bstack111l111ll1_opy_(bstack111l11_opy_ (u"ࠬࡳ࡯ࡥࡷ࡯ࡩࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ፅ"))
            Class._register_setup_class_fixture = self.bstack111l111ll1_opy_(bstack111l11_opy_ (u"࠭ࡣ࡭ࡣࡶࡷࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ፆ"))
            Class._register_setup_method_fixture = self.bstack111l111ll1_opy_(bstack111l11_opy_ (u"ࠧ࡮ࡧࡷ࡬ࡴࡪ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨፇ"))
        else:
            self._111l111l11_opy_[bstack111l11_opy_ (u"ࠨࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫፈ")] = Module._inject_setup_function_fixture
            self._111l111l11_opy_[bstack111l11_opy_ (u"ࠩࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࠪፉ")] = Module._inject_setup_module_fixture
            self._111l111l11_opy_[bstack111l11_opy_ (u"ࠪࡧࡱࡧࡳࡴࡡࡩ࡭ࡽࡺࡵࡳࡧࠪፊ")] = Class._inject_setup_class_fixture
            self._111l111l11_opy_[bstack111l11_opy_ (u"ࠫࡲ࡫ࡴࡩࡱࡧࡣ࡫࡯ࡸࡵࡷࡵࡩࠬፋ")] = Class._inject_setup_method_fixture
            Module._inject_setup_function_fixture = self.bstack111l111ll1_opy_(bstack111l11_opy_ (u"ࠬ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨፌ"))
            Module._inject_setup_module_fixture = self.bstack111l111ll1_opy_(bstack111l11_opy_ (u"࠭࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠧፍ"))
            Class._inject_setup_class_fixture = self.bstack111l111ll1_opy_(bstack111l11_opy_ (u"ࠧࡤ࡮ࡤࡷࡸࡥࡦࡪࡺࡷࡹࡷ࡫ࠧፎ"))
            Class._inject_setup_method_fixture = self.bstack111l111ll1_opy_(bstack111l11_opy_ (u"ࠨ࡯ࡨࡸ࡭ࡵࡤࡠࡨ࡬ࡼࡹࡻࡲࡦࠩፏ"))
    def bstack111l11l1ll_opy_(self, bstack111l1111ll_opy_, hook_type):
        meth = getattr(bstack111l1111ll_opy_, hook_type, None)
        if meth is not None and fixtures.getfixturemarker(meth) is None:
            self._111l11l1l1_opy_[hook_type] = meth
            setattr(bstack111l1111ll_opy_, hook_type, self.bstack111l11111l_opy_(hook_type))
    def bstack111l11l111_opy_(self, instance, bstack111l111l1l_opy_):
        if bstack111l111l1l_opy_ == bstack111l11_opy_ (u"ࠤࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠧፐ"):
            self.bstack111l11l1ll_opy_(instance.obj, bstack111l11_opy_ (u"ࠥࡷࡪࡺࡵࡱࡡࡩࡹࡳࡩࡴࡪࡱࡱࠦፑ"))
            self.bstack111l11l1ll_opy_(instance.obj, bstack111l11_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠣፒ"))
        if bstack111l111l1l_opy_ == bstack111l11_opy_ (u"ࠧࡳ࡯ࡥࡷ࡯ࡩࡤ࡬ࡩࡹࡶࡸࡶࡪࠨፓ"):
            self.bstack111l11l1ll_opy_(instance.obj, bstack111l11_opy_ (u"ࠨࡳࡦࡶࡸࡴࡤࡳ࡯ࡥࡷ࡯ࡩࠧፔ"))
            self.bstack111l11l1ll_opy_(instance.obj, bstack111l11_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡳࡩࡻ࡬ࡦࠤፕ"))
        if bstack111l111l1l_opy_ == bstack111l11_opy_ (u"ࠣࡥ࡯ࡥࡸࡹ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠣፖ"):
            self.bstack111l11l1ll_opy_(instance.obj, bstack111l11_opy_ (u"ࠤࡶࡩࡹࡻࡰࡠࡥ࡯ࡥࡸࡹࠢፗ"))
            self.bstack111l11l1ll_opy_(instance.obj, bstack111l11_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࡤࡩ࡬ࡢࡵࡶࠦፘ"))
        if bstack111l111l1l_opy_ == bstack111l11_opy_ (u"ࠦࡲ࡫ࡴࡩࡱࡧࡣ࡫࡯ࡸࡵࡷࡵࡩࠧፙ"):
            self.bstack111l11l1ll_opy_(instance.obj, bstack111l11_opy_ (u"ࠧࡹࡥࡵࡷࡳࡣࡲ࡫ࡴࡩࡱࡧࠦፚ"))
            self.bstack111l11l1ll_opy_(instance.obj, bstack111l11_opy_ (u"ࠨࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡨࡸ࡭ࡵࡤࠣ፛"))
    @staticmethod
    def bstack111l11ll11_opy_(hook_type, func, args):
        if hook_type in [bstack111l11_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡦࡶ࡫ࡳࡩ࠭፜"), bstack111l11_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡪࡺࡨࡰࡦࠪ፝")]:
            _1111lllll1_opy_(func, args[0], args[1])
            return
        _call_with_optional_argument(func, args[0])
    def bstack111l11111l_opy_(self, hook_type):
        def bstack111l1111l1_opy_(arg=None):
            self.handler(hook_type, bstack111l11_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࠩ፞"))
            result = None
            exception = None
            try:
                self.bstack111l11ll11_opy_(hook_type, self._111l11l1l1_opy_[hook_type], (arg,))
                result = Result(result=bstack111l11_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪ፟"))
            except Exception as e:
                result = Result(result=bstack111l11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ፠"), exception=e)
                self.handler(hook_type, bstack111l11_opy_ (u"ࠬࡧࡦࡵࡧࡵࠫ፡"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack111l11_opy_ (u"࠭ࡡࡧࡶࡨࡶࠬ።"), result)
        def bstack111l111lll_opy_(this, arg=None):
            self.handler(hook_type, bstack111l11_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫ࠧ፣"))
            result = None
            exception = None
            try:
                self.bstack111l11ll11_opy_(hook_type, self._111l11l1l1_opy_[hook_type], (this, arg))
                result = Result(result=bstack111l11_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨ፤"))
            except Exception as e:
                result = Result(result=bstack111l11_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ፥"), exception=e)
                self.handler(hook_type, bstack111l11_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࠩ፦"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack111l11_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࠪ፧"), result)
        if hook_type in [bstack111l11_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲ࡫ࡴࡩࡱࡧࠫ፨"), bstack111l11_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡨࡸ࡭ࡵࡤࠨ፩")]:
            return bstack111l111lll_opy_
        return bstack111l1111l1_opy_
    def bstack111l111ll1_opy_(self, bstack111l111l1l_opy_):
        def bstack111l11l11l_opy_(this, *args, **kwargs):
            self.bstack111l11l111_opy_(this, bstack111l111l1l_opy_)
            self._111l111l11_opy_[bstack111l111l1l_opy_](this, *args, **kwargs)
        return bstack111l11l11l_opy_
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
from uuid import uuid4
from bstack_utils.helper import bstack11ll1l1ll_opy_, bstack11l11l11l1_opy_
from bstack_utils.bstack1llll1ll11_opy_ import bstack1llll1ll111_opy_
class bstack1l111l111l_opy_:
    def __init__(self, name=None, code=None, uuid=None, file_path=None, bstack11llllll11_opy_=None, framework=None, tags=[], scope=[], bstack1lll1ll1111_opy_=None, bstack1lll1lllll1_opy_=True, bstack1lll1l1ll1l_opy_=None, bstack1llllll111_opy_=None, result=None, duration=None, bstack1l11111l1l_opy_=None, meta={}):
        self.bstack1l11111l1l_opy_ = bstack1l11111l1l_opy_
        self.name = name
        self.code = code
        self.file_path = file_path
        self.uuid = uuid
        if not self.uuid and bstack1lll1lllll1_opy_:
            self.uuid = uuid4().__str__()
        self.bstack11llllll11_opy_ = bstack11llllll11_opy_
        self.framework = framework
        self.tags = tags
        self.scope = scope
        self.bstack1lll1ll1111_opy_ = bstack1lll1ll1111_opy_
        self.bstack1lll1l1ll1l_opy_ = bstack1lll1l1ll1l_opy_
        self.bstack1llllll111_opy_ = bstack1llllll111_opy_
        self.result = result
        self.duration = duration
        self.meta = meta
    def bstack11lll11ll1_opy_(self):
        if self.uuid:
            return self.uuid
        self.uuid = uuid4().__str__()
        return self.uuid
    def bstack1lll1lll111_opy_(self):
        bstack1lll1ll11ll_opy_ = os.path.relpath(self.file_path, start=os.getcwd())
        return {
            bstack111l11_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩᓕ"): bstack1lll1ll11ll_opy_,
            bstack111l11_opy_ (u"ࠧ࡭ࡱࡦࡥࡹ࡯࡯࡯ࠩᓖ"): bstack1lll1ll11ll_opy_,
            bstack111l11_opy_ (u"ࠨࡸࡦࡣ࡫࡯࡬ࡦࡲࡤࡸ࡭࠭ᓗ"): bstack1lll1ll11ll_opy_
        }
    def set(self, **kwargs):
        for key, val in kwargs.items():
            if not hasattr(self, key):
                raise TypeError(bstack111l11_opy_ (u"ࠤࡘࡲࡪࡾࡰࡦࡥࡷࡩࡩࠦࡡࡳࡩࡸࡱࡪࡴࡴ࠻ࠢࠥᓘ") + key)
            setattr(self, key, val)
    def bstack1lll1ll1ll1_opy_(self):
        return {
            bstack111l11_opy_ (u"ࠪࡲࡦࡳࡥࠨᓙ"): self.name,
            bstack111l11_opy_ (u"ࠫࡧࡵࡤࡺࠩᓚ"): {
                bstack111l11_opy_ (u"ࠬࡲࡡ࡯ࡩࠪᓛ"): bstack111l11_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭ᓜ"),
                bstack111l11_opy_ (u"ࠧࡤࡱࡧࡩࠬᓝ"): self.code
            },
            bstack111l11_opy_ (u"ࠨࡵࡦࡳࡵ࡫ࡳࠨᓞ"): self.scope,
            bstack111l11_opy_ (u"ࠩࡷࡥ࡬ࡹࠧᓟ"): self.tags,
            bstack111l11_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ᓠ"): self.framework,
            bstack111l11_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨᓡ"): self.bstack11llllll11_opy_
        }
    def bstack1lll1ll1l1l_opy_(self):
        return {
         bstack111l11_opy_ (u"ࠬࡳࡥࡵࡣࠪᓢ"): self.meta
        }
    def bstack1lll1l1llll_opy_(self):
        return {
            bstack111l11_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲࡘࡥࡳࡷࡱࡔࡦࡸࡡ࡮ࠩᓣ"): {
                bstack111l11_opy_ (u"ࠧࡳࡧࡵࡹࡳࡥ࡮ࡢ࡯ࡨࠫᓤ"): self.bstack1lll1ll1111_opy_
            }
        }
    def bstack1lll1l1ll11_opy_(self, bstack1lll1ll1l11_opy_, details):
        step = next(filter(lambda st: st[bstack111l11_opy_ (u"ࠨ࡫ࡧࠫᓥ")] == bstack1lll1ll1l11_opy_, self.meta[bstack111l11_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨᓦ")]), None)
        step.update(details)
    def bstack1lll1ll111l_opy_(self, bstack1lll1ll1l11_opy_):
        step = next(filter(lambda st: st[bstack111l11_opy_ (u"ࠪ࡭ࡩ࠭ᓧ")] == bstack1lll1ll1l11_opy_, self.meta[bstack111l11_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪᓨ")]), None)
        step.update({
            bstack111l11_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩᓩ"): bstack11ll1l1ll_opy_()
        })
    def bstack1l1111l111_opy_(self, bstack1lll1ll1l11_opy_, result, duration=None):
        bstack1lll1l1ll1l_opy_ = bstack11ll1l1ll_opy_()
        if bstack1lll1ll1l11_opy_ is not None and self.meta.get(bstack111l11_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬᓪ")):
            step = next(filter(lambda st: st[bstack111l11_opy_ (u"ࠧࡪࡦࠪᓫ")] == bstack1lll1ll1l11_opy_, self.meta[bstack111l11_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧᓬ")]), None)
            step.update({
                bstack111l11_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧᓭ"): bstack1lll1l1ll1l_opy_,
                bstack111l11_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࠬᓮ"): duration if duration else bstack11l11l11l1_opy_(step[bstack111l11_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨᓯ")], bstack1lll1l1ll1l_opy_),
                bstack111l11_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬᓰ"): result.result,
                bstack111l11_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫ࠧᓱ"): str(result.exception) if result.exception else None
            })
    def add_step(self, bstack1lll1lll1ll_opy_):
        if self.meta.get(bstack111l11_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭ᓲ")):
            self.meta[bstack111l11_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧᓳ")].append(bstack1lll1lll1ll_opy_)
        else:
            self.meta[bstack111l11_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨᓴ")] = [ bstack1lll1lll1ll_opy_ ]
    def bstack1lll1llll1l_opy_(self):
        return {
            bstack111l11_opy_ (u"ࠪࡹࡺ࡯ࡤࠨᓵ"): self.bstack11lll11ll1_opy_(),
            **self.bstack1lll1ll1ll1_opy_(),
            **self.bstack1lll1lll111_opy_(),
            **self.bstack1lll1ll1l1l_opy_()
        }
    def bstack1lll1lll1l1_opy_(self):
        if not self.result:
            return {}
        data = {
            bstack111l11_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩᓶ"): self.bstack1lll1l1ll1l_opy_,
            bstack111l11_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴ࡟ࡪࡰࡢࡱࡸ࠭ᓷ"): self.duration,
            bstack111l11_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ᓸ"): self.result.result
        }
        if data[bstack111l11_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧᓹ")] == bstack111l11_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᓺ"):
            data[bstack111l11_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࡢࡸࡾࡶࡥࠨᓻ")] = self.result.bstack11ll11llll_opy_()
            data[bstack111l11_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࠫᓼ")] = [{bstack111l11_opy_ (u"ࠫࡧࡧࡣ࡬ࡶࡵࡥࡨ࡫ࠧᓽ"): self.result.bstack111l1l1l11_opy_()}]
        return data
    def bstack1lll1lll11l_opy_(self):
        return {
            bstack111l11_opy_ (u"ࠬࡻࡵࡪࡦࠪᓾ"): self.bstack11lll11ll1_opy_(),
            **self.bstack1lll1ll1ll1_opy_(),
            **self.bstack1lll1lll111_opy_(),
            **self.bstack1lll1lll1l1_opy_(),
            **self.bstack1lll1ll1l1l_opy_()
        }
    def bstack11lllllll1_opy_(self, event, result=None):
        if result:
            self.result = result
        if bstack111l11_opy_ (u"࠭ࡓࡵࡣࡵࡸࡪࡪࠧᓿ") in event:
            return self.bstack1lll1llll1l_opy_()
        elif bstack111l11_opy_ (u"ࠧࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩᔀ") in event:
            return self.bstack1lll1lll11l_opy_()
    def bstack11llll1111_opy_(self):
        pass
    def stop(self, time=None, duration=None, result=None):
        self.bstack1lll1l1ll1l_opy_ = time if time else bstack11ll1l1ll_opy_()
        self.duration = duration if duration else bstack11l11l11l1_opy_(self.bstack11llllll11_opy_, self.bstack1lll1l1ll1l_opy_)
        if result:
            self.result = result
class bstack11lll1ll11_opy_(bstack1l111l111l_opy_):
    def __init__(self, hooks=[], bstack1l111ll111_opy_={}, *args, **kwargs):
        self.hooks = hooks
        self.bstack1l111ll111_opy_ = bstack1l111ll111_opy_
        super().__init__(*args, **kwargs, bstack1llllll111_opy_=bstack111l11_opy_ (u"ࠨࡶࡨࡷࡹ࠭ᔁ"))
    @classmethod
    def bstack1lll1l1lll1_opy_(cls, scenario, feature, test, **kwargs):
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack111l11_opy_ (u"ࠩ࡬ࡨࠬᔂ"): id(step),
                bstack111l11_opy_ (u"ࠪࡸࡪࡾࡴࠨᔃ"): step.name,
                bstack111l11_opy_ (u"ࠫࡰ࡫ࡹࡸࡱࡵࡨࠬᔄ"): step.keyword,
            })
        return bstack11lll1ll11_opy_(
            **kwargs,
            meta={
                bstack111l11_opy_ (u"ࠬ࡬ࡥࡢࡶࡸࡶࡪ࠭ᔅ"): {
                    bstack111l11_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᔆ"): feature.name,
                    bstack111l11_opy_ (u"ࠧࡱࡣࡷ࡬ࠬᔇ"): feature.filename,
                    bstack111l11_opy_ (u"ࠨࡦࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳ࠭ᔈ"): feature.description
                },
                bstack111l11_opy_ (u"ࠩࡶࡧࡪࡴࡡࡳ࡫ࡲࠫᔉ"): {
                    bstack111l11_opy_ (u"ࠪࡲࡦࡳࡥࠨᔊ"): scenario.name
                },
                bstack111l11_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪᔋ"): steps,
                bstack111l11_opy_ (u"ࠬ࡫ࡸࡢ࡯ࡳࡰࡪࡹࠧᔌ"): bstack1llll1ll111_opy_(test)
            }
        )
    def bstack1lll1ll11l1_opy_(self):
        return {
            bstack111l11_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬᔍ"): self.hooks
        }
    def bstack1lll1llll11_opy_(self):
        if self.bstack1l111ll111_opy_:
            return {
                bstack111l11_opy_ (u"ࠧࡪࡰࡷࡩ࡬ࡸࡡࡵ࡫ࡲࡲࡸ࠭ᔎ"): self.bstack1l111ll111_opy_
            }
        return {}
    def bstack1lll1lll11l_opy_(self):
        return {
            **super().bstack1lll1lll11l_opy_(),
            **self.bstack1lll1ll11l1_opy_()
        }
    def bstack1lll1llll1l_opy_(self):
        return {
            **super().bstack1lll1llll1l_opy_(),
            **self.bstack1lll1llll11_opy_()
        }
    def bstack11llll1111_opy_(self):
        return bstack111l11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࠪᔏ")
class bstack11lll11111_opy_(bstack1l111l111l_opy_):
    def __init__(self, hook_type, *args, **kwargs):
        self.hook_type = hook_type
        super().__init__(*args, **kwargs, bstack1llllll111_opy_=bstack111l11_opy_ (u"ࠩ࡫ࡳࡴࡱࠧᔐ"))
    def bstack11lllll111_opy_(self):
        return self.hook_type
    def bstack1lll1ll1lll_opy_(self):
        return {
            bstack111l11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡶࡼࡴࡪ࠭ᔑ"): self.hook_type
        }
    def bstack1lll1lll11l_opy_(self):
        return {
            **super().bstack1lll1lll11l_opy_(),
            **self.bstack1lll1ll1lll_opy_()
        }
    def bstack1lll1llll1l_opy_(self):
        return {
            **super().bstack1lll1llll1l_opy_(),
            **self.bstack1lll1ll1lll_opy_()
        }
    def bstack11llll1111_opy_(self):
        return bstack111l11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳ࠭ᔒ")
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
import json
class bstack11l1l1lll1_opy_(object):
  bstack11llll1ll_opy_ = os.path.join(os.path.expanduser(bstack111l11_opy_ (u"ࠨࢀࠪ໨")), bstack111l11_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩ໩"))
  bstack11l1l1ll11_opy_ = os.path.join(bstack11llll1ll_opy_, bstack111l11_opy_ (u"ࠪࡧࡴࡳ࡭ࡢࡰࡧࡷ࠳ࡰࡳࡰࡰࠪ໪"))
  bstack11l1l1ll1l_opy_ = None
  perform_scan = None
  bstack1llll111ll_opy_ = None
  bstack1111lll1l_opy_ = None
  bstack11ll11l1l1_opy_ = None
  def __new__(cls):
    if not hasattr(cls, bstack111l11_opy_ (u"ࠫ࡮ࡴࡳࡵࡣࡱࡧࡪ࠭໫")):
      cls.instance = super(bstack11l1l1lll1_opy_, cls).__new__(cls)
      cls.instance.bstack11l1l1l1ll_opy_()
    return cls.instance
  def bstack11l1l1l1ll_opy_(self):
    try:
      with open(self.bstack11l1l1ll11_opy_, bstack111l11_opy_ (u"ࠬࡸࠧ໬")) as bstack1l1ll111l_opy_:
        bstack11l1l1llll_opy_ = bstack1l1ll111l_opy_.read()
        data = json.loads(bstack11l1l1llll_opy_)
        if bstack111l11_opy_ (u"࠭ࡣࡰ࡯ࡰࡥࡳࡪࡳࠨ໭") in data:
          self.bstack11l1ll1ll1_opy_(data[bstack111l11_opy_ (u"ࠧࡤࡱࡰࡱࡦࡴࡤࡴࠩ໮")])
        if bstack111l11_opy_ (u"ࠨࡵࡦࡶ࡮ࡶࡴࡴࠩ໯") in data:
          self.bstack11l1ll1l11_opy_(data[bstack111l11_opy_ (u"ࠩࡶࡧࡷ࡯ࡰࡵࡵࠪ໰")])
    except:
      pass
  def bstack11l1ll1l11_opy_(self, scripts):
    if scripts != None:
      self.perform_scan = scripts[bstack111l11_opy_ (u"ࠪࡷࡨࡧ࡮ࠨ໱")]
      self.bstack1llll111ll_opy_ = scripts[bstack111l11_opy_ (u"ࠫ࡬࡫ࡴࡓࡧࡶࡹࡱࡺࡳࠨ໲")]
      self.bstack1111lll1l_opy_ = scripts[bstack111l11_opy_ (u"ࠬ࡭ࡥࡵࡔࡨࡷࡺࡲࡴࡴࡕࡸࡱࡲࡧࡲࡺࠩ໳")]
      self.bstack11ll11l1l1_opy_ = scripts[bstack111l11_opy_ (u"࠭ࡳࡢࡸࡨࡖࡪࡹࡵ࡭ࡶࡶࠫ໴")]
  def bstack11l1ll1ll1_opy_(self, bstack11l1l1ll1l_opy_):
    if bstack11l1l1ll1l_opy_ != None and len(bstack11l1l1ll1l_opy_) != 0:
      self.bstack11l1l1ll1l_opy_ = bstack11l1l1ll1l_opy_
  def store(self):
    try:
      with open(self.bstack11l1l1ll11_opy_, bstack111l11_opy_ (u"ࠧࡸࠩ໵")) as file:
        json.dump({
          bstack111l11_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࡵࠥ໶"): self.bstack11l1l1ll1l_opy_,
          bstack111l11_opy_ (u"ࠤࡶࡧࡷ࡯ࡰࡵࡵࠥ໷"): {
            bstack111l11_opy_ (u"ࠥࡷࡨࡧ࡮ࠣ໸"): self.perform_scan,
            bstack111l11_opy_ (u"ࠦ࡬࡫ࡴࡓࡧࡶࡹࡱࡺࡳࠣ໹"): self.bstack1llll111ll_opy_,
            bstack111l11_opy_ (u"ࠧ࡭ࡥࡵࡔࡨࡷࡺࡲࡴࡴࡕࡸࡱࡲࡧࡲࡺࠤ໺"): self.bstack1111lll1l_opy_,
            bstack111l11_opy_ (u"ࠨࡳࡢࡸࡨࡖࡪࡹࡵ࡭ࡶࡶࠦ໻"): self.bstack11ll11l1l1_opy_
          }
        }, file)
    except:
      pass
  def bstack1lll1l1ll1_opy_(self, bstack11l1l1l1l1_opy_):
    try:
      return any(command.get(bstack111l11_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ໼")) == bstack11l1l1l1l1_opy_ for command in self.bstack11l1l1ll1l_opy_)
    except:
      return False
bstack1l1lll1lll_opy_ = bstack11l1l1lll1_opy_()
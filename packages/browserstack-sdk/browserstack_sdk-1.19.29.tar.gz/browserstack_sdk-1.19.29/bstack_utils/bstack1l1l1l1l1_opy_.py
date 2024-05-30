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
import logging
import tarfile
import io
import os
import requests
import re
from requests_toolbelt.multipart.encoder import MultipartEncoder
from bstack_utils.constants import bstack11l1l111l1_opy_
import tempfile
import json
bstack1111ll111l_opy_ = os.path.join(tempfile.gettempdir(), bstack111l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡤࡦࡤࡸ࡫࠳ࡲ࡯ࡨࠩ፪"))
def get_logger(name=__name__, level=None):
  logger = logging.getLogger(name)
  if level:
    logging.basicConfig(
      level=level,
      format=bstack111l11_opy_ (u"ࠨ࡞ࡱࠩ࠭ࡧࡳࡤࡶ࡬ࡱࡪ࠯ࡳࠡ࡝ࠨࠬࡳࡧ࡭ࡦࠫࡶࡡࡠࠫࠨ࡭ࡧࡹࡩࡱࡴࡡ࡮ࡧࠬࡷࡢࠦ࠭ࠡࠧࠫࡱࡪࡹࡳࡢࡩࡨ࠭ࡸ࠭፫"),
      datefmt=bstack111l11_opy_ (u"ࠩࠨࡌ࠿ࠫࡍ࠻ࠧࡖࠫ፬"),
      stream=sys.stdout
    )
  return logger
def bstack1111lll1ll_opy_():
  global bstack1111ll111l_opy_
  if os.path.exists(bstack1111ll111l_opy_):
    os.remove(bstack1111ll111l_opy_)
def bstack1111l111l_opy_():
  for handler in logging.getLogger().handlers:
    logging.getLogger().removeHandler(handler)
def bstack11ll1ll1l_opy_(config, log_level):
  bstack1111ll1111_opy_ = log_level
  if bstack111l11_opy_ (u"ࠪࡰࡴ࡭ࡌࡦࡸࡨࡰࠬ፭") in config and config[bstack111l11_opy_ (u"ࠫࡱࡵࡧࡍࡧࡹࡩࡱ࠭፮")] in bstack11l1l111l1_opy_:
    bstack1111ll1111_opy_ = bstack11l1l111l1_opy_[config[bstack111l11_opy_ (u"ࠬࡲ࡯ࡨࡎࡨࡺࡪࡲࠧ፯")]]
  if config.get(bstack111l11_opy_ (u"࠭ࡤࡪࡵࡤࡦࡱ࡫ࡁࡶࡶࡲࡇࡦࡶࡴࡶࡴࡨࡐࡴ࡭ࡳࠨ፰"), False):
    logging.getLogger().setLevel(bstack1111ll1111_opy_)
    return bstack1111ll1111_opy_
  global bstack1111ll111l_opy_
  bstack1111l111l_opy_()
  bstack1111lll111_opy_ = logging.Formatter(
    fmt=bstack111l11_opy_ (u"ࠧ࡝ࡰࠨࠬࡦࡹࡣࡵ࡫ࡰࡩ࠮ࡹࠠ࡜ࠧࠫࡲࡦࡳࡥࠪࡵࡠ࡟ࠪ࠮࡬ࡦࡸࡨࡰࡳࡧ࡭ࡦࠫࡶࡡࠥ࠳ࠠࠦࠪࡰࡩࡸࡹࡡࡨࡧࠬࡷࠬ፱"),
    datefmt=bstack111l11_opy_ (u"ࠨࠧࡋ࠾ࠪࡓ࠺ࠦࡕࠪ፲")
  )
  bstack1111ll11l1_opy_ = logging.StreamHandler(sys.stdout)
  file_handler = logging.FileHandler(bstack1111ll111l_opy_)
  file_handler.setFormatter(bstack1111lll111_opy_)
  bstack1111ll11l1_opy_.setFormatter(bstack1111lll111_opy_)
  file_handler.setLevel(logging.DEBUG)
  bstack1111ll11l1_opy_.setLevel(log_level)
  file_handler.addFilter(lambda r: r.name != bstack111l11_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰ࠲ࡼ࡫ࡢࡥࡴ࡬ࡺࡪࡸ࠮ࡳࡧࡰࡳࡹ࡫࠮ࡳࡧࡰࡳࡹ࡫࡟ࡤࡱࡱࡲࡪࡩࡴࡪࡱࡱࠫ፳"))
  logging.getLogger().setLevel(logging.DEBUG)
  bstack1111ll11l1_opy_.setLevel(bstack1111ll1111_opy_)
  logging.getLogger().addHandler(bstack1111ll11l1_opy_)
  logging.getLogger().addHandler(file_handler)
  return bstack1111ll1111_opy_
def bstack1111llll11_opy_(config):
  try:
    bstack1111lll1l1_opy_ = set([
      bstack111l11_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬ፴"), bstack111l11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧ፵"), bstack111l11_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨ፶"), bstack111l11_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪ፷"), bstack111l11_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳࡖࡢࡴ࡬ࡥࡧࡲࡥࡴࠩ፸"),
      bstack111l11_opy_ (u"ࠨࡲࡵࡳࡽࡿࡕࡴࡧࡵࠫ፹"), bstack111l11_opy_ (u"ࠩࡳࡶࡴࡾࡹࡑࡣࡶࡷࠬ፺"), bstack111l11_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡒࡵࡳࡽࡿࡕࡴࡧࡵࠫ፻"), bstack111l11_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡓࡶࡴࡾࡹࡑࡣࡶࡷࠬ፼")
    ])
    bstack1111ll1lll_opy_ = bstack111l11_opy_ (u"ࠬ࠭፽")
    with open(bstack111l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡿ࡭࡭ࠩ፾")) as bstack1111ll1ll1_opy_:
      bstack1111lll11l_opy_ = bstack1111ll1ll1_opy_.read()
      bstack1111ll1lll_opy_ = re.sub(bstack111l11_opy_ (u"ࡲࠨࡠࠫࡠࡸ࠱ࠩࡀࠥ࠱࠮ࠩࡢ࡮ࠨ፿"), bstack111l11_opy_ (u"ࠨࠩᎀ"), bstack1111lll11l_opy_, flags=re.M)
      bstack1111ll1lll_opy_ = re.sub(
        bstack111l11_opy_ (u"ࡴࠪࡢ࠭ࡢࡳࠬࠫࡂࠬࠬᎁ") + bstack111l11_opy_ (u"ࠪࢀࠬᎂ").join(bstack1111lll1l1_opy_) + bstack111l11_opy_ (u"ࠫ࠮࠴ࠪࠥࠩᎃ"),
        bstack111l11_opy_ (u"ࡷ࠭࡜࠳࠼ࠣ࡟ࡗࡋࡄࡂࡅࡗࡉࡉࡣࠧᎄ"),
        bstack1111ll1lll_opy_, flags=re.M | re.I
      )
    def bstack1111ll1l11_opy_(dic):
      bstack1111llll1l_opy_ = {}
      for key, value in dic.items():
        if key in bstack1111lll1l1_opy_:
          bstack1111llll1l_opy_[key] = bstack111l11_opy_ (u"࡛࠭ࡓࡇࡇࡅࡈ࡚ࡅࡅ࡟ࠪᎅ")
        else:
          if isinstance(value, dict):
            bstack1111llll1l_opy_[key] = bstack1111ll1l11_opy_(value)
          else:
            bstack1111llll1l_opy_[key] = value
      return bstack1111llll1l_opy_
    bstack1111llll1l_opy_ = bstack1111ll1l11_opy_(config)
    return {
      bstack111l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹ࡮࡮ࠪᎆ"): bstack1111ll1lll_opy_,
      bstack111l11_opy_ (u"ࠨࡨ࡬ࡲࡦࡲࡣࡰࡰࡩ࡭࡬࠴ࡪࡴࡱࡱࠫᎇ"): json.dumps(bstack1111llll1l_opy_)
    }
  except Exception as e:
    return {}
def bstack1l11111l1_opy_(config):
  global bstack1111ll111l_opy_
  try:
    if config.get(bstack111l11_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧࡄࡹࡹࡵࡃࡢࡲࡷࡹࡷ࡫ࡌࡰࡩࡶࠫᎈ"), False):
      return
    uuid = os.getenv(bstack111l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨᎉ"))
    if not uuid or uuid == bstack111l11_opy_ (u"ࠫࡳࡻ࡬࡭ࠩᎊ"):
      return
    bstack1111ll1l1l_opy_ = [bstack111l11_opy_ (u"ࠬࡸࡥࡲࡷ࡬ࡶࡪࡳࡥ࡯ࡶࡶ࠲ࡹࡾࡴࠨᎋ"), bstack111l11_opy_ (u"࠭ࡐࡪࡲࡩ࡭ࡱ࡫ࠧᎌ"), bstack111l11_opy_ (u"ࠧࡱࡻࡳࡶࡴࡰࡥࡤࡶ࠱ࡸࡴࡳ࡬ࠨᎍ"), bstack1111ll111l_opy_]
    bstack1111l111l_opy_()
    logging.shutdown()
    output_file = os.path.join(tempfile.gettempdir(), bstack111l11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠮࡮ࡲ࡫ࡸ࠳ࠧᎎ") + uuid + bstack111l11_opy_ (u"ࠩ࠱ࡸࡦࡸ࠮ࡨࡼࠪᎏ"))
    with tarfile.open(output_file, bstack111l11_opy_ (u"ࠥࡻ࠿࡭ࡺࠣ᎐")) as archive:
      for file in filter(lambda f: os.path.exists(f), bstack1111ll1l1l_opy_):
        try:
          archive.add(file,  arcname=os.path.basename(file))
        except:
          pass
      for name, data in bstack1111llll11_opy_(config).items():
        tarinfo = tarfile.TarInfo(name)
        bstack1111ll11ll_opy_ = data.encode()
        tarinfo.size = len(bstack1111ll11ll_opy_)
        archive.addfile(tarinfo, io.BytesIO(bstack1111ll11ll_opy_))
    bstack1lllllll1_opy_ = MultipartEncoder(
      fields= {
        bstack111l11_opy_ (u"ࠫࡩࡧࡴࡢࠩ᎑"): (os.path.basename(output_file), open(os.path.abspath(output_file), bstack111l11_opy_ (u"ࠬࡸࡢࠨ᎒")), bstack111l11_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳ࡽ࠳ࡧࡻ࡫ࡳࠫ᎓")),
        bstack111l11_opy_ (u"ࠧࡤ࡮࡬ࡩࡳࡺࡂࡶ࡫࡯ࡨ࡚ࡻࡩࡥࠩ᎔"): uuid
      }
    )
    response = requests.post(
      bstack111l11_opy_ (u"ࠣࡪࡷࡸࡵࡹ࠺࠰࠱ࡸࡴࡱࡵࡡࡥ࠯ࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡩ࡬ࡪࡧࡱࡸ࠲ࡲ࡯ࡨࡵ࠲ࡹࡵࡲ࡯ࡢࡦࠥ᎕"),
      data=bstack1lllllll1_opy_,
      headers={bstack111l11_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡘࡾࡶࡥࠨ᎖"): bstack1lllllll1_opy_.content_type},
      auth=(config[bstack111l11_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬ᎗")], config[bstack111l11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧ᎘")])
    )
    os.remove(output_file)
    if response.status_code != 200:
      get_logger().debug(bstack111l11_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤࡺࡶ࡬ࡰࡣࡧࠤࡱࡵࡧࡴ࠼ࠣࠫ᎙") + response.status_code)
  except Exception as e:
    get_logger().debug(bstack111l11_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡹࡥ࡯ࡦ࡬ࡲ࡬ࠦ࡬ࡰࡩࡶ࠾ࠬ᎚") + str(e))
  finally:
    try:
      bstack1111lll1ll_opy_()
    except:
      pass
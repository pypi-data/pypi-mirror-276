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
import re
import sys
import json
import time
import shutil
import tempfile
import requests
import subprocess
from threading import Thread
from os.path import expanduser
from bstack_utils.constants import *
from requests.auth import HTTPBasicAuth
from bstack_utils.helper import bstack1lllll11l_opy_, bstack1lllll1lll_opy_
class bstack1l11l11l1l_opy_:
  working_dir = os.getcwd()
  bstack1ll111lll1_opy_ = False
  config = {}
  binary_path = bstack111l11_opy_ (u"ࠨࠩᏢ")
  bstack1111l1111l_opy_ = bstack111l11_opy_ (u"ࠩࠪᏣ")
  bstack1lll1l1l1_opy_ = False
  bstack11111111l1_opy_ = None
  bstack11111l1l1l_opy_ = {}
  bstack1lllllll1l1_opy_ = 300
  bstack11111l111l_opy_ = False
  logger = None
  bstack1lllllll11l_opy_ = False
  bstack1111l1l11l_opy_ = bstack111l11_opy_ (u"ࠪࠫᏤ")
  bstack11111llll1_opy_ = {
    bstack111l11_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࠫᏥ") : 1,
    bstack111l11_opy_ (u"ࠬ࡬ࡩࡳࡧࡩࡳࡽ࠭Ꮶ") : 2,
    bstack111l11_opy_ (u"࠭ࡥࡥࡩࡨࠫᏧ") : 3,
    bstack111l11_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯ࠧᏨ") : 4
  }
  def __init__(self) -> None: pass
  def bstack111111l111_opy_(self):
    bstack1111111ll1_opy_ = bstack111l11_opy_ (u"ࠨࠩᏩ")
    bstack111111l1ll_opy_ = sys.platform
    bstack1111l11ll1_opy_ = bstack111l11_opy_ (u"ࠩࡳࡩࡷࡩࡹࠨᏪ")
    if re.match(bstack111l11_opy_ (u"ࠥࡨࡦࡸࡷࡪࡰࡿࡱࡦࡩࠠࡰࡵࠥᏫ"), bstack111111l1ll_opy_) != None:
      bstack1111111ll1_opy_ = bstack11l11llll1_opy_ + bstack111l11_opy_ (u"ࠦ࠴ࡶࡥࡳࡥࡼ࠱ࡴࡹࡸ࠯ࡼ࡬ࡴࠧᏬ")
      self.bstack1111l1l11l_opy_ = bstack111l11_opy_ (u"ࠬࡳࡡࡤࠩᏭ")
    elif re.match(bstack111l11_opy_ (u"ࠨ࡭ࡴࡹ࡬ࡲࢁࡳࡳࡺࡵࡿࡱ࡮ࡴࡧࡸࡾࡦࡽ࡬ࡽࡩ࡯ࡾࡥࡧࡨࡽࡩ࡯ࡾࡺ࡭ࡳࡩࡥࡽࡧࡰࡧࢁࡽࡩ࡯࠵࠵ࠦᏮ"), bstack111111l1ll_opy_) != None:
      bstack1111111ll1_opy_ = bstack11l11llll1_opy_ + bstack111l11_opy_ (u"ࠢ࠰ࡲࡨࡶࡨࡿ࠭ࡸ࡫ࡱ࠲ࡿ࡯ࡰࠣᏯ")
      bstack1111l11ll1_opy_ = bstack111l11_opy_ (u"ࠣࡲࡨࡶࡨࡿ࠮ࡦࡺࡨࠦᏰ")
      self.bstack1111l1l11l_opy_ = bstack111l11_opy_ (u"ࠩࡺ࡭ࡳ࠭Ᏹ")
    else:
      bstack1111111ll1_opy_ = bstack11l11llll1_opy_ + bstack111l11_opy_ (u"ࠥ࠳ࡵ࡫ࡲࡤࡻ࠰ࡰ࡮ࡴࡵࡹ࠰ࡽ࡭ࡵࠨᏲ")
      self.bstack1111l1l11l_opy_ = bstack111l11_opy_ (u"ࠫࡱ࡯࡮ࡶࡺࠪᏳ")
    return bstack1111111ll1_opy_, bstack1111l11ll1_opy_
  def bstack1111111l11_opy_(self):
    try:
      bstack1111111lll_opy_ = [os.path.join(expanduser(bstack111l11_opy_ (u"ࠧࢄࠢᏴ")), bstack111l11_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭Ᏽ")), self.working_dir, tempfile.gettempdir()]
      for path in bstack1111111lll_opy_:
        if(self.bstack11111l11ll_opy_(path)):
          return path
      raise bstack111l11_opy_ (u"ࠢࡖࡰࡤࡰࡧ࡫ࠠࡵࡱࠣࡨࡴࡽ࡮࡭ࡱࡤࡨࠥࡶࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼࠦ᏶")
    except Exception as e:
      self.logger.error(bstack111l11_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤ࡫࡯࡮ࡥࠢࡤࡺࡦ࡯࡬ࡢࡤ࡯ࡩࠥࡶࡡࡵࡪࠣࡪࡴࡸࠠࡱࡧࡵࡧࡾࠦࡤࡰࡹࡱࡰࡴࡧࡤ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࠳ࠠࡼࡿࠥ᏷").format(e))
  def bstack11111l11ll_opy_(self, path):
    try:
      if not os.path.exists(path):
        os.makedirs(path)
      return True
    except:
      return False
  def bstack111111111l_opy_(self, bstack1111111ll1_opy_, bstack1111l11ll1_opy_):
    try:
      bstack1111l111ll_opy_ = self.bstack1111111l11_opy_()
      bstack11111l1l11_opy_ = os.path.join(bstack1111l111ll_opy_, bstack111l11_opy_ (u"ࠩࡳࡩࡷࡩࡹ࠯ࡼ࡬ࡴࠬᏸ"))
      bstack11111l1ll1_opy_ = os.path.join(bstack1111l111ll_opy_, bstack1111l11ll1_opy_)
      if os.path.exists(bstack11111l1ll1_opy_):
        self.logger.info(bstack111l11_opy_ (u"ࠥࡔࡪࡸࡣࡺࠢࡥ࡭ࡳࡧࡲࡺࠢࡩࡳࡺࡴࡤࠡ࡫ࡱࠤࢀࢃࠬࠡࡵ࡮࡭ࡵࡶࡩ࡯ࡩࠣࡨࡴࡽ࡮࡭ࡱࡤࡨࠧᏹ").format(bstack11111l1ll1_opy_))
        return bstack11111l1ll1_opy_
      if os.path.exists(bstack11111l1l11_opy_):
        self.logger.info(bstack111l11_opy_ (u"ࠦࡕ࡫ࡲࡤࡻࠣࡾ࡮ࡶࠠࡧࡱࡸࡲࡩࠦࡩ࡯ࠢࡾࢁ࠱ࠦࡵ࡯ࡼ࡬ࡴࡵ࡯࡮ࡨࠤᏺ").format(bstack11111l1l11_opy_))
        return self.bstack1111l11lll_opy_(bstack11111l1l11_opy_, bstack1111l11ll1_opy_)
      self.logger.info(bstack111l11_opy_ (u"ࠧࡊ࡯ࡸࡰ࡯ࡳࡦࡪࡩ࡯ࡩࠣࡴࡪࡸࡣࡺࠢࡥ࡭ࡳࡧࡲࡺࠢࡩࡶࡴࡳࠠࡼࡿࠥᏻ").format(bstack1111111ll1_opy_))
      response = bstack1lllll1lll_opy_(bstack111l11_opy_ (u"࠭ࡇࡆࡖࠪᏼ"), bstack1111111ll1_opy_, {}, {})
      if response.status_code == 200:
        with open(bstack11111l1l11_opy_, bstack111l11_opy_ (u"ࠧࡸࡤࠪᏽ")) as file:
          file.write(response.content)
        self.logger.info(bstack111l11_opy_ (u"ࠣࡆࡲࡻࡳࡲ࡯ࡢࡦࡨࡨࠥࡶࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼࠤࡦࡴࡤࠡࡵࡤࡺࡪࡪࠠࡢࡶࠣࡿࢂࠨ᏾").format(bstack11111l1l11_opy_))
        return self.bstack1111l11lll_opy_(bstack11111l1l11_opy_, bstack1111l11ll1_opy_)
      else:
        raise(bstack111l11_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࠠࡵࡪࡨࠤ࡫࡯࡬ࡦ࠰ࠣࡗࡹࡧࡴࡶࡵࠣࡧࡴࡪࡥ࠻ࠢࡾࢁࠧ᏿").format(response.status_code))
    except Exception as e:
      self.logger.error(bstack111l11_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡤࡰࡹࡱࡰࡴࡧࡤࠡࡲࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿ࠺ࠡࡽࢀࠦ᐀").format(e))
  def bstack1111111l1l_opy_(self, bstack1111111ll1_opy_, bstack1111l11ll1_opy_):
    try:
      retry = 2
      bstack11111l1ll1_opy_ = None
      bstack11111l1111_opy_ = False
      while retry > 0:
        bstack11111l1ll1_opy_ = self.bstack111111111l_opy_(bstack1111111ll1_opy_, bstack1111l11ll1_opy_)
        bstack11111l1111_opy_ = self.bstack111111l1l1_opy_(bstack1111111ll1_opy_, bstack1111l11ll1_opy_, bstack11111l1ll1_opy_)
        if bstack11111l1111_opy_:
          break
        retry -= 1
      return bstack11111l1ll1_opy_, bstack11111l1111_opy_
    except Exception as e:
      self.logger.error(bstack111l11_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡨࡧࡷࠤࡵ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻࠣࡴࡦࡺࡨࠣᐁ").format(e))
    return bstack11111l1ll1_opy_, False
  def bstack111111l1l1_opy_(self, bstack1111111ll1_opy_, bstack1111l11ll1_opy_, bstack11111l1ll1_opy_, bstack1llllllll1l_opy_ = 0):
    if bstack1llllllll1l_opy_ > 1:
      return False
    if bstack11111l1ll1_opy_ == None or os.path.exists(bstack11111l1ll1_opy_) == False:
      self.logger.warn(bstack111l11_opy_ (u"ࠧࡖࡥࡳࡥࡼࠤࡵࡧࡴࡩࠢࡱࡳࡹࠦࡦࡰࡷࡱࡨ࠱ࠦࡲࡦࡶࡵࡽ࡮ࡴࡧࠡࡦࡲࡻࡳࡲ࡯ࡢࡦࠥᐂ"))
      return False
    bstack111111l11l_opy_ = bstack111l11_opy_ (u"ࠨ࡞࠯ࠬࡃࡴࡪࡸࡣࡺ࡞࠲ࡧࡱ࡯ࠠ࡝ࡦ࠱ࡠࡩ࠱࠮࡝ࡦ࠮ࠦᐃ")
    command = bstack111l11_opy_ (u"ࠧࡼࡿࠣ࠱࠲ࡼࡥࡳࡵ࡬ࡳࡳ࠭ᐄ").format(bstack11111l1ll1_opy_)
    bstack11111lll1l_opy_ = subprocess.check_output(command, shell=True, text=True)
    if re.match(bstack111111l11l_opy_, bstack11111lll1l_opy_) != None:
      return True
    else:
      self.logger.error(bstack111l11_opy_ (u"ࠣࡒࡨࡶࡨࡿࠠࡷࡧࡵࡷ࡮ࡵ࡮ࠡࡥ࡫ࡩࡨࡱࠠࡧࡣ࡬ࡰࡪࡪࠢᐅ"))
      return False
  def bstack1111l11lll_opy_(self, bstack11111l1l11_opy_, bstack1111l11ll1_opy_):
    try:
      working_dir = os.path.dirname(bstack11111l1l11_opy_)
      shutil.unpack_archive(bstack11111l1l11_opy_, working_dir)
      bstack11111l1ll1_opy_ = os.path.join(working_dir, bstack1111l11ll1_opy_)
      os.chmod(bstack11111l1ll1_opy_, 0o755)
      return bstack11111l1ll1_opy_
    except Exception as e:
      self.logger.error(bstack111l11_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡻ࡮ࡻ࡫ࡳࠤࡵ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻࠥᐆ"))
  def bstack1lllllll1ll_opy_(self):
    try:
      percy = str(self.config.get(bstack111l11_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩᐇ"), bstack111l11_opy_ (u"ࠦ࡫ࡧ࡬ࡴࡧࠥᐈ"))).lower()
      if percy != bstack111l11_opy_ (u"ࠧࡺࡲࡶࡧࠥᐉ"):
        return False
      self.bstack1lll1l1l1_opy_ = True
      return True
    except Exception as e:
      self.logger.error(bstack111l11_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡧࡩࡹ࡫ࡣࡵࠢࡳࡩࡷࡩࡹ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࢁࡽࠣᐊ").format(e))
  def bstack1llllllll11_opy_(self):
    try:
      bstack1llllllll11_opy_ = str(self.config.get(bstack111l11_opy_ (u"ࠧࡱࡧࡵࡧࡾࡉࡡࡱࡶࡸࡶࡪࡓ࡯ࡥࡧࠪᐋ"), bstack111l11_opy_ (u"ࠣࡣࡸࡸࡴࠨᐌ"))).lower()
      return bstack1llllllll11_opy_
    except Exception as e:
      self.logger.error(bstack111l11_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡪࡥࡵࡧࡦࡸࠥࡶࡥࡳࡥࡼࠤࡨࡧࡰࡵࡷࡵࡩࠥࡳ࡯ࡥࡧ࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡼࡿࠥᐍ").format(e))
  def init(self, bstack1ll111lll1_opy_, config, logger):
    self.bstack1ll111lll1_opy_ = bstack1ll111lll1_opy_
    self.config = config
    self.logger = logger
    if not self.bstack1lllllll1ll_opy_():
      return
    self.bstack11111l1l1l_opy_ = config.get(bstack111l11_opy_ (u"ࠪࡴࡪࡸࡣࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩᐎ"), {})
    self.bstack1111l1l111_opy_ = config.get(bstack111l11_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࡆࡥࡵࡺࡵࡳࡧࡐࡳࡩ࡫ࠧᐏ"), bstack111l11_opy_ (u"ࠧࡧࡵࡵࡱࠥᐐ"))
    try:
      bstack1111111ll1_opy_, bstack1111l11ll1_opy_ = self.bstack111111l111_opy_()
      bstack11111l1ll1_opy_, bstack11111l1111_opy_ = self.bstack1111111l1l_opy_(bstack1111111ll1_opy_, bstack1111l11ll1_opy_)
      if bstack11111l1111_opy_:
        self.binary_path = bstack11111l1ll1_opy_
        thread = Thread(target=self.bstack11111l11l1_opy_)
        thread.start()
      else:
        self.bstack1lllllll11l_opy_ = True
        self.logger.error(bstack111l11_opy_ (u"ࠨࡉ࡯ࡸࡤࡰ࡮ࡪࠠࡱࡧࡵࡧࡾࠦࡰࡢࡶ࡫ࠤ࡫ࡵࡵ࡯ࡦࠣ࠱ࠥࢁࡽ࠭ࠢࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡴࡢࡴࡷࠤࡕ࡫ࡲࡤࡻࠥᐑ").format(bstack11111l1ll1_opy_))
    except Exception as e:
      self.logger.error(bstack111l11_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡷࡹࡧࡲࡵࠢࡳࡩࡷࡩࡹ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࢁࡽࠣᐒ").format(e))
  def bstack11111l1lll_opy_(self):
    try:
      logfile = os.path.join(self.working_dir, bstack111l11_opy_ (u"ࠨ࡮ࡲ࡫ࠬᐓ"), bstack111l11_opy_ (u"ࠩࡳࡩࡷࡩࡹ࠯࡮ࡲ࡫ࠬᐔ"))
      os.makedirs(os.path.dirname(logfile)) if not os.path.exists(os.path.dirname(logfile)) else None
      self.logger.debug(bstack111l11_opy_ (u"ࠥࡔࡺࡹࡨࡪࡰࡪࠤࡵ࡫ࡲࡤࡻࠣࡰࡴ࡭ࡳࠡࡣࡷࠤࢀࢃࠢᐕ").format(logfile))
      self.bstack1111l1111l_opy_ = logfile
    except Exception as e:
      self.logger.error(bstack111l11_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡴࡧࡷࠤࡵ࡫ࡲࡤࡻࠣࡰࡴ࡭ࠠࡱࡣࡷ࡬࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡾࢁࠧᐖ").format(e))
  def bstack11111l11l1_opy_(self):
    bstack1lllllllll1_opy_ = self.bstack111111ll11_opy_()
    if bstack1lllllllll1_opy_ == None:
      self.bstack1lllllll11l_opy_ = True
      self.logger.error(bstack111l11_opy_ (u"ࠧࡖࡥࡳࡥࡼࠤࡹࡵ࡫ࡦࡰࠣࡲࡴࡺࠠࡧࡱࡸࡲࡩ࠲ࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡹࡧࡲࡵࠢࡳࡩࡷࡩࡹࠣᐗ"))
      return False
    command_args = [bstack111l11_opy_ (u"ࠨࡡࡱࡲ࠽ࡩࡽ࡫ࡣ࠻ࡵࡷࡥࡷࡺࠢᐘ") if self.bstack1ll111lll1_opy_ else bstack111l11_opy_ (u"ࠧࡦࡺࡨࡧ࠿ࡹࡴࡢࡴࡷࠫᐙ")]
    bstack1llllll1lll_opy_ = self.bstack11111ll1l1_opy_()
    if bstack1llllll1lll_opy_ != None:
      command_args.append(bstack111l11_opy_ (u"ࠣ࠯ࡦࠤࢀࢃࠢᐚ").format(bstack1llllll1lll_opy_))
    env = os.environ.copy()
    env[bstack111l11_opy_ (u"ࠤࡓࡉࡗࡉ࡙ࡠࡖࡒࡏࡊࡔࠢᐛ")] = bstack1lllllllll1_opy_
    bstack1111l1l1l1_opy_ = [self.binary_path]
    self.bstack11111l1lll_opy_()
    self.bstack11111111l1_opy_ = self.bstack1111l111l1_opy_(bstack1111l1l1l1_opy_ + command_args, env)
    self.logger.debug(bstack111l11_opy_ (u"ࠥࡗࡹࡧࡲࡵ࡫ࡱ࡫ࠥࡎࡥࡢ࡮ࡷ࡬ࠥࡉࡨࡦࡥ࡮ࠦᐜ"))
    bstack1llllllll1l_opy_ = 0
    while self.bstack11111111l1_opy_.poll() == None:
      bstack1111l11111_opy_ = self.bstack11111lllll_opy_()
      if bstack1111l11111_opy_:
        self.logger.debug(bstack111l11_opy_ (u"ࠦࡍ࡫ࡡ࡭ࡶ࡫ࠤࡈ࡮ࡥࡤ࡭ࠣࡷࡺࡩࡣࡦࡵࡶࡪࡺࡲࠢᐝ"))
        self.bstack11111l111l_opy_ = True
        return True
      bstack1llllllll1l_opy_ += 1
      self.logger.debug(bstack111l11_opy_ (u"ࠧࡎࡥࡢ࡮ࡷ࡬ࠥࡉࡨࡦࡥ࡮ࠤࡗ࡫ࡴࡳࡻࠣ࠱ࠥࢁࡽࠣᐞ").format(bstack1llllllll1l_opy_))
      time.sleep(2)
    self.logger.error(bstack111l11_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡸࡦࡸࡴࠡࡲࡨࡶࡨࡿࠬࠡࡊࡨࡥࡱࡺࡨࠡࡅ࡫ࡩࡨࡱࠠࡇࡣ࡬ࡰࡪࡪࠠࡢࡨࡷࡩࡷࠦࡻࡾࠢࡤࡸࡹ࡫࡭ࡱࡶࡶࠦᐟ").format(bstack1llllllll1l_opy_))
    self.bstack1lllllll11l_opy_ = True
    return False
  def bstack11111lllll_opy_(self, bstack1llllllll1l_opy_ = 0):
    try:
      if bstack1llllllll1l_opy_ > 10:
        return False
      bstack1111l11l1l_opy_ = os.environ.get(bstack111l11_opy_ (u"ࠧࡑࡇࡕࡇ࡞ࡥࡓࡆࡔ࡙ࡉࡗࡥࡁࡅࡆࡕࡉࡘ࡙ࠧᐠ"), bstack111l11_opy_ (u"ࠨࡪࡷࡸࡵࡀ࠯࠰࡮ࡲࡧࡦࡲࡨࡰࡵࡷ࠾࠺࠹࠳࠹ࠩᐡ"))
      bstack111111lll1_opy_ = bstack1111l11l1l_opy_ + bstack11l11l1lll_opy_
      response = requests.get(bstack111111lll1_opy_)
      return True if response.json() else False
    except:
      return False
  def bstack111111ll11_opy_(self):
    bstack11111ll111_opy_ = bstack111l11_opy_ (u"ࠩࡤࡴࡵ࠭ᐢ") if self.bstack1ll111lll1_opy_ else bstack111l11_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷࡩࠬᐣ")
    bstack11l11111l1_opy_ = bstack111l11_opy_ (u"ࠦࡦࡶࡩ࠰ࡣࡳࡴࡤࡶࡥࡳࡥࡼ࠳࡬࡫ࡴࡠࡲࡵࡳ࡯࡫ࡣࡵࡡࡷࡳࡰ࡫࡮ࡀࡰࡤࡱࡪࡃࡻࡾࠨࡷࡽࡵ࡫࠽ࡼࡿࠥᐤ").format(self.config[bstack111l11_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠪᐥ")], bstack11111ll111_opy_)
    uri = bstack1lllll11l_opy_(bstack11l11111l1_opy_)
    try:
      response = bstack1lllll1lll_opy_(bstack111l11_opy_ (u"࠭ࡇࡆࡖࠪᐦ"), uri, {}, {bstack111l11_opy_ (u"ࠧࡢࡷࡷ࡬ࠬᐧ"): (self.config[bstack111l11_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪᐨ")], self.config[bstack111l11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬᐩ")])})
      if response.status_code == 200:
        bstack1lllllll111_opy_ = response.json()
        if bstack111l11_opy_ (u"ࠥࡸࡴࡱࡥ࡯ࠤᐪ") in bstack1lllllll111_opy_:
          return bstack1lllllll111_opy_[bstack111l11_opy_ (u"ࠦࡹࡵ࡫ࡦࡰࠥᐫ")]
        else:
          raise bstack111l11_opy_ (u"࡚ࠬ࡯࡬ࡧࡱࠤࡓࡵࡴࠡࡈࡲࡹࡳࡪࠠ࠮ࠢࡾࢁࠬᐬ").format(bstack1lllllll111_opy_)
      else:
        raise bstack111l11_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡩࡩࡹࡩࡨࠡࡲࡨࡶࡨࡿࠠࡵࡱ࡮ࡩࡳ࠲ࠠࡓࡧࡶࡴࡴࡴࡳࡦࠢࡶࡸࡦࡺࡵࡴࠢ࠰ࠤࢀࢃࠬࠡࡔࡨࡷࡵࡵ࡮ࡴࡧࠣࡆࡴࡪࡹࠡ࠯ࠣࡿࢂࠨᐭ").format(response.status_code, response.json())
    except Exception as e:
      self.logger.error(bstack111l11_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡣࡳࡧࡤࡸ࡮ࡴࡧࠡࡲࡨࡶࡨࡿࠠࡱࡴࡲ࡮ࡪࡩࡴࠣᐮ").format(e))
  def bstack11111ll1l1_opy_(self):
    bstack11111ll1ll_opy_ = os.path.join(tempfile.gettempdir(), bstack111l11_opy_ (u"ࠣࡲࡨࡶࡨࡿࡃࡰࡰࡩ࡭࡬࠴ࡪࡴࡱࡱࠦᐯ"))
    try:
      if bstack111l11_opy_ (u"ࠩࡹࡩࡷࡹࡩࡰࡰࠪᐰ") not in self.bstack11111l1l1l_opy_:
        self.bstack11111l1l1l_opy_[bstack111l11_opy_ (u"ࠪࡺࡪࡸࡳࡪࡱࡱࠫᐱ")] = 2
      with open(bstack11111ll1ll_opy_, bstack111l11_opy_ (u"ࠫࡼ࠭ᐲ")) as fp:
        json.dump(self.bstack11111l1l1l_opy_, fp)
      return bstack11111ll1ll_opy_
    except Exception as e:
      self.logger.error(bstack111l11_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡥࡵࡩࡦࡺࡥࠡࡲࡨࡶࡨࡿࠠࡤࡱࡱࡪ࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡾࢁࠧᐳ").format(e))
  def bstack1111l111l1_opy_(self, cmd, env = os.environ.copy()):
    try:
      if self.bstack1111l1l11l_opy_ == bstack111l11_opy_ (u"࠭ࡷࡪࡰࠪᐴ"):
        bstack11111lll11_opy_ = [bstack111l11_opy_ (u"ࠧࡤ࡯ࡧ࠲ࡪࡾࡥࠨᐵ"), bstack111l11_opy_ (u"ࠨ࠱ࡦࠫᐶ")]
        cmd = bstack11111lll11_opy_ + cmd
      cmd = bstack111l11_opy_ (u"ࠩࠣࠫᐷ").join(cmd)
      self.logger.debug(bstack111l11_opy_ (u"ࠥࡖࡺࡴ࡮ࡪࡰࡪࠤࢀࢃࠢᐸ").format(cmd))
      with open(self.bstack1111l1111l_opy_, bstack111l11_opy_ (u"ࠦࡦࠨᐹ")) as bstack111111ll1l_opy_:
        process = subprocess.Popen(cmd, shell=True, stdout=bstack111111ll1l_opy_, text=True, stderr=bstack111111ll1l_opy_, env=env, universal_newlines=True)
      return process
    except Exception as e:
      self.bstack1lllllll11l_opy_ = True
      self.logger.error(bstack111l11_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡷࡥࡷࡺࠠࡱࡧࡵࡧࡾࠦࡷࡪࡶ࡫ࠤࡨࡳࡤࠡ࠯ࠣࡿࢂ࠲ࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰ࠽ࠤࢀࢃࠢᐺ").format(cmd, e))
  def shutdown(self):
    try:
      if self.bstack11111l111l_opy_:
        self.logger.info(bstack111l11_opy_ (u"ࠨࡓࡵࡱࡳࡴ࡮ࡴࡧࠡࡒࡨࡶࡨࡿࠢᐻ"))
        cmd = [self.binary_path, bstack111l11_opy_ (u"ࠢࡦࡺࡨࡧ࠿ࡹࡴࡰࡲࠥᐼ")]
        self.bstack1111l111l1_opy_(cmd)
        self.bstack11111l111l_opy_ = False
    except Exception as e:
      self.logger.error(bstack111l11_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸࡺ࡯ࡱࠢࡶࡩࡸࡹࡩࡰࡰࠣࡻ࡮ࡺࡨࠡࡥࡲࡱࡲࡧ࡮ࡥࠢ࠰ࠤࢀࢃࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱ࠾ࠥࢁࡽࠣᐽ").format(cmd, e))
  def bstack11l1l11l1_opy_(self):
    if not self.bstack1lll1l1l1_opy_:
      return
    try:
      bstack111111llll_opy_ = 0
      while not self.bstack11111l111l_opy_ and bstack111111llll_opy_ < self.bstack1lllllll1l1_opy_:
        if self.bstack1lllllll11l_opy_:
          self.logger.info(bstack111l11_opy_ (u"ࠤࡓࡩࡷࡩࡹࠡࡵࡨࡸࡺࡶࠠࡧࡣ࡬ࡰࡪࡪࠢᐾ"))
          return
        time.sleep(1)
        bstack111111llll_opy_ += 1
      os.environ[bstack111l11_opy_ (u"ࠪࡔࡊࡘࡃ࡚ࡡࡅࡉࡘ࡚࡟ࡑࡎࡄࡘࡋࡕࡒࡎࠩᐿ")] = str(self.bstack11111111ll_opy_())
      self.logger.info(bstack111l11_opy_ (u"ࠦࡕ࡫ࡲࡤࡻࠣࡷࡪࡺࡵࡱࠢࡦࡳࡲࡶ࡬ࡦࡶࡨࡨࠧᑀ"))
    except Exception as e:
      self.logger.error(bstack111l11_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡨࡸࡺࡶࠠࡱࡧࡵࡧࡾ࠲ࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡿࢂࠨᑁ").format(e))
  def bstack11111111ll_opy_(self):
    if self.bstack1ll111lll1_opy_:
      return
    try:
      bstack11111ll11l_opy_ = [platform[bstack111l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫᑂ")].lower() for platform in self.config.get(bstack111l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪᑃ"), [])]
      bstack1111111111_opy_ = sys.maxsize
      bstack1llllllllll_opy_ = bstack111l11_opy_ (u"ࠨࠩᑄ")
      for browser in bstack11111ll11l_opy_:
        if browser in self.bstack11111llll1_opy_:
          bstack1111l11l11_opy_ = self.bstack11111llll1_opy_[browser]
        if bstack1111l11l11_opy_ < bstack1111111111_opy_:
          bstack1111111111_opy_ = bstack1111l11l11_opy_
          bstack1llllllllll_opy_ = browser
      return bstack1llllllllll_opy_
    except Exception as e:
      self.logger.error(bstack111l11_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥ࡬ࡩ࡯ࡦࠣࡦࡪࡹࡴࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡼࡿࠥᑅ").format(e))
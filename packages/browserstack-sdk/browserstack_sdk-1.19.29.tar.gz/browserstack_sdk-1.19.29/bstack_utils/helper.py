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
import datetime
import json
import os
import platform
import re
import subprocess
import traceback
import tempfile
import multiprocessing
import threading
import sys
import logging
from math import ceil
from urllib.parse import urlparse
import git
import requests
from packaging import version
from bstack_utils.config import Config
from bstack_utils.constants import (bstack11l11ll11l_opy_, bstack1lllllll11_opy_, bstack1l11ll11l_opy_, bstack1ll1111lll_opy_,
                                    bstack11l1l11111_opy_, bstack11l11lllll_opy_)
from bstack_utils.messages import bstack1l11llll11_opy_, bstack1l1l1lllll_opy_
from bstack_utils.proxy import bstack1l11ll11l1_opy_, bstack1llll1l11_opy_
bstack1l11l111ll_opy_ = Config.bstack1l1l1l1111_opy_()
logger = logging.getLogger(__name__)
def bstack11ll11l1ll_opy_(config):
    return config[bstack111l11_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩᆜ")]
def bstack11l1llll11_opy_(config):
    return config[bstack111l11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫᆝ")]
def bstack111l1l1ll_opy_():
    try:
        import playwright
        return True
    except ImportError:
        return False
def bstack11l111l1ll_opy_(obj):
    values = []
    bstack111l1l11ll_opy_ = re.compile(bstack111l11_opy_ (u"ࡴࠥࡢࡈ࡛ࡓࡕࡑࡐࡣ࡙ࡇࡇࡠ࡞ࡧ࠯ࠩࠨᆞ"), re.I)
    for key in obj.keys():
        if bstack111l1l11ll_opy_.match(key):
            values.append(obj[key])
    return values
def bstack11l11l1111_opy_(config):
    tags = []
    tags.extend(bstack11l111l1ll_opy_(os.environ))
    tags.extend(bstack11l111l1ll_opy_(config))
    return tags
def bstack111lll11l1_opy_(markers):
    tags = []
    for marker in markers:
        tags.append(marker.name)
    return tags
def bstack111lll1l11_opy_(bstack111ll11l1l_opy_):
    if not bstack111ll11l1l_opy_:
        return bstack111l11_opy_ (u"ࠪࠫᆟ")
    return bstack111l11_opy_ (u"ࠦࢀࢃࠠࠩࡽࢀ࠭ࠧᆠ").format(bstack111ll11l1l_opy_.name, bstack111ll11l1l_opy_.email)
def bstack11ll11111l_opy_():
    try:
        repo = git.Repo(search_parent_directories=True)
        bstack11l1111111_opy_ = repo.common_dir
        info = {
            bstack111l11_opy_ (u"ࠧࡹࡨࡢࠤᆡ"): repo.head.commit.hexsha,
            bstack111l11_opy_ (u"ࠨࡳࡩࡱࡵࡸࡤࡹࡨࡢࠤᆢ"): repo.git.rev_parse(repo.head.commit, short=True),
            bstack111l11_opy_ (u"ࠢࡣࡴࡤࡲࡨ࡮ࠢᆣ"): repo.active_branch.name,
            bstack111l11_opy_ (u"ࠣࡶࡤ࡫ࠧᆤ"): repo.git.describe(all=True, tags=True, exact_match=True),
            bstack111l11_opy_ (u"ࠤࡦࡳࡲࡳࡩࡵࡶࡨࡶࠧᆥ"): bstack111lll1l11_opy_(repo.head.commit.committer),
            bstack111l11_opy_ (u"ࠥࡧࡴࡳ࡭ࡪࡶࡷࡩࡷࡥࡤࡢࡶࡨࠦᆦ"): repo.head.commit.committed_datetime.isoformat(),
            bstack111l11_opy_ (u"ࠦࡦࡻࡴࡩࡱࡵࠦᆧ"): bstack111lll1l11_opy_(repo.head.commit.author),
            bstack111l11_opy_ (u"ࠧࡧࡵࡵࡪࡲࡶࡤࡪࡡࡵࡧࠥᆨ"): repo.head.commit.authored_datetime.isoformat(),
            bstack111l11_opy_ (u"ࠨࡣࡰ࡯ࡰ࡭ࡹࡥ࡭ࡦࡵࡶࡥ࡬࡫ࠢᆩ"): repo.head.commit.message,
            bstack111l11_opy_ (u"ࠢࡳࡱࡲࡸࠧᆪ"): repo.git.rev_parse(bstack111l11_opy_ (u"ࠣ࠯࠰ࡷ࡭ࡵࡷ࠮ࡶࡲࡴࡱ࡫ࡶࡦ࡮ࠥᆫ")),
            bstack111l11_opy_ (u"ࠤࡦࡳࡲࡳ࡯࡯ࡡࡪ࡭ࡹࡥࡤࡪࡴࠥᆬ"): bstack11l1111111_opy_,
            bstack111l11_opy_ (u"ࠥࡻࡴࡸ࡫ࡵࡴࡨࡩࡤ࡭ࡩࡵࡡࡧ࡭ࡷࠨᆭ"): subprocess.check_output([bstack111l11_opy_ (u"ࠦ࡬࡯ࡴࠣᆮ"), bstack111l11_opy_ (u"ࠧࡸࡥࡷ࠯ࡳࡥࡷࡹࡥࠣᆯ"), bstack111l11_opy_ (u"ࠨ࠭࠮ࡩ࡬ࡸ࠲ࡩ࡯࡮࡯ࡲࡲ࠲ࡪࡩࡳࠤᆰ")]).strip().decode(
                bstack111l11_opy_ (u"ࠧࡶࡶࡩ࠱࠽࠭ᆱ")),
            bstack111l11_opy_ (u"ࠣ࡮ࡤࡷࡹࡥࡴࡢࡩࠥᆲ"): repo.git.describe(tags=True, abbrev=0, always=True),
            bstack111l11_opy_ (u"ࠤࡦࡳࡲࡳࡩࡵࡵࡢࡷ࡮ࡴࡣࡦࡡ࡯ࡥࡸࡺ࡟ࡵࡣࡪࠦᆳ"): repo.git.rev_list(
                bstack111l11_opy_ (u"ࠥࡿࢂ࠴࠮ࡼࡿࠥᆴ").format(repo.head.commit, repo.git.describe(tags=True, abbrev=0, always=True)), count=True)
        }
        remotes = repo.remotes
        bstack11l111l11l_opy_ = []
        for remote in remotes:
            bstack11l11111ll_opy_ = {
                bstack111l11_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᆵ"): remote.name,
                bstack111l11_opy_ (u"ࠧࡻࡲ࡭ࠤᆶ"): remote.url,
            }
            bstack11l111l11l_opy_.append(bstack11l11111ll_opy_)
        bstack111lll111l_opy_ = {
            bstack111l11_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᆷ"): bstack111l11_opy_ (u"ࠢࡨ࡫ࡷࠦᆸ"),
            **info,
            bstack111l11_opy_ (u"ࠣࡴࡨࡱࡴࡺࡥࡴࠤᆹ"): bstack11l111l11l_opy_
        }
        bstack111lll111l_opy_ = bstack111l11ll1l_opy_(bstack111lll111l_opy_)
        return bstack111lll111l_opy_
    except git.InvalidGitRepositoryError:
        return {}
    except Exception as err:
        print(bstack111l11_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡲࡴࡺࡲࡡࡵ࡫ࡱ࡫ࠥࡍࡩࡵࠢࡰࡩࡹࡧࡤࡢࡶࡤࠤࡼ࡯ࡴࡩࠢࡨࡶࡷࡵࡲ࠻ࠢࡾࢁࠧᆺ").format(err))
        return {}
def bstack111l11ll1l_opy_(bstack111lll111l_opy_):
    bstack111l1l111l_opy_ = bstack111lll1111_opy_(bstack111lll111l_opy_)
    if bstack111l1l111l_opy_ and bstack111l1l111l_opy_ > bstack11l1l11111_opy_:
        bstack111ll1ll11_opy_ = bstack111l1l111l_opy_ - bstack11l1l11111_opy_
        bstack111l1ll111_opy_ = bstack11l111ll1l_opy_(bstack111lll111l_opy_[bstack111l11_opy_ (u"ࠥࡧࡴࡳ࡭ࡪࡶࡢࡱࡪࡹࡳࡢࡩࡨࠦᆻ")], bstack111ll1ll11_opy_)
        bstack111lll111l_opy_[bstack111l11_opy_ (u"ࠦࡨࡵ࡭࡮࡫ࡷࡣࡲ࡫ࡳࡴࡣࡪࡩࠧᆼ")] = bstack111l1ll111_opy_
        logger.info(bstack111l11_opy_ (u"࡚ࠧࡨࡦࠢࡦࡳࡲࡳࡩࡵࠢ࡫ࡥࡸࠦࡢࡦࡧࡱࠤࡹࡸࡵ࡯ࡥࡤࡸࡪࡪ࠮ࠡࡕ࡬ࡾࡪࠦ࡯ࡧࠢࡦࡳࡲࡳࡩࡵࠢࡤࡪࡹ࡫ࡲࠡࡶࡵࡹࡳࡩࡡࡵ࡫ࡲࡲࠥ࡯ࡳࠡࡽࢀࠤࡐࡈࠢᆽ")
                    .format(bstack111lll1111_opy_(bstack111lll111l_opy_) / 1024))
    return bstack111lll111l_opy_
def bstack111lll1111_opy_(bstack1lll1l1l_opy_):
    try:
        if bstack1lll1l1l_opy_:
            bstack111ll111ll_opy_ = json.dumps(bstack1lll1l1l_opy_)
            bstack11l11l11ll_opy_ = sys.getsizeof(bstack111ll111ll_opy_)
            return bstack11l11l11ll_opy_
    except Exception as e:
        logger.debug(bstack111l11_opy_ (u"ࠨࡓࡰ࡯ࡨࡸ࡭࡯࡮ࡨࠢࡺࡩࡳࡺࠠࡸࡴࡲࡲ࡬ࠦࡷࡩ࡫࡯ࡩࠥࡩࡡ࡭ࡥࡸࡰࡦࡺࡩ࡯ࡩࠣࡷ࡮ࢀࡥࠡࡱࡩࠤࡏ࡙ࡏࡏࠢࡲࡦ࡯࡫ࡣࡵ࠼ࠣࡿࢂࠨᆾ").format(e))
    return -1
def bstack11l111ll1l_opy_(field, bstack11l11l111l_opy_):
    try:
        bstack111ll1lll1_opy_ = len(bytes(bstack11l11lllll_opy_, bstack111l11_opy_ (u"ࠧࡶࡶࡩ࠱࠽࠭ᆿ")))
        bstack11l111ll11_opy_ = bytes(field, bstack111l11_opy_ (u"ࠨࡷࡷࡪ࠲࠾ࠧᇀ"))
        bstack111llllll1_opy_ = len(bstack11l111ll11_opy_)
        bstack111l1lll1l_opy_ = ceil(bstack111llllll1_opy_ - bstack11l11l111l_opy_ - bstack111ll1lll1_opy_)
        if bstack111l1lll1l_opy_ > 0:
            bstack11l111l1l1_opy_ = bstack11l111ll11_opy_[:bstack111l1lll1l_opy_].decode(bstack111l11_opy_ (u"ࠩࡸࡸ࡫࠳࠸ࠨᇁ"), errors=bstack111l11_opy_ (u"ࠪ࡭࡬ࡴ࡯ࡳࡧࠪᇂ")) + bstack11l11lllll_opy_
            return bstack11l111l1l1_opy_
    except Exception as e:
        logger.debug(bstack111l11_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡷࡶࡺࡴࡣࡢࡶ࡬ࡲ࡬ࠦࡦࡪࡧ࡯ࡨ࠱ࠦ࡮ࡰࡶ࡫࡭ࡳ࡭ࠠࡸࡣࡶࠤࡹࡸࡵ࡯ࡥࡤࡸࡪࡪࠠࡩࡧࡵࡩ࠿ࠦࡻࡾࠤᇃ").format(e))
    return field
def bstack1l111ll1_opy_():
    env = os.environ
    if (bstack111l11_opy_ (u"ࠧࡐࡅࡏࡍࡌࡒࡘࡥࡕࡓࡎࠥᇄ") in env and len(env[bstack111l11_opy_ (u"ࠨࡊࡆࡐࡎࡍࡓ࡙࡟ࡖࡔࡏࠦᇅ")]) > 0) or (
            bstack111l11_opy_ (u"ࠢࡋࡇࡑࡏࡎࡔࡓࡠࡊࡒࡑࡊࠨᇆ") in env and len(env[bstack111l11_opy_ (u"ࠣࡌࡈࡒࡐࡏࡎࡔࡡࡋࡓࡒࡋࠢᇇ")]) > 0):
        return {
            bstack111l11_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᇈ"): bstack111l11_opy_ (u"ࠥࡎࡪࡴ࡫ࡪࡰࡶࠦᇉ"),
            bstack111l11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᇊ"): env.get(bstack111l11_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠣᇋ")),
            bstack111l11_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᇌ"): env.get(bstack111l11_opy_ (u"ࠢࡋࡑࡅࡣࡓࡇࡍࡆࠤᇍ")),
            bstack111l11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᇎ"): env.get(bstack111l11_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠣᇏ"))
        }
    if env.get(bstack111l11_opy_ (u"ࠥࡇࡎࠨᇐ")) == bstack111l11_opy_ (u"ࠦࡹࡸࡵࡦࠤᇑ") and bstack1ll11l1l11_opy_(env.get(bstack111l11_opy_ (u"ࠧࡉࡉࡓࡅࡏࡉࡈࡏࠢᇒ"))):
        return {
            bstack111l11_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᇓ"): bstack111l11_opy_ (u"ࠢࡄ࡫ࡵࡧࡱ࡫ࡃࡊࠤᇔ"),
            bstack111l11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᇕ"): env.get(bstack111l11_opy_ (u"ࠤࡆࡍࡗࡉࡌࡆࡡࡅ࡙ࡎࡒࡄࡠࡗࡕࡐࠧᇖ")),
            bstack111l11_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᇗ"): env.get(bstack111l11_opy_ (u"ࠦࡈࡏࡒࡄࡎࡈࡣࡏࡕࡂࠣᇘ")),
            bstack111l11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᇙ"): env.get(bstack111l11_opy_ (u"ࠨࡃࡊࡔࡆࡐࡊࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࠤᇚ"))
        }
    if env.get(bstack111l11_opy_ (u"ࠢࡄࡋࠥᇛ")) == bstack111l11_opy_ (u"ࠣࡶࡵࡹࡪࠨᇜ") and bstack1ll11l1l11_opy_(env.get(bstack111l11_opy_ (u"ࠤࡗࡖࡆ࡜ࡉࡔࠤᇝ"))):
        return {
            bstack111l11_opy_ (u"ࠥࡲࡦࡳࡥࠣᇞ"): bstack111l11_opy_ (u"࡙ࠦࡸࡡࡷ࡫ࡶࠤࡈࡏࠢᇟ"),
            bstack111l11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᇠ"): env.get(bstack111l11_opy_ (u"ࠨࡔࡓࡃ࡙ࡍࡘࡥࡂࡖࡋࡏࡈࡤ࡝ࡅࡃࡡࡘࡖࡑࠨᇡ")),
            bstack111l11_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᇢ"): env.get(bstack111l11_opy_ (u"ࠣࡖࡕࡅ࡛ࡏࡓࡠࡌࡒࡆࡤࡔࡁࡎࡇࠥᇣ")),
            bstack111l11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᇤ"): env.get(bstack111l11_opy_ (u"ࠥࡘࡗࡇࡖࡊࡕࡢࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠤᇥ"))
        }
    if env.get(bstack111l11_opy_ (u"ࠦࡈࡏࠢᇦ")) == bstack111l11_opy_ (u"ࠧࡺࡲࡶࡧࠥᇧ") and env.get(bstack111l11_opy_ (u"ࠨࡃࡊࡡࡑࡅࡒࡋࠢᇨ")) == bstack111l11_opy_ (u"ࠢࡤࡱࡧࡩࡸ࡮ࡩࡱࠤᇩ"):
        return {
            bstack111l11_opy_ (u"ࠣࡰࡤࡱࡪࠨᇪ"): bstack111l11_opy_ (u"ࠤࡆࡳࡩ࡫ࡳࡩ࡫ࡳࠦᇫ"),
            bstack111l11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᇬ"): None,
            bstack111l11_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᇭ"): None,
            bstack111l11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᇮ"): None
        }
    if env.get(bstack111l11_opy_ (u"ࠨࡂࡊࡖࡅ࡙ࡈࡑࡅࡕࡡࡅࡖࡆࡔࡃࡉࠤᇯ")) and env.get(bstack111l11_opy_ (u"ࠢࡃࡋࡗࡆ࡚ࡉࡋࡆࡖࡢࡇࡔࡓࡍࡊࡖࠥᇰ")):
        return {
            bstack111l11_opy_ (u"ࠣࡰࡤࡱࡪࠨᇱ"): bstack111l11_opy_ (u"ࠤࡅ࡭ࡹࡨࡵࡤ࡭ࡨࡸࠧᇲ"),
            bstack111l11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᇳ"): env.get(bstack111l11_opy_ (u"ࠦࡇࡏࡔࡃࡗࡆࡏࡊ࡚࡟ࡈࡋࡗࡣࡍ࡚ࡔࡑࡡࡒࡖࡎࡍࡉࡏࠤᇴ")),
            bstack111l11_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᇵ"): None,
            bstack111l11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᇶ"): env.get(bstack111l11_opy_ (u"ࠢࡃࡋࡗࡆ࡚ࡉࡋࡆࡖࡢࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠤᇷ"))
        }
    if env.get(bstack111l11_opy_ (u"ࠣࡅࡌࠦᇸ")) == bstack111l11_opy_ (u"ࠤࡷࡶࡺ࡫ࠢᇹ") and bstack1ll11l1l11_opy_(env.get(bstack111l11_opy_ (u"ࠥࡈࡗࡕࡎࡆࠤᇺ"))):
        return {
            bstack111l11_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᇻ"): bstack111l11_opy_ (u"ࠧࡊࡲࡰࡰࡨࠦᇼ"),
            bstack111l11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᇽ"): env.get(bstack111l11_opy_ (u"ࠢࡅࡔࡒࡒࡊࡥࡂࡖࡋࡏࡈࡤࡒࡉࡏࡍࠥᇾ")),
            bstack111l11_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᇿ"): None,
            bstack111l11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣሀ"): env.get(bstack111l11_opy_ (u"ࠥࡈࡗࡕࡎࡆࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠣሁ"))
        }
    if env.get(bstack111l11_opy_ (u"ࠦࡈࡏࠢሂ")) == bstack111l11_opy_ (u"ࠧࡺࡲࡶࡧࠥሃ") and bstack1ll11l1l11_opy_(env.get(bstack111l11_opy_ (u"ࠨࡓࡆࡏࡄࡔࡍࡕࡒࡆࠤሄ"))):
        return {
            bstack111l11_opy_ (u"ࠢ࡯ࡣࡰࡩࠧህ"): bstack111l11_opy_ (u"ࠣࡕࡨࡱࡦࡶࡨࡰࡴࡨࠦሆ"),
            bstack111l11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧሇ"): env.get(bstack111l11_opy_ (u"ࠥࡗࡊࡓࡁࡑࡊࡒࡖࡊࡥࡏࡓࡉࡄࡒࡎࡠࡁࡕࡋࡒࡒࡤ࡛ࡒࡍࠤለ")),
            bstack111l11_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨሉ"): env.get(bstack111l11_opy_ (u"࡙ࠧࡅࡎࡃࡓࡌࡔࡘࡅࡠࡌࡒࡆࡤࡔࡁࡎࡇࠥሊ")),
            bstack111l11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧላ"): env.get(bstack111l11_opy_ (u"ࠢࡔࡇࡐࡅࡕࡎࡏࡓࡇࡢࡎࡔࡈ࡟ࡊࡆࠥሌ"))
        }
    if env.get(bstack111l11_opy_ (u"ࠣࡅࡌࠦል")) == bstack111l11_opy_ (u"ࠤࡷࡶࡺ࡫ࠢሎ") and bstack1ll11l1l11_opy_(env.get(bstack111l11_opy_ (u"ࠥࡋࡎ࡚ࡌࡂࡄࡢࡇࡎࠨሏ"))):
        return {
            bstack111l11_opy_ (u"ࠦࡳࡧ࡭ࡦࠤሐ"): bstack111l11_opy_ (u"ࠧࡍࡩࡵࡎࡤࡦࠧሑ"),
            bstack111l11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤሒ"): env.get(bstack111l11_opy_ (u"ࠢࡄࡋࡢࡎࡔࡈ࡟ࡖࡔࡏࠦሓ")),
            bstack111l11_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥሔ"): env.get(bstack111l11_opy_ (u"ࠤࡆࡍࡤࡐࡏࡃࡡࡑࡅࡒࡋࠢሕ")),
            bstack111l11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤሖ"): env.get(bstack111l11_opy_ (u"ࠦࡈࡏ࡟ࡋࡑࡅࡣࡎࡊࠢሗ"))
        }
    if env.get(bstack111l11_opy_ (u"ࠧࡉࡉࠣመ")) == bstack111l11_opy_ (u"ࠨࡴࡳࡷࡨࠦሙ") and bstack1ll11l1l11_opy_(env.get(bstack111l11_opy_ (u"ࠢࡃࡗࡌࡐࡉࡑࡉࡕࡇࠥሚ"))):
        return {
            bstack111l11_opy_ (u"ࠣࡰࡤࡱࡪࠨማ"): bstack111l11_opy_ (u"ࠤࡅࡹ࡮ࡲࡤ࡬࡫ࡷࡩࠧሜ"),
            bstack111l11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨም"): env.get(bstack111l11_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡎࡍ࡙ࡋ࡟ࡃࡗࡌࡐࡉࡥࡕࡓࡎࠥሞ")),
            bstack111l11_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢሟ"): env.get(bstack111l11_opy_ (u"ࠨࡂࡖࡋࡏࡈࡐࡏࡔࡆࡡࡏࡅࡇࡋࡌࠣሠ")) or env.get(bstack111l11_opy_ (u"ࠢࡃࡗࡌࡐࡉࡑࡉࡕࡇࡢࡔࡎࡖࡅࡍࡋࡑࡉࡤࡔࡁࡎࡇࠥሡ")),
            bstack111l11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢሢ"): env.get(bstack111l11_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡌࡋࡗࡉࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦሣ"))
        }
    if bstack1ll11l1l11_opy_(env.get(bstack111l11_opy_ (u"ࠥࡘࡋࡥࡂࡖࡋࡏࡈࠧሤ"))):
        return {
            bstack111l11_opy_ (u"ࠦࡳࡧ࡭ࡦࠤሥ"): bstack111l11_opy_ (u"ࠧ࡜ࡩࡴࡷࡤࡰ࡙ࠥࡴࡶࡦ࡬ࡳ࡚ࠥࡥࡢ࡯ࠣࡗࡪࡸࡶࡪࡥࡨࡷࠧሦ"),
            bstack111l11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤሧ"): bstack111l11_opy_ (u"ࠢࡼࡿࡾࢁࠧረ").format(env.get(bstack111l11_opy_ (u"ࠨࡕ࡜ࡗ࡙ࡋࡍࡠࡖࡈࡅࡒࡌࡏࡖࡐࡇࡅ࡙ࡏࡏࡏࡕࡈࡖ࡛ࡋࡒࡖࡔࡌࠫሩ")), env.get(bstack111l11_opy_ (u"ࠩࡖ࡝ࡘ࡚ࡅࡎࡡࡗࡉࡆࡓࡐࡓࡑࡍࡉࡈ࡚ࡉࡅࠩሪ"))),
            bstack111l11_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧራ"): env.get(bstack111l11_opy_ (u"ࠦࡘ࡟ࡓࡕࡇࡐࡣࡉࡋࡆࡊࡐࡌࡘࡎࡕࡎࡊࡆࠥሬ")),
            bstack111l11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦር"): env.get(bstack111l11_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡈࡕࡊࡎࡇࡍࡉࠨሮ"))
        }
    if bstack1ll11l1l11_opy_(env.get(bstack111l11_opy_ (u"ࠢࡂࡒࡓ࡚ࡊ࡟ࡏࡓࠤሯ"))):
        return {
            bstack111l11_opy_ (u"ࠣࡰࡤࡱࡪࠨሰ"): bstack111l11_opy_ (u"ࠤࡄࡴࡵࡼࡥࡺࡱࡵࠦሱ"),
            bstack111l11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨሲ"): bstack111l11_opy_ (u"ࠦࢀࢃ࠯ࡱࡴࡲ࡮ࡪࡩࡴ࠰ࡽࢀ࠳ࢀࢃ࠯ࡣࡷ࡬ࡰࡩࡹ࠯ࡼࡿࠥሳ").format(env.get(bstack111l11_opy_ (u"ࠬࡇࡐࡑࡘࡈ࡝ࡔࡘ࡟ࡖࡔࡏࠫሴ")), env.get(bstack111l11_opy_ (u"࠭ࡁࡑࡒ࡙ࡉ࡞ࡕࡒࡠࡃࡆࡇࡔ࡛ࡎࡕࡡࡑࡅࡒࡋࠧስ")), env.get(bstack111l11_opy_ (u"ࠧࡂࡒࡓ࡚ࡊ࡟ࡏࡓࡡࡓࡖࡔࡐࡅࡄࡖࡢࡗࡑ࡛ࡇࠨሶ")), env.get(bstack111l11_opy_ (u"ࠨࡃࡓࡔ࡛ࡋ࡙ࡐࡔࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠬሷ"))),
            bstack111l11_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦሸ"): env.get(bstack111l11_opy_ (u"ࠥࡅࡕࡖࡖࡆ࡛ࡒࡖࡤࡐࡏࡃࡡࡑࡅࡒࡋࠢሹ")),
            bstack111l11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥሺ"): env.get(bstack111l11_opy_ (u"ࠧࡇࡐࡑࡘࡈ࡝ࡔࡘ࡟ࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨሻ"))
        }
    if env.get(bstack111l11_opy_ (u"ࠨࡁ࡛ࡗࡕࡉࡤࡎࡔࡕࡒࡢ࡙ࡘࡋࡒࡠࡃࡊࡉࡓ࡚ࠢሼ")) and env.get(bstack111l11_opy_ (u"ࠢࡕࡈࡢࡆ࡚ࡏࡌࡅࠤሽ")):
        return {
            bstack111l11_opy_ (u"ࠣࡰࡤࡱࡪࠨሾ"): bstack111l11_opy_ (u"ࠤࡄࡾࡺࡸࡥࠡࡅࡌࠦሿ"),
            bstack111l11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨቀ"): bstack111l11_opy_ (u"ࠦࢀࢃࡻࡾ࠱ࡢࡦࡺ࡯࡬ࡥ࠱ࡵࡩࡸࡻ࡬ࡵࡵࡂࡦࡺ࡯࡬ࡥࡋࡧࡁࢀࢃࠢቁ").format(env.get(bstack111l11_opy_ (u"࡙࡙ࠬࡔࡖࡈࡑࡤ࡚ࡅࡂࡏࡉࡓ࡚ࡔࡄࡂࡖࡌࡓࡓ࡙ࡅࡓࡘࡈࡖ࡚ࡘࡉࠨቂ")), env.get(bstack111l11_opy_ (u"࠭ࡓ࡚ࡕࡗࡉࡒࡥࡔࡆࡃࡐࡔࡗࡕࡊࡆࡅࡗࠫቃ")), env.get(bstack111l11_opy_ (u"ࠧࡃࡗࡌࡐࡉࡥࡂࡖࡋࡏࡈࡎࡊࠧቄ"))),
            bstack111l11_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥቅ"): env.get(bstack111l11_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡄࡘࡍࡑࡊࡉࡅࠤቆ")),
            bstack111l11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤቇ"): env.get(bstack111l11_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡋࡇࠦቈ"))
        }
    if any([env.get(bstack111l11_opy_ (u"ࠧࡉࡏࡅࡇࡅ࡙ࡎࡒࡄࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠥ቉")), env.get(bstack111l11_opy_ (u"ࠨࡃࡐࡆࡈࡆ࡚ࡏࡌࡅࡡࡕࡉࡘࡕࡌࡗࡇࡇࡣࡘࡕࡕࡓࡅࡈࡣ࡛ࡋࡒࡔࡋࡒࡒࠧቊ")), env.get(bstack111l11_opy_ (u"ࠢࡄࡑࡇࡉࡇ࡛ࡉࡍࡆࡢࡗࡔ࡛ࡒࡄࡇࡢ࡚ࡊࡘࡓࡊࡑࡑࠦቋ"))]):
        return {
            bstack111l11_opy_ (u"ࠣࡰࡤࡱࡪࠨቌ"): bstack111l11_opy_ (u"ࠤࡄ࡛ࡘࠦࡃࡰࡦࡨࡆࡺ࡯࡬ࡥࠤቍ"),
            bstack111l11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨ቎"): env.get(bstack111l11_opy_ (u"ࠦࡈࡕࡄࡆࡄࡘࡍࡑࡊ࡟ࡑࡗࡅࡐࡎࡉ࡟ࡃࡗࡌࡐࡉࡥࡕࡓࡎࠥ቏")),
            bstack111l11_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢቐ"): env.get(bstack111l11_opy_ (u"ࠨࡃࡐࡆࡈࡆ࡚ࡏࡌࡅࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠦቑ")),
            bstack111l11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨቒ"): env.get(bstack111l11_opy_ (u"ࠣࡅࡒࡈࡊࡈࡕࡊࡎࡇࡣࡇ࡛ࡉࡍࡆࡢࡍࡉࠨቓ"))
        }
    if env.get(bstack111l11_opy_ (u"ࠤࡥࡥࡲࡨ࡯ࡰࡡࡥࡹ࡮ࡲࡤࡏࡷࡰࡦࡪࡸࠢቔ")):
        return {
            bstack111l11_opy_ (u"ࠥࡲࡦࡳࡥࠣቕ"): bstack111l11_opy_ (u"ࠦࡇࡧ࡭ࡣࡱࡲࠦቖ"),
            bstack111l11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ቗"): env.get(bstack111l11_opy_ (u"ࠨࡢࡢ࡯ࡥࡳࡴࡥࡢࡶ࡫࡯ࡨࡗ࡫ࡳࡶ࡮ࡷࡷ࡚ࡸ࡬ࠣቘ")),
            bstack111l11_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤ቙"): env.get(bstack111l11_opy_ (u"ࠣࡤࡤࡱࡧࡵ࡯ࡠࡵ࡫ࡳࡷࡺࡊࡰࡤࡑࡥࡲ࡫ࠢቚ")),
            bstack111l11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣቛ"): env.get(bstack111l11_opy_ (u"ࠥࡦࡦࡳࡢࡰࡱࡢࡦࡺ࡯࡬ࡥࡐࡸࡱࡧ࡫ࡲࠣቜ"))
        }
    if env.get(bstack111l11_opy_ (u"ࠦ࡜ࡋࡒࡄࡍࡈࡖࠧቝ")) or env.get(bstack111l11_opy_ (u"ࠧ࡝ࡅࡓࡅࡎࡉࡗࡥࡍࡂࡋࡑࡣࡕࡏࡐࡆࡎࡌࡒࡊࡥࡓࡕࡃࡕࡘࡊࡊࠢ቞")):
        return {
            bstack111l11_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ቟"): bstack111l11_opy_ (u"ࠢࡘࡧࡵࡧࡰ࡫ࡲࠣበ"),
            bstack111l11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦቡ"): env.get(bstack111l11_opy_ (u"ࠤ࡚ࡉࡗࡉࡋࡆࡔࡢࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠨቢ")),
            bstack111l11_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧባ"): bstack111l11_opy_ (u"ࠦࡒࡧࡩ࡯ࠢࡓ࡭ࡵ࡫࡬ࡪࡰࡨࠦቤ") if env.get(bstack111l11_opy_ (u"ࠧ࡝ࡅࡓࡅࡎࡉࡗࡥࡍࡂࡋࡑࡣࡕࡏࡐࡆࡎࡌࡒࡊࡥࡓࡕࡃࡕࡘࡊࡊࠢብ")) else None,
            bstack111l11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧቦ"): env.get(bstack111l11_opy_ (u"ࠢࡘࡇࡕࡇࡐࡋࡒࡠࡉࡌࡘࡤࡉࡏࡎࡏࡌࡘࠧቧ"))
        }
    if any([env.get(bstack111l11_opy_ (u"ࠣࡉࡆࡔࡤࡖࡒࡐࡌࡈࡇ࡙ࠨቨ")), env.get(bstack111l11_opy_ (u"ࠤࡊࡇࡑࡕࡕࡅࡡࡓࡖࡔࡐࡅࡄࡖࠥቩ")), env.get(bstack111l11_opy_ (u"ࠥࡋࡔࡕࡇࡍࡇࡢࡇࡑࡕࡕࡅࡡࡓࡖࡔࡐࡅࡄࡖࠥቪ"))]):
        return {
            bstack111l11_opy_ (u"ࠦࡳࡧ࡭ࡦࠤቫ"): bstack111l11_opy_ (u"ࠧࡍ࡯ࡰࡩ࡯ࡩࠥࡉ࡬ࡰࡷࡧࠦቬ"),
            bstack111l11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤቭ"): None,
            bstack111l11_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤቮ"): env.get(bstack111l11_opy_ (u"ࠣࡒࡕࡓࡏࡋࡃࡕࡡࡌࡈࠧቯ")),
            bstack111l11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣተ"): env.get(bstack111l11_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡌࡈࠧቱ"))
        }
    if env.get(bstack111l11_opy_ (u"ࠦࡘࡎࡉࡑࡒࡄࡆࡑࡋࠢቲ")):
        return {
            bstack111l11_opy_ (u"ࠧࡴࡡ࡮ࡧࠥታ"): bstack111l11_opy_ (u"ࠨࡓࡩ࡫ࡳࡴࡦࡨ࡬ࡦࠤቴ"),
            bstack111l11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥት"): env.get(bstack111l11_opy_ (u"ࠣࡕࡋࡍࡕࡖࡁࡃࡎࡈࡣࡇ࡛ࡉࡍࡆࡢ࡙ࡗࡒࠢቶ")),
            bstack111l11_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦቷ"): bstack111l11_opy_ (u"ࠥࡎࡴࡨࠠࠤࡽࢀࠦቸ").format(env.get(bstack111l11_opy_ (u"ࠫࡘࡎࡉࡑࡒࡄࡆࡑࡋ࡟ࡋࡑࡅࡣࡎࡊࠧቹ"))) if env.get(bstack111l11_opy_ (u"࡙ࠧࡈࡊࡒࡓࡅࡇࡒࡅࡠࡌࡒࡆࡤࡏࡄࠣቺ")) else None,
            bstack111l11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧቻ"): env.get(bstack111l11_opy_ (u"ࠢࡔࡊࡌࡔࡕࡇࡂࡍࡇࡢࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠤቼ"))
        }
    if bstack1ll11l1l11_opy_(env.get(bstack111l11_opy_ (u"ࠣࡐࡈࡘࡑࡏࡆ࡚ࠤች"))):
        return {
            bstack111l11_opy_ (u"ࠤࡱࡥࡲ࡫ࠢቾ"): bstack111l11_opy_ (u"ࠥࡒࡪࡺ࡬ࡪࡨࡼࠦቿ"),
            bstack111l11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢኀ"): env.get(bstack111l11_opy_ (u"ࠧࡊࡅࡑࡎࡒ࡝ࡤ࡛ࡒࡍࠤኁ")),
            bstack111l11_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣኂ"): env.get(bstack111l11_opy_ (u"ࠢࡔࡋࡗࡉࡤࡔࡁࡎࡇࠥኃ")),
            bstack111l11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢኄ"): env.get(bstack111l11_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡋࡇࠦኅ"))
        }
    if bstack1ll11l1l11_opy_(env.get(bstack111l11_opy_ (u"ࠥࡋࡎ࡚ࡈࡖࡄࡢࡅࡈ࡚ࡉࡐࡐࡖࠦኆ"))):
        return {
            bstack111l11_opy_ (u"ࠦࡳࡧ࡭ࡦࠤኇ"): bstack111l11_opy_ (u"ࠧࡍࡩࡵࡊࡸࡦࠥࡇࡣࡵ࡫ࡲࡲࡸࠨኈ"),
            bstack111l11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ኉"): bstack111l11_opy_ (u"ࠢࡼࡿ࠲ࡿࢂ࠵ࡡࡤࡶ࡬ࡳࡳࡹ࠯ࡳࡷࡱࡷ࠴ࢁࡽࠣኊ").format(env.get(bstack111l11_opy_ (u"ࠨࡉࡌࡘࡍ࡛ࡂࡠࡕࡈࡖ࡛ࡋࡒࡠࡗࡕࡐࠬኋ")), env.get(bstack111l11_opy_ (u"ࠩࡊࡍ࡙ࡎࡕࡃࡡࡕࡉࡕࡕࡓࡊࡖࡒࡖ࡞࠭ኌ")), env.get(bstack111l11_opy_ (u"ࠪࡋࡎ࡚ࡈࡖࡄࡢࡖ࡚ࡔ࡟ࡊࡆࠪኍ"))),
            bstack111l11_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ኎"): env.get(bstack111l11_opy_ (u"ࠧࡍࡉࡕࡊࡘࡆࡤ࡝ࡏࡓࡍࡉࡐࡔ࡝ࠢ኏")),
            bstack111l11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧነ"): env.get(bstack111l11_opy_ (u"ࠢࡈࡋࡗࡌ࡚ࡈ࡟ࡓࡗࡑࡣࡎࡊࠢኑ"))
        }
    if env.get(bstack111l11_opy_ (u"ࠣࡅࡌࠦኒ")) == bstack111l11_opy_ (u"ࠤࡷࡶࡺ࡫ࠢና") and env.get(bstack111l11_opy_ (u"࡚ࠥࡊࡘࡃࡆࡎࠥኔ")) == bstack111l11_opy_ (u"ࠦ࠶ࠨን"):
        return {
            bstack111l11_opy_ (u"ࠧࡴࡡ࡮ࡧࠥኖ"): bstack111l11_opy_ (u"ࠨࡖࡦࡴࡦࡩࡱࠨኗ"),
            bstack111l11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥኘ"): bstack111l11_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࡽࢀࠦኙ").format(env.get(bstack111l11_opy_ (u"࡙ࠩࡉࡗࡉࡅࡍࡡࡘࡖࡑ࠭ኚ"))),
            bstack111l11_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧኛ"): None,
            bstack111l11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥኜ"): None,
        }
    if env.get(bstack111l11_opy_ (u"࡚ࠧࡅࡂࡏࡆࡍ࡙࡟࡟ࡗࡇࡕࡗࡎࡕࡎࠣኝ")):
        return {
            bstack111l11_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦኞ"): bstack111l11_opy_ (u"ࠢࡕࡧࡤࡱࡨ࡯ࡴࡺࠤኟ"),
            bstack111l11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦአ"): None,
            bstack111l11_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦኡ"): env.get(bstack111l11_opy_ (u"ࠥࡘࡊࡇࡍࡄࡋࡗ࡝ࡤࡖࡒࡐࡌࡈࡇ࡙ࡥࡎࡂࡏࡈࠦኢ")),
            bstack111l11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥኣ"): env.get(bstack111l11_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦኤ"))
        }
    if any([env.get(bstack111l11_opy_ (u"ࠨࡃࡐࡐࡆࡓ࡚ࡘࡓࡆࠤእ")), env.get(bstack111l11_opy_ (u"ࠢࡄࡑࡑࡇࡔ࡛ࡒࡔࡇࡢ࡙ࡗࡒࠢኦ")), env.get(bstack111l11_opy_ (u"ࠣࡅࡒࡒࡈࡕࡕࡓࡕࡈࡣ࡚࡙ࡅࡓࡐࡄࡑࡊࠨኧ")), env.get(bstack111l11_opy_ (u"ࠤࡆࡓࡓࡉࡏࡖࡔࡖࡉࡤ࡚ࡅࡂࡏࠥከ"))]):
        return {
            bstack111l11_opy_ (u"ࠥࡲࡦࡳࡥࠣኩ"): bstack111l11_opy_ (u"ࠦࡈࡵ࡮ࡤࡱࡸࡶࡸ࡫ࠢኪ"),
            bstack111l11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣካ"): None,
            bstack111l11_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣኬ"): env.get(bstack111l11_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡊࡐࡄࡢࡒࡆࡓࡅࠣክ")) or None,
            bstack111l11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢኮ"): env.get(bstack111l11_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡋࡇࠦኯ"), 0)
        }
    if env.get(bstack111l11_opy_ (u"ࠥࡋࡔࡥࡊࡐࡄࡢࡒࡆࡓࡅࠣኰ")):
        return {
            bstack111l11_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ኱"): bstack111l11_opy_ (u"ࠧࡍ࡯ࡄࡆࠥኲ"),
            bstack111l11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤኳ"): None,
            bstack111l11_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤኴ"): env.get(bstack111l11_opy_ (u"ࠣࡉࡒࡣࡏࡕࡂࡠࡐࡄࡑࡊࠨኵ")),
            bstack111l11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣ኶"): env.get(bstack111l11_opy_ (u"ࠥࡋࡔࡥࡐࡊࡒࡈࡐࡎࡔࡅࡠࡅࡒ࡙ࡓ࡚ࡅࡓࠤ኷"))
        }
    if env.get(bstack111l11_opy_ (u"ࠦࡈࡌ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠤኸ")):
        return {
            bstack111l11_opy_ (u"ࠧࡴࡡ࡮ࡧࠥኹ"): bstack111l11_opy_ (u"ࠨࡃࡰࡦࡨࡊࡷ࡫ࡳࡩࠤኺ"),
            bstack111l11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥኻ"): env.get(bstack111l11_opy_ (u"ࠣࡅࡉࡣࡇ࡛ࡉࡍࡆࡢ࡙ࡗࡒࠢኼ")),
            bstack111l11_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦኽ"): env.get(bstack111l11_opy_ (u"ࠥࡇࡋࡥࡐࡊࡒࡈࡐࡎࡔࡅࡠࡐࡄࡑࡊࠨኾ")),
            bstack111l11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ኿"): env.get(bstack111l11_opy_ (u"ࠧࡉࡆࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠥዀ"))
        }
    return {bstack111l11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧ዁"): None}
def get_host_info():
    return {
        bstack111l11_opy_ (u"ࠢࡩࡱࡶࡸࡳࡧ࡭ࡦࠤዂ"): platform.node(),
        bstack111l11_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠥዃ"): platform.system(),
        bstack111l11_opy_ (u"ࠤࡷࡽࡵ࡫ࠢዄ"): platform.machine(),
        bstack111l11_opy_ (u"ࠥࡺࡪࡸࡳࡪࡱࡱࠦዅ"): platform.version(),
        bstack111l11_opy_ (u"ࠦࡦࡸࡣࡩࠤ዆"): platform.architecture()[0]
    }
def bstack1ll1l11l11_opy_():
    try:
        import selenium
        return True
    except ImportError:
        return False
def bstack111l1l1lll_opy_():
    if bstack1l11l111ll_opy_.get_property(bstack111l11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡹࡥࡴࡵ࡬ࡳࡳ࠭዇")):
        return bstack111l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬወ")
    return bstack111l11_opy_ (u"ࠧࡶࡰ࡮ࡲࡴࡽ࡮ࡠࡩࡵ࡭ࡩ࠭ዉ")
def bstack111l1llll1_opy_(driver):
    info = {
        bstack111l11_opy_ (u"ࠨࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧዊ"): driver.capabilities,
        bstack111l11_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡢ࡭ࡩ࠭ዋ"): driver.session_id,
        bstack111l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࠫዌ"): driver.capabilities.get(bstack111l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩው"), None),
        bstack111l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠧዎ"): driver.capabilities.get(bstack111l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧዏ"), None),
        bstack111l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩዐ"): driver.capabilities.get(bstack111l11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡑࡥࡲ࡫ࠧዑ"), None),
    }
    if bstack111l1l1lll_opy_() == bstack111l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨዒ"):
        info[bstack111l11_opy_ (u"ࠪࡴࡷࡵࡤࡶࡥࡷࠫዓ")] = bstack111l11_opy_ (u"ࠫࡦࡶࡰ࠮ࡣࡸࡸࡴࡳࡡࡵࡧࠪዔ") if bstack1ll111lll1_opy_() else bstack111l11_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡫ࠧዕ")
    return info
def bstack1ll111lll1_opy_():
    if bstack1l11l111ll_opy_.get_property(bstack111l11_opy_ (u"࠭ࡡࡱࡲࡢࡥࡺࡺ࡯࡮ࡣࡷࡩࠬዖ")):
        return True
    if bstack1ll11l1l11_opy_(os.environ.get(bstack111l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨ዗"), None)):
        return True
    return False
def bstack1lllll1lll_opy_(bstack111l1l11l1_opy_, url, data, config):
    headers = config.get(bstack111l11_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡴࠩዘ"), None)
    proxies = bstack1l11ll11l1_opy_(config, url)
    auth = config.get(bstack111l11_opy_ (u"ࠩࡤࡹࡹ࡮ࠧዙ"), None)
    response = requests.request(
            bstack111l1l11l1_opy_,
            url=url,
            headers=headers,
            auth=auth,
            json=data,
            proxies=proxies
        )
    return response
def bstack1lll1lll1l_opy_(bstack1ll1ll11ll_opy_, size):
    bstack11l1llll_opy_ = []
    while len(bstack1ll1ll11ll_opy_) > size:
        bstack1l1ll1l11_opy_ = bstack1ll1ll11ll_opy_[:size]
        bstack11l1llll_opy_.append(bstack1l1ll1l11_opy_)
        bstack1ll1ll11ll_opy_ = bstack1ll1ll11ll_opy_[size:]
    bstack11l1llll_opy_.append(bstack1ll1ll11ll_opy_)
    return bstack11l1llll_opy_
def bstack111ll11111_opy_(message, bstack11l111lll1_opy_=False):
    os.write(1, bytes(message, bstack111l11_opy_ (u"ࠪࡹࡹ࡬࠭࠹ࠩዚ")))
    os.write(1, bytes(bstack111l11_opy_ (u"ࠫࡡࡴࠧዛ"), bstack111l11_opy_ (u"ࠬࡻࡴࡧ࠯࠻ࠫዜ")))
    if bstack11l111lll1_opy_:
        with open(bstack111l11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࠳࡯࠲࠳ࡼ࠱ࠬዝ") + os.environ[bstack111l11_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡇ࡛ࡉࡍࡆࡢࡌࡆ࡙ࡈࡆࡆࡢࡍࡉ࠭ዞ")] + bstack111l11_opy_ (u"ࠨ࠰࡯ࡳ࡬࠭ዟ"), bstack111l11_opy_ (u"ࠩࡤࠫዠ")) as f:
            f.write(message + bstack111l11_opy_ (u"ࠪࡠࡳ࠭ዡ"))
def bstack111ll1ll1l_opy_():
    return os.environ[bstack111l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅ࡚࡚ࡏࡎࡃࡗࡍࡔࡔࠧዢ")].lower() == bstack111l11_opy_ (u"ࠬࡺࡲࡶࡧࠪዣ")
def bstack1lllll11l_opy_(bstack11l11111l1_opy_):
    return bstack111l11_opy_ (u"࠭ࡻࡾ࠱ࡾࢁࠬዤ").format(bstack11l11ll11l_opy_, bstack11l11111l1_opy_)
def bstack11ll1l1ll_opy_():
    return bstack1l111llll1_opy_().replace(tzinfo=None).isoformat() + bstack111l11_opy_ (u"࡛ࠧࠩዥ")
def bstack11l11l11l1_opy_(start, finish):
    return (datetime.datetime.fromisoformat(finish.rstrip(bstack111l11_opy_ (u"ࠨ࡜ࠪዦ"))) - datetime.datetime.fromisoformat(start.rstrip(bstack111l11_opy_ (u"ࠩ࡝ࠫዧ")))).total_seconds() * 1000
def bstack111ll1111l_opy_(timestamp):
    return bstack111l11llll_opy_(timestamp).isoformat() + bstack111l11_opy_ (u"ࠪ࡞ࠬየ")
def bstack111lllll1l_opy_(bstack111ll11ll1_opy_):
    date_format = bstack111l11_opy_ (u"ࠫࠪ࡟ࠥ࡮ࠧࡧࠤࠪࡎ࠺ࠦࡏ࠽ࠩࡘ࠴ࠥࡧࠩዩ")
    bstack11l111llll_opy_ = datetime.datetime.strptime(bstack111ll11ll1_opy_, date_format)
    return bstack11l111llll_opy_.isoformat() + bstack111l11_opy_ (u"ࠬࡠࠧዪ")
def bstack11l11l1ll1_opy_(outcome):
    _, exception, _ = outcome.excinfo or (None, None, None)
    if exception:
        return bstack111l11_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ያ")
    else:
        return bstack111l11_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧዬ")
def bstack1ll11l1l11_opy_(val):
    if val is None:
        return False
    return val.__str__().lower() == bstack111l11_opy_ (u"ࠨࡶࡵࡹࡪ࠭ይ")
def bstack11l1111lll_opy_(val):
    return val.__str__().lower() == bstack111l11_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨዮ")
def bstack1l1111ll11_opy_(bstack111l1l1111_opy_=Exception, class_method=False, default_value=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except bstack111l1l1111_opy_ as e:
                print(bstack111l11_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡩࡹࡳࡩࡴࡪࡱࡱࠤࢀࢃࠠ࠮ࡀࠣࡿࢂࡀࠠࡼࡿࠥዯ").format(func.__name__, bstack111l1l1111_opy_.__name__, str(e)))
                return default_value
        return wrapper
    def bstack111lll1l1l_opy_(bstack111llll11l_opy_):
        def wrapped(cls, *args, **kwargs):
            try:
                return bstack111llll11l_opy_(cls, *args, **kwargs)
            except bstack111l1l1111_opy_ as e:
                print(bstack111l11_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡪࡺࡴࡣࡵ࡫ࡲࡲࠥࢁࡽࠡ࠯ࡁࠤࢀࢃ࠺ࠡࡽࢀࠦደ").format(bstack111llll11l_opy_.__name__, bstack111l1l1111_opy_.__name__, str(e)))
                return default_value
        return wrapped
    if class_method:
        return bstack111lll1l1l_opy_
    else:
        return decorator
def bstack1l11lll11_opy_(bstack11ll1lll1l_opy_):
    if bstack111l11_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩዱ") in bstack11ll1lll1l_opy_ and bstack11l1111lll_opy_(bstack11ll1lll1l_opy_[bstack111l11_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪዲ")]):
        return False
    if bstack111l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩዳ") in bstack11ll1lll1l_opy_ and bstack11l1111lll_opy_(bstack11ll1lll1l_opy_[bstack111l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪዴ")]):
        return False
    return True
def bstack11l1l111_opy_():
    try:
        from pytest_bdd import reporting
        return True
    except Exception as e:
        return False
def bstack1l1l1l111_opy_(hub_url):
    if bstack1lll1l1ll_opy_() <= version.parse(bstack111l11_opy_ (u"ࠩ࠶࠲࠶࠹࠮࠱ࠩድ")):
        if hub_url != bstack111l11_opy_ (u"ࠪࠫዶ"):
            return bstack111l11_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࠧዷ") + hub_url + bstack111l11_opy_ (u"ࠧࡀ࠸࠱࠱ࡺࡨ࠴࡮ࡵࡣࠤዸ")
        return bstack1l11ll11l_opy_
    if hub_url != bstack111l11_opy_ (u"࠭ࠧዹ"):
        return bstack111l11_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤዺ") + hub_url + bstack111l11_opy_ (u"ࠣ࠱ࡺࡨ࠴࡮ࡵࡣࠤዻ")
    return bstack1ll1111lll_opy_
def bstack111l1l1l1l_opy_():
    return isinstance(os.getenv(bstack111l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒ࡜ࡘࡊ࡙ࡔࡠࡒࡏ࡙ࡌࡏࡎࠨዼ")), str)
def bstack1lll11ll1l_opy_(url):
    return urlparse(url).hostname
def bstack1l1ll1lll1_opy_(hostname):
    for bstack1llllll11l_opy_ in bstack1lllllll11_opy_:
        regex = re.compile(bstack1llllll11l_opy_)
        if regex.match(hostname):
            return True
    return False
def bstack111l1ll1ll_opy_(bstack111ll11lll_opy_, file_name, logger):
    bstack11llll1ll_opy_ = os.path.join(os.path.expanduser(bstack111l11_opy_ (u"ࠪࢂࠬዽ")), bstack111ll11lll_opy_)
    try:
        if not os.path.exists(bstack11llll1ll_opy_):
            os.makedirs(bstack11llll1ll_opy_)
        file_path = os.path.join(os.path.expanduser(bstack111l11_opy_ (u"ࠫࢃ࠭ዾ")), bstack111ll11lll_opy_, file_name)
        if not os.path.isfile(file_path):
            with open(file_path, bstack111l11_opy_ (u"ࠬࡽࠧዿ")):
                pass
            with open(file_path, bstack111l11_opy_ (u"ࠨࡷࠬࠤጀ")) as outfile:
                json.dump({}, outfile)
        return file_path
    except Exception as e:
        logger.debug(bstack1l11llll11_opy_.format(str(e)))
def bstack111lll11ll_opy_(file_name, key, value, logger):
    file_path = bstack111l1ll1ll_opy_(bstack111l11_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧጁ"), file_name, logger)
    if file_path != None:
        if os.path.exists(file_path):
            bstack1111ll1l1_opy_ = json.load(open(file_path, bstack111l11_opy_ (u"ࠨࡴࡥࠫጂ")))
        else:
            bstack1111ll1l1_opy_ = {}
        bstack1111ll1l1_opy_[key] = value
        with open(file_path, bstack111l11_opy_ (u"ࠤࡺ࠯ࠧጃ")) as outfile:
            json.dump(bstack1111ll1l1_opy_, outfile)
def bstack1l11l1l11l_opy_(file_name, logger):
    file_path = bstack111l1ll1ll_opy_(bstack111l11_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪጄ"), file_name, logger)
    bstack1111ll1l1_opy_ = {}
    if file_path != None and os.path.exists(file_path):
        with open(file_path, bstack111l11_opy_ (u"ࠫࡷ࠭ጅ")) as bstack1l1ll111l_opy_:
            bstack1111ll1l1_opy_ = json.load(bstack1l1ll111l_opy_)
    return bstack1111ll1l1_opy_
def bstack1l1l1l11_opy_(file_path, logger):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        logger.debug(bstack111l11_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡥࡧ࡯ࡩࡹ࡯࡮ࡨࠢࡩ࡭ࡱ࡫࠺ࠡࠩጆ") + file_path + bstack111l11_opy_ (u"࠭ࠠࠨጇ") + str(e))
def bstack1lll1l1ll_opy_():
    from selenium import webdriver
    return version.parse(webdriver.__version__)
class Notset:
    def __repr__(self):
        return bstack111l11_opy_ (u"ࠢ࠽ࡐࡒࡘࡘࡋࡔ࠿ࠤገ")
def bstack11ll111ll_opy_(config):
    if bstack111l11_opy_ (u"ࠨ࡫ࡶࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠧጉ") in config:
        del (config[bstack111l11_opy_ (u"ࠩ࡬ࡷࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠨጊ")])
        return False
    if bstack1lll1l1ll_opy_() < version.parse(bstack111l11_opy_ (u"ࠪ࠷࠳࠺࠮࠱ࠩጋ")):
        return False
    if bstack1lll1l1ll_opy_() >= version.parse(bstack111l11_opy_ (u"ࠫ࠹࠴࠱࠯࠷ࠪጌ")):
        return True
    if bstack111l11_opy_ (u"ࠬࡻࡳࡦ࡙࠶ࡇࠬግ") in config and config[bstack111l11_opy_ (u"࠭ࡵࡴࡧ࡚࠷ࡈ࠭ጎ")] is False:
        return False
    else:
        return True
def bstack1l111l11l_opy_(args_list, bstack111ll1l11l_opy_):
    index = -1
    for value in bstack111ll1l11l_opy_:
        try:
            index = args_list.index(value)
            return index
        except Exception as e:
            return index
    return index
class Result:
    def __init__(self, result=None, duration=None, exception=None, bstack11llllll1l_opy_=None):
        self.result = result
        self.duration = duration
        self.exception = exception
        self.exception_type = type(self.exception).__name__ if exception else None
        self.bstack11llllll1l_opy_ = bstack11llllll1l_opy_
    @classmethod
    def passed(cls):
        return Result(result=bstack111l11_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧጏ"))
    @classmethod
    def failed(cls, exception=None):
        return Result(result=bstack111l11_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨጐ"), exception=exception)
    def bstack11ll11llll_opy_(self):
        if self.result != bstack111l11_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ጑"):
            return None
        if bstack111l11_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࠨጒ") in self.exception_type:
            return bstack111l11_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࡅࡳࡴࡲࡶࠧጓ")
        return bstack111l11_opy_ (u"࡛ࠧ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡆࡴࡵࡳࡷࠨጔ")
    def bstack111l1l1l11_opy_(self):
        if self.result != bstack111l11_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ጕ"):
            return None
        if self.bstack11llllll1l_opy_:
            return self.bstack11llllll1l_opy_
        return bstack11l1111ll1_opy_(self.exception)
def bstack11l1111ll1_opy_(exc):
    return [traceback.format_exception(exc)]
def bstack111l1lll11_opy_(message):
    if isinstance(message, str):
        return not bool(message and message.strip())
    return True
def bstack1ll111l1ll_opy_(object, key, default_value):
    if not object or not object.__dict__:
        return default_value
    if key in object.__dict__.keys():
        return object.__dict__.get(key)
    return default_value
def bstack1ll11111l1_opy_(config, logger):
    try:
        import playwright
        bstack111ll1l1l1_opy_ = playwright.__file__
        bstack111llll1ll_opy_ = os.path.split(bstack111ll1l1l1_opy_)
        bstack11l11l1l11_opy_ = bstack111llll1ll_opy_[0] + bstack111l11_opy_ (u"ࠧ࠰ࡦࡵ࡭ࡻ࡫ࡲ࠰ࡲࡤࡧࡰࡧࡧࡦ࠱࡯࡭ࡧ࠵ࡣ࡭࡫࠲ࡧࡱ࡯࠮࡫ࡵࠪ጖")
        os.environ[bstack111l11_opy_ (u"ࠨࡉࡏࡓࡇࡇࡌࡠࡃࡊࡉࡓ࡚࡟ࡉࡖࡗࡔࡤࡖࡒࡐ࡚࡜ࠫ጗")] = bstack1llll1l11_opy_(config)
        with open(bstack11l11l1l11_opy_, bstack111l11_opy_ (u"ࠩࡵࠫጘ")) as f:
            bstack11l111l1l_opy_ = f.read()
            bstack111llll1l1_opy_ = bstack111l11_opy_ (u"ࠪ࡫ࡱࡵࡢࡢ࡮࠰ࡥ࡬࡫࡮ࡵࠩጙ")
            bstack11l1111l11_opy_ = bstack11l111l1l_opy_.find(bstack111llll1l1_opy_)
            if bstack11l1111l11_opy_ == -1:
              process = subprocess.Popen(bstack111l11_opy_ (u"ࠦࡳࡶ࡭ࠡ࡫ࡱࡷࡹࡧ࡬࡭ࠢࡪࡰࡴࡨࡡ࡭࠯ࡤ࡫ࡪࡴࡴࠣጚ"), shell=True, cwd=bstack111llll1ll_opy_[0])
              process.wait()
              bstack111ll111l1_opy_ = bstack111l11_opy_ (u"ࠬࠨࡵࡴࡧࠣࡷࡹࡸࡩࡤࡶࠥ࠿ࠬጛ")
              bstack111ll1l111_opy_ = bstack111l11_opy_ (u"ࠨࠢࠣࠢ࡟ࠦࡺࡹࡥࠡࡵࡷࡶ࡮ࡩࡴ࡝ࠤ࠾ࠤࡨࡵ࡮ࡴࡶࠣࡿࠥࡨ࡯ࡰࡶࡶࡸࡷࡧࡰࠡࡿࠣࡁࠥࡸࡥࡲࡷ࡬ࡶࡪ࠮ࠧࡨ࡮ࡲࡦࡦࡲ࠭ࡢࡩࡨࡲࡹ࠭ࠩ࠼ࠢ࡬ࡪࠥ࠮ࡰࡳࡱࡦࡩࡸࡹ࠮ࡦࡰࡹ࠲ࡌࡒࡏࡃࡃࡏࡣࡆࡍࡅࡏࡖࡢࡌ࡙࡚ࡐࡠࡒࡕࡓ࡝࡟ࠩࠡࡤࡲࡳࡹࡹࡴࡳࡣࡳࠬ࠮ࡁࠠࠣࠤࠥጜ")
              bstack111lllll11_opy_ = bstack11l111l1l_opy_.replace(bstack111ll111l1_opy_, bstack111ll1l111_opy_)
              with open(bstack11l11l1l11_opy_, bstack111l11_opy_ (u"ࠧࡸࠩጝ")) as f:
                f.write(bstack111lllll11_opy_)
    except Exception as e:
        logger.error(bstack1l1l1lllll_opy_.format(str(e)))
def bstack11l1l1ll_opy_():
  try:
    bstack111llll111_opy_ = os.path.join(tempfile.gettempdir(), bstack111l11_opy_ (u"ࠨࡱࡳࡸ࡮ࡳࡡ࡭ࡡ࡫ࡹࡧࡥࡵࡳ࡮࠱࡮ࡸࡵ࡮ࠨጞ"))
    bstack111lllllll_opy_ = []
    if os.path.exists(bstack111llll111_opy_):
      with open(bstack111llll111_opy_) as f:
        bstack111lllllll_opy_ = json.load(f)
      os.remove(bstack111llll111_opy_)
    return bstack111lllllll_opy_
  except:
    pass
  return []
def bstack111llllll_opy_(bstack1llll1l1_opy_):
  try:
    bstack111lllllll_opy_ = []
    bstack111llll111_opy_ = os.path.join(tempfile.gettempdir(), bstack111l11_opy_ (u"ࠩࡲࡴࡹ࡯࡭ࡢ࡮ࡢ࡬ࡺࡨ࡟ࡶࡴ࡯࠲࡯ࡹ࡯࡯ࠩጟ"))
    if os.path.exists(bstack111llll111_opy_):
      with open(bstack111llll111_opy_) as f:
        bstack111lllllll_opy_ = json.load(f)
    bstack111lllllll_opy_.append(bstack1llll1l1_opy_)
    with open(bstack111llll111_opy_, bstack111l11_opy_ (u"ࠪࡻࠬጠ")) as f:
        json.dump(bstack111lllllll_opy_, f)
  except:
    pass
def bstack1l1l1lll11_opy_(logger, bstack111l1l1ll1_opy_ = False):
  try:
    test_name = os.environ.get(bstack111l11_opy_ (u"ࠫࡕ࡟ࡔࡆࡕࡗࡣ࡙ࡋࡓࡕࡡࡑࡅࡒࡋࠧጡ"), bstack111l11_opy_ (u"ࠬ࠭ጢ"))
    if test_name == bstack111l11_opy_ (u"࠭ࠧጣ"):
        test_name = threading.current_thread().__dict__.get(bstack111l11_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࡂࡥࡦࡢࡸࡪࡹࡴࡠࡰࡤࡱࡪ࠭ጤ"), bstack111l11_opy_ (u"ࠨࠩጥ"))
    bstack111ll11l11_opy_ = bstack111l11_opy_ (u"ࠩ࠯ࠤࠬጦ").join(threading.current_thread().bstackTestErrorMessages)
    if bstack111l1l1ll1_opy_:
        bstack1ll11lllll_opy_ = os.environ.get(bstack111l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪጧ"), bstack111l11_opy_ (u"ࠫ࠵࠭ጨ"))
        bstack11l1l11l_opy_ = {bstack111l11_opy_ (u"ࠬࡴࡡ࡮ࡧࠪጩ"): test_name, bstack111l11_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬጪ"): bstack111ll11l11_opy_, bstack111l11_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭ጫ"): bstack1ll11lllll_opy_}
        bstack111lll1ll1_opy_ = []
        bstack11l1111l1l_opy_ = os.path.join(tempfile.gettempdir(), bstack111l11_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡲࡳࡴࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵ࠰࡭ࡷࡴࡴࠧጬ"))
        if os.path.exists(bstack11l1111l1l_opy_):
            with open(bstack11l1111l1l_opy_) as f:
                bstack111lll1ll1_opy_ = json.load(f)
        bstack111lll1ll1_opy_.append(bstack11l1l11l_opy_)
        with open(bstack11l1111l1l_opy_, bstack111l11_opy_ (u"ࠩࡺࠫጭ")) as f:
            json.dump(bstack111lll1ll1_opy_, f)
    else:
        bstack11l1l11l_opy_ = {bstack111l11_opy_ (u"ࠪࡲࡦࡳࡥࠨጮ"): test_name, bstack111l11_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪጯ"): bstack111ll11l11_opy_, bstack111l11_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫጰ"): str(multiprocessing.current_process().name)}
        if bstack111l11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡥࡳࡴࡲࡶࡤࡲࡩࡴࡶࠪጱ") not in multiprocessing.current_process().__dict__.keys():
            multiprocessing.current_process().bstack_error_list = []
        multiprocessing.current_process().bstack_error_list.append(bstack11l1l11l_opy_)
  except Exception as e:
      logger.warn(bstack111l11_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡷࡹࡵࡲࡦࠢࡳࡽࡹ࡫ࡳࡵࠢࡩࡹࡳࡴࡥ࡭ࠢࡧࡥࡹࡧ࠺ࠡࡽࢀࠦጲ").format(e))
def bstack11ll11l1l_opy_(error_message, test_name, index, logger):
  try:
    bstack11l111l111_opy_ = []
    bstack11l1l11l_opy_ = {bstack111l11_opy_ (u"ࠨࡰࡤࡱࡪ࠭ጳ"): test_name, bstack111l11_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨጴ"): error_message, bstack111l11_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩጵ"): index}
    bstack111lll1lll_opy_ = os.path.join(tempfile.gettempdir(), bstack111l11_opy_ (u"ࠫࡷࡵࡢࡰࡶࡢࡩࡷࡸ࡯ࡳࡡ࡯࡭ࡸࡺ࠮࡫ࡵࡲࡲࠬጶ"))
    if os.path.exists(bstack111lll1lll_opy_):
        with open(bstack111lll1lll_opy_) as f:
            bstack11l111l111_opy_ = json.load(f)
    bstack11l111l111_opy_.append(bstack11l1l11l_opy_)
    with open(bstack111lll1lll_opy_, bstack111l11_opy_ (u"ࠬࡽࠧጷ")) as f:
        json.dump(bstack11l111l111_opy_, f)
  except Exception as e:
    logger.warn(bstack111l11_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡶࡸࡴࡸࡥࠡࡴࡲࡦࡴࡺࠠࡧࡷࡱࡲࡪࡲࠠࡥࡣࡷࡥ࠿ࠦࡻࡾࠤጸ").format(e))
def bstack11l1l1l11_opy_(bstack1ll1llllll_opy_, name, logger):
  try:
    bstack11l1l11l_opy_ = {bstack111l11_opy_ (u"ࠧ࡯ࡣࡰࡩࠬጹ"): name, bstack111l11_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧጺ"): bstack1ll1llllll_opy_, bstack111l11_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨጻ"): str(threading.current_thread()._name)}
    return bstack11l1l11l_opy_
  except Exception as e:
    logger.warn(bstack111l11_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡵࡱࡵࡩࠥࡨࡥࡩࡣࡹࡩࠥ࡬ࡵ࡯ࡰࡨࡰࠥࡪࡡࡵࡣ࠽ࠤࢀࢃࠢጼ").format(e))
  return
def bstack11l111111l_opy_():
    return platform.system() == bstack111l11_opy_ (u"ࠫ࡜࡯࡮ࡥࡱࡺࡷࠬጽ")
def bstack1l11l111_opy_(bstack111ll1l1ll_opy_, config, logger):
    bstack111l1lllll_opy_ = {}
    try:
        return {key: config[key] for key in config if bstack111ll1l1ll_opy_.match(key)}
    except Exception as e:
        logger.debug(bstack111l11_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡨ࡬ࡰࡹ࡫ࡲࠡࡥࡲࡲ࡫࡯ࡧࠡ࡭ࡨࡽࡸࠦࡢࡺࠢࡵࡩ࡬࡫ࡸࠡ࡯ࡤࡸࡨ࡮࠺ࠡࡽࢀࠦጾ").format(e))
    return bstack111l1lllll_opy_
def bstack111l11lll1_opy_(bstack111ll1llll_opy_, bstack111l1ll1l1_opy_):
    bstack11l11l1l1l_opy_ = version.parse(bstack111ll1llll_opy_)
    bstack111l1ll11l_opy_ = version.parse(bstack111l1ll1l1_opy_)
    if bstack11l11l1l1l_opy_ > bstack111l1ll11l_opy_:
        return 1
    elif bstack11l11l1l1l_opy_ < bstack111l1ll11l_opy_:
        return -1
    else:
        return 0
def bstack1l111llll1_opy_():
    return datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
def bstack111l11llll_opy_(timestamp):
    return datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc).replace(tzinfo=None)
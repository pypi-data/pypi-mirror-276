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
from urllib.parse import urlparse
from bstack_utils.messages import bstack1111l1llll_opy_
def bstack1lllll11ll1_opy_(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
def bstack1lllll11lll_opy_(bstack1lllll111ll_opy_, bstack1lllll11l11_opy_):
    from pypac import get_pac
    from pypac import PACSession
    from pypac.parser import PACFile
    import socket
    if os.path.isfile(bstack1lllll111ll_opy_):
        with open(bstack1lllll111ll_opy_) as f:
            pac = PACFile(f.read())
    elif bstack1lllll11ll1_opy_(bstack1lllll111ll_opy_):
        pac = get_pac(url=bstack1lllll111ll_opy_)
    else:
        raise Exception(bstack111l11_opy_ (u"ࠫࡕࡧࡣࠡࡨ࡬ࡰࡪࠦࡤࡰࡧࡶࠤࡳࡵࡴࠡࡧࡻ࡭ࡸࡺ࠺ࠡࡽࢀࠫᑇ").format(bstack1lllll111ll_opy_))
    session = PACSession(pac)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((bstack111l11_opy_ (u"ࠧ࠾࠮࠹࠰࠻࠲࠽ࠨᑈ"), 80))
        bstack1lllll1111l_opy_ = s.getsockname()[0]
        s.close()
    except:
        bstack1lllll1111l_opy_ = bstack111l11_opy_ (u"࠭࠰࠯࠲࠱࠴࠳࠶ࠧᑉ")
    proxy_url = session.get_pac().find_proxy_for_url(bstack1lllll11l11_opy_, bstack1lllll1111l_opy_)
    return proxy_url
def bstack111ll1111_opy_(config):
    return bstack111l11_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪᑊ") in config or bstack111l11_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬᑋ") in config
def bstack1llll1l11_opy_(config):
    if not bstack111ll1111_opy_(config):
        return
    if config.get(bstack111l11_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬᑌ")):
        return config.get(bstack111l11_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭ᑍ"))
    if config.get(bstack111l11_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨᑎ")):
        return config.get(bstack111l11_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩᑏ"))
def bstack1l11ll11l1_opy_(config, bstack1lllll11l11_opy_):
    proxy = bstack1llll1l11_opy_(config)
    proxies = {}
    if config.get(bstack111l11_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩᑐ")) or config.get(bstack111l11_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫᑑ")):
        if proxy.endswith(bstack111l11_opy_ (u"ࠨ࠰ࡳࡥࡨ࠭ᑒ")):
            proxies = bstack1l1l11l11l_opy_(proxy, bstack1lllll11l11_opy_)
        else:
            proxies = {
                bstack111l11_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࠨᑓ"): proxy
            }
    return proxies
def bstack1l1l11l11l_opy_(bstack1lllll111ll_opy_, bstack1lllll11l11_opy_):
    proxies = {}
    global bstack1lllll11l1l_opy_
    if bstack111l11_opy_ (u"ࠪࡔࡆࡉ࡟ࡑࡔࡒ࡜࡞࠭ᑔ") in globals():
        return bstack1lllll11l1l_opy_
    try:
        proxy = bstack1lllll11lll_opy_(bstack1lllll111ll_opy_, bstack1lllll11l11_opy_)
        if bstack111l11_opy_ (u"ࠦࡉࡏࡒࡆࡅࡗࠦᑕ") in proxy:
            proxies = {}
        elif bstack111l11_opy_ (u"ࠧࡎࡔࡕࡒࠥᑖ") in proxy or bstack111l11_opy_ (u"ࠨࡈࡕࡖࡓࡗࠧᑗ") in proxy or bstack111l11_opy_ (u"ࠢࡔࡑࡆࡏࡘࠨᑘ") in proxy:
            bstack1lllll111l1_opy_ = proxy.split(bstack111l11_opy_ (u"ࠣࠢࠥᑙ"))
            if bstack111l11_opy_ (u"ࠤ࠽࠳࠴ࠨᑚ") in bstack111l11_opy_ (u"ࠥࠦᑛ").join(bstack1lllll111l1_opy_[1:]):
                proxies = {
                    bstack111l11_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࠪᑜ"): bstack111l11_opy_ (u"ࠧࠨᑝ").join(bstack1lllll111l1_opy_[1:])
                }
            else:
                proxies = {
                    bstack111l11_opy_ (u"࠭ࡨࡵࡶࡳࡷࠬᑞ"): str(bstack1lllll111l1_opy_[0]).lower() + bstack111l11_opy_ (u"ࠢ࠻࠱࠲ࠦᑟ") + bstack111l11_opy_ (u"ࠣࠤᑠ").join(bstack1lllll111l1_opy_[1:])
                }
        elif bstack111l11_opy_ (u"ࠤࡓࡖࡔ࡞࡙ࠣᑡ") in proxy:
            bstack1lllll111l1_opy_ = proxy.split(bstack111l11_opy_ (u"ࠥࠤࠧᑢ"))
            if bstack111l11_opy_ (u"ࠦ࠿࠵࠯ࠣᑣ") in bstack111l11_opy_ (u"ࠧࠨᑤ").join(bstack1lllll111l1_opy_[1:]):
                proxies = {
                    bstack111l11_opy_ (u"࠭ࡨࡵࡶࡳࡷࠬᑥ"): bstack111l11_opy_ (u"ࠢࠣᑦ").join(bstack1lllll111l1_opy_[1:])
                }
            else:
                proxies = {
                    bstack111l11_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧᑧ"): bstack111l11_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥᑨ") + bstack111l11_opy_ (u"ࠥࠦᑩ").join(bstack1lllll111l1_opy_[1:])
                }
        else:
            proxies = {
                bstack111l11_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࠪᑪ"): proxy
            }
    except Exception as e:
        print(bstack111l11_opy_ (u"ࠧࡹ࡯࡮ࡧࠣࡩࡷࡸ࡯ࡳࠤᑫ"), bstack1111l1llll_opy_.format(bstack1lllll111ll_opy_, str(e)))
    bstack1lllll11l1l_opy_ = proxies
    return proxies
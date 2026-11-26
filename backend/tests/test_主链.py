import os, tempfile
from pathlib import Path

_tmp = tempfile.mkdtemp()
os.environ['数据目录'] = _tmp
os.environ['夹具目录'] = str(Path(__file__).resolve().parents[2] / 'fixtures')

from app import seed
from app.services import 入队, 投递, 死信, 互证, 夹具, 签名目录


def setup_module():
    seed.初始化库()


def test_主链贯通():
    ev = 入队.建事件({'事件类型': 'invoice.paid', '端点键': 'ep-partner', '载荷摘要': 'ok-1'})
    eid = ev['事件号']
    r = 投递.投递一次(eid)
    assert r['状态'] == '成功'
    assert 签名目录.事件一条(eid)['状态'] == '已投递'


def test_失败进死信():
    # 最大重试默认3，连续强制失败
    ev = 入队.建事件({'事件类型': 'x.fail', '端点键': 'ep-billing', '载荷摘要': 'f'})
    eid = ev['事件号']
    last = None
    for _ in range(5):
        last = 投递.投递一次(eid, 强制失败=True)
        if last.get('事件状态') == '死信':
            break
    assert last and last.get('事件状态') == '死信'
    assert any(x['事件号']==eid for x in 签名目录.死信列表())


def test_夹具入队():
    体 = 夹具.读取('批量事件样例')
    n0 = len(签名目录.事件列表())
    for item in 体['事件']:
        入队.建事件(item)
    assert len(签名目录.事件列表()) >= n0 + 3


def test_互证():
    rep = 互证.跑一次()
    assert '明细' in rep
    assert isinstance(rep['是否全部对齐'], bool)

import os, tempfile
from pathlib import Path

_tmp = tempfile.mkdtemp()
os.environ['数据目录'] = _tmp
os.environ['夹具目录'] = str(Path(__file__).resolve().parents[2] / 'fixtures')

from app.factory import create_app
from app import seed


def setup_module():
    seed.初始化库()


def test_登录页与登录():
    app = create_app()
    c = app.test_client()
    r = c.get('/login')
    assert r.status_code == 200
    assert '密码' in r.get_data(as_text=True) or 'password' in r.get_data(as_text=True).lower() or '登录' in r.get_data(as_text=True)
    bad = c.post('/api/登录', json={'账号': 'admin', '密码': 'wrong'})
    assert bad.status_code == 401
    ok = c.post('/api/登录', json={'账号': 'admin', '密码': '123456'})
    assert ok.status_code == 200
    g = c.get('/api/概览')
    assert g.status_code == 200
    assert '事件总数' in g.get_json()


def test_未登录拦api():
    app = create_app()
    c = app.test_client()
    r = c.get('/api/事件')
    assert r.status_code == 401

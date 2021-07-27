from libs.Curator import Curator


def test_fix_cas_number():
    curator = Curator()
    assert curator.fix_cas_number('7783893') == '7783-89-3'
    assert curator.fix_cas_number('7783-89-3') == '7783-89-3'

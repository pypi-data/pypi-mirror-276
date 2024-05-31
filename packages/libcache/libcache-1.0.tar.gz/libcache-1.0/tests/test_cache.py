import libcache, time

def test_cache():
    d = libcache.Cache()
    d.saveElement("test", 50)
    assert d.getElement("test") == 50
    d.clearCache()
    try:
        d.getElement("test")
        raise AssertionError("Test exists")
    except libcache.NotInCache:
        pass
    d.saveElement("test", 60, 0.5)
    time.sleep(0.4)
    assert d.getElement("test") == 60
    time.sleep(0.1)
    assert d.doesElementExist("test") == False
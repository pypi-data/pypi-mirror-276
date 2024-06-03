from threading import get_ident


class GoodLib:
    def __init__(self, getGoodFunc, closeGoodfunc=lambda g: g.close()) -> None:
        self._getf = getGoodFunc
        self._closef = closeGoodfunc
        self._lib = dict()

    def getGood(self, key):
        if self._lib.get(key) is None:
            self._lib[key] = self._getf()
        good = self._lib[key]
        return good

    def delGood(self, key, iftz=True):
        if self._lib.get(key, None) is not None:
            good = self._lib[key]
            self._closef(good)
            self._lib.pop(key)
            if iftz:
                print('线程%s的资源已删除' % key)
        else:
            if iftz:
                print('线程%s未拥有资源,删除失败' % key)

    def delAllGood(self, iftz=True):
        [self._closef(good) for good in self._lib.values()]
        self._lib.clear()
        if iftz:
            print('线程资源已全部关闭')


class ThreadGoodLib(GoodLib):
    def __init__(self, getGoodFunc, closeGoodfunc=lambda g: g.close()) -> None:
        super().__init__(getGoodFunc, closeGoodfunc)

    def getThreadGood(self):
        return self.getGood(get_ident())

    def delThreadGood(self, iftz=True):
        return self.delGood(get_ident(), iftz)

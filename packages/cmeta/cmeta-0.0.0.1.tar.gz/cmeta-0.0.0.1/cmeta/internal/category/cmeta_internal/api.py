from cmeta.category import Category

class CMetaCategory(Category):
    """
    """

    ############################################################
    def __init__(self, cmeta):
        super().__init__(cmeta)

        self._version = '0.1.1'

    ############################################################
    def test(self):
        from cmeta_internal import test
        return test.test(self.cmeta)

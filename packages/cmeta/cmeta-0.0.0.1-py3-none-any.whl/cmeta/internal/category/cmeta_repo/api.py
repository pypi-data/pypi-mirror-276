from cmeta.category import Category

class CMetaCategory(Category):
    """
    """

    ############################################################
    def __init__(self, cmeta):
        super().__init__(cmeta, __file__, __name__)

        self._logger.debug('****** REPO INIT ******')

        self._version = '0.1.1'

    ############################################################
    def ls(self, args=[]):
        print (args)
        from cmeta_repo import ls
        return ls.run(self)

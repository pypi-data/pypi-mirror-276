

class CMBase(object):
    def __init__(self):
        pass


class CMWrapper(CMBase):
    def __init__(self):
        super().__init__()


class CMObject(CMWrapper):
    def __init__(self):
        super().__init__()


class CMNode(CMObject):
    '''
    maya节点
    '''

    def __init__(self):
        super().__init__()


class CMDagNodeBase(CMObject):
    '''
    自定义DAG节点
    '''

    def __init__(self, ):
        super().__init__()



class CMProperty(CMObject):
    def __init__(self):
        super().__init__()


class CMJSProperty(CMObject):
    def __init__(self):
        super().__init__()

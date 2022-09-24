class BooleanFormatter(object):

    def __init__(self, truestr=' ', falsestr='não'):
        self.strs = {True: truestr, False: falsestr}

    
    def format(self, value):
        return self.strs[value or False]


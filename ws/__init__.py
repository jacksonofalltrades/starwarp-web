class DataChoice(object):
    CHOICE_PREFIX = 'CHOICE'
    LABEL_PREFIX = 'LABEL'
    def __init__(self):
        self.choice_dict = {}
        self.label_dict = {}
        cindex = 0
        lindex = 0
        for attr in dir(self):
            if attr.startswith(DataChoice.CHOICE_PREFIX):
                attrval = getattr(self, attr)
                self.choice_dict[cindex] = attrval
                cindex += 1
            if attr.startswith(DataChoice.LABEL_PREFIX):
                attrval = getattr(self, attr)
                self.label_dict[lindex] = attrval
                lindex += 1
                
        self.inv_choice_dict = dict((v,k) for k, v in self.choice_dict.iteritems())
        choices = []
        for key, val in self.choice_dict.items():
            choices.append((key, val))
        self.choices = tuple(choices)
    
    @classmethod
    def get_code(cls, key):
        inst = cls()
        if key in inst.inv_choice_dict:
            return inst.inv_choice_dict[key]
        else:
            return None
    
    @classmethod
    def get_key(cls, code):
        inst = cls()
        if code in inst.choice_dict:
            return inst.choice_dict[code]
        else:
            return None
        
    @classmethod
    def get_label(cls, code):
        inst = cls()
        if code in inst.label_dict:
            return inst.label_dict[code]
        else:
            return None
    
    @classmethod
    def choices(cls):
        inst = cls()
        return inst.choices
    
    @classmethod
    def keys(cls):
        inst = cls()
        return inst.choice_dict.values()
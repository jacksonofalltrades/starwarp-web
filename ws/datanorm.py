import re
import logging
from datetime import datetime

# Key must be present in object
class RequiredConstraint(object):
    @classmethod
    def check(cls, obj, keyname):
        if keyname in obj:
            return (True, None)
        else:
            logging.error("[%s] is a required field."%keyname)
            return (False, "[%s] is a required field."%keyname)

# Value must be non-empty
class NotEmptyConstraint(object):
    @classmethod
    def check(cls, obj, keyname):
        if keyname in obj:
            if str(obj[keyname]):
                return (True, None)
            else:
                logging.error("Value for field [%s] must not be empty."%keyname)
                return (False, "Value for field [%s] must not be empty."%keyname)
        else:
            return (True, None)

class MinLengthConstraint(object):
    def __init__(self, minlen):
        self.minlen = minlen
    
    def check(self, obj, keyname):
        if keyname in obj and str(obj[keyname]):
            if len(str(obj[keyname])) >= self.minlen:
                return (True, None)
            else:
                return (False, "Value for field is below the minimum length of %s"%self.minlen)
        else:
            return (True, None)

class MaxLengthConstraint(object):
    def __init__(self, maxlen):
        self.maxlen = maxlen
    
    def check(self, obj, keyname):
        if keyname in obj and str(obj[keyname]):
            if len(str(obj[keyname])) <= self.maxlen:
                return (True, None)
            else:
                return (False, "Value for field exceeds the maximum length of %s"%self.maxlen)
        else:
            return (True, None)

class EnumConstraint(object):
    def __init__(self, *valuelist):
        self.valuelist = valuelist
    
    def check(self, obj, keyname):
        if keyname in obj and str(obj[keyname]):
            val = str(obj[keyname])
            if val in self.valuelist:
                return (True, None)
            else:
                return (False, "Field [%s] with value [%s] is not in list of acceptable values: %s"%(keyname, val, self.valuelist))
        else:
            return (True, None)

class AttributeDef(object):
    def __init__(self, typename, keyname):
        self.typename = typename
        self.keyname = keyname
        self.constraint_cls_list = []
    
    def add_constraint(self, c):
        self.constraint_cls_list.append(c)
        
    def check_constraints(self, obj):
        final_status = True
        msgs = []
        for c in self.constraint_cls_list:
            (status, msg) = c.check(obj, self.keyname)
            final_status = status and final_status
            if msg:
                msgs.append(msg)
        return (final_status, msgs)

class DataNormalizer(object):
    TYPES = {}
    
    def __init__(self):
        self.attrdefs = {}
    
    def add_attr_def(self, varname, keyname, typename, *constraints):
        setattr(self, varname, keyname)
        self.attrdefs[keyname] = AttributeDef(typename, keyname)
        for c in constraints:
            self.attrdefs[keyname].add_constraint(c)
                
    def blank_fill(self):
        retval = {}
        for attr in self.attrdefs.values():
            retval[attr.keyname] = None
        return retval
    
    # Return (normed_dict, None) only if all attributes check out
    # otherwise return (False, err_msg)
    def normalize(self, obj):
        normed_dict = self.blank_fill()
        final_status = True
        msglist = []
        if type(obj) == dict:
            # Check constraints
            for attrdef in self.attrdefs.values():
                (status, msgs) = attrdef.check_constraints(obj)
                final_status = status and final_status
                if msgs:
                    msglist.extend(msgs)
            
            for key, val in obj.items():
                if key in self.attrdefs:
                    attr = self.attrdefs[key]
                    if attr.typename in DataNormalizer.TYPES:
                        typefunc = DataNormalizer.TYPES[attr.typename]
                        (attr_status, normed_val) = typefunc(val)
                        final_status = attr_status and final_status
                        if attr_status:
                            normed_dict[key] = normed_val
                        else:
                            final_status = False
                            logging.error("Could not convert attribute [%s] with value [%s] to type [%s]"%(key, val, attr.typename))
                            msglist.append("Could not convert attribute [%s] with value [%s] to type [%s]"%(key, val, attr.typename))
                    else:
                        final_status = False
                        logging.error("Cannot find type definition for attribute [%s] with typename=[%s]"%(key, attr.typename))
                        msglist.append("Cannot find type definition for attribute [%s] with typename=[%s]"%(key, attr.typename))
                else:
                    final_status = False
                    logging.error("Key [%s] not defined in this DataNormalizer instance"%key)
                    msglist.append("Key [%s] not defined in this DataNormalizer instance"%key)
        else:
            logging.error("DataNormalizer instance can only normalize a dictionary")
            msglist.append("DataNormalizer instance can only normalize a dictionary")
            final_status = False

        return (final_status, normed_dict, msglist)
    
    # Built-in normalization funcs
    # nfunc(value) : (status, normed-value)
    
    # At some point, might need to have this encode to ascii or utf8
    @classmethod
    def norm_str(cls, value):
        cleaned = str(value).strip()
        return (True, cleaned)
    
    @classmethod
    def norm_int(cls, value):
        cleaned = str(value).strip()
        return (True, int(value))
    
    @classmethod
    def norm_float(cls, value):
        cleaned = str(value).strip()
        try:
            normed = float(cleaned)
            return (True, normed)
        except ValueError, ve:
            return (False, None)
    
    @classmethod
    def norm_datetime(cls, value):
        cleaned = str(value).strip()
        pat = re.compile("\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2} UTC")
        if pat.match(cleaned):
            try:
                normed = datetime.strptime(cleaned, "%Y-%m-%dT%H:%M:%S %Z")
                return (True, normed)
            except ValueError, ve:
                return (False, None)
        else:
            return (False, None)
    
    @classmethod
    def norm_bool(cls, value):
        cleaned = int(value)
        if cleaned == 1:
            return (True, True)
        elif cleaned == 0:
            return (True, False)
        else:
            return (False, None)
        
    @classmethod
    def norm_email(cls, value):
        cleaned = str(value).strip()
        pat = re.compile("[A-Za-z0-9._-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}")
        if pat.match(cleaned):
            return (True, cleaned)
        else:
            return (False, None)
        
    @classmethod
    def norm_str_list(cls, value):
        cleaned = str(value).strip()
        str_list = filter(lambda d: len(d) > 0, reduce(lambda b, c: b + c, map(lambda a: re.split('\s+', a), re.split(',', cleaned))))
        return (True, list(set(str_list)))
        
    # Map typenames to validation functions
    
    @classmethod
    def register_type(cls, typename, normfunc):
        cls.TYPES[typename] = normfunc
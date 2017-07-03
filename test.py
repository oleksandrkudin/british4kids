"""
Should be one function:
    input: object
    return: accumulated statement list collected from parent classes

object, class, bases
     list = each subclass should provide statements relevant only to it = regular method
"""

class Statements ():
    @classmethod
    def accumulate (cls, self):
        visited_classes = set()
        def go_through_classes (cls, self):
            res = []
            if cls.__bases__:
                for i_class in cls.__bases__:
                    #if i_class.__name__ in ['object','Statements']  or i_class.__name__ in visited_classes:
                    if i_class in visited_classes:
                        break
                    visited_classes.add (i_class)
                    tmp_res = go_through_classes (i_class, self)
                    
                    
                    """
                    try:
                        tmp_res = i_class.accumulate (self)
                    except:
                        tmp_res = i_class.get_statements (self) if 'get_statements' in i_class.__dict__ else []
                    """
                    res.extend (tmp_res)
                
                return res + (cls.get_statements (self) if 'get_statements' in cls.__dict__ else [])
            else:
                if 'get_statements' in cls.__dict__ and not (cls in visited_classes):
                    visited_classes.add (cls)
                    res.extend ( cls.get_statements (self) )
                    return res
                else:
                    return []
        return  go_through_classes (cls, self)

def accumulate (cls, self):
        res = []
        if cls.__bases__ and cls.__name__ != 'object' :
            for i_class in cls.__bases__:
                tmp_res = accumulate (i_class,self)
                res.extend (tmp_res)
            return res + (cls.get_statements (self) if 'get_statements' in cls.__dict__ else [])
        else:
            if 'get_statements' in cls.__dict__:
                res.extend ( cls.get_statements (self) )
                return res
            else:
                return []
    

class first (Statements):
    @classmethod
    def print_class_name (cls):
        print ('class name:', cls.__name__)
    def get_statements (self):
        return ['this is first state.']

class mixing_base (Statements):
    def get_statements (self):
        return ['this is base mixing class.']

class mixing (mixing_base):
    def get_statements (self):
        return ['this is mixing class.']

class second (first):
    def get_statements (self):
        return ['this is second state.']
class third (mixing, second):
    pass
"""
    def get_statements (self):
        return ['this is third state.']"""
class fourth (third,first):
    def get_statements (self):
        return ['this is fourth state.']


a = fourth()
first.print_class_name()
print (a.__class__.__bases__)

print (a.accumulate(a))
print ('\n')
print (accumulate(a.__class__, a))

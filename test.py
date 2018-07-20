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
    @classmethod
    def aggregate (cls, self):
        visited_classes = set()
        # add firstly values from current class
        res = []
        if 'get_statements' in cls.__dict__:
            res.append(cls.get_statements (self))
        def go_through_classes (cls, self):
            res = []
            if cls.__bases__:
                # add values from parrent classes (bases)
                for i_class in cls.__bases__:
                    if i_class in visited_classes:
                        break
                    visited_classes.add (i_class)
                    tmp_res = go_through_classes (i_class, self)
                    res.extend (tmp_res)
                
                return res
            else:
                if 'get_statements' in cls.__dict__ and not (cls in visited_classes):
                    visited_classes.add (cls)
                    res.append ( cls.get_statements (self) )
                    return res
                else:
                    return []
        res.append(go_through_classes (cls, self))
        return  res

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


#
#Check if __attr is inheritant
#
class A():
    __attr = 3
    def __str__(self):
        return str(self.__attr)

class B(A):
    __attr = 5


class MyInt():
    def __init__(self, value):
        self.__value = value
        #self.value = value
    def __add__(self, value):
        return MyInt(self.__value + value)
    def __radd__(self, value):
        return self.__add__(value)
    def __iadd__(self, value):
        return self.__add__(value)  
    def __str__(self):
        return str(self.__value)
    @property
    def value(self):
        print('value = %d' % self.__value)
        return self.__value
    @value.setter
    def value(self, value):
        self.__value = value
    def __getattr__(self, attr):
        print('%s.%s invoked.' % (self.__class__.__name__, attr))
        #return self.__dict__[attr]
    def __setattr__(self, attr, value):
        print('%s.%s = %s invoked.' % (self.__class__.__name__, attr, value))
        #self.__dict__[attr] = value
        #setattr(self, attr, value)
        object.__setattr__(self, attr, value)

def decorator(func):
    print('decorator is invoked!')
    def wrapper (*argv):
        print('wrapper is invoked!')
        func (*argv)
    return wrapper

@decorator
def func():
    print ('func is invoked!')

#func = decorator(func)

def get_value2():
        return 1
class TestProperty():
    #@staticmethod
    def get_value(self):
        return 1

    value = property(fget=get_value)

if __name__ == '__main__':

    a = fourth()
    first.print_class_name()
    print (a.__class__.__bases__)

    print (a.accumulate(a))
    print ('\n')
    print (accumulate(a.__class__, a))
    print ('\n')

    print (a.aggregate(a))

    my_int = MyInt(5)
    my_int = my_int + 10
    print(my_int + my_int)
    print(my_int.value)
    my_int.value = 45
    print(my_int.value)
    print('type of my_int = MyInt():', type(my_int))
    print('type of MyInt class:', type(MyInt))
    print('Class of MyInt class is', MyInt.__class__.__name__)
    my_int.x
    my_int.y
    print(dir(MyInt.value))

    func()
    func()

    my_b = B()
    my_a = A()
    #print(dir(A))
    print('A', A._A__attr)
    print('my_a', my_a)
    print('my_b', my_b)

    print(TestProperty.value)

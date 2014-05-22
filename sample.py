class X(object):
    def x_f1(self):
        y1 = 10
        print y1

def somefunc():
    x = X()
    x.x_f1()

def somefunc_referer():
    somefunc()

class Y(object):
    # def use_X(self):
    #     x = X()
    #     x.x_f1()
    #     self.getX().x_f2()

    # def use_global(self):
    #     somefunc()

    def getX_y(self):
        x = X()
        return x

def somethingelse():
    pass

def fn_using_y_getX():
    y = Y()
    y.getX_y()
    #print yy
    somethingelse()

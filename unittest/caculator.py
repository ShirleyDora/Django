# 实现简单的计算器：+-*/ byShirley-2023-05-05
class Calculator():
    def __init__(self,a,b):
        self.a = int(a)
        self.b = int(b)
    def add(self):
        return self.a+self.b
    def sub(self):
        return self.a-self.b
    def mul(self):
        return self.a*self.b
    def div(self):
        return self.a/self.b
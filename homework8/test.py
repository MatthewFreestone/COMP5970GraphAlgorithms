


class A:
    var = 0
    def __init__(self, x):
        print("hello")

x = A(1)
y = A(2)
print(x.var, y.var)
print(x.__class__.var)
print(A.var)



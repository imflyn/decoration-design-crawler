def foo(x, y):
    print(x, y)


alist = [1, 2]
adict = {'x': 1, 'y': 2}
foo(*alist)  # 1, 2
foo(**adict)  # 1, 2

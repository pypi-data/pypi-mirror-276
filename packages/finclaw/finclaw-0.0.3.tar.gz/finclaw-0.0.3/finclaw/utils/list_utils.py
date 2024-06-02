
def select(iterable, predicate):
    for i in iterable:
        if predicate(i):
            yield i
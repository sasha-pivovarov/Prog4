class SingletonDecorator:
    """
    Is only intended for use as a decorator.
    """

    def __init__(self, decorated):
        self._decorated = decorated

    def create_object(self):
        try:
            return self._instance
        except AttributeError:
            self._instance = self._decorated()
            return self._instance

    def __call__(self):
        raise TypeError('this object is accessed through the create_object method`.')

    def __instancecheck__(self, inst):
        return isinstance(inst, self._decorated)


@SingletonDecorator
class UniqObject:
    def __init__(self):
        pass

uo1 = UniqObject.create_object()
uo2 = UniqObject.create_object()

print(uo1)
print(uo2)
print(uo1 == uo2)
print(uo1 is uo2)
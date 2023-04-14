import jsonpickle


class SubObject:
    def __init__(self, sub_name, sub_age):
        self.sub_name = sub_name
        self.sub_age = sub_age


class TestClass:

    def __init__(self, name, age, sub_object):
        self.name = name
        self.age = age
        self.sub_object = sub_object


john_junior = SubObject("John jr.", 2)

john = TestClass("John", 21, john_junior)

file_name = 'JohnWithSon' + '.json'

john_string = jsonpickle.encode(john)

with open(file_name, 'w') as fp:
    fp.write(john_string)

john_from_file = open(file_name).read()

test_class_2 = jsonpickle.decode(john_from_file)

print(test_class_2.name)
print(test_class_2.age)
print(test_class_2.sub_object.sub_name)
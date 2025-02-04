import ast
test = '["ff59a8e0-161c-4a0d-b320-d8ff3ee93332", "006b2fc6-1a70-4ed2-b673-80ac7b4e0045", "a969fd1b-af53-446f-af8c-0c36649ec877", "7afb34f4-b896-4af0-bec1-8dddb37ce3d3", "4a5f2125-54c7-43e0-bc43-d1db551c80b2"]'

test_list_of_strings = ast.literal_eval(test)
print(test_list_of_strings)
print(type(test_list_of_strings))
for item in test_list_of_strings:
    print(item)
    print(type(item))

test2 = '["b1f40927-b280-4c04-9f53-10443b901d30", "a3c6e76f-a443-47f6-b2d4-c72de6c11969", "84b4ef69-ed26-440a-8250-4fddc58ef50b", "f7fbea07-31ac-4eb1-b252-7fe76314ffa2", "185a036c-da89-4add-b257-86ae87e79209"]'
test2_list_of_strings = ast.literal_eval(test2)
print(test2_list_of_strings)
print(type(test2_list_of_strings))

'["b1f40927-b280-4c04-9f53-10443b901d30", "a3c6e76f-a443-47f6-b2d4-c72de6c11969", "84b4ef69-ed26-440a-8250-4fddc58ef50b", "f7fbea07-31ac-4eb1-b252-7fe76314ffa2", "185a036c-da89-4add-b257-86ae87e79209"]'
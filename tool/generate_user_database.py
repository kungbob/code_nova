import numpy, random
# The database is like
#database = {'condition': 3, 'loop': 4, 'array': 1, 'function': 1, 'class': 6,
#           'module': 5, 'basicIO': 8, '01': True, '02': True, '03': True}

# Database is randomly generated
# For Condition... terms, 0-10 is used to represent ability
# For exercise no (1, 2, 3)....., 0 or 1 is used, 0 means not finished, 1
# means finished
def generate_user_database():
    # randomly generate 100 users
    number_of_user = 100
    database = dict()
    # Ability list of user
    value_list = ['condition', 'loop', 'array', 'function', 'class', 'module',
                'basicIO', '1', '2', '3']
    for i in range(number_of_user):
        # Generate user name
        new_username = "test_user_" + str(i)
        new_user_dict = dict()
        for item in value_list:
            if not item.isdigit():
                temp = {item: random.randint(0, 10)}
                new_user_dict[item] = random.randint(0,10)
            else:
                new_user_dict[item] = random.random() < 0.5
        database[new_username] = new_user_dict
    return database

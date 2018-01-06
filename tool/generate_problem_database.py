import numpy, random

def generate_problem_database():
    # randomly generate 100 problem
    number_of_problem = 100
    database = dict()
    # Problem
    value_list = ['condition', 'loop', 'array', 'function', 'class', 'module',
                'basicIO']
    for i in range(number_of_problem):
        # Generate Problem
        new_problem = str(i)
        new_problem_dict = dict()
        for item in value_list:
            temp = {item: random.randint(0, 10)}
            new_problem_dict[item] = random.randint(0,10)
        database[new_problem] = new_problem_dict
    return database

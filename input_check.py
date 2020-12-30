import sqlite3
from collections import Counter

# Connecting to database
db = sqlite3.connect('movies.db', check_same_thread=False)
cursor = db.cursor()


def input_check(person, person2):

    # Getting numerical id's of given names
    cursor.execute("""SELECT name, id, birth FROM people WHERE ? = LOWER(people.name) AND people.birth IS NOT NULL
                      OR ? = LOWER(people.name) AND people.birth IS NOT NULL""", (person, person2,))

    person_id = cursor.fetchall()

    # Make data list of tuples a list of lists
    person_id = [list(elem) for elem in person_id]
    print("person_id", person_id)

    length = len(person_id)
    print("length: ", length)

    # Check there are at least two names returned from Database
    if length < 2:
        if length == 0:
            solution = [6]
            return solution
        else:
            if person == person_id[0][0].lower():
                if person2 == person_id[0][0].lower():
                    solution = [8, person]
                    return solution
                else:
                    solution = [5, person2]
                    print("1")
                    return solution
            else:
                solution = [5, person]
                print("2")
                return solution

    # Check that there are at least two different names returned
    diff_count = 0
    for i in range(length):
        if person_id[0] != person_id[i]:
            diff_count += 1
    if diff_count == 0:
        if person == person_id[0][0].lower():
            solution = [5, person2]
            print("3")
            return solution
        else:
            solution = [5, person]
            print("4")
            return solution

    # Check in case one input returned nothing but the other returned more than one
    for name in [person, person2]:
        name_check = any(name.lower() in sublist[0].lower() for sublist in person_id)
        if not name_check:
            solution = [5, name]
            print("5")
            return solution

    # Check in case an input returned more than one person from database
    if length > 2:
        solution = [7, person_id]
        return solution

    return person_id


# Function for filtering data where there is more than one name returned for an input
def over_two_names(person_id):

    # Defining temporary list variable for use throughout program
    temp_list = []

    person_count = Counter(elem[0] for elem in person_id)
    print(person_count)

    # If more than 2 id's returned check which same name actor was wanted
    # First append names of actors to be checked to list
    question_names = []
    for key, value in person_count.items():
        if value > 1:
            for item in person_id:
                if key in item:
                    question_names.append(item)

    # Remove names of actors in question names from person_id (keeps inputs where only one actor was returned)
    for item in person_id:
        if item not in question_names:
            temp_list.append(item)
    person_id.clear()
    person_id[:] = temp_list
    temp_list.clear()

    names = [person_id, question_names]
    return names





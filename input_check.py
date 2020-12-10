import sqlite3
from collections import Counter

# Connecting to database
db = sqlite3.connect('movies.db')
cursor = db.cursor()


def input_check(person, person2):

    # Getting numerical id's of given names
    cursor.execute("""SELECT name, id, birth FROM people WHERE ? = LOWER(people.name) AND people.birth IS NOT NULL
                      OR ? = LOWER(people.name) AND people.birth IS NOT NULL""", (person, person2,))

    person_id = cursor.fetchall()

    # Make data list of tuples a list of lists
    person_id = [list(elem) for elem in person_id]
    print(person_id)

    length = len(person_id)

    # Check there are at least two names returned from Database
    if length < 2:
        if length == 0:
            print("Both names are invalid please try again")
        else:
            if person == person_id[0][0].lower():
                print(f"{person2} is not a valid name, please try again")
            else:
                print(f"{person} is not a valid name, please try again")
        exit()

    # Check that there are at least two different names returned
    diff_count = 0
    for i in range(length):
        if person_id[0] != person_id[i]:
            diff_count += 1
    if diff_count == 0:
        if person == person_id[0][0].lower():
            print(f"{person2} is not a valid name, please try again")
        else:
            print(f"{person} is not a valid name, please try again")
        exit()

    # Defining temporary list variable for use throughout program
    temp_list = []

    # Check in case an input returned more than one person from database
    if length > 2:
        person_count = Counter(elem[0] for elem in person_id)

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

        # Add names that are the same to temporary list (needed in case both inputs return multiple actors)
        for i in question_names:
            for j in question_names:
                if i[0] == j[0]:
                    temp_list.append(j)
            for k in question_names:
                if k[0] == temp_list[0][0]:
                    question_names.remove(k)

            # Use temporary list to ask user to confirm which person they meant
            print(f"Which {temp_list[0][0]} did you mean?")
            for counter, person in enumerate(temp_list):
                print(str(counter + 1) + ".", person[0], person[2])
            confirmed_person = 0
            while 1 > confirmed_person or confirmed_person > len(temp_list):
                confirmed_person = int(input("Enter number starting at 1 to select from list: "))
            confirmed_person -= 1
            person_id.append(temp_list[confirmed_person])
            temp_list.clear()

    return person_id

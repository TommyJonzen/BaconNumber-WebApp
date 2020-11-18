import sqlite3
from collections import Counter

# Connecting to database
db = sqlite3.connect('movies.db')
cursor = db.cursor()

# Getting names for Bacon Number generator
person = input("Enter a movie star: ")
person2 = input("Enter another movie star: ")

# Getting numerical id's of given names
cursor.execute("""SELECT name, id, birth FROM people WHERE ? = people.name OR ? = 
               people.name AND people.birth IS NOT NULL""", (person, person2,))

person_id = cursor.fetchall()
person_id = list(person_id)

# Making sure names only returned 1 id each
if len(person_id) > 2:
    person_count = Counter(elem[0] for elem in person_id)

    # If more than 2 id's returned check which same name actor was wanted
    question_names = []
    for key, value in person_count.items():
        print(key, value)
        if value > 1:
            for item in person_id:
                if key in item:
                    question_names.append(item)

    # Clear person_id for refill with only two correct people
    person_id.clear()

    # Create temporary list for names that are the same
    temp_list = []
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
print(person_id)


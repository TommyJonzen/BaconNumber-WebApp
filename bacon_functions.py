import sqlite3
from person import Star

# Connecting to database
db = sqlite3.connect('movies.db')
cursor = db.cursor()


# Duplicate person remover
def duplicate_remove(co_star_list, person_id):
    temp_list = []
    for i in co_star_list:
        counter = 0
        for j in temp_list:
            if i[0] == j[0]:
                counter += 1
        if counter == 0 and i[0] != person_id[1][1]:
            temp_list.append(i)

    co_star_list.clear()
    co_star_list[:] = temp_list
    temp_list.clear()
    return co_star_list


# Creates list of one inputs co_stars so can search for all their costars rather than just one ID
def find_list(person_id):
    # SQL query pulls all people that have starred in a film with one of the inputs
    cursor.execute("""SELECT person_id, name, movies.title FROM movies JOIN stars JOIN people 
                      ON movies.id = stars.movie_id AND stars.person_id = people.id
                      WHERE movies.id IN (SELECT movies.id FROM movies JOIN stars ON movies.id = stars.movie_id
                      WHERE stars.person_id =?)""", (person_id[1][1],))

    print(person_id[1][1])

    # Variable holds all co-stars returned by this query
    costars_list = cursor.fetchall()
    costars_list = [list(elem) for elem in costars_list]

    # Removing duplicate people in stars_person_id
    costars_list = duplicate_remove(costars_list, person_id)

    for row in costars_list:
        if person_id[0][1] == row[0]:
            print(f"There are no steps between {person_id[0][0]} and {person_id[1][0]}")
            print(f'They starred in "{row[2]}" together')
            exit()

    costars_list.insert(0, person_id[1])

    return costars_list


# Recursive search through objects for correct route between two stars
def solved_search(star_id, solved_list, star_dictionary):
    print(star_dictionary[star_id].name)
    if len(star_dictionary[star_id].parents) >= 1:
        star_parent = star_dictionary[star_id].parents[-1]
        for i in star_dictionary[star_parent].co_stars:
            if i[0] == star_id:
                solved_list.append(i)
                solved_list = solved_search(star_parent, solved_list, star_dictionary)
    else:
        solved_list.append([star_dictionary[star_id].id, star_dictionary[star_id].name])

    return solved_list


def bacon_query(find_id, star_object, star_dictionary, check_list, to_be_checked):

    cursor.execute("""SELECT person_id, name, movies.title FROM movies JOIN stars JOIN people 
                      ON movies.id = stars.movie_id AND stars.person_id = people.id
                      WHERE movies.id IN (SELECT movies.id FROM movies JOIN stars ON movies.id = stars.movie_id
                      WHERE stars.person_id =?)""", (star_object.id,))

    query_return = cursor.fetchall()
    query_return = [list(elem) for elem in query_return]

    check_list.append(star_object.id)

    # Remove duplicates
    tmp_list = []
    for m in query_return:
        bacon_counter = 0
        for n in tmp_list:
            if m[0] == n[0]:
                bacon_counter += 1
        if bacon_counter == 0 and m[0] != star_object.id and m[0] not in check_list and m[0] not in to_be_checked:
            tmp_list.append(m)
    query_return.clear()
    query_return[:] = tmp_list
    tmp_list.clear()

    # Assigning list of Co-Stars to each Star
    star_object.co_stars = query_return

    # Creating parents list for each Star in star_object.co_stars
    parents = []
    for parent in star_object.parents:
        parents.append(parent)
    parents.append(star_object.id)

    # Making each star in star_object.co_stars its own object
    for i in star_object.co_stars:
        star_dictionary[i[0]] = Star(i[1], i[0], parents)

    # Check for find_id, if found create solution path and return
    for k in star_object.co_stars:
        if k[0] == find_id[0]:
            solved_list = []
            print("Solved ID Found")
            solved_list = solved_search(k[0], solved_list, star_dictionary)
            return solved_list

    for p in star_object.co_stars:
        if p[0] in find_id:
            solved_list = []
            print("Solved ID Found")
            solved_list = solved_search(p[0], solved_list, star_dictionary)
            return solved_list

    # Create ordered list of IDs to check from lists of co_stars:
    for n in star_object.co_stars:
        to_be_checked.append(n[0])

    for o in to_be_checked:
        if o not in check_list:
            print("Calling bacon query on", star_dictionary[o].name)
            solved_list = bacon_query(find_id, star_dictionary[o], star_dictionary, check_list, to_be_checked)
            return solved_list

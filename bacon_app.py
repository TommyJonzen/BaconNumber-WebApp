import time
from person import Star
import bacon_functions
import input_check
import sys


def main_query(star1, star2, override=0):
    sys.setrecursionlimit(1500)

    if override == 0:
        # Getting names for Bacon Number generator
        person = star1.strip()
        person = person.lower()
        person2 = star2.strip()
        person2 = person2.lower()

        # Checking names are valid & that no more than one name is returned from database for each input
        checker = input_check.input_check(person, person2)
        if isinstance(checker[0], int):
            solution = checker
            return solution
        else:
            person_id = checker
    else:
        person_id = [star1, star2]

    # Getting list of one inputs co_stars to search for. More efficient than search for just their ID
    co_stars_list, person_id = bacon_functions.find_list(person_id)

    # Dealing with error and the two stars already being costars
    if co_stars_list == 1:
        solution = [1, f"{person_id} can't be linked to any other actor as they have no co stars."]
        return solution
    if co_stars_list == 2:
        solution = [2, person_id]
        return solution

    # find co_stars_list but with just the IDs
    co_stars_id_list = []
    for item in co_stars_list:
        co_stars_id_list.append(item[0])

    # Creating star object to record details of one of the given film stars
    star_objects_dict = {}
    star_objects_dict[person_id[0][1]] = Star(person_id[0][0], person_id[0][1], [])
    checked_list = []
    to_check = []

    solved_list = bacon_functions.bacon_query(co_stars_id_list, star_objects_dict[person_id[0][1]],
                                              star_objects_dict, checked_list, to_check)

    if solved_list == 3:
        solution = [3, "No Link Could Be Found"]
        return solution

    # Insert the film star being looked for into solved list
    # Query so far will have only found one of their co_stars
    for i in co_stars_list:
        if i[0] == solved_list[0][0]:
            solved_list.insert(0, [person_id[1][1], person_id[1][0], i[2]])

    # Calculate and print steps between 2 film stars
    solution = [0]
    steps = len(solved_list) - 2
    if steps == 1:
        solution.append(f"There is {steps} step between {person_id[1][0]} and {person_id[0][0]}:")
    else:
        solution.append(f"There are {steps} steps between {person_id[1][0]} and {person_id[0][0]}.")

    # Print route solution
    for j in range(len(solved_list) - 1):
        if j == 0:
            solution.append(f"{solved_list[j][1]} starred in '{solved_list[j][2]}' with {solved_list[j + 1][1]}")
        else:
            solution.append(f"who starred in '{solved_list[j][2]}' with {solved_list[j + 1][1]}")

    return solution


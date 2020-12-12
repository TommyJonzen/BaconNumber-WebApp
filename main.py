import time
from person import Star
import bacon_functions
import input_check
import sys

#seth allen and kevin bacon??
sys.setrecursionlimit(1500)

# Getting names for Bacon Number generator
person = input("Enter a movie star: ").strip()
person = person.lower()
person2 = input("Enter another movie star: ").strip()
person2 = person2.lower()

# Checking names are valid & that no more than one name is returned from database for each input
person_id = input_check.input_check(person, person2)
print(person_id)
start_time = time.time()

# Getting list of one inputs co_stars to search for. More efficient than search for just their ID
co_stars_list, person_id = bacon_functions.find_list(person_id)

# co_stars_list but with just the IDs
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
print(solved_list)

# Insert the film star being looked for into solved list
# Query so far will have only found one of their co_stars
for i in co_stars_list:
    if i[0] == solved_list[0][0]:
        solved_list.insert(0, [person_id[1][1], person_id[1][0], i[2]])

# Calculate and print steps between 2 film stars
steps = len(solved_list) - 2
if steps == 1:
    print(f"There is {steps} step between {person_id[1][0]} and {person_id[0][0]}")
else:
    print(f"There are {steps} steps between {person_id[1][0]} and {person_id[0][0]}")

# Print route solution
for j in range(len(solved_list) - 1):
    if j == 0:
        print(f"{solved_list[j][1]} starred in {solved_list[j][2]} with {solved_list[j + 1][1]}")
    else:
        print(f"who starred in {solved_list[j][2]} with {solved_list[j + 1][1]}")

print(f"This program took", {time.time() - start_time}, "to run")
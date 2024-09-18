#  set = collection which is unordered, unindexed. no duplicate values

# utensils = {'fork', 'spoon', 'knife'}

# for x in utensils:
#     print(x)
# output:
# fork
# spoon
# knife

# utensils = {'fork', 'spoon', 'knife','knife','knife'}

# for x in utensils:
#     print(x)
# output: 
# fork
# spoon
# knife

# utensils = {'fork', 'spoon', 'knife'}

# utensils.add('napkin')
# utensils.remove('fork')
# for x in utensils:
#     print(x)

# output:
# spoon
# napkin
# knife

# to remove all elements within my set:
# utensils = {'fork', 'spoon', 'knife'}

# utensils.add('napkin')
# utensils.remove('fork')
# utensils.clear()
# for x in utensils:
#     print(x)

# utensils = {'fork', 'spoon', 'knife'}
# dishes = {'bowl','plate','cup'}

# utensils.add('napkin')
# utensils.remove('fork')
# utensils.clear()
# utensils.update(dishes)

# for x in utensils:
#     print(x)
# this will move all the elements from 'dishes' to the utensils set.


# utensils = {'fork', 'spoon', 'knife'}
# dishes = {'bowl','plate','cup'}

# dinner_table = utensils.union(dishes)

# for x in dinner_table:
#     print(x)
# now ill get elemts from both the sets

# utensils = {'fork', 'spoon', 'knife'}
# dishes = {'bowl','plate','cup'}

# print(utensils.difference(dishes))
# will print every thing the set 'utensils' has  that the set 'dishes' dosnt.


utensils = {'fork', 'spoon', 'knife'}
dishes = {'bowl','plate','cup','knife'}

print(utensils.intersection(dishes))
# this will print any elements both sets have in common

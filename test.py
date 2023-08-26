pipe_scroll_array = [0, 0, 0]
for i, pos in enumerate(pipe_scroll_array):
    pos += 300 - 78 + 100 + i * 100
    print(i, pos)

print(pipe_scroll_array)

fruits = ['apple', 'banana', 'cherry']
for i, fruit in enumerate(fruits):
    fruit = fruit + ' juice'
print(fruits)

my_list = [1, 2, 3, 4, 5]

for index, value in enumerate(my_list):
    my_list[index] = value * 2

print(my_list)
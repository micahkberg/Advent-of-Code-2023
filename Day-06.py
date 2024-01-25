from numpy import sqrt, floor, ceil

def load(day):
    contents = open(f"./inputs/{day}.txt", "r").read().strip().split("\n")
    return contents


contents = load("06")
times = contents[0].split()[1:]
distances = contents[1].split()[1:]
winning_product = 1
for i in range(len(times)):
    time = int(times[i])
    min_distance = int(distances[i])
    winning_methods = 0
    for t in range(time):
        if (time-t)*t > min_distance:
            winning_methods += 1

    winning_product *= winning_methods

print("part 1")
print(winning_product)

unkerned_time = int("".join(times))
unkerned_distance = int("".join(distances))

# test
# unkerned_time = 71530
# unkerned_distance = 940200

test_time = unkerned_time//2
print("time")
print(unkerned_time)
print("distance")
print(unkerned_distance)

a = -1
b = unkerned_time
c = -1*unkerned_distance

int_1 = (-b+sqrt(b**2-4*a*c))/(2*a)
int_2 = (-b-sqrt(b**2-4*a*c))/(2*a)
print(int_1)
print(int_2)
print(floor(int_2)-ceil(int_1)+1)


#try 1 : 28545090 high
#try 2 : 12384704 low
#try 3 : 28545088
def test_func():

    """# 1. пузырьком (bubble_sort)
a = [1, 6, 3, -5, 111, 9]
n = len(a)
for i in range(n - 1):
    for j in range(n - 1 - i):
        if a[j] > a[j + 1]:
            a[j], a[j + 1] = a[j + 1], a[j]
a


# 2. шейкерная сортировка (cocktail shaker sort)
a = [1, 6, 3, -5, 111, 9]
left = 0
right = len(a) - 1
flag = right
while left < right:
    for i in range(left, right):
        if a[i] > a[i + 1]:
            a[i], a[i + 1] = a[i + 1], a[i]
            flag = i
    right = flag
    for i in range(right, left, -1):
        if a[i] < a[i - 1]:
            a[i], a[i - 1] = a[i - 1], a[i]
            flag = i
    left = flag
a


# 3. сортировка расческой (comb sort)
a = [1, 6, 3, -5, 111, 9]
step = int(len(a) / 1.247)
swap = 1
while step > 1 or swap > 0:
    swap = 0
    i = 0
    while i + step < len(a):
        if a[i] > a[i + step]:
            a[i], a[i + step] = a[i + step], a[i]
            swap += 1
        i = i + 1
    if step > 1:
        step = int(step / 1.247)
a


# 4. выбором (selection sort)
a = [1, 6, 3, -5, 9, 11]
n = len(a)
for i in range(n - 1):
    min_index = i
    for j in range(i + 1, n):
        if a[j] < a[min_index]:
            min_index = j
    if i != min_index:
        a[min_index], a[i] = a[i], a[min_index]
a


# 5. вставсками (insertion sort)
a = [1, 6, 3, -5, 9, 11]
n = len(a)
for i in range(1, n):
    elem_now = a[i]
    j = i
    while j > 0 and a[j - 1] > elem_now:
        a[j] = a[j - 1]
        j -= 1
    a[j] = elem_now
a


# 6. быстрая сортирловка (quick sort)
a = [1, 6, 3, -5, 111, 9]
def quick_sort(list_1):
    if len(list_1) <= 1:
        return list_1
    elem = list_1[0]
    left = [i for i in list_1 if i < elem]
    center = [i for i in list_1 if i == elem]
    right = [i for i in list_1 if i > elem]

    return quick_sort(left) + center + quick_sort(right)

quick_sort(a)



# 7. сортировка Шелла (shell sort)
a = [1, 6, 3, -5, 111, 9]
half = len(a) // 2
while half != 0:
    for i in range(half, len(a)):
        elem_now = a[i]
        j = i
        while j >= half and a[j - half] > elem_now:
            a[j] = a[j - half]
            j = j - half
        a[j] = elem_now
    half = half // 2
print(a)


# 8. сортировка слиянием (merge sort)
def merge_two_list(list_1, list_2):
    answer = []
    i, j = 0, 0
    while i < len(list_1) and j < len(list_2):
        if list_1[i] < list_2[j]:
            answer.append(list_1[i])
            i += 1
        else:
            answer.append(list_2[j])
            j += 1
    if i < len(list_1):
        answer += list_1[i:]
    if j < len(list_2):
        answer += list_2[j:]

    return answer


def merge_sort(list_1):
    if len(list_1) == 1:
        return list_1
    middle = len(list_1) // 2
    left = merge_sort(list_1[:middle])
    right = merge_sort(list_1[middle:])
    return merge_two_list(left, right)

a = [1, 6, 3, -5, 111, 9]
merge_sort(a)


# пример декоратора
import time

def decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        res = func(*args, **kwargs)
        end_time = time.time()
        print(func.__name__, end_time - start_time)
        return res
    return wrapper

@decorator
def sort_1():
    with open('rrr.txt', 'r') as f:
        s = f.readlines()

    d = {}
    for i in s:
        elem = i.rstrip().split()
        d[int(elem[1])] = elem[0]

    a = list(d.keys())
    n = len(a)
    for i in range(n - 1):
        min_index = i
        for j in range(i + 1, n):
            if a[j] < a[min_index]:
                min_index = j
        if i != min_index:
            a[min_index], a[i] = a[i], a[min_index]

    new_d = {i: d[i] for i in a}
    return new_d

@decorator
def sort_2():
    with open('rrr.txt', 'r') as f:
        s = f.readlines()

    d = {}
    for i in s:
        elem = i.rstrip().split()
        d[int(elem[1])] = elem[0]

    a = list(d.keys())
    n = len(a)
    for i in range(1, n):
        elem_now = a[i]
        j = i
        while j > 0 and a[j - 1] > elem_now:
            a[j] = a[j - 1]
            j -= 1
        a[j] = elem_now

    new_d = {i: d[i] for i in a}
    return new_d


sort_1()
sort_2()"""
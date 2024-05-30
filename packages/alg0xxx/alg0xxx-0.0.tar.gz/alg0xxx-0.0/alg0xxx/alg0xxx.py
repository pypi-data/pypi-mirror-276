


def all():
    '''
def bubble_sort(a):
    n = len(a)
    for i in range(n):
        for j in range(n-1-i):
            if a[j] > a[j+1]:
                a[j], a[j+1] = a[j+1], a[j]
    return a

print(f"Исходный список:{a}\nОтсортированный список:{bubble_sort(a)}")

a = [1, 6, 3, -5, 111, 9]

def cocktail_sort(a):
    left = 0
    right = len(a)-1
    swapped = True
    while swapped:
        swapped = False
        for i in range(left,right):
            if a[i]> a[i+1]:
                a[i], a[i+1] = a[i+1], a[i]
                swapped = True
        if not swapped:
            break
        swapped = False
        right = right - 1
        for i in range(right-1,left-1,-1):
            if a[i]> a[i+1]:
                a[i], a[i+1] = a[i+1], a[i]
                swapped = True
            left = left + 1
    return a

print(f"Исходный список:{a}\nОтсортированный список:{cocktail_sort(a)}")

a = [1, 6, 3, -5, 111, 9]

def comb_sort(a):
    step = int(len(a) / 1.3)
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
            step = int(step / 1.3)
    return a
print(f"Исходный список:{a}\nОтсортированный список:{comb_sort(a)}")

a = [1, 6, 3, -5, 111, 9]

def selection_sort(a):
    n = len(a)
    for i in range(n):
        min_idx = i
        for j in range(i+1, n):
            if a[j] < a[min_idx]:
                min_idx = j
        a[i], a[min_idx] = a[min_idx], a[i]
    return a
print(f"Исходный список:{a}\nОтсортированный список:{selection_sort(a)}")

a = [1, 6, 3, -5, 111, 9]

def insertion_sort(a):
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j+1] = a[j]
            j -= 1
            a[j+1] = key
    return a

print(f"Исходный список:{a}\nОтсортированный список:{insertion_sort(a)}")

a = [1, 6, 3, -5, 111, 9]


def quick_sort(list_1):
    if len(list_1) <= 1:
        return list_1
    elem = list_1[0]
    left = [i for i in list_1 if i < elem]
    center = [i for i in list_1 if i == elem]
    right = [i for i in list_1 if i > elem]

    return quick_sort(left) + center + quick_sort(right)

def shell_sort(arr):
    gap = len(arr) // 2
    while gap > 0:
        for i in range(gap, len(arr)):
            temp = arr[i]
            j = i
            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = temp
        gap //= 2
    return arr

a = [1, 6, 3, -5, 111, 9]
print(f"Исходный список: {a}\nОтсортированный список: {shell_sort(a)}")

def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left_half = arr[:mid]
    right_half = arr[mid:]

    left_half = merge_sort(left_half)
    right_half = merge_sort(right_half)

    return merge(left_half, right_half)

def merge(left_half, right_half):
    result = []
    i = 0
    j = 0

    while i < len(left_half) and j < len(right_half):
        if left_half[i] <= right_half[j]:
            result.append(left_half[i])
            i += 1
        else:
            result.append(right_half[j])
            j += 1

    result += left_half[i:]
    result += right_half[j:]

    return result

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
sort_2()
'''
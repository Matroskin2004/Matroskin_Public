list = []
n = None
import random

def quick_sort(nums):
    if len(nums) <= 1:
        return nums
    else:
        q = random.choice(nums)
    l_nums = [n for n in nums if n < q]

    e_nums = [q] * nums.count(q)
    b_nums = [n for n in nums if n > q]
    return quick_sort(l_nums) + e_nums + quick_sort(b_nums)

def binary_search(array, element, left, right):

    if left > right:
        return left

    middle = (right + left) // 2
    if array[middle] == element:
        return middle
    elif element < array[middle]:
        return binary_search(array, element, left, middle - 1)
    else:
        return binary_search(array, element, middle + 1, right)

for element in input('Введите последовательность чисел через пробел \n').split():
    try:
        list.append(float(element))
    except ValueError:
        print (element, 'не является числом')

if len(list) > 1:
    list = quick_sort(list)
    print('Последовательность отсортирована по возрастанию', list)
else:
    print('Последовательность пустая или содержит только один элемент')
    exit()

try:
    n = (input('Введите число для поиска: '))
    n = float(n)
except ValueError:
    print (n, ' не является числом')

if type(n) != float:
    exit()
elif n <= list[0] or n > list[len(list) - 1]:
    print ('Заданное число равно минимальному элементу последовательности или меньше его, либо больше максимального элемента последоватеьности')
else:
    print('Номер позиции элемента, который меньше введенного числа, а следующий за ним больше или равен этому числу:', binary_search(list, n, 0, len(list)))
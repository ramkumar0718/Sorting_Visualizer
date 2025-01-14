from app import draw_list

# Bubble Sort
def bubble_sort(draw_info, ascending=True):
	num_list = draw_info.num_list

	for i in range(len(num_list) - 1):
		for j in range(len(num_list) - 1 - i):
			num1 = num_list[j]
			num2 = num_list[j + 1]

			if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
				num_list[j], num_list[j + 1] = num_list[j + 1], num_list[j]
				draw_list(draw_info, {j: draw_info.GREEN, j + 1: draw_info.RED}, True)
				yield True

	return num_list

# Insertion Sort
def insertion_sort(draw_info, ascending=True):
    num_list = draw_info.num_list

    for i in range(1, len(num_list)):
        temp = num_list[i]
        j = i - 1

        while j >= 0 and ((num_list[j] > temp and ascending) or (num_list[j] < temp and not ascending)):
            num_list[j + 1] = num_list[j]
            draw_list(draw_info, {j: draw_info.GREEN, j + 1: draw_info.RED}, True)
            yield True
            j -= 1

        num_list[j + 1] = temp
        draw_list(draw_info, {j + 1: draw_info.GREEN}, True)
        yield True

    return num_list

# Selection Sort
def selection_sort(draw_info, ascending=True):
    num_list = draw_info.num_list

    for i in range(len(num_list) - 1):
        min_ele = i

        for j in range(i + 1, len(num_list)):
            if (num_list[j] < num_list[min_ele] and ascending) or (num_list[j] > num_list[min_ele] and not ascending):
                min_ele = j

        if min_ele != i:
            num_list[i], num_list[min_ele] = num_list[min_ele], num_list[i]
            draw_list(draw_info, {i: draw_info.GREEN, min_ele: draw_info.RED}, True)
            yield True

    return num_list

# Merge Sort
def merge_sort(draw_info, ascending=True):
    num_list = draw_info.num_list

    def merge(left, right):
        sorted_list = []
        l = r = 0

        while l < len(left) and r < len(right):
            if (left[l] < right[r] and ascending) or (left[l] > right[r] and not ascending):
                draw_list(draw_info, {left[l]: draw_info.GREEN, right[r]: draw_info.RED}, True)
                sorted_list.append(left[l])
                l += 1
            else:
                draw_list(draw_info, {left[l]: draw_info.RED, right[r]: draw_info.GREEN}, True)
                sorted_list.append(right[r])
                r += 1

        while l < len(left):
            sorted_list.append(left[l])
            l += 1

        while r < len(right):
            sorted_list.append(right[r])
            r += 1

        return sorted_list

    def merge_sort_recursive(lst):
        if len(lst) <= 1:
            return lst

        mid = len(lst) // 2
        left_half = lst[:mid]
        right_half = lst[mid:]

        left_half = merge_sort_recursive(left_half)
        right_half = merge_sort_recursive(right_half)

        return merge(left_half, right_half)

    num_list[:] = merge_sort_recursive(num_list)

    draw_list(draw_info, {i: draw_info.GREEN for i in range(len(num_list))}, True)
    yield True

    return num_list

# Quick Sort
def quick_sort(draw_info, ascending=True):
    num_list = draw_info.num_list

    def partition(start, end):
        pivot = num_list[end]
        i = start - 1
        for j in range(start, end):
            if (num_list[j] < pivot and ascending) or (num_list[j] > pivot and not ascending):
                i += 1
                num_list[i], num_list[j] = num_list[j], num_list[i]
                draw_list(draw_info, {i: draw_info.GREEN, j: draw_info.RED}, True)
                yield True
        i += 1
        num_list[i], num_list[end] = num_list[end], num_list[i]
        draw_list(draw_info, {i + 1: draw_info.GREEN, end: draw_info.RED}, True)
        yield True
        return i

    def quick_sort_recursive(start, end):
        if start < end:
            pi = yield from partition(start, end)
            yield from quick_sort_recursive(start, pi - 1)
            yield from quick_sort_recursive(pi + 1, end)

    yield from quick_sort_recursive(0, len(num_list) - 1)

    draw_list(draw_info, {i: draw_info.GREEN for i in range(len(num_list))}, True)
    yield True

    print(num_list == sorted(num_list))
    return num_list

# Heap Sort
def heap_sort(draw_info, ascending=True):
    num_list = draw_info.num_list

    def heapify(n, i):
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2

        if left < n and ((num_list[left] > num_list[largest] and ascending) or (num_list[left] < num_list[largest] and not ascending)):
            largest = left

        if right < n and ((num_list[right] > num_list[largest] and ascending) or (num_list[right] < num_list[largest] and not ascending)):
            largest = right

        if largest != i:
            num_list[i], num_list[largest] = num_list[largest], num_list[i]  # Swap
            draw_list(draw_info, {i: draw_info.GREEN, largest: draw_info.RED}, True)
            yield True

            yield from heapify(n, largest)

    def build_max_heap():
        n = len(num_list)
        for i in range(n // 2 - 1, -1, -1):
            yield from heapify(n, i)

    def sort_heap():
        n = len(num_list)
        yield from build_max_heap()

        for i in range(n - 1, 0, -1):
            num_list[i], num_list[0] = num_list[0], num_list[i]
            draw_list(draw_info, {0: draw_info.GREEN, i: draw_info.RED}, True)
            yield True

            yield from heapify(i, 0)

    yield from sort_heap()
    
    draw_list(draw_info, {i: draw_info.GREEN for i in range(len(num_list))}, True)
    yield True

    return num_list
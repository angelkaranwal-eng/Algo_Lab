"""
Sorting algorithm implementations using generator patterns.
Each yielded operation dictionary carries operational telemetry:
{
    'type': 'compare' | 'swap' | 'overwrite' | 'partition' | 'sorted',
    'indices': [i, j],
    'array': list(current_state),
    'comparisons': count,
    'swaps': count,
    'desc': string description
}
"""

def bubble_sort(arr_input):
    arr = list(arr_input)
    n = len(arr)
    comparisons = 0
    swaps = 0

    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            comparisons += 1
            yield {
                'type': 'compare',
                'indices': [j, j + 1],
                'array': list(arr),
                'comparisons': comparisons,
                'swaps': swaps,
                'desc': f"Comparing index {j} ({arr[j]}) and {j + 1} ({arr[j + 1]})"
            }
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swaps += 1
                swapped = True
                yield {
                    'type': 'swap',
                    'indices': [j, j + 1],
                    'array': list(arr),
                    'comparisons': comparisons,
                    'swaps': swaps,
                    'desc': f"Swapping index {j} and {j + 1}"
                }
        if not swapped:
            break

    yield {
        'type': 'sorted',
        'indices': list(range(n)),
        'array': list(arr),
        'comparisons': comparisons,
        'swaps': swaps,
        'desc': "Sorting completed."
    }


def selection_sort(arr_input):
    arr = list(arr_input)
    n = len(arr)
    comparisons = 0
    swaps = 0

    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            comparisons += 1
            yield {
                'type': 'compare',
                'indices': [min_idx, j],
                'array': list(arr),
                'comparisons': comparisons,
                'swaps': swaps,
                'desc': f"Searching minimum: comparing current min {arr[min_idx]} with {arr[j]}"
            }
            if arr[j] < arr[min_idx]:
                min_idx = j
        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
            swaps += 1
            yield {
                'type': 'swap',
                'indices': [i, min_idx],
                'array': list(arr),
                'comparisons': comparisons,
                'swaps': swaps,
                'desc': f"Placed smallest remaining element {arr[i]} at position {i}"
            }

    yield {
        'type': 'sorted',
        'indices': list(range(n)),
        'array': list(arr),
        'comparisons': comparisons,
        'swaps': swaps,
        'desc': "Sorting completed."
    }


def insertion_sort(arr_input):
    arr = list(arr_input)
    n = len(arr)
    comparisons = 0
    swaps = 0

    for i in range(1, n):
        key = arr[i]
        j = i - 1
        while j >= 0:
            comparisons += 1
            yield {
                'type': 'compare',
                'indices': [j, j + 1],
                'array': list(arr),
                'comparisons': comparisons,
                'swaps': swaps,
                'desc': f"Comparing key {key} with {arr[j]} at index {j}"
            }
            if arr[j] > key:
                arr[j + 1] = arr[j]
                swaps += 1
                yield {
                    'type': 'overwrite',
                    'indices': [j + 1],
                    'array': list(arr),
                    'comparisons': comparisons,
                    'swaps': swaps,
                    'desc': f"Shifted {arr[j]} rightwards to index {j + 1}"
                }
                j -= 1
            else:
                break
        arr[j + 1] = key
        yield {
            'type': 'overwrite',
            'indices': [j + 1],
            'array': list(arr),
            'comparisons': comparisons,
            'swaps': swaps,
            'desc': f"Inserted key {key} at index {j + 1}"
        }

    yield {
        'type': 'sorted',
        'indices': list(range(n)),
        'array': list(arr),
        'comparisons': comparisons,
        'swaps': swaps,
        'desc': "Sorting completed."
    }


def merge_sort(arr_input):
    arr = list(arr_input)
    stats = {'comparisons': 0, 'swaps': 0}

    def _merge_sort_helper(start, end):
        if start >= end:
            return
        mid = (start + end) // 2
        yield from _merge_sort_helper(start, mid)
        yield from _merge_sort_helper(mid + 1, end)
        yield from _merge(start, mid, end)

    def _merge(start, mid, end):
        left = arr[start:mid + 1]
        right = arr[mid + 1:end + 1]
        i = j = 0
        k = start

        while i < len(left) and j < len(right):
            stats['comparisons'] += 1
            yield {
                'type': 'compare',
                'indices': [start + i, mid + 1 + j],
                'array': list(arr),
                'comparisons': stats['comparisons'],
                'swaps': stats['swaps'],
                'desc': f"Comparing left partition {left[i]} and right partition {right[j]}"
            }
            if left[i] <= right[j]:
                arr[k] = left[i]
                i += 1
            else:
                arr[k] = right[j]
                j += 1
            stats['swaps'] += 1
            yield {
                'type': 'overwrite',
                'indices': [k],
                'array': list(arr),
                'comparisons': stats['comparisons'],
                'swaps': stats['swaps'],
                'desc': f"Merged value {arr[k]} into position {k}"
            }
            k += 1

        while i < len(left):
            arr[k] = left[i]
            i += 1
            k += 1
            stats['swaps'] += 1
            yield {
                'type': 'overwrite',
                'indices': [k - 1],
                'array': list(arr),
                'comparisons': stats['comparisons'],
                'swaps': stats['swaps'],
                'desc': f"Flushed remaining left value {arr[k - 1]}"
            }

        while j < len(right):
            arr[k] = right[j]
            j += 1
            k += 1
            stats['swaps'] += 1
            yield {
                'type': 'overwrite',
                'indices': [k - 1],
                'array': list(arr),
                'comparisons': stats['comparisons'],
                'swaps': stats['swaps'],
                'desc': f"Flushed remaining right value {arr[k - 1]}"
            }

    yield from _merge_sort_helper(0, len(arr) - 1)
    yield {
        'type': 'sorted',
        'indices': list(range(len(arr))),
        'array': list(arr),
        'comparisons': stats['comparisons'],
        'swaps': stats['swaps'],
        'desc': "Sorting completed."
    }


def quick_sort(arr_input):
    arr = list(arr_input)
    stats = {'comparisons': 0, 'swaps': 0}

    def _quick_sort_helper(low, high):
        if low < high:
            pivot_index = yield from _partition(low, high)
            yield from _quick_sort_helper(low, pivot_index - 1)
            yield from _quick_sort_helper(pivot_index + 1, high)

    def _partition(low, high):
        pivot = arr[high]
        i = low - 1
        yield {
            'type': 'partition',
            'indices': [high],
            'array': list(arr),
            'comparisons': stats['comparisons'],
            'swaps': stats['swaps'],
            'desc': f"Selected pivot {pivot} at index {high}"
        }

        for j in range(low, high):
            stats['comparisons'] += 1
            yield {
                'type': 'compare',
                'indices': [j, high],
                'array': list(arr),
                'comparisons': stats['comparisons'],
                'swaps': stats['swaps'],
                'desc': f"Comparing element {arr[j]} against pivot {pivot}"
            }
            if arr[j] < pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
                stats['swaps'] += 1
                yield {
                    'type': 'swap',
                    'indices': [i, j],
                    'array': list(arr),
                    'comparisons': stats['comparisons'],
                    'swaps': stats['swaps'],
                    'desc': f"Partition swap: {arr[i]} with {arr[j]}"
                }

        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        stats['swaps'] += 1
        yield {
            'type': 'swap',
            'indices': [i + 1, high],
            'array': list(arr),
            'comparisons': stats['comparisons'],
            'swaps': stats['swaps'],
            'desc': f"Placed pivot {pivot} at final partitioned index {i + 1}"
        }
        return i + 1

    yield from _quick_sort_helper(0, len(arr) - 1)
    yield {
        'type': 'sorted',
        'indices': list(range(len(arr))),
        'array': list(arr),
        'comparisons': stats['comparisons'],
        'swaps': stats['swaps'],
        'desc': "Sorting completed."
    }
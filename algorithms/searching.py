"""
Searching algorithm implementations yielding step-by-step inspection states.
"""

def linear_search(arr, target: int):
    comparisons = 0
    for idx, val in enumerate(arr):
        comparisons += 1
        found = (val == target)
        yield {
            'index': idx,
            'range': (0, len(arr) - 1),
            'found': found,
            'comparisons': comparisons,
            'desc': f"Inspecting index {idx} (value {val}) against target {target}"
        }
        if found:
            return

    yield {
        'index': -1,
        'range': (0, len(arr) - 1),
        'found': False,
        'comparisons': comparisons,
        'desc': f"Target {target} not found in array."
    }


def binary_search(arr, target: int):
    low = 0
    high = len(arr) - 1
    comparisons = 0

    while low <= high:
        mid = (low + high) // 2
        comparisons += 1
        mid_val = arr[mid]

        if mid_val == target:
            yield {
                'index': mid,
                'range': (low, high),
                'found': True,
                'comparisons': comparisons,
                'desc': f"Target {target} located at middle index {mid}."
            }
            return
        elif mid_val < target:
            yield {
                'index': mid,
                'range': (low, high),
                'found': False,
                'comparisons': comparisons,
                'desc': f"{mid_val} < {target}: Narrowing right window ({mid + 1} to {high})"
            }
            low = mid + 1
        else:
            yield {
                'index': mid,
                'range': (low, high),
                'found': False,
                'comparisons': comparisons,
                'desc': f"{mid_val} > {target}: Narrowing left window ({low} to {mid - 1})"
            }
            high = mid - 1

    yield {
        'index': -1,
        'range': (low, high),
        'found': False,
        'comparisons': comparisons,
        'desc': f"Target {target} not found in search space."
    }
# Afleveret af
#   Magnus Simoni Jahn (majah25) &
#   Kjell Schoke (kjsch25) &
#   Yasmina Mojib (yamoj25)

import math

def _left(i):
    return 2*i+1

def _right(i):
    return 2*i+2

def _parent(i):
    return math.floor((i-1)/2)

def _minHeapify(A, i):
    l = _left(i)
    r = _right(i)

    if l <= len(A) - 1 and A[l] < A[i]:
        smallest = l
    else:
        smallest = i

    if r <= len(A) - 1 and A[r] < A[smallest]:
        smallest = r

    if smallest != i:
        A[i], A[smallest] = A[smallest], A[i]
        _minHeapify(A, smallest)

def extractMin(A):
    A[0], A[len(A)-1] = A[len(A)-1], A[0]
    minimal = A.pop()
    _minHeapify(A, 0)
    return minimal

def insert(A, e):
    A.append(e)
    i = len(A) - 1

    while i > 0 and A[_parent(i)] > A[i]:
        A[i], A[_parent(i)] = A[_parent(i)], A[i]
        i = _parent(i)

def createEmptyPQ():
    return []
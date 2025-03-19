from geometric_lib import square
from geometric_lib import circle

print("hello this is my first docker program, you can calculate 1) square per 2) square square 3) circle per 4) circle square")
print("print number (from 1 to 4) I don't validate input this is your problems")
ind = int(input())
if ind == 1:
    print("oh nice you chose square per, not very original, enter A (I don't validate input)")
    a = float(input())
    print(square.perimeter(a))
if ind == 2:
    print("oh nice you chose square square, not very original, enter A (I don't validate input)")
    a = float(input())
    print(square.area(a))
if ind == 3:
    print("oh nice you chose circle per, not very original, enter R (I don't validate input)")
    r = float(input())
    print(circle.perimeter(r))
if ind == 4:
    print("oh nice you chose circle square, not very original, enter R (I don't validate input)")
    r = float(input())
    print(circle.area(r))
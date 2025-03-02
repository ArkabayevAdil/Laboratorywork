import time
import math
print("Sample Input: ")
number = int(input())
milisec = float(input())
time.sleep(round(milisec/1000))
print(f"Square root of {number} after {int(milisec)} miliseconds is {math.sqrt(number)}")
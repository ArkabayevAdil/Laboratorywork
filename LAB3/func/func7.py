def has33(nums):
    for i in nums:
        if nums[i+1] == nums[i] and nums[i] == 3:
            return True
    return False
x = list(map(int, input().split()))
has33(x)

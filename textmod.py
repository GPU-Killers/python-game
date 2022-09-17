def rainbow(index):
    arr = ((230,0,0),(230,150,0),(230,230,0),(0,230,0),(0,0,230),(230,0,230))
    if index == len(arr):
        index = 0
    color = arr[index]
    return (color, index+1)
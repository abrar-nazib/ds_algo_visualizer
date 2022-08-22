import time


def linearSearchV(caller, arr, searchItem):
    for i in range(0, len(arr), 1):
        if(arr[i].value == searchItem):
            arr[i].toggleSelection()
            arr[i].toggleSuccess()
            caller.updateBoard(arr)
            arr[i].toggleSuccess()
            arr[i].toggleSelection()
            time.sleep(1)
            return i
        arr[i].toggleSelection()
        caller.updateBoard(arr)
        arr[i].toggleSelection()
        time.sleep(0.1)
        if(arr[i].value > searchItem):
            return False
    return False

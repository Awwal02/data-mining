
def find_one_frequent_itemset(data, min_support):
    items = {}
    for itemset in data:
        d = {}
        for item in itemset:
                if item not in d:
                    items[item] = items.get(item, 0) + 1
                    d[item] = True

    items = {k: v for k, v in items.items() if v >= min_support}
    
    return items

def join_n_strings(arr, n):
    result = []
    for i in range(0, len(arr) - n + 1):
        group = " ".join(arr[i:i+n])
        result.append(group)
    return result

def find_arr_str(data, length_space):
    arr = []
    for itemset in data:
        ind2 = []
        ind = []
        arr2 = join_n_strings(itemset, length_space)
        # for count, item in enumerate(itemset):
        #     if (count % length_space) == 0:
        #         r = " ".join(ind)
        #         if r != '' and len(ind) == length_space:
        #             ind2.append(r)
        #         ind = []
        #     ind.append(item)
        # arr.append(ind2)
        arr.append(arr2)
    return arr
            
                
            

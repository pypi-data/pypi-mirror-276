import re



#+---------------------------------------------------------------------------+
# Freestanding functions
#+---------------------------------------------------------------------------+

def natural_sort(array, inplace=False):
    '''
    Description
    ----------
    Sorts list via natural sorting as opposed to lexicographical sorting. For example, consider a
    list of file names starting with numbers ['101 Dalmatians.xlsx', '3 Blind Mice.xlsx']. Sorting
    using the default method will yield the same list because the first character "1" < "3". Conversely,
    natural sorting will intuitively place the name beginning with "3" before "101" since "3" < "101".

    Parameters
    ----------
    array :  list
        list to sort
    inplace : bool
        if True, sorting will be done inplace

    Returns
    ----------
    out : list | None
        list if inplace is False otherwise None
    '''

    def alphanumeric_key(element):
        ''' converts string into a list of string and number chunks (e.g. 'z23a' -> ['z', 23, 'a']) '''

        def try_int(x):
            try:
                return int(x)
            except:
                return x

        out = list(map(try_int, re.split('([0-9]+)', str(element))))
        return out

    if inplace:
        array.sort(key=alphanumeric_key)
    else:
        return sorted(array, key=alphanumeric_key)



def iter_get(array, index=0, default=None):
    ''' extends dictionary's .get() to other iterables such as lists '''
    if array is None: return
    try:
        return array[index]
    except IndexError:
        return default



def to_iter(x):
    ''' converts variable to a list '''
    return x if isinstance(x, (list, tuple)) else [x]



def delimit_iter(x, typ=str, delimiter=', ', encase=True):
    x = [str(typ(z)) for z in x]
    if typ == str and encase: x = ["'%s'" % z for z in x]
    return delimiter.join(x)



def lower_iter(iterable):
    return [x.lower() for x in iterable]



def text_to_iter(text, transform=str, delimiter='\n'):
    '''
    Description
    ----------
    Converts a list of items in text format to a Python list.

    Parameters
    ----------
    text : str
        Delimited string
    transform : func
        Function applied to each item as list is constructed
    delimiter : str
        text delimiter

    Returns
    ----------
    out : list
        list if items in text file
    '''
    return [transform(x.strip()) for x in text.split(delimiter) if x.strip()]



def iter_window(x, left=0, right=0, strict=False, step=False, include_index=False):
    '''
    iterates over a window of values in a list

    Parameters
    ----------
    x : list | other iterable
        list to iterate over
    left : int
        how many indices to the left of the current index to include in each returned slice
    right : int
        how many indices to the right of the current index to include in each returned slice
    strict : bool
        if True, only complete slices will be returned. (e.g. x=[1,2,3,4,5] and left=2 the first
        slice returned will be [1,2,3] at index 2. Index 0 and 1 would be partial slices and not returned.
    step : bool
        if True, the right-most index of a slice will define the boundary line for the next slice so that
        no values repeat. (e.g. x=[1,2,3,4,5] and right=2 will return slices [1,2,3] and [4,5])
    include_index : bool
        if True, the index of the slice is also returned
    '''
    n, start = len(x) - 1, -1
    for i,v in enumerate(x):
        a, b = max(0, i - left), min(n, i + right)
        #print('i =', i, 'v =', v, 'start again =', start, 'a =', a, 'b =', b)
        if step:
            if left > 0 and i == n: a = max(start, 0)
            if a < start: continue
        subset = x[ a : b + 1 ]
        #print('subset =',subset,a,b+1)
        if strict and len(subset) < left + right + 1: continue
        start = b + 1
        #color.print(str(subset),'o')
        yield (i, subset) if include_index else subset





if __name__ == '__main__':
    for x in iter_window([0,1,3,4], left=1, strict=True, step=True):
        print('x =', x)
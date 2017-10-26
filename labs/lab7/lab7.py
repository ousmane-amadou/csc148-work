from typing import Union, List



def flatten1(lst: Union[int, List]) -> List[int]:
    if isinstance(lst, int):
        return [lst]
    else:
        result = []
        for lst_i in lst:
            result = result + flatten1(lst_i)
        return result

if __name__ == '__main__':
    print(flatten1([[1, 5, 7], [[4]], 0, [-4, [6], [7, [8], 8]]]))

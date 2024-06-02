import json
import os


def get_dict(path: str="dict.json", package_dir: bool=True):
    if package_dir:
        path = f"{os.path.dirname(os.path.abspath(__file__))}/{path}"
    with open(path, "r") as file:
        return json.load(file)


def get_color(name: str, dictionary: dict=None, path: str="dict.json", package_dir: bool=True, no_exeption: bool=False) -> int:
    if dictionary != None:
        colors = dictionary
    else:
        colors = get_dict(path=path, package_dir=package_dir)

    if name in colors:
        for i in colors:
            if name == i:
                return colors[i]
    else:
        if not no_exeption:
            raise Exception(f"Color: '{name}' not found")
        return 38


def out(text, color: int|str=0, *args, 
        dictionary: dict=None, path: str="dict.json", package_dir: bool=True, no_exeption: bool=False, keep: bool=False, output: bool=True) -> str:
    if type(color) == str:
        color = get_color(color, dictionary=dictionary, path=path, package_dir=package_dir, no_exeption=no_exeption)
    combine = f"\033[{color}m{text}"
    for i in range(int(len(args)/2)):
        if type(args[i*2+1]) == str:
            args[i*2+1] = get_color(args[i*2+1])
        combine += f"\033[{args[i*2+1]}m{args[i*2]}"
    
    if keep and not len(args) % 2 == 0:
        combine += f"\033[{args[-1]}m"
    elif not keep:
        combine += "\033[0m"
    
    if output:
        print(combine)
    return combine


def inp(text, color: int|str=0, *args, 
        dictionary: dict=None, path: str="dict.json", package_dir: bool=True, no_exeption: bool=False, colored_input: bool=True, keep: bool=False) -> str:
    if colored_input:
        text = input(out(text, color, *args, dictionary=dictionary, path=path, package_dir=package_dir, no_exeption=no_exeption, keep=True, output=False))
        if not keep:
            print("\033[0m", end="")
    else:
        text = input(out(text, color, *args, dictionary=dictionary, path=path, package_dir=package_dir, no_exeption=no_exeption, keep=False, output=False))
        if keep:
            if len(args) >= 2:
                print(f"\033[{args[-1]}m")
            else:
                print(f"\033[{color}m")
    return text
    

def options(reach: int=None, dictionary: dict=None, path: str="dict.json", package_dir: bool=True) -> None:
    if type(reach) == int:
        for i in range(reach):
            out(i, i)

    if dictionary == None and path != "":
        dictionary = get_dict(path=path, package_dir=package_dir)
        
    elif dictionary == None:
        for color in dictionary:
            out(f"{color}: {dictionary[color]}", dictionary[color])

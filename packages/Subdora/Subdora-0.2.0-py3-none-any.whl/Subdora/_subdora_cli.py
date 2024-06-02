import argparse
import os 
from datetime import datetime , timedelta  
from ._subdora import subdora_encode_file , subdora_encode_to_image , subdora_parse , subdora_parse_img 

'''
This is the main function that handles the cli related thing
'''

def main():
    desc = '''
    Subdora cli tool 
    All subdora functionality on terminal 
    usage :
    type "subdora -h" to see full list of arguments
    or visit https://github.com/Lakshit-Karsoliya/Subdora for usage and further query
    '''
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument("--obfuscate", type=str, help="python file going to be obfuscated")
    parser.add_argument("--img",type=str,help="image file which in which code is going to attached")
    parser.add_argument("--run",type=str,help=".myst or .png file to run")
    parser.add_argument("--itr",type=int,help="iteration counter")
    parser.add_argument("--time",type=str,help="time of expiry")

    args = parser.parse_args()

    py_file_arg, img_file_arg  , myst_file_arg , itr_arg , time_arg = args.obfuscate , args.img , args.run , args.itr , args.time 

    if py_file_arg!=None:
        iterations = -100 if itr_arg == None else itr_arg 
        exp_time = "INF" if time_arg == None else time_arg
        if img_file_arg!=None:
            subdora_encode_to_image(
                py_file_arg,
                img_file_arg,
                iterations,
                exp_time
            )
            return
        else:
            subdora_encode_file(
                py_file_arg,
                iterations,
                exp_time
            )
            return
    elif myst_file_arg!=None:
        if myst_file_arg[-4:]=='myst':
            subdora_parse(myst_file_arg)
        elif myst_file_arg[-3:]=='png':
            subdora_parse_img(myst_file_arg)
        else:
            print("Invalid Arguments")
        return 
    else:
        print("Invalid Arguments")


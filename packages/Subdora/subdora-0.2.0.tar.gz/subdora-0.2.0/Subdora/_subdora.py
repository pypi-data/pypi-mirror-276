import os
import ctypes
from sys import platform
from datetime import datetime, timedelta
from PIL import Image

'''
This funciton is used to get the image dimentions if image dimentions 
are greater of equal that full hd then we encode else jhinga la la 
'''
def get_image_dimensions(image_path):
    try:
        with Image.open(image_path) as img:
            width, height = img.size
            return width, height
    except IOError:
        print(f"Unable to open image file: {image_path}")
        return None, None


if platform == "linux" or platform == "linux2":
    path = os.path.join(os.path.dirname(__file__))
    path += "/corex64/linux/Subdora.so"
    subdora_core = ctypes.CDLL(path)
elif platform == "win32":
    path = os.path.join(os.path.dirname(__file__))
    path += "/corex64/win/Subdora.dll"
    subdora_core = ctypes.CDLL(path)

'''
This Funciton is used to encode the python file inot .myst file 
it contsins some arguments like 
iteration counter : which specifies how many times a file can run
expiry_time : specify the expiry tiem of myst file
'''
subdora_encode_file_with_itr_and_time = subdora_core.Encode
subdora_encode_file_with_itr_and_time.argtypes = [
    ctypes.c_char_p, ctypes.c_size_t, ctypes.c_char_p, ctypes.c_char_p]
subdora_encode_file_with_itr_and_time.restype = None
'''
This Funciton is used to encode the python file into an image file
[Noet] any jpg image is converted to uncompressed png format [I dont know about jpg compression and decompression]
it also support the funciton of iteration counter and expity time
[Note] use files greater than or equal to FHD resolution
'''
subdora_encode_file_with_itr_and_time_img = subdora_core.Encode_Img
subdora_encode_file_with_itr_and_time_img.argtypes = [
    ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_size_t, ctypes.c_char_p]
subdora_encode_file_with_itr_and_time_img.restype = None
'''
This Function is used to parse the encoded .myst file 
[Note] if os Header of file is changed parsing will Fail 
'''
subdora_parse_file = subdora_core.Parse
subdora_parse_file.argtypes = [ctypes.c_char_p]
subdora_parse_file.restype = None
'''
This funcitno is specific for parsing encoded image files
[Note] use files greater than or equal to FHD resolution
'''
subdora_parse_file_img = subdora_core.Parse_Img
subdora_parse_file_img.argtypes = [ctypes.c_char_p]
subdora_parse_file_img.restype = None


'''
Encoding funcitns 
1. subdora_encode_file(input_file_path: str,iterations: int = -100,exp_time: str = "INF")
2. subdora_encode_to_image(input_pyton_file_path: str,input_image_file_path: str,iterations: int = -100,exp_time: str = "INF"):
'''


def subdora_encode_file(
    input_file_path: str,
    iterations: int = -100,
    exp_time: str = "INF"
):
    current_time = datetime.now()
    if isinstance(input_file_path, str) and input_file_path[-3:] == ".py" and os.path.exists(input_file_path):
        output_file_path = input_file_path[:-3]+".myst"
        if not isinstance(iterations, int):
            print("[ERROR] invalid arguments")
            return
        if exp_time != "INF":
            if not (isinstance(exp_time, str) and (exp_time[-1] in ['m', 'h']) and isinstance(int(exp_time[:-1]), int)):
                print("[ERROR] invalid arguments")
                return
            if exp_time[-1] == 'm':
                current_time += timedelta(minutes=int(exp_time[:-1]))
            elif exp_time[-1] == 'h':
                current_time += timedelta(hours=int(exp_time[:-1]))
            exp_time = current_time.strftime("%a %b %d %H:%M:%S %Y")
        subdora_encode_file_with_itr_and_time(input_file_path.encode(
        ), iterations, exp_time.encode(), output_file_path.encode())
    else:
        print("[ERROR] invalid arguments")


def subdora_encode_to_image(
    input_python_file_path: str,
    input_image_file_path: str,
    iterations: int = -100,
    exp_time: str = "INF"
):
    current_time = datetime.now()
    if input_image_file_path[-4:] in ['.jpg', '.png']:
        if os.path.exists(input_python_file_path):
            output_image_path = os.getcwd()+'/' + input_python_file_path.split('.')[0]+'.png'
            if not isinstance(iterations, int):
                print("[ERROR] invalid arguments")
                return
            if exp_time != "INF":
                if not( (isinstance(exp_time, str) and (exp_time[-1] in ['m', 'h']) and isinstance(int(exp_time[:-1]), int))):
                    print("[ERROR] invalid arguments")
                    return
                if exp_time[-1] == 'm':
                    current_time += timedelta(minutes=int(exp_time[:-1]))
                elif exp_time[-1] == 'h':
                    current_time += timedelta(hours=int(exp_time[:-1]))
                exp_time = current_time.strftime("%a %b %d %H:%M:%S %Y")
            width , height = get_image_dimensions(os.path.abspath(input_image_file_path))
            if width<1920 or height<1080 :
                print("[ERROR] Image resolution should be greater than full hd width greater than or equals to 1920 and height greater than or equals to 1080")
                return
            subdora_encode_file_with_itr_and_time_img(
                os.path.abspath(input_python_file_path).encode(),
                os.path.abspath(input_image_file_path).encode(),
                os.path.abspath(output_image_path).encode(),
                iterations,
                exp_time.encode()
            )
        else:
            print("Invalid Python file path")
    else:
        print("Image should be in jpg or png ")


'''
Parsing Functions
1. subdora_parse(myst_file_path: str)
2. subdora_parse_img(encoded_image_flie_path: str)
'''
def subdora_parse(myst_file_path: str):
    if isinstance(myst_file_path, str) and os.path.exists(myst_file_path):
        subdora_parse_file(os.path.abspath(myst_file_path).encode())
    else:
        print("Invalid file path")

def subdora_parse_img(encoded_image_flie_path: str):
    if isinstance(encoded_image_flie_path, str) and os.path.exists(encoded_image_flie_path):
        subdora_parse_file_img(os.path.abspath(encoded_image_flie_path).encode())
    else:
        print("Invalid file path")

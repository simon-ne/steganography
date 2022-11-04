from PIL import Image
from math import floor

MSG_LENGTH_SPACE = 16

def get_new_val(val, binary_data, bit_counter):
    if bit_counter >= len(binary_data):
        # print("YEY")
        return val

    bit = binary_data[bit_counter]

    val_parity = True if val % 2 == 0 else False
    bit_parity = True if bit == '1' else False

    if val_parity == bit_parity:
        return val
    
    if val == 255:
        return 254
    else:
        return val + 1

def get_altered_pixel(pixel, binary_data, bit_counter):
    new_pixel = []

    # print(pixel)
    for val in pixel:
        new_val = get_new_val(val, binary_data, bit_counter)
        new_pixel.append(new_val)
        bit_counter += 1
    
    return bit_counter, tuple(new_pixel)

def encode_to_binary(data):
    encoded_str = data.encode()
    encoded_str_hex = encoded_str.hex()
    binary_str = bin(int(encoded_str_hex, 16))[2:]

    if len(binary_str) > 65535:
        return "ERROR: Message is too big. Maximum binary message length is 65535."

    binary_str_len_binary = '{:0>16}'.format(str(bin(len(binary_str) + MSG_LENGTH_SPACE))[2:])
    # Add length of data to the beginning
    binary_data = binary_str_len_binary + binary_str

    return binary_data

def decode_from_binary(data):
    hex_data = "{0:0>4X}".format(int(data, 2))
    bytes_str = bytes.fromhex(hex_data)
    decoded_str = bytes_str.decode()

    return decoded_str

def get_data_len(image):
    pixel_map = image.load()

    bin_string = ""
    bit_counter = 0
    for row in range(image.height):
        for col in range(image.width):

            pixel = pixel_map[col, row]
            for val in pixel:
                if val % 2 == 0:
                    bin_string += "1"
                else:
                    bin_string += "0"
                
                bit_counter += 1

            if bit_counter >= MSG_LENGTH_SPACE:
                break

        if bit_counter >= MSG_LENGTH_SPACE:
                break

    return int(bin_string, 2)


def encode_to_img(img_path, message, output_path="encoded.png"):
    try:
        input_image = Image.open(img_path)
    except:
        return "Error: Something went wrong with opening image."
    pixel_map = input_image.load()

    binary_data = encode_to_binary(message)
    if "ERROR" in binary_data:
        return binary_data # Sloppy

    # print("ahoj")
    # print(input_image.height)
    # print(input_image.width)
    # print(len(binary_data))
    bit_counter = 0
    for row in range(input_image.height - 1):
        for col in range(input_image.width - 1):
            # print(row)

            pixel = pixel_map[col, row]
            bit_counter, new_pixel = get_altered_pixel(pixel, binary_data, bit_counter)
            pixel_map[col, row] = new_pixel

            if bit_counter == -1:
                break

        if bit_counter == -1:
            break

    input_image.save(output_path, format="png")
    input_image.close() 


def decode_from_img(img_path):
    try:
        encoded_image = Image.open(img_path)
    except:
        return "Error: Something went wrong with opening image."
    pixel_map = encoded_image.load()
    bin_data_length = get_data_len(encoded_image)

    counter = 0
    bin_string = ""
    for row in range(encoded_image.height):
        for col in range(encoded_image.width):
            pixel = pixel_map[col, row]
            for val in pixel:
                if counter >= bin_data_length:
                    break

                if val % 2 == 0:
                    bin_string += "1"
                else:
                    bin_string += "0"
                
                counter += 1

            if counter >= bin_data_length:
                    break

        if counter >= bin_data_length:
                    break
    
    return decode_from_binary(bin_string[MSG_LENGTH_SPACE:])


def get_img_capacity(img_path):
    try:
        image = Image.open(img_path)
    except:
        return "Error: Something went wrong with opening image."

    pixel_count = image.width * image.height
    values_count = pixel_count * 4
    capacity_in_bytes = floor( values_count / 8 )

    return capacity_in_bytes
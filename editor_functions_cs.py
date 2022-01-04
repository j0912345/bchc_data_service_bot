import hashlib
import os
game_language="en"# fix this
ponos_save_server = "nyanko-save.ponosgames.com"
# most of the save editing funtions are based on https://github.com/fieryhenry/Battle-Cats-Save-File-Editor.
# most of the functions were made by fiery henry,
# all i did was translate them into python code.

def find_bytes_in_file(filename, byte_string, get_all_in_file=False):
    with open(filename, "rb") as save_file:
        file_data_len = os.path.getsize(filename)
        byte_str_len = len(byte_string)
        if not get_all_in_file:
            for ___current_loop_num___ in range(0, file_data_len):
                save_file.seek(___current_loop_num___)
                if save_file.read(byte_str_len) == byte_string:
                    return save_file.tell()-1
        else:
            location_list = []
            for ___current_loop_num___ in range(0, file_data_len):
                save_file.seek(___current_loop_num___)
                if save_file.read(byte_str_len) == byte_string:
                    location_list.append(save_file.tell()-1)
            return location_list


def find_something_idk_what_OccurrenceB_in_henrys_tool(filename):
    with open(filename, "rb") as save_file:
        pass

#basic stuff
def edit_catfood(filename, catfood_amount):
    with open(filename, "r+b") as save_file:
        save_file.seek(7)
        save_file.write((catfood_amount).to_bytes(4, byteorder='little'))
    patch_savefile(filename)

def edit_xp(filename, xp_amount):
    with open(filename, "r+b") as save_file:
        #xp is at a dif pos in bc jp version

        if game_language != "jp":
            save_file.seek(76)
        else:
            save_file.seek(75)
        save_file.write((xp_amount).to_bytes(4, byteorder='little'))
    patch_savefile(filename)

def get_cat_number(file_var_name, thing_to_look_for=2):
    # idk why these numbers
    start_range = 7344
    end_range = 10800
    dif_of_end_start = end_range - start_range
    file_var_name.seek(start_range)
    data_range = file_var_name.read(dif_of_end_start)
    for ___current_loop_num_cat_num___ in range(0, dif_of_end_start):
#        print("loop"+str(___current_loop_num_cat_num___))
        print(data_range[___current_loop_num_cat_num___])
        if data_range[___current_loop_num_cat_num___] == thing_to_look_for:
            return str(___current_loop_num_cat_num___+start_range)+" found"

def edit_np():
    pass


def patch_savefile(filename):
    checksum_length = 32
    if game_language != "jp":
        location_bytes = bytes("battlecats"+game_language, "ascii")
    else:
        location_bytes = bytes("battlecats", "ascii")

    with open(filename, "r+b") as save_file:
        file_data_len = os.path.getsize(filename) - checksum_length
        file_len = file_data_len + 32
        user_save_data_without_checksum = save_file.read(file_data_len)
#        test = checksum_length - len(location_bytes)
        data_to_get_checksum_of = (location_bytes + user_save_data_without_checksum)
        save_hash = hashlib.md5(data_to_get_checksum_of).hexdigest()

        save_file.seek(file_data_len)
        save_file.write(bytes(save_hash, "ascii"))
        

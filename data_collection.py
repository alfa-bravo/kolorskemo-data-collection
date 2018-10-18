from subprocess import call
import csv
import urllib.request
import io
import os
from itertools import islice
from shutil import rmtree
from subprocess import Popen, PIPE
import json
import matplotlib
import time


TRANSPARENT = "transparent"
DOWNLOAD_FOLDER = "downloads/"
BIRD_DATASET = "dataset/Avibase_bird_species.csv"
BIRD_DATASET_OUTPUT = "dataset/Avibase_bird_species_output.csv"
LIMIT = 4
COLOR_LIMIT = 5
START= 60
END = 80


def run(dataset, dataset_output, limit, start, end, color_limit):
    """

    :param dataset: original
    :param dataset_output: file to write to
    :param limit: number of pics
    :param start: where to start in csv
    :param end: exclusive, where to end in csv
    :param color_limit: number of colors
    :return: None
    """
    with open(dataset, "r", encoding='ISO-8859-1') as file:
        csv_f = csv.reader(file)
        with open(dataset_output, "a", newline="") as output_file:
            for row in islice(csv_f, start, end, 1):
                search_term = row[0]  # bird species
                process(search_term, limit,color_limit, output_file)


def process(keyword, limit, color_limit, file):
    """
    main process
    1. download
    2. rename image directory (to no-space ones)
    3. color process
    4. update output csv
    5. delete dowloaded folder
    :param keyword:
    :param limit:
    :param color_limit:
    :param file:
    :return:
    """
    if not _is_folder_exist(DOWNLOAD_FOLDER+keyword):
        keyword_original = keyword
        keyword = _apply_keyword_rule(keyword) # with transparent word
        download_image(keyword, limit)

        list = []
        keyword_for_directory = _str_eliminate_special_charater(keyword) # no space and '
        if ' ' in _get_folder_name(keyword):
            # rename
            _rename(DOWNLOAD_FOLDER, keyword)
            _rename_image_files(keyword_for_directory)

            # color processing

            print("keyword_for_directory, ", keyword_for_directory)
            color_processing(keyword_for_directory, color_limit, list)

        # write to csv
        lst = [keyword_original]
        for x in list:
            lst.append(x)

        writer = csv.writer(file)
        writer.writerow(lst)

        # delete
        delete_folder(DOWNLOAD_FOLDER, keyword_for_directory)


def download_image(keyword, limit):
    """
    download image to downloads folders
    :param keyword: query
    :param limit: # of images
    :return: none
    """
    print("\n\nDownloading image...\n\n")

    if not _is_folder_exist(DOWNLOAD_FOLDER):
        os.mkdir(DOWNLOAD_FOLDER)

    call(["googleimagesdownload", "-k", keyword, "-l", str(limit), "-f", "jpg"])


def _rename(path, keyword_with_space):
    """
    rename folder so they don't have any space
    :param path:
    :param keyword_with_space:
    :return:
    """
    os.rename(path + keyword_with_space, path + _str_eliminate_special_charater(keyword_with_space))


def _rename_image_files(folder_name_with_out_space):
    """
    rename all files in a image folder
    :param folder_name_with_out_space:
    :return: None --> all file renamed to one without space
    """
    for dir_path, subdir_list, file_list in os.walk(DOWNLOAD_FOLDER + folder_name_with_out_space):
        for fname in file_list:
            print("file rename to,  ", _str_eliminate_special_charater(fname))
            os.rename(dir_path +"/" + fname, dir_path +"/" + _str_eliminate_special_charater(fname))


def color_processing(keyword, color_num, list):
    """
    call Vince's ekstrakto
    :param keyword: search term
    :param color_num: # of colors
    :param list: hold parsed colors
    :return:
    """
    print ("\n\ncolor_processing...\n\n")
    if _is_folder_exist(DOWNLOAD_FOLDER+keyword):
        if _count_files(DOWNLOAD_FOLDER+keyword) != 0:
            for dir_path, subdir_list, file_list in os.walk(DOWNLOAD_FOLDER + keyword):
                for fname in file_list:
                    img_path = os.path.abspath(dir_path+"/"+fname)
                    # call cli ek ...
                    print("img path, ", img_path)
                    ek_command = "ek "+ img_path+ " --number-of-colors "+str(color_num)

                    print(ek_command)
                    pipe = Popen(ek_command, shell=True, stdout=PIPE).stdout
                    # pipe out the json output
                    color_analysis_json = _str_to_json(pipe.read().decode("utf-8"))
                    print(color_analysis_json)
                    _get_colors_analysis(color_analysis_json, list)


def _get_folder_name(keyword):
    return os.path.basename(DOWNLOAD_FOLDER+keyword)


def _str_eliminate_special_charater(str):
    return str.replace(" ","-").replace("\'", "-").replace("%", "-").replace("&", "-")


def delete_folder(path, folder_name):
    """
    delete a folder
    :param path:
    :param folder_name:
    :return:
    """
    print("\n\ndeleting_images...\n\n")

    full_path = path+folder_name
    if os.path.exists(full_path):
        rmtree(full_path)


def _is_folder_exist(path):
    """
    check if a folder exits
    :param path:
    :return:
    """
    if os.path.exists(path):
        return True
    return False


def _count_files(path):
    """
    count # of file
    :param path:
    :return:
    """
    #exclude hidden files
    return len([f for f in os.listdir(path) if f[0] != '.'])


def _apply_keyword_rule(keyword):
    """
    add word transparent after each keyword
    :param keyword:
    :return:
    """
    return keyword + " " + TRANSPARENT


def _str_to_json(str):
    return json.loads(str)


def _get_colors_analysis(json, list):
    """
    parse rbg colors to hex and append to list
    :param json:
    :param list:
    :return:
    """
    for color in json.get("colors"):
        list.append(_rgb_to_hex(color))


def _rgb_to_hex(rgb):
    """
    convert rgb to hex
    :param rgb:
    :return:
    """
    return matplotlib.colors.to_hex(rgb) # return type str


def main():
    start_time = time.time()
    run(BIRD_DATASET, BIRD_DATASET_OUTPUT, LIMIT, START, END, COLOR_LIMIT)
    print("Finished! total time: ", time.time() - start_time)

if __name__ == "__main__":
    main()
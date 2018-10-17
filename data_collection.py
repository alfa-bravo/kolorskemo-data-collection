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


TRANSPARENT = "transparent"
DOWNLOAD_FOLDER = "downloads/"
BIRD_DATASET = "dataset/Avibase_bird_species.csv"
LIMIT = 4
COLOR_LIMIT = 5
START= 1
END = 5


def run(dataset, limit, start, end, color_limit):
    with open(dataset, "r+", encoding='ISO-8859-1') as file:
        csv_f = csv.reader(file)
        for row in islice(csv_f, start, end, 1):
            search_term = row[0]  # bird species
            process(search_term, limit,color_limit, file, row)


def process(keyword, limit, color_limit, file, row):
    if not _is_folder_exist(DOWNLOAD_FOLDER+keyword):
        keyword_original = keyword
        keyword = _apply_keyword_rule(keyword)
        download_image(keyword, limit)
        if _count_files(DOWNLOAD_FOLDER+keyword) < limit:
            download_image(keyword, limit)
        list = []
        if ' ' in _get_folder_name(keyword):
            _rename(DOWNLOAD_FOLDER, keyword)
            _rename_image_files(_str_eliminate_special_charater(keyword))
            color_processing(_str_eliminate_special_charater(keyword), color_limit, list)
        #print(list)
        lst = [keyword_original]
        for x in list:
            lst.append(x)

        print(lst)

        ##writer = csv.writer(file)
        #writer.writerow(lst)

        print (row) d

        #delete_folder(DOWNLOAD_FOLDER, keyword)


def download_image(keyword, limit):
    print("\n\nDownloading image...\n\n")

    call(["googleimagesdownload", "-k", keyword, "-l", str(limit), "-f", "jpg"])


def _rename(path, keyword_with_space):
    os.rename(path + keyword_with_space, path + _str_eliminate_special_charater(keyword_with_space))


def _rename_image_files(folder_name_with_out_space):
    for dir_path, subdir_list, file_list in os.walk(DOWNLOAD_FOLDER + folder_name_with_out_space):
        for fname in file_list:
            os.rename(dir_path +"/" + fname, dir_path +"/" + _str_eliminate_special_charater(fname))


def color_processing(keyword, color_num, list):
    print ("\n\ncolor_processing...\n\n")
    if _is_folder_exist(DOWNLOAD_FOLDER+keyword):
        if _count_files(DOWNLOAD_FOLDER+keyword) != 0:
            for dir_path, subdir_list, file_list in os.walk(DOWNLOAD_FOLDER + keyword):
                for fname in file_list:
                    img_path = os.path.abspath(dir_path+"/"+fname)
                    pipe = Popen("ek "+ img_path+" --number-of-colors "+str(color_num), shell=True, stdout=PIPE).stdout
                    color_analysis_json = _str_to_json(pipe.read().decode("utf-8"))
                    _get_colors_analysis(color_analysis_json, list)


def _get_folder_name(keyword):
    return os.path.basename(DOWNLOAD_FOLDER+keyword)


def _str_eliminate_special_charater(str):
    return str.replace(" ","-").replace("\'", "-")


def delete_folder(path, folder_name):
    print ("\n\ndeleting_images...\n\n")
    full_path = path+folder_name
    if os.path.exists(full_path):
        rmtree(full_path)


def _is_folder_exist(path):
    if os.path.exists(path):
        return True
    return False


def _count_files(path):
    #exclude hidden files
    return len([f for f in os.listdir(path) if f[0] != '.'])


def _apply_keyword_rule(keyword):
    return keyword + " " + TRANSPARENT


def _str_to_json(str):
    return json.loads(str)


def _get_colors_analysis(json, list):
    for color in json.get("colors"):
        list.append(_rgb_to_hex(color))


def _rgb_to_hex(rgb):
    return matplotlib.colors.to_hex(rgb) # return type str


def main():
    run(BIRD_DATASET, LIMIT, START, END, COLOR_LIMIT)


if __name__ == "__main__":
    main()

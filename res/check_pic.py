import csv
from pathlib import Path
import shutil
import requests

def unsplash_downloader(url, file_name):

    res = requests.get(f"{url}/download?force=true&w=640", stream=True)

    if res.status_code == 200:
        with open(file_name, 'wb') as f:
            shutil.copyfileobj(res.raw, f)
        print('Image sucessfully Downloaded: ', file_name)
    else:
        print('Image Couldn\'t be retrieved', url)


def pixabay_downloader(url, file_name):
    # 转换URL为下载链接
    img_suffix = "jpg"
    #url后面的‘/’不能少
    if not url.endswith("/"):
        url = url + "/"

    url_split = url.split('/')[-2]
    name_split = url_split.split('-')

    #有一些是矢量图png
    if url.find("vectors") == 0:
        img_suffix = "png"

    url_down = "https://pixabay.com/zh/images/download/" + name_split[1] + "-" + name_split[2] + "-" + name_split[-1] + "_640." + img_suffix + "?attachment"

    res = requests.get(url_down, stream=True)
    with open(file_name, 'wb') as f:
        shutil.copyfileobj(res.raw, f)
    print('Image sucessfully Downloaded: ', file_name)



def find_all_file(src_dir) -> list:
    ignores = [".DS_Store", "Thumbs.db"]
    result = []
    for i in Path(src_dir).iterdir():
        if not i.name in ignores:
            if i.is_file():
                result.append(i)
            else:
                for x in find_all_file(i):
                    result.append(x)
    return result


def check_csv(existing_file, csv_file):
    exclude_list = []
    for i in existing_file:
        if not i in csv_file:
            exclude_list.append(i)

    return exclude_list


def get_theory_path(res_file, file_chapter, file_topic, file_name, down_link):
    # 检查文件是否存在，返回图片路径
    image_path = Path(res_file, file_chapter, file_topic, file_name)
    if not image_path.exists():
        # 如果down_link为unsplash的图片，则下载
        if down_link.startswith("https://unsplash.com/photos/"):
            print(f"{image_path} not exists, downloading from unsplash...")
            unsplash_downloader(down_link, str(image_path))
        elif down_link.startswith("https://pixabay.com/"):
            print(f"{image_path} not exists, downloading from pixabay...")
            pixabay_downloader(down_link, str(image_path))
        else:
            print(f"{image_path} not exists, PLS download from {down_link}")
    return image_path


def find_file_using_name(file_name, file_library):
    for item in file_library:
        if file_name == item.name:
            return item
    return Path("res/pictures", file_name)


with open("res/picture.csv", newline="") as f:
    reader = csv.DictReader(f)
    theoty_path_list = []
    print("========================! ( ⊙ o ⊙ ) !===========================")
    for row in reader:
        # 检查csv中的图片是否都存在
        theoty_path_list.append(
            get_theory_path(
                "res/pictures", row["Chapter"], row["Topic"], row["File Name"], row["From"]
            )
        )
    print("========================! ( ⊙ o ⊙ ) !===========================")

    auto_path_result = []
    for i in check_csv(find_all_file("res/pictures"), theoty_path_list):
        print(f"{i} is not in place")

        auto_path = find_file_using_name(i.name, theoty_path_list)
        i.rename(auto_path)
        auto_path_result.append(f"moved {i} to {auto_path}")

    if not auto_path_result == []:
        for x in auto_path_result:
            print(x)

import xml.etree.ElementTree as elemTree
import os
import torch
import numpy as np
import cv2 
from glob import glob
from distutils.dir_util import copy_tree
import shutil


#class names: ['person', 'bicycle', 'scooter', 'bollard', 'traffic_light']

pascal_class_index = {
    'person':0,
    'bicycle': 1,
    'scooter': 2,
    'bollard': 3,
    'traffic_light': 4       
}

#train/ val/ test 디렉토리 변경
root_dir = "./train/"
img_dir = os.path.join(root_dir, 'images')  
xml_dir = os.path.join(root_dir, 'annotations')
label_dir = os.path.join(root_dir, 'labels')


def empty_delete(img_dir, label_dir):
    # 이미지 파일과 txt 파일이 저장된 디렉토리 경로 설정
    img_path = img_dir
    txt_path = label_dir

    # 디렉토리 내 모든 파일 리스트 가져오기
    img_list = os.listdir(img_path)
    txt_list = os.listdir(txt_path)

    # 이미지 디렉토리 내 모든 파일에 대해 반복
    for txt_name in txt_list:
        f = open(os.path.join(txt_path, txt_name), 'r')
        line = f.readlines()
        if line == []:
            fname = txt_name[:-3]+'jpg'
            fname1 = txt_name[:-3]+'png'
            try:
                os.remove(os.path.join(img_path, fname))
                os.remove(os.path.join(img_path, fname1))
            except FileNotFoundError:
                pass
            
            os.remove(os.path.join(txt_path, txt_name))
            f.close()

def data_ch(img_dir):
    #train/images 디렉토리 경로
    target_path = img_dir
    #bbox_new_** 폴더 내에서
    #하나씩 순회해서 bbox_2201 - > 파일 뽑아내기
    #example
    #rootdir = "./train/images/Bbox_26_new"
    #target_path = "./train/images"
    dir = glob(os.path.join(target_path,'*'))
    for i in dir:
        #i -> ./train/images/bbox_25_new/
        os.chdir(i)
        rootdir = os.getcwd()
        dirlist = os.listdir()
        for j in dirlist:
            subdir = os.path.join(rootdir, j)
            for f in os.listdir(subdir):
                source_obj = os.path.join(subdir, f)
                shutil.copy2(source_obj, dst=target_path)

def delete_img_without_txt(root_dir, img_dir, label_dir):
    # 이미지 파일과 txt 파일이 저장된 디렉토리 경로 설정
    dir_path = root_dir
    img_path = img_dir
    txt_path = label_dir

    # 디렉토리 내 모든 파일 리스트 가져오기
    img_list = os.listdir(img_path)
    txt_list = os.listdir(txt_path)

    #이미지 디렉토리에는 있는데 라벨 디렉토리에는 없을때 이미지 디렉토리의 파일 삭제
    for img_name in img_list:
        fname = img_name[:-3]+'txt'
        if fname not in txt_list:
            os.remove(os.path.join(img_path, img_name))   

def Read_xml():
    width = float(1920)
    height = float(1080)
    image_path = os.path.join(root_dir, 'images')
    dirs = glob(os.path.join(image_path,'*/*'))
    xmls = glob(os.path.join(image_path,'*/*/*.xml'))
    total_result = []
    #for xml in xmls:
    for sub_dir in dirs:
        xml_path = glob(os.path.join(sub_dir,"*.xml"))[0]
        tree = elemTree.parse(xml_path)
        for image in tree.findall('./image'):
            fname = image.attrib['name']
            box_result = []
            for box in image.findall("./box"):
                name = box.attrib["label"]
                try:
                    class_index = pascal_class_index[name]
                except KeyError:
                    continue
        
                #xtl,ytl이 좌상단/ xbr,ybr이 우하단 
                xmin = float(box.attrib["xtl"])
                ymin = float(box.attrib["ytl"])
                xmax = float(box.attrib["xbr"])
                ymax = float(box.attrib["ybr"])
                bb_width = round((xmax - xmin) / width, 15)
                bb_height = round((ymax - ymin) / height, 15)
                x_center = round((xmax + xmin)/2/width, 15)
                y_center = round((ymax + ymin)/2/height, 15)
                box_result.append([class_index, x_center, y_center, bb_width, bb_height])
            Write_txt(file_name = fname, result= box_result)

            
def Write_txt(file_name, result):
    file_name = file_name[:-3]+'txt'
    file_path = os.path.join(label_dir, file_name)
    f = open(file_path, 'w')
    for i, data in enumerate(result):
        data = f'{data}\n'
        data = data.replace(",", "").replace("[", "").replace("]", "")
        f.write(data)
    f.close()

 
def createfolder(dir):
    try:
        if not os.path.exists(dir):
            os.makedirs(dir)
    except OSError:
        print("Error : creating directory." + dir)
        


def main():
    if not os.path.isdir(xml_dir):
        raise Exception("there is no XML directory(for annotations)")
    createfolder(label_dir)
    Read_xml()


if __name__ == '__main__':
    #main()
    #data_ch(img_dir)
    #empty_delete(img_dir, label_dir)
    #delete_img_without_txt(root_dir, img_dir, label_dir)
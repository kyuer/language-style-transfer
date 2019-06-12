#-*- coding: utf-8 -*-
import re

if __name__ == '__main__':
    fw = open("pcm_split_byalivad_tmp.dec", "w")
    diction = {}
    with open("pcm_split_byalivad.dec", "r") as f:
        for lines in f:
            split_list = lines.strip().split("_driver")
            # print(split_list[0])
            ex = split_list[0]+":"
            tmp = split_list[-1].split("\t")[-1]
            if not tmp.startswith("0"):
                content = tmp
            if ex in diction.keys(): # and not content.startswith("0")
                diction[ex].append(content)
            else:
                content_list = []
                content_list.append(content)
                diction[ex] = content_list

        for key in diction.keys():
            li = diction[key]
            li = "".join(li)
            diction[key] = li
    # print(diction)

    for i,j in diction.items():
        print(i+j)
        fw.write(str(i+j)+"\n")
    fw.close()
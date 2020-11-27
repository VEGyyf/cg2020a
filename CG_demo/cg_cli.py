#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import os
import cg_algorithms as alg
import numpy as np
from PIL import Image


if __name__ == '__main__':
    input_file = 'C:\\Users\yyf01\Desktop\cg2020\CG_demo\input.txt' # sys.argv[1]
    output_dir = 'C:\\Users\yyf01\Desktop\cg2020\CG_demo\output' # sys.argv[2]
    os.makedirs(output_dir, exist_ok=True)

    item_dict = {}# 图元存放 字典结构，value为item_type, p_list, algorithm, color，key为item_id
    pen_color = np.zeros(3, np.uint8)# 返回来一个给定形状和类型的用0填充的数组；
    width = 0
    height = 0
    li=0

    with open(input_file, 'r') as fp:# 读取文件
        li+=1
        line = fp.readline()
        while line:# 解析每一行命令
            line = line.strip().split(' ')
            if line[0] == 'resetCanvas':# 100 <= width, height <= 1000
                    width = int(line[1])
                    height = int(line[2])
                    item_dict = {}
                    if not (100 <= width <= 1000 and 100 <= height <= 1000):
                        print("Line %d Invalid size parameters." %(li))
                    
            elif line[0] == 'saveCanvas':
                save_name = line[1]
                canvas = np.zeros([height, width, 3], np.uint8)
                canvas.fill(255)
                for item_type, p_list, algorithm, color in item_dict.values():
                    if item_type == 'line':
                        pixels = alg.draw_line(p_list, algorithm)
                        for x, y in pixels:
                            canvas[height - 1 - y, x] = color
                    elif item_type == 'polygon':
                        pass
                    elif item_type == 'ellipse':
                        pass
                    elif item_type == 'curve':
                        pass
                Image.fromarray(canvas).save(os.path.join(output_dir, save_name + '.bmp'), 'bmp')
            elif line[0] == 'setColor':
                pen_color[0] = int(line[1])
                pen_color[1] = int(line[2])
                pen_color[2] = int(line[3])
            elif line[0] == 'drawLine':
                item_id = line[1]
                x0 = int(line[2])
                y0 = int(line[3])
                x1 = int(line[4])
                y1 = int(line[5])
                algorithm = line[6]
                item_dict[item_id] = ['line', [[x0, y0], [x1, y1]], algorithm, np.array(pen_color)]
            elif line[0] == 'drawPolygon':
                pass
            elif line[0] == 'drawEllipse':
                pass
            elif line[0] == 'drawCurve':
                pass
            elif line[0] == 'translate':
                pass          
            elif line[0] == 'rotate':
                pass                
            elif line[0] == 'scale':
                pass  
            elif line[0] == 'clip':
                pass              

            line = fp.readline()


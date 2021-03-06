#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import os
import cg_algorithms as alg
import numpy as np
from PIL import Image


if __name__ == '__main__':
    current_path = os.path.dirname(__file__)
    input_file = '\input.txt' # sys.argv[1]
    input_file = current_path+input_file
    output_dir = '\output' # sys.argv[2]
    output_dir=current_path+output_dir
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
                        if pixels is not None:
                            for x, y in pixels:
                                canvas[y, x] = color
                    elif item_type == 'polygon':
                        pixels = alg.draw_polygon(p_list, algorithm)
                        if pixels is not None:
                            for x, y in pixels:
                                canvas[y, x] = color
                    elif item_type == 'ellipse':
                        pixels = alg.draw_ellipse(p_list)
                        if pixels is not None:
                            for x, y in pixels:
                                canvas[y, x] = color
                    elif item_type == 'curve':
                        pixels = alg.draw_curve(p_list, algorithm)
                        if pixels is not None:
                            for x, y in pixels:
                                canvas[y, x] = color
                    else:
                        item_type = item_type.strip().split(' ')
                        if item_type[0] == 'translate':
                            pixels=[]
                            newpixels=[]
                            dx=int(item_type[1])
                            dy=int(item_type[2])
                            newpixels=alg.translate(p_list, dx, dy,algorithm,item_type[len(item_type)-1])
                            if newpixels is not None:
                                for x, y in newpixels:
                                    canvas[y, x] = color 
                        elif item_type[0] == 'rotate':
                            pixels=[]
                            newpixels=[]
                            x=int(item_type[1])
                            y=int(item_type[2])
                            r=int(item_type[3])
                            newpixels=alg.rotate(p_list, x, y, r,algorithm,item_type[len(item_type)-1])
                            if newpixels is not None:
                                for x, y in newpixels:
                                    canvas[y, x] = color  
                        elif item_type[0] == 'scale':
                            parl=[]
                            newpixels=[]
                            x=int(item_type[1])
                            y=int(item_type[2])
                            r=float(item_type[3])
                            newpixels=alg.scale(p_list, x, y, r,algorithm,item_type[len(item_type)-1])
                            if newpixels is not None:
                                for x, y in newpixels:
                                    canvas[y, x] = color                                                               
                        elif item_type[0] == 'clip':
                            pixels=[]
                            newpixels=[]
                            xm=int(item_type[1])
                            ym=int(item_type[2])
                            xM=int(item_type[3])
                            yM=int(item_type[4])                            
                            clipalg=item_type[5]
                            newpixels=alg.clip(p_list, xm, ym, xM, yM, clipalg,algorithm)
                            if newpixels is not None:
                                for x, y in newpixels:
                                    canvas[y, x] = color                                                               


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
                item_id = line[1]
                plist=[]
                for i in range(2,len(line)-1,2):
                    x=int(line[i])
                    y=int(line[i+1])
                    plist.append([x,y])
                algorithm = line[len(line)-1]
                item_dict[item_id] = ['polygon', plist, algorithm, np.array(pen_color)]
            elif line[0] == 'drawEllipse':
                item_id = line[1]
                x0 = int(line[2])
                y0 = int(line[3])
                x1 = int(line[4])
                y1 = int(line[5])
                algorithm = 'midpoint'
                item_dict[item_id] = ['ellipse', [[x0, y0], [x1, y1]], algorithm, np.array(pen_color)]
            elif line[0] == 'drawCurve':
                item_id = line[1]
                plist=[]
                for i in range(2,len(line)-1,2):
                    x=int(line[i])
                    y=int(line[i+1])
                    plist.append([x,y])
                algorithm = line[len(line)-1]
                item_dict[item_id] = ['curve', plist, algorithm, np.array(pen_color)]
            elif line[0] == 'translate':
                item_id = line[1]+' translate' 
                old = item_dict[line[1]]                       
                dx = line[2]
                dy = line[3]   
                transtype='translate '+dx+' '+dy+' '+old[0]
                item_dict[item_id] = [transtype,  old[1], old[2], old[3]]
                del item_dict[line[1]]
                     
            elif line[0] == 'rotate':
                item_id = line[1]+' rotate' 
                old = item_dict[line[1]]                       
                dx = line[2]
                dy = line[3]   
                r = line[4]
                transtype='rotate '+dx+' '+dy+' '+r+' '+old[0]
                item_dict[item_id] = [transtype,  old[1], old[2], old[3]] 
                del item_dict[line[1]]              
            elif line[0] == 'scale':
                item_id = line[1]+' scale' 
                old = item_dict[line[1]]                       
                x = line[2]
                y = line[3]   
                s = line[4]
                transtype='scale '+x+' '+y+' '+s+' '+old[0]
                item_dict[item_id] = [transtype,  old[1], old[2], old[3]] 
                del item_dict[line[1]]
            elif line[0] == 'clip':
                item_id = line[1]+' clip' 
                old = item_dict[line[1]]                       
                xm = line[2]
                ym = line[3]   
                xM = line[4]
                yM = line[5]  
                clipalg=line[6]
                transtype='clip '+xm+' '+ym+' '+xM+' '+yM+' '+clipalg+' '+old[0]
                item_dict[item_id] = [transtype,  old[1], old[2], old[3]]
                del item_dict[line[1]]
               

            line = fp.readline()


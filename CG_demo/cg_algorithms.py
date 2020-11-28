#!/usr/bin/env python
# -*- coding:utf-8 -*-

# 本文件只允许依赖math库
import math


def draw_line(p_list, algorithm):
    """绘制线段

    :param p_list: (list of list of int: [[x0, y0], [x1, y1]]) 线段的起点和终点坐标
    :param algorithm: (string) 绘制使用的算法，包括'DDA'和'Bresenham'，此处的'Naive'仅作为示例，测试时不会出现
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    x0, y0 = p_list[0]
    x1, y1 = p_list[1]
    result = []
# test git
    if algorithm == 'Naive':
        if x0 == x1:
            if y0 > y1: 
                y0, y1 = y1,y0
            for y in range(y0, y1 + 1):
                result.append([x0, y])
        else:
            k = (y1 - y0) / (x1 - x0)
            if x0 > x1: # 统一转换成从左向右生成
                x0, y0, x1, y1 = x1, y1, x0, y0
            for x in range(x0, x1 + 1):
                result.append([x, int(y0 + k * (x - x0))])
    elif algorithm == 'DDA':# TODO:debug
        if x0 == x1:  # case:x=k
            if y0 > y1: 
                y0, y1 = y1,y0
            for y in range(y0, y1 + 1):
                result.append([x0, y])
        else:
            k = (y1 - y0) / (x1 - x0)
            if x0 > x1:
                x0, y0, x1, y1 = x1, y1, x0, y0
            deltax = abs(x1-x0)
            deltay = abs(y1-y0)
            if deltax > deltay:
                y=y0
                for x in range(x0, x1 + 1):
                    y = y+k
                    result.append([int(x), int(y)])
            else:
                x = x0
                for y in range(y0, y1 + 1):
                    x=x+1/k
                    result.append([int(x), int(y)])
    elif algorithm == 'Bresenham':

        if x0 == x1:
            if y0 > y1: 
                y0, y1 = y1,y0
            for y in range(y0, y1 + 1):
                result.append([x0, y])
        else:
            if x0 > x1:
                x0, y0, x1, y1 = x1, y1, x0, y0
            deltax = x1-x0
            deltay = y1-y0
            k = deltay/deltax
            x = x0
            y = y0
            if abs(k) < 1:
                p = 2 * deltay - deltax
                for x in range(x0, x1+1):
                    if p < 0:
                        y = y
                        p = p +2 *deltay
                    else:
                        y = y + 1
                        p = p + 2 * deltay - 2 * deltax
                    result.append([x, y])
            else:
                p = 2 * deltax - deltay
                for y in range(y0,y1+1):
                    if p < 0:
                        x = x
                        p = p + 2 * deltax
                    else:
                        x = x + 1
                        p = p + 2 * deltax - 2 * deltay
                    result.append([x, y])

    return result


def draw_polygon(p_list, algorithm):
    """绘制多边形

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 多边形的顶点坐标列表
    :param algorithm: (string) 绘制使用的算法，包括'DDA'和'Bresenham'
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    result = []
    for i in range(len(p_list)-1):
        line = draw_line([p_list[i], p_list[i+1]], algorithm)
        result += line
    return result


def draw_ellipse(p_list):
    """绘制椭圆（采用中点圆生成算法）

    :param p_list: (list of list of int: [[x0, y0], [x1, y1]]) 椭圆的矩形包围框左上角和右下角顶点坐标
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    x0,y0 = p_list[0]
    x1,y1 = p_list[1]
    xc = (x0+x1)/2
    yc = (y0+y1)/2
    rx = abs(x1-x0)/2
    ry = abs(y1-y0)/2  # 默认为正
    result = []
    x = 0
    y = ry  # 第一个点
    p1 = ry**2-rx**2*ry+rx**2/4
    while 2*ry**2*x < 2*rx**2*y:  # section 1
        if p1 < 0:
            x = x+1
            y = y
            p1 = p1+2*ry**2*x+ry**2
        else:
            x = x+1
            y = y-1
            p1 = p1+2*ry**2*x-2*rx**2*y+ry**2
        result.append([int(x), int(y)])
    p2 = ry**2*(x+0.5)**2+rx**2*(y-1)**2-rx**2*ry**2
    while x != rx or y != 0:  # section 2
        if p2 > 0:
            x = x
            y = y-1
            p2 = p2-2*rx**2*y+rx**2
        else:
            x = x+1
            y = y-1
            p2 = p2+2*ry**2*x-2*rx**2*y+rx**2
        result.append([int(x), int(y)])
    tmp =result.copy()
    for point in tmp: # 死循环
        result.append([int(point[0]), int(-point[1])])  # 其他三个象限的对称点?
        result.append([int(-point[0]), int(-point[1])]) # 元组（tuple）是不能修改的,而若想改变里面的元素，则应该用列表（list）。
        result.append([int(-point[0]), int(point[1])])
    for point in result:  # 平移
        point[0] = int(point[0]+xc)
        point[1] = int(point[1]+yc)
    return result


def draw_curve(p_list, algorithm):
    """绘制曲线
TODO
    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 曲线的控制点坐标列表
    :param algorithm: (string) 绘制使用的算法，包括'Bezier'和'B-spline'（三次均匀B样条曲线，曲线不必经过首末控制点）
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    if algorithm == 'Bezier':
        pass
    elif algorithm == 'B-spline':
        pass


def translate(p_list, dx, dy):
    """平移变换
    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 图元参数
    :param dx: (int) 水平方向平移量
    :param dy: (int) 垂直方向平移量
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 变换后的图元参数
    """
    for point in p_list:
        point[0] = int(point[0]+dx)
        point[1] = int(point[1]+dy)
    return p_list


def rotate(p_list, x, y, r):
    """旋转变换（除椭圆外）

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 图元参数
    :param x: (int) 旋转中心x坐标
    :param y: (int) 旋转中心y坐标
    :param r: (int) 顺时针旋转角度（°）
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 变换后的图元参数
    """
    r = math.radians(360-r)  # 转换为逆时针，角度转换为弧度！
    for point in p_list:
        tmpx = point[0]
        tmpy = point[1]
        point[0] = int(x + (tmpx-x)*math.cos(r)-(tmpy-y)*math.sin(r))
        point[1] = int(y + (tmpx-x)*math.sin(r)+(tmpy-y)*math.cos(r))# point[0]变了！
    return p_list


def scale(p_list, x, y, s):
    """缩放变换

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 图元参数
    :param x: (int) 缩放中心x坐标
    :param y: (int) 缩放中心y坐标
    :param s: (float) 缩放倍数
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 变换后的图元参数
    """
    for point in p_list:
        point[0] = int(point[0]*s + x*(1-s))
        point[1] = int(point[1]*s + y*(1-s))
    return p_list

def encode(x,y,xmin,xmax,ymin,ymax):
    res = 0b0
    if x < xmin:
        res = res | 0b1000
    else:
        res = res | 0b0000
    if x > xmax:
        res =res | 0b0100
    else:
        res = res | 0b0000
    if y < ymin:
        res = res | 0b0010
    else:
        res = res | 0b0000
    if y > ymax:
        res =res | 0b0001
    else:
        res = res | 0b0000
    return res

def clip(p_list, x_min, y_min, x_max, y_max, algorithm):
    """线段裁剪

    :param p_list: (list of list of int: [[x0, y0], [x1, y1]]) 线段的起点和终点坐标
    :param x_min: 裁剪窗口左上角x坐标
    :param y_min: 裁剪窗口左上角y坐标
    :param x_max: 裁剪窗口右下角x坐标
    :param y_max: 裁剪窗口右下角y坐标
    :param algorithm: (string) 使用的裁剪算法，包括'Cohen-Sutherland'和'Liang-Barsky'
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1]]) 裁剪后线段的起点和终点坐标
    """
    x1,y1=p_list[0]
    x2,y2=p_list[1]
    result = []
    if algorithm == 'Cohen-Sutherland':
        while 1:
            c1 = encode(x1,y1,x_min,x_max,y_min,y_max)
            c2 = encode(x2, y2, x_min, x_max, y_min, y_max)
            if c1 & c2 != 0:
                return result
            elif c1 | c2 == 0:
                return draw_line(p_list, 'DDA')
            elif c1 == 0:
                x1, y1, x2, y2 = x2, y2, x1, y1
            if c1&0b1000:  # 线段与上边界相交
                x1 = x1+(x2-x1)*(y_max-y1)/(y2-y1)
                y1 = y_max
            elif c1&0b0100:  # 线段与下边界相交
                x1 =x1+(x2-x1)*(y_min-y1)/(y2-y1)
                y1 = y_min
            elif c1&0b0010:  # 线段与右边界相交
                y1 = y1+(y2-y1)*(x_max-x1)/(x2-x1)
                x1 = x_max
            elif c1&0b0001:  # 线段与左边界相交
                y1 =y1+(y2-y1)*(x_min-x1)/(x2-x1)
                x1 = x_min
        # TODO
    elif algorithm == 'Liang-Barsky':
        pass
    #return None

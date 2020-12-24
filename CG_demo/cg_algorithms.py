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
    result = [[x0, y0], [x1, y1]]
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
            deltax = abs(x1-x0)
            deltay = abs(y1-y0)
            
            if deltax > deltay:
                if x0 > x1:
                    x0, y0, x1, y1 = x1, y1, x0, y0
                y=y0
                for x in range(x0, x1 + 1):#x0<=x1必然
                    y = y+k
                    result.append([int(x), int(y)])
            else:
                if y0 > y1:
                    x0, y0, x1, y1 = x1, y1, x0, y0
                x = x0
                for y in range(y0, y1 + 1):
                    x=x+1/k
                    result.append([int(x), int(y)])

    elif algorithm == 'Bresenham':
        '''
        if x0 == x1:
            if y0 > y1: 
                y0, y1 = y1,y0
            for y in range(y0, y1 + 1):
                result.append([x0, y])
        if y0 == y1:
            if x0 > x1: 
                x0,x1 = x1,x0
            for x in range(x0, x1 + 1):
                result.append([x, y0])
        '''
        dx=abs(x1-x0)
        sx=-1 if x0>x1 else 1
        dy=abs(y1-y0)
        sy=-1 if y0>y1 else 1
        x,y=x0,y0
        if dx>dy:
            err = dx/2.0
            while x!=x1:
                result.append([x,y])
                err-=dy
                if err < 0:
                    y+=sy
                    err +=dx
                x+=sx
        else:
            err = dy/2.0
            while y!=y1:
                result.append([x,y])
                err-=dx
                if err < 0:
                    x+=sx
                    err +=dy
                y+=sy
       
    return result


def draw_polygon(p_list, algorithm):
    """绘制多边形

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 多边形的顶点坐标列表
    :param algorithm: (string) 绘制使用的算法，包括'DDA'和'Bresenham'
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    result = []
    for i in range(len(p_list)):
        line = draw_line([p_list[i - 1], p_list[i]], algorithm)
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
    result.append([int(x), int(y)])
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
    while x < int(rx+2) and y > 0:  # section 2
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
    """TODO:绘制曲线
TODO
    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 曲线的控制点坐标列表
    :param algorithm: (string) 绘制使用的算法，包括'Bezier'和'B-spline'（三次均匀B样条曲线，曲线不必经过首末控制点）
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    if algorithm == 'Bezier':
        pass
    elif algorithm == 'B-spline':
        pass


def translate(p_list, dx, dy,alg,itemtype):
    """平移变换
    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 图元参数
    :param dx: (int) 水平方向平移量
    :param dy: (int) 垂直方向平移量
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 变换后的图元参数
    """
    res=[]
    for point in p_list:
        point[0] = int(point[0]+dx)
        point[1] = int(point[1]+dy)
    if itemtype=='line':
        res=draw_line(p_list, alg)
    elif itemtype=='polygon':
        res=draw_polygon(p_list, alg)
    elif itemtype=='ellipse':
        res=draw_ellipse(p_list)
    elif itemtype=='curve':
        res=draw_curve(p_list, alg)                

    return res


def rotate(p_list, x, y, r,alg,itemtype):
    """旋转变换（除椭圆外）

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 图元参数
    :param x: (int) 旋转中心x坐标
    :param y: (int) 旋转中心y坐标
    :param r: (int) 顺时针旋转角度（°）
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 变换后的图元参数
    """
    res=[]
    if itemtype=='ellipse':
        res=draw_ellipse(p_list)
    r = math.radians(r)  # 角度转换为弧度！
    for point in p_list:
        tmpx = point[0]
        tmpy = point[1]
        point[0] = int(x + (tmpx-x)*math.cos(r)-(tmpy-y)*math.sin(r))
        point[1] = int(y + (tmpx-x)*math.sin(r)+(tmpy-y)*math.cos(r))# point[0]变了！
    if itemtype=='line':
        res=draw_line(p_list, alg)
    elif itemtype=='polygon':
        res=draw_polygon(p_list, alg)

    elif itemtype=='curve':
        res=draw_curve(p_list, alg)                

    return res


def scale(p_list, x, y, s,alg,itemtype):
    """缩放变换

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 图元参数
    :param x: (int) 缩放中心x坐标
    :param y: (int) 缩放中心y坐标
    :param s: (float) 缩放倍数
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 变换后的图元参数
    """
    res=[]
    for point in p_list:# 对控制点进行缩放
        point[0] = int(point[0]*s + x*(1-s))
        point[1] = int(point[1]*s + y*(1-s))
    if itemtype=='line':
        res=draw_line(p_list, alg)
    elif itemtype=='polygon':
        res=draw_polygon(p_list, alg)
    elif itemtype=='ellipse':
        res=draw_ellipse(p_list)
    elif itemtype=='curve':
        res=draw_curve(p_list, alg)                

    return res # 放大后填充空隙

def encode(x,y,xmin,xmax,ymin,ymax):
    res = 0b0
    if x < xmin:#左
        res = res | 0b0001
    else:
        res = res | 0b0000
    if x > xmax:#右
        res =res | 0b0010
    else:
        res = res | 0b0000
    if y > ymax:#下
        res = res | 0b0100
    else:
        res = res | 0b0000
    if y <ymin:#上
        res =res | 0b1000
    else:
        res = res | 0b0000
    return res

def cansee(q,d,par_list):
    t0,t1=par_list[0],par_list[1]
    cansee=True
    r=0
    if q<0:# 从窗口外到内
        r=d/q
        if r>t1:
            cansee=False
        elif r>t0:
            t0=r
    elif q>0:# 从窗口内到外
        r=d/q
        if r<t0:
            cansee=False
        elif r<t1:
            t1=r
    elif d<0 and q == 0:
        cansee=False
    par_list[0],par_list[1]=t0,t1
    return cansee

def clip(p_list, x_min, y_min, x_max, y_max, algorithm):
    """TODO:线段裁剪

    :param p_list: (list of list of int: [[x0, y0], [x1, y1]]) 线段的起点和终点坐标
    :param x_min: 裁剪窗口左上角x坐标
    :param y_min: 裁剪窗口左上角y坐标!
    :param x_max: 裁剪窗口右下角x坐标
    :param y_max: 裁剪窗口右下角y坐标!
    :param algorithm: (string) 使用的裁剪算法，包括'Cohen-Sutherland'和'Liang-Barsky'
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1]]) 裁剪后线段的起点和终点坐标
    """
    x0,y0=p_list[0]
    x1,y1=p_list[1]
    result = []

    if algorithm == 'Cohen-Sutherland':
        c0 = encode(x0,y0,x_min,x_max,y_min,y_max)
        c1 = encode(x1, y1, x_min, x_max, y_min, y_max)
        outcode=c0
        if c1 !=0:
            outcode=c1
        #accept=false
        while 1:

            if c0 & c1 != 0:#完全在窗口外
                break
                
            elif c0 | c1 == 0: # 完全在窗口边界内
                #accept=true
                
                break
            else:
                x=0
                y=0
                outcode=c0 if outcode == c0 else c1 #找出区域外的点落在哪一部分

                if  outcode&0b1000:  # 线段与上边界相交
                    x = x0+(x1-x0)*(y_max-y0)/(y1-y0)
                    y = y_max
                elif  outcode&0b0100:  # 线段与下边界相交
                    x =x0+(x1-x0)*(y_min-y0)/(y1-y0)
                    y = y_min
                elif  outcode&0b0010:  # 线段与右边界相交
                    y = y0+(y1-y0)*(x_max-x0)/(x1-x0)
                    x = x_max
                elif  outcode&0b0001:  # 线段与左边界相交
                    y =y0+(y1-y0)*(x_min-x0)/(x1-x0)
                    x = x_min

                if outcode==c0:
                    x0=x
                    y0=y
                    c0 = encode(x0,y0,x_min,x_max,y_min,y_max)
                else:
                    x1=x
                    y1=y
                    c1 = encode(x1, y1, x_min, x_max, y_min, y_max)

        
        #if accept:
        result=[[x0, y0], [x1, y1]]
        # return draw_line(result, 'DDA')

    elif algorithm == 'Liang-Barsky':
        t0=0.0
        t1=1.0
        deltax=x1-x0
        deltay=y1-y0
        if cansee(-deltax,x0-x_min,[t0,t1])==False:
            return
        if cansee(deltax,x_max-x0,[t0,t1])==False:
            return 
        if cansee(-deltay,y0-y_max,[t0,t1])==False:
            return                  
        if cansee(deltay,y_min-y0,[t0,t1])==False:
            return
        x1=x0+t1*deltax
        y1=y0+t1*deltay
        x0=x0+t0*deltax
        y0=y0+t0*deltay  
        result=[[x0, y0], [x1, y1]]
        
    return draw_line(result, 'DDA')

    #return None

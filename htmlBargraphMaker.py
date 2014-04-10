#!/usr/bin/env python
from GChartWrapper import *
G = Line('AAAATTTTTAAAAAAc',encoding='simple')
G.color('76A4FB')
G.line(2)
G.axes('x')
G.axes.range(0,10,50,5)
print G

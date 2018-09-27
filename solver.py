#!/usr/bin/python
# -*- coding: utf-8 -*-
#利用DFS的分支定界算法解决背包问题
from collections import namedtuple
from functools import cmp_to_key
#物体类
Item = namedtuple("Item", ['index', 'value', 'weight'])
#自定义比较函数
def mycmp(item1, item2): 
    if(item1.value*1.0/item1.weight > item2.value*1.0/item2.weight): #value/weight大的排前边
        return -1
    else:
        return 0
#节点类        
class Node:
    def __init__(self, level, curvalue, room, bestvalue, taken, capacity): #成员变量
        self.level = level 
        self.curvalue = curvalue
        self.room = room
        self.bestvalue = bestvalue
        self.path = taken
        self.capacity = capacity

    def show(self):
        print(self.level , ",", self.curvalue, ",", self.room, "," , self.bestvalue)
    #所求的bound值
    def bound(self, items):
        weight = 0
        value = 0
        if self.level == -1:
            for i in range(len(items)):
                if weight + items[i].weight <= self.capacity:
                    value += items[i].value
                    weight += items[i].weight
                else:
                    value += (self.capacity - weight) * 1.0 / items[i].weight * items[i].value
                    break
        else:
            value += self.curvalue
            weight += self.capacity - self.room
            for i in range(self.level+1, len(items), 1):
                if weight + items[i].weight <= self.capacity:
                    value += items[i].value
                    weight += items[i].weight
                else:
                    value += (self.capacity - weight) * 1.0 / items[i].weight * items[i].value
                    break
        return value
    

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0]) #物体数目
    capacity = int(firstLine[1]) #背包容量
    items = []  
    
    for i in range(1, item_count+1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i-1, int(parts[0]), int(parts[1]))) #物体初始化

    value = 0
    weight = 0
    taken = [0]*len(items)  
    empty = [0]*len(items)    
    #关于python3的自定义比较函数用法
    items.sort(key=cmp_to_key(lambda a, b : mycmp(a,b))) 
    
  #  for item in items:
   #     print (str(item.index) + "," + str(item.value) + "," + str(item.weight))
    
    stack = [] #深度优先用栈实现，python中list代替
    u = Node(-1, 0, capacity, 0, empty, capacity)
    temp = u.bound(items)
    u.bestvalue = temp
   # print("curvalue:", u.curvalue) 
    #print("bound:", u.bestvalue)
    stack.append(u)
    max_profit = 0
    while(len(stack) != 0):
        #弹出末尾的节点
        t = stack.pop() 
        v = Node(-1, 0, capacity, 0, empty, capacity)
        if t.level == -1:
            v.level = 0
        if t.level == item_count-1:
            continue
        #not choose this item
        v.level = t.level + 1
        v.room = t.room
        v.curvalue = t.curvalue
        v.bestvalue = v.bound(items)
        v.path = t.path.copy() #注意Python中list为引用，故不能直接赋值，而是用copy()方法
        if v.bestvalue > max_profit:
            stack.append(v)
            if v.level == item_count -1:
                max_profit = v.curvalue #保留最大profit
                taken = v.path #保留最优解

        #choose this item
        v1 = Node(-1, 0, capacity, 0, empty, capacity)
        v1.level = t.level + 1
        v1.room = t.room - items[v1.level].weight
        v1.curvalue = t.curvalue + items[v1.level].value
#        print("curvalue:", v1.curvalue) 
        #copy(), 不能直接赋值，因为都是引用
        v1.path = t.path.copy() 
        v1.path[items[v1.level].index] = 1
        v1.bestvalue = t.bestvalue
#        print("v1.path:", v1.path)
        if (v1.room >= 0) and (v1.bestvalue > max_profit):
   #         print(taken)
            #满足则加入stack
            stack.append(v1)
            if v1.level == item_count-1:
                max_profit = v1.curvalue #保留最大profit
                taken = v1.path #保留最优解集
              #  print(taken)
    value = max_profit

    #prepare the solution in the specified output format
    output_data = str(value) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, taken))
    return output_data


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')


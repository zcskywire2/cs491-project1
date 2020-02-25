import math
from contextlib import redirect_stdout
import io
import random
class BST:
    def __init__(self):
        self.data = []
    def insertRec(self, item, index=0):
        if(len(self.data) == 0):
            self.data.append(item)
            self.data.append(None)
            self.data.append(None)
        else:
            #search left or right for insert
            if(item < self.data[index]):
                #check if we need to generate a new level
                if(self.hasLeftChild(index)):
                    #get value of child to see if we can insert
                    if(self.data[self.getLeftChild(index)] == None):
                        self.data[self.getLeftChild(index)] = item
                    #call recursive if we cant insert
                    else:
                        self.insertRec(item, self.getLeftChild(index))
                else:
                    for i in range(len(self.data)+1):
                        self.data.append(None)
                    self.data[self.getLeftChild(index)] = item
            else:
                  #check if we need to generate a new level
                if(self.hasRightChild(index)):
                    #get value of child to see if we can insert
                    if(self.data[self.getRightChild(index)] == None):
                        self.data[self.getRightChild(index)] = item
                    #call recursive if we cant insert
                    else:
                        self.insertRec(item, self.getRightChild(index))
                else:
                    for i in range(len(self.data)+1):
                        self.data.append(None)
                    self.data[self.getRightChild(index)] = item
    def deleteRec(self, item, index=-1):
        if(index == -1):
            loc = self.findItemRec(item)
            if(loc !=-1):
                self.deleteRec(item,loc)
        elif(self.hasRightChild(index) and self.hasLeftChild(index)):
            #node has no children
            if(self.data[self.getLeftChild(index)] == None and self.data[self.getRightChild(index)] == None):
                self.data[index]=None
                pass
            #node has 2 chindren
            elif(self.data[self.getLeftChild(index)] != None and self.data[self.getRightChild(index)] != None):
                mindex= self.findItemRec(self.findMinRec(self.getRightChild(index)))
                self.data[index] = self.data[mindex]
                self.data[mindex] = None
            #node has a left child
            elif(self.data[self.getLeftChild(index)] != None):
                #left child has a sub tree
                if(self.getLeftChild(self.getLeftChild(index)) != None or self.getRightChild(self.getLeftChild(index)) != None):
                    self.moveUpRec(self.getLeftChild(index))
                else:
                    #left child has no sub tree
                    self.data[index] = self.data[self.getLeftChild(index)]
                    self.data[self.getLeftChild(index)] = None
            #node has a right child        
            else:
                #right child has a sub tree
                if(self.getLeftChild(self.getRightChild(index)) != None or self.getRightChild(self.getRightChild(index)) != None):
                    self.moveUpRec(self.getRightChild(index))    
                #right child has no subtree    
                else:
                    self.data[index] = self.data[self.getRightChild(index)]
                    self.data[self.getRightChild(index)] = None
        else:
            self.data[index]=None
            pass
            
    def findNextRec(self, item, index=0):
        #print('call')
        left = None
        right = None
        if(self.hasLeftChild(index)):
            if(self.data[self.getLeftChild(index)] != None):
                #print('left call')
                left = self.findNextRec(item, self.getLeftChild(index))
        if(self.hasRightChild(index)):
            if(self.data[self.getRightChild(index)] != None):
                #print('right call')
                right = self.findNextRec(item, self.getRightChild(index))
        if(left == None and right == None):
            #print('return self')
            return self.data[index]
        elif(left == None):
            disSelf = self.data[index]-item
            disRig = right-item
            #print('right = ' + str(right) + ' self = ' + str(self.data[index]))
            #print('disSelf = ' + str(disSelf) + ' disRig = ' +str(disRig))
            if(disRig < 0):
                #print('return self')
                return self.data[index]
            if(disSelf < 0):
                #print('return right')
                return right
            if(disRig < disSelf):
                #print('return right')
                return right
            else:
                #print('return self')
                return self.data[index]
        elif(right == None):
            disSelf = self.data[index] -item
            dislef = left - item
            #print('right = ' + str(left) + ' self = ' + str(self.data[index]))
            #print('disSelf = ' + str(disSelf) + ' dislef = ' +str(dislef))
            if(dislef < 0):
                #print('retunr self')
                return self.data[index]
            if(disSelf < 0):
                #print('return left')
                return left
            if(dislef < disSelf):
                #print('return left')
                return left
            else:
                #print('return self')
                return self.data[index]
        else:
            disSelf = self.data[index] -item
            disRig = right - item
            dislef = left - item
            #print('right = ' + str(right) + ' left = '+ str(left) +' self = ' + str(self.data[index]))
            #print('disSelf = ' + str(disSelf) + ' disRig = ' +str(disRig) + ' dislef = ' +str(dislef))
            if(disRig < 0 and dislef < 0):
                #print('return self')
                return self.data[index]
            if(dislef < 0 and disSelf <0):
                #print('return right')
                return right
            if(disRig < 0 and disSelf < 0):
                #print('return left')
                return left
            if(disSelf < 0):
                if(disRig <dislef):
                    #print('return left')
                    return left
                else:
                    #print('return right')
                    return right
            if(disRig < 0):
                if(dislef < disSelf):
                    #print('return left')
                    return left
                else:
                    #print('return self')
                    return self.data[index]
            if(dislef < 0):
                if(disRig < disSelf):
                    #print('return right')
                    return right
                else:
                    #print('return self')
                    return self.data[index]
            if(disRig < dislef):
                if(disRig < disSelf):
                    #print('return right')
                    return right
                else:
                    #print('return self')
                    return self.data[index]
            elif(dislef < disSelf):
                #print('return left fall through')
                return left
            else:
                #print('return self')
                return self.data[index]
    def findPrevRec(self, item,index=0):
        left = None
        right = None
        if(self.hasLeftChild(index)):
            if(self.data[self.getLeftChild(index)] != None):
                left = self.findPrevRec(item, self.getLeftChild(index))
        if(self.hasRightChild(index)):
            if(self.data[self.getRightChild(index)] != None):
                right = self.findPrevRec(item, self.getRightChild(index))
        if(left == None and right == None):
            return self.data[index]
        elif(left == None):
            disSelf = item-self.data[index]
            disRig = item - right
            #print('right = ' + str(right) + ' self = ' + str(self.data[index]))
            #print('disSelf = ' + str(disSelf) + ' disRig = ' +str(disRig))
            if(disRig < 0):
                return self.data[index]
            if(disSelf < 0):
                return right
            if(disRig > disSelf):
                return right
            else:
                return self.data[index]
        elif(right == None):
            disSelf = item-self.data[index]
            dislef = item - left
            #print('right = ' + str(left) + ' self = ' + str(self.data[index]))
            #print('disSelf = ' + str(disSelf) + ' dislef = ' +str(dislef))
            if(dislef < 0):
                return self.data[index]
            if(disSelf < 0):
                return left
            if(dislef > disSelf):
                return left
            else:
                return self.data[index]
        else:
            disSelf = item-self.data[index]
            disRig = item - right
            dislef = item - left
            #print('right = ' + str(right) + ' left = '+ str(left) +' self = ' + str(self.data[index]))
            #print('disSelf = ' + str(disSelf) + ' disRig = ' +str(disRig) + ' dislef = ' +str(dislef))
            if(disRig < 0 and dislef < 0):
                return self.data[index]
            if(dislef < 0 and disSelf <0):
                return right
            if(disRig < 0 and disSelf < 0):
                return left
            if(disSelf < 0):
                if(disRig <dislef):
                    return left
                else:
                    return right
            if(disRig < 0):
                if(dislef < disSelf):
                    return left
                else:
                    return self.data[index]
            if(dislef < 0):
                if(disRig < disSelf):
                    return right
                else:
                    return self.data[index]
            if(disRig < dislef):
                if(disRig < disSelf):
                    return right
                else:
                    return self.data[index]
            elif(dislef < disSelf):
                return left
            else:
                return self.data[index]
    def findMinRec(self,index=0):
        left = None
        right = None
        if(self.hasLeftChild(index)):
            left = self.findMinRec(self.getLeftChild(index))
        if(self.hasRightChild(index)):
            right = self.findMinRec(self.getRightChild(index))
        if(left == None and right == None):
            return self.data[index]
        elif(left == None):
            if(self.data[index] > right):
                return right
            else:
                return self.data[index]
        elif(right == None):
            if(self.data[index]> left):
                return left
            else:
                return self.data[index]
        else:
            lesser = left if right > left else right
            if(lesser < self.data[index]):
                return lesser
            else: 
                return self.data[index]
    def findMaxRec(self,index=0):
        left = None
        right = None
        if(self.hasLeftChild(index)):
            left = self.findMaxRec(self.getLeftChild(index))
        if(self.hasRightChild(index)):
            right = self.findMaxRec(self.getRightChild(index))
        if(left == None and right == None):
            return self.data[index]
        elif(left == None):
            if(self.data[index] < right):
                return right
            else:
                return self.data[index]
        elif(right == None):
            if(self.data[index] < left):
                return left
            else:
                return self.data[index]
        else:
            greater = left if right < left else right
            if(greater > self.data[index]):
                return greater
            else: 
                return self.data[index]
    def insertIter(self,item):
        if(len(self.data) == 0):
            self.data.append(item)
            self.data.append(None)
            self.data.append(None)
        else:
            index = 0
            while(True):
                if(self.data[index] > item):
                    if(self.hasLeftChild(index)):
                        if(self.data[self.getLeftChild(index)] == None):
                            self.data[self.getLeftChild(index)] = item
                            break
                        else:
                            index = self.getLeftChild(index)
                            continue
                    else:
                        for i in range(len(self.data)+1):
                            self.data.append(None)
                        self.data[self.getLeftChild(index)] = item
                        break
                else:
                    if(self.hasRightChild(index)):
                        if(self.data[self.getRightChild(index)] == None):
                            self.data[self.getRightChild(index)] = item
                            break
                        else:
                            index = self.getRightChild(index)
                            continue
                    else:
                        for i in range(len(self.data)+1):
                            self.data.append(None)
                        self.data[self.getRightChild(index)] = item
                        break
                
    def deleteIter(self, item):
        index = self.findItemIter(item)
        if(index > -1):
            if(self.hasLeftChild(index) and self.hasRightChild(index)):
                if(self.getLeftChild(index) != None and self.getLeftChild(index) != None):
                    mindex = self.findItemIter(self.findMinIter(self.getRightChild(index)))
                    self.data[index] = self.data[mindex]
                    self.data[mindex] = None
                elif(self.getLeftChild(index) != None or self.getLeftChild(index) != None):
                    if(self.getLeftChild(index) != None):
                        if(self.getLeftChild(self.getLeftChild(index)) != None or self.getRightChild(self.getLeftChild(index)) != None):
                            self.moveUpIter(self.getLeftChild(index))
                        else:
                            self.data[index] = self.data[self.getLeftChild(index)]
                            self.data[self.getLeftChild(index)] = None
                    else:
                        if(self.getLeftChild(self.getRightChild(index)) != None or self.getRightChild(self.getRightChild(index)) != None):
                            self.moveUpIter(self.getRightChild(index))
                        else:
                            self.data[index] = self.data[self.getRightChild(index)]
                            self.data[self.getRightChild(index)] = None
                else:
                    self.data[index] = None
            else:
                self.data[index] = None
    def findNextIter(self,search):
        closest = math.inf
        index = None
        for i in self.data:
            if(i == None):
                continue
            if (i <= search):
                continue
            diff = i-search
            if (diff < closest):
                closest = diff
                index = i
        return index         
    def findPrevIter(self,search):
        closest = math.inf
        index = None
        for i in self.data:
            if (i == None):
                continue
            if (i >= search):
                continue
            diff = search - i
            if (diff < closest):
                closest = diff
                index = i
        return index           
    def findMinIter(self):
        min = math.inf
        for i in self.data:
            if (i == None):
                continue
            if (i < min):
                min = i
        return min
    def findMaxIter(self):
        max = -math.inf
        for i in self.data:
            if (i == None):
                continue
            if (i > max):
                max = i
        return max
    def hasLeftChild(self,index):
        return(len(self.data) > (2*(index)+1))
    def hasRightChild(self,index):
        return(len(self.data) > (2*(index)+2))
    def getLeftChild(self,index):
        if(self.hasLeftChild):
            return (2*index+1)
        else:
            return None
    def getRightChild(self,index):
        if(self.hasRightChild):
            return (2*index+2)
        else:
            return None
    def printTree(self):
        print (self.data)
    def findItemRec(self,item,index=0):
        #print('call')
        #print(self.data[index])
        if (self.data[index]== item):
            return index
        if(self.hasLeftChild(index) and self.hasRightChild(index)):
            if(self.data[self.getLeftChild(index)] != None and self.data[self.getRightChild(index)] != None):
                #print(self.data[self.getLeftChild(index)] != None)
                #print(self.data[self.getRightChild(index)])
                if(self.data[self.getLeftChild(index)] == item):
                    return self.getLeftChild(index)
                elif(self.data[self.getRightChild(index)] == item):
                    return self.getRightChild(index)
                else:
                    left = self.findItemRec(item,self.getLeftChild(index))
                    #print("left call, left = " +str(left))
                    right = self.findItemRec(item,self.getRightChild(index))
                    #print('right call, right = ' +str(right))
                    if(right >left):
                        return right
                    else:
                        return left
            if(self.hasLeftChild(index)):
                if(self.data[self.getLeftChild(index)] != None):
                    if(self.data[self.getLeftChild(index)] == item):
                        return self.getLeftChild(index)
                    else:
                        #print('left solo call)')
                        left = self.findItemRec(item,self.getLeftChild(index))
                        return left
            if(self.hasRightChild(index)):
                #print('test for right')
                if(self.data[self.getRightChild(index)] != None):
                    #print('right not none')
                    if(self.data[self.getRightChild(index)] == item):
                        #print('return right')
                        return self.getRightChild(index)
                    else:
                        #print('right not none call')
                        right = self.findItemRec(item,self.getRightChild(index))
                        return right
            return -1       
        if(self.hasLeftChild(index)):
            if(self.data[self.getLeftChild(index)] != None):
                if(self.data[self.getLeftChild(index)] == item):
                    return self.getLeftChild(index)
                else:
                    left = self.findItemRec(item,self.getLeftChild(index))
                    return left
            else:
                return -1
        if(self.hasRightChild(index)):
            #print('test for right')
            if(self.data[self.getRightChild(index)] != None):
                #print('right not none')
                if(self.data[self.getRightChild(index)] == item):
                    #print('return right')
                    return self.getRightChild(index)
                else:
                    right = self.findItemRec(self.getRightChild(index))
                    return right
            else:
                #print('interior return')
                return -1
        else:
            #print('outside return')
            return -1
    def findItemIter(self,item):
        for i in range(len(self.data)):
            if(self.data[i] == None):
                continue
            if(self.data[i] == item):
                return i
        return -1
    def getParent(self, item):
        if (item == 0):
            return 0
        else:
            return ((item -1)//2)
    def moveUpRec(self, index, offset = 0):
        #check for kids and set flags
        left = False
        right = False
        if(self.hasLeftChild(index) and self.hasRightChild(index)):
            if(self.getLeftChild(index) != None):
                left = True
            if(self.getRightChild(index) != None):
                right = True
        self.data[self.getParent(index)- offset] = self.data[index]
        self.data[index] = None
        if(left):
            self.moveUpRec(self.getLeftChild(index),-1)
        if(right):
            self.moveUpRec(self.getRightChild(index))
    def moveUpIter(self,index):
        children = []
        run = True
        current = [[index, 'r']]
        while(run):
            run = False
            temp = []
            for i in current:
                if(self.hasLeftChild(i[0]) and self.hasRightChild(i[0])):
                    if(self.data[self.getLeftChild(i[0])] != None):
                        temp.append([self.getLeftChild(i[0]),'l'])
                        run = True
                    if(self.data[self.getRightChild(i[0])] != None):
                        temp.append([self.getRightChild(i[0]),'r'])
                        run = True
                children.extend(current)
                current = temp
        for i in children:
            if(i[1] == 'r'):
                self.data[self.getParent(index)] = self.data[i[0]]
            else:
                self.data[self.getParent(index)-1] = self.data[i[0]]
    def sort(self,index=0):
        f = io.StringIO()
        with redirect_stdout(f):
            self.inOrder(0)
        ret = f.getvalue().split()
        return ret
    def inOrder(self, index):
        if (self.hasLeftChild(index)):
            if(self.data[self.getLeftChild(index)] != None):
                self.inOrder(self.getLeftChild(index))
        print(self.data[index], end=' ')
        if (self.hasRightChild(index)):
            if(self.data[self.getRightChild(index)] != None):
                self.inOrder(self.getRightChild(index))
def getRandomArray(n):
    ret = list(range(n))
    random.shuffle(ret)
    return ret
def getSortedArray(n):
    ret = list(range(n,-1,-1))
    return ret
tree = BST()
tree2 = BST()

tree.insertRec(10)
tree.printTree()
print()
tree.insertRec(5)
tree.printTree()
print()
tree.insertRec(8)
tree.printTree()
print()
tree.insertRec(9)
tree.printTree()
print()
tree.insertRec(11)
tree.printTree()
print()
tree.insertRec(15)
tree.printTree()
print()
tree.insertRec(20)
tree.printTree()
print()
tree.insertRec(18)
tree.printTree()
print()
tree.insertRec(19)
tree.printTree()
print()
print("iter tree")

tree2.insertRec(10)
tree2.printTree()
print()
tree2.insertIter(5)
tree2.printTree()
print()
tree2.insertIter(8)
tree2.printTree()
print()
tree2.insertIter(9)
tree2.printTree()
print()
tree2.insertIter(11)
tree2.printTree()
print()
tree2.insertIter(15)
tree2.printTree()
print()
tree2.insertIter(20)
tree2.printTree()
print()
tree2.insertIter(18)
tree2.printTree()
print()
tree2.insertIter(19)
tree2.printTree()
print()
tree2.printTree()

#print(tree.findMaxRec())
#print(tree.findMinIter())
#print(tree.findMaxIter())
#print(tree.findNextIter(7))
#print(tree.findPrevIter(7))
#print(tree.findNextRec(7))
#print(tree.findPrevRec(7))
print(tree.findItemRec(9))
print(tree.findItemIter(9))
print(tree.findItemIter(19))
print(tree.sort())
print(getRandomArray(10))
print(getSortedArray(10))
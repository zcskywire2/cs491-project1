import math
import time
from contextlib import redirect_stdout
import io
import random
class BST:
    def __init__(self):
        self.data = []
        self.trav=0
    def insertRec(self, item, index=0):
        #Length is 0 which means empty tree
        if(len(self.data) == 0):
            #create root and empty childre
            self.data.append(item)
            self.data.append(None)
            self.data.append(None)
        else:
            
            #search left or right for insert
            if(item < self.data[index]):
                self.trav = self.trav +1
                #check if we need to generate a new level
                if(self.hasLeftChild(index)):
                    #get value of child to see if we can insert
                    if(self.data[self.getLeftChild(index)] == None):
                        self.data[self.getLeftChild(index)] = item
                    #call recursive if we cant insert
                    else:
                        self.insertRec(item, self.getLeftChild(index))
                else:
                    #generate a new tree hight with empty parts
                    for i in range(len(self.data)+1):
                        self.data.append(None)
                    self.data[self.getLeftChild(index)] = item
            else:
                #check if we need to generate a new level
                self.trav = self.trav +1
                if(self.hasRightChild(index)):
                    #get value of child to see if we can insert
                    if(self.data[self.getRightChild(index)] == None):
                        self.data[self.getRightChild(index)] = item
                    #call recursive if we cant insert
                    else:
                        self.insertRec(item, self.getRightChild(index))
                else:
                    #generate a new tree level with empty nodes
                    for i in range(len(self.data)+1):
                        self.data.append(None)
                    self.data[self.getRightChild(index)] = item
    def deleteRec(self, item, index=-1):
        #inital call, get index of item to remove
        if(index == -1):
            #recursive search for the index of the item
            loc = self.findItemRec(item)
            #if it exists recursive call to the location, else exit
            if(loc !=-1):
                self.deleteRec(item,loc)
        #start recursive call from location provided in first call
        elif(self.hasRightChild(index) and self.hasLeftChild(index)):
            #node has no children
            if(self.data[self.getLeftChild(index)] == None and self.data[self.getRightChild(index)] == None):
                #just remove
                self.data[index]=None
                pass
            #node has 2 chindren
            elif(self.data[self.getLeftChild(index)] != None and self.data[self.getRightChild(index)] != None):
                #replace node with lowest value in right subtree
                mindex= self.findItemRec(self.findMinRec(self.getRightChild(index)))
                self.data[index] = self.data[mindex]
                self.data[mindex] = None
            #node has a left child
            elif(self.data[self.getLeftChild(index)] != None):
                #left child has a sub tree
                self.trav = self.trav +1
                if(self.getLeftChild(self.getLeftChild(index)) != None or self.getRightChild(self.getLeftChild(index)) != None):
                    #shuffle up left tree
                    self.moveUpRec(self.getLeftChild(index))
                else:
                    #left child has no sub tree
                    #swap and remove
                    self.trav = self.trav +1
                    self.data[index] = self.data[self.getLeftChild(index)]
                    self.data[self.getLeftChild(index)] = None
            #node has a right child        
            else:
                self.trav = self.trav +1
                #right child has a sub tree
                if(self.getLeftChild(self.getRightChild(index)) != None or self.getRightChild(self.getRightChild(index)) != None):
                    #shuffle up right tree
                    self.moveUpRec(self.getRightChild(index))    
                #right child has no subtree    
                else:
                    #swap and remove tree
                    self.trav = self.trav +1
                    self.data[index] = self.data[self.getRightChild(index)]
                    self.data[self.getRightChild(index)] = None
        else:
            #no child means last level of tree
            #just remove
            self.data[index]=None
            pass
            
    def findNextRec(self, item, index=0):
        #print('call')
        left = None
        right = None
        #check if current node has chidren
        if(self.hasLeftChild(index)):
            #get left child if valid
            if(self.data[self.getLeftChild(index)] != None):
                #recursive call on left tree
                self.trav = self.trav +1
                left = self.findNextRec(item, self.getLeftChild(index))
        if(self.hasRightChild(index)):
            #get right child if valid
            if(self.data[self.getRightChild(index)] != None):
                #recursive call on right child
                self.trav = self.trav +1
                right = self.findNextRec(item, self.getRightChild(index))
        if(left == None and right == None):
            #if no valid children return value of self
            return self.data[index]
        elif(left == None):
            #calculate difference between target and current values
            disSelf = self.data[index]-item
            disRig = right-item
            #ingore differeces that zero as they are lesser than item
            if(disRig < 0):
                return self.data[index]
            if(disSelf < 0):
                return right
            #return value of smaller difference
            if(disRig < disSelf):
                return right
            else:
                return self.data[index]
        elif(right == None):
            #calculate difference betweel values and target
            disSelf = self.data[index] -item
            dislef = left - item
            #ingore values less than zero as they are smaller than item
            if(dislef < 0):
                return self.data[index]
            if(disSelf < 0):
                return left
            #return smaller difference
            if(dislef < disSelf):
                return left
            else:
                return self.data[index]
        #compare self and values from children
        else:
            #calculare distants from items to target
            disSelf = self.data[index] -item
            disRig = right - item
            dislef = left - item
            #ingore values if double zero
            if(disRig < 0 and dislef < 0):
                return self.data[index]
            if(dislef < 0 and disSelf <0):
                return right
            if(disRig < 0 and disSelf < 0):
                return left
            #compare on children in self is less than zero
            if(disSelf < 0):
                if(disRig <dislef):
                    return left
                else:
                    return right
            #Compare with a right child less than zero
            if(disRig < 0):
                if(dislef < disSelf):
                    return left
                else:
                    return self.data[index]
            #comapre with left child zero
            if(dislef < 0):
                if(disRig < disSelf):
                    return right
                else:
                    return self.data[index]
            #compare with three values greater than zero
            if(disRig < dislef):
                if(disRig < disSelf):
                    return right
                else:
                    return self.data[index]
            elif(dislef < disSelf):
                return left
            else:
                return self.data[index]
    def findPrevRec(self, item,index=0):
        left = None
        right = None
        # Runs the same as the above
        # Check if current node has children
        if(self.hasLeftChild(index)):
            #if you have a left chilf recursive call
            if(self.data[self.getLeftChild(index)] != None):
                self.trav = self.trav +1
                left = self.findPrevRec(item, self.getLeftChild(index))
        if(self.hasRightChild(index)):
            #if you have a right child recursive call
            if(self.data[self.getRightChild(index)] != None):
                self.trav = self.trav +1
                right = self.findPrevRec(item, self.getRightChild(index))
        # if no chilfren return self
        if(left == None and right == None):
            return self.data[index]
        #comparision based on only right child
        elif(left == None):
            # calculate distance between current value and the target item
            disSelf = item-self.data[index]
            disRig = item - right
            #ingore values of less than zero as they are greater than target
            if(disRig < 0):
                return self.data[index]
            if(disSelf < 0):
                return right
            #return lower value after ingoring zero
            if(disRig > disSelf):
                return right
            else:
                return self.data[index]
        #comparison based on no right child
        elif(right == None):
            #calculate distance from target to item
            disSelf = item-self.data[index]
            dislef = item - left
            # ingore items less than zero
            if(dislef < 0):
                return self.data[index]
            if(disSelf < 0):
                return left
            #return lower value
            if(dislef > disSelf):
                return left
            else:
                return self.data[index]
        # comparsion with two children
        else:
            disSelf = item-self.data[index]
            disRig = item - right
            dislef = item - left
            #ingore zero values
            if(disRig < 0 and dislef < 0):
                return self.data[index]
            if(dislef < 0 and disSelf <0):
                return right
            if(disRig < 0 and disSelf < 0):
                return left
            #comparison with self less than zero value
            if(disSelf < 0):
                if(disRig <dislef):
                    return left
                else:
                    return right
            #comparison with right less that zero
            if(disRig < 0):
                if(dislef < disSelf):
                    return left
                else:
                    return self.data[index]
            #comparison with left less than zero
            if(dislef < 0):
                if(disRig < disSelf):
                    return right
                else:
                    return self.data[index]
            #return lowest of all three if no zeros
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
        # search if children exist and rec call them
        if(self.hasLeftChild(index)):
            self.trav = self.trav +1
            left = self.findMinRec(self.getLeftChild(index))
        if(self.hasRightChild(index)):
            self.trav = self.trav +1
            right = self.findMinRec(self.getRightChild(index))
        #compare self and possible children and return lowest
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
        #call recursive call on children if they exist
        if(self.hasLeftChild(index)):
            self.trav = self.trav +1
            left = self.findMaxRec(self.getLeftChild(index))
        if(self.hasRightChild(index)):
            self.trav = self.trav +1
            right = self.findMaxRec(self.getRightChild(index))
        # Compare self and possible children and return greatest value
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
        #create tree if empty
        if(len(self.data) == 0):
            self.data.append(item)
            self.data.append(None)
            self.data.append(None)
        #insert in tree if exists
        else:
            index = 0
            #interate down the tree untill we get to where we need
            while(True):
                self.trav = self.trav +1
                #go left if item is less than current node
                if(self.data[index] > item):
                    #check if left node exists
                    if(self.hasLeftChild(index)):
                        #if empty insert
                        if(self.data[self.getLeftChild(index)] == None):
                            self.data[self.getLeftChild(index)] = item
                            break
                        else:
                            #update current index if slot is full
                            index = self.getLeftChild(index)
                            continue
                    # left node doesnt exist add level and insert
                    else:
                        for i in range(len(self.data)+1):
                            self.data.append(None)
                        self.data[self.getLeftChild(index)] = item
                        break
                #go right because node is greater than current
                else:
                    #check if current node has children
                    if(self.hasRightChild(index)):
                        #if child is empty insert
                        if(self.data[self.getRightChild(index)] == None):
                            self.data[self.getRightChild(index)] = item
                            break
                        #update index if child has value
                        else:
                            index = self.getRightChild(index)
                            continue
                    # next level of tree doesnt exist, generate and insert
                    else:
                        for i in range(len(self.data)+1):
                            self.data.append(None)
                        self.data[self.getRightChild(index)] = item
                        break
                
    def deleteIter(self, item):
        #find the index of the item to remove
        index = self.findItemIter(item)
        #if the item is in the tree
        if(index > -1):
            #check if node has 2 childres
            if(self.hasLeftChild(index) and self.hasRightChild(index)):
                #if both are valid find min value in right subtree and swap
                if(self.getLeftChild(index) != None and self.getLeftChild(index) != None):
                    self.trav = self.trav +1
                    mindex = self.findItemIter(self.findMinIter(self.getRightChild(index)))
                    self.data[index] = self.data[mindex]
                    self.data[mindex] = None
                #  check if one is valid
                elif(self.getLeftChild(index) != None or self.getLeftChild(index) != None):
                    #if its left child
                    if(self.getLeftChild(index) != None):
                        # if left child has sub tree, iterate it up
                        if(self.getLeftChild(self.getLeftChild(index)) != None or self.getRightChild(self.getLeftChild(index)) != None):
                            self.trav = self.trav +1
                            self.moveUpIter(self.getLeftChild(index))
                        #swap and remove if no sub child
                        else:
                            self.trav = self.trav +1
                            self.data[index] = self.data[self.getLeftChild(index)]
                            self.data[self.getLeftChild(index)] = None
                    #else its right child
                    else:
                        #move up iteratively if right child has a sub tree
                        if(self.getLeftChild(self.getRightChild(index)) != None or self.getRightChild(self.getRightChild(index)) != None):
                            self.trav = self.trav +1
                            self.moveUpIter(self.getRightChild(index))
                        #swap and remove if no sub tree
                        else:
                            self.trav = self.trav +1
                            self.data[index] = self.data[self.getRightChild(index)]
                            self.data[self.getRightChild(index)] = None
                #remove as we have no children
                else:
                    self.data[index] = None
            #we are at the bottom of a tree just remove
            else:
                self.data[index] = None
    def findNextIter(self,search):
        #iterate through the whole list comparing values to find andreturn the closest value over
        closest = math.inf
        index = None
        for i in self.data:
            self.trav = self.trav +1
            #skip if empty
            if(i == None):
                continue
            #skip if lesser
            if (i <= search):
                continue
            diff = i-search
            if (diff < closest):
                closest = diff
                index = i
        return index         
    def findPrevIter(self,search):
        #iterate through the whole list comparing list to find and return the cloest value under
        closest = math.inf
        index = None
        for i in self.data:
            self.trav = self.trav +1
            #skip empty
            if (i == None):
                continue
            #skip greater values
            if (i >= search):
                continue
            diff = search - i
            if (diff < closest):
                closest = diff
                index = i
        return index           
    def findMinIter(self):
        #iterate through tree list and return smallest
        min = math.inf
        for i in self.data:
            self.trav = self.trav +1
            #skip empty values 
            if (i == None):
                continue
            if (i < min):
                min = i
        return min
    def findMaxIter(self):
        #iterate through list and return largest
        max = -math.inf
        for i in self.data:
            self.trav = self.trav +1
            #skip empty
            if (i == None):
                continue
            if (i > max):
                max = i
        return max
    def hasLeftChild(self,index):
        #check if the list is long enough to have a  left child
        return(len(self.data) > (2*(index)+1))
    def hasRightChild(self,index):
        #check if the list is long enough to have a right child
        return(len(self.data) > (2*(index)+2))
    def getLeftChild(self,index):
        # returns the index of a c left hild if it exists
        if(self.hasLeftChild):
            return (2*index+1)
    def getRightChild(self,index):
        #returns the right child of a index if it exists
        if(self.hasRightChild):
            return (2*index+2)
    def printTree(self):
        #prints the values of the tree
        print (self.data)
    def findItemRec(self,item,index=0):
        #if current index is the value retun it
        if (self.data[index]== item):
            return index
        #check if we have childres
        if(self.hasLeftChild(index) and self.hasRightChild(index)):
            #if we have two childen
            if(self.data[self.getLeftChild(index)] != None and self.data[self.getRightChild(index)] != None):
                #see if our childre have the item
                if(self.data[self.getLeftChild(index)] == item):
                    self.trav = self.trav +1
                    return self.getLeftChild(index)
                elif(self.data[self.getRightChild(index)] == item):
                    self.trav = self.trav +1
                    return self.getRightChild(index)
                #recursive call on each child otherwise
                else:
                    self.trav = self.trav +2
                    left = self.findItemRec(item,self.getLeftChild(index))
                    right = self.findItemRec(item,self.getRightChild(index))
                    #return the greater value of each child
                    if(right >left):
                        return right
                    else:
                        return left
            #if we have only have a left child 
            if(self.hasLeftChild(index)):
                #check if it is valid
                if(self.data[self.getLeftChild(index)] != None):
                    #return the child if it contains our value
                    if(self.data[self.getLeftChild(index)] == item):
                        self.trav = self.trav +1
                        return self.getLeftChild(index)
                    else:
                        #recursive call on the child
                        self.trav = self.trav +1
                        left = self.findItemRec(item,self.getLeftChild(index))
                        return left
                #no valid children return indicator
                else:
                    return -1
            #if we only have a right child
            if(self.hasRightChild(index)):
                #check if right child is valid
                if(self.data[self.getRightChild(index)] != None):
                    #check if right child has value
                    if(self.data[self.getRightChild(index)] == item):
                        self.trav = self.trav +1
                        return self.getRightChild(index)
                    #else make recursive call on right child
                    else:
                        self.trav = self.trav +1
                        right = self.findItemRec(item,self.getRightChild(index))
                        return right
                else:
                    return -1
        #we only had one child, check to see which it was
        if(self.hasLeftChild(index)):
            #check if left child is valid
            if(self.data[self.getLeftChild(index)] != None):
                #check if it has the item we are looking for
                if(self.data[self.getLeftChild(index)] == item):
                    self.trav = self.trav +1
                    return self.getLeftChild(index)
                #else recursive call on it
                else:
                    self.trav = self.trav +1
                    left = self.findItemRec(item,self.getLeftChild(index))
                    return left
            #not a valid child
            else:
                return -1
        #check if right child exists
        if(self.hasRightChild(index)):
            #check if it is valid
            if(self.data[self.getRightChild(index)] != None):
                #see if it  has the value we are looking for
                if(self.data[self.getRightChild(index)] == item):
                    self.trav = self.trav +1
                    return self.getRightChild(index)
                # else make a recursive call on the child
                else:
                    self.trav = self.trav +1
                    right = self.findItemRec(self.getRightChild(index))
                    return right
            #not a valid child
            else:
                return -1
        #no child exists
        else:
            return -1
    def findItemIter(self,item):
        #search through the list to find the index of a specfic item
        for i in range(len(self.data)):
            self.trav = self.trav +1
            #skip if empty
            if(self.data[i] == None):
                continue
            #exit on found
            if(self.data[i] == item):
                return i
        #item isnt in tree
        return -1
    def getParent(self, item):
        #root doesnt have a parent
        if (item == 0):
            return 0
        #return parent index otherwise
        else:
            return ((item -1)//2)
    def moveUpRec(self, index, offset = 0):
        #check for kids and set flags
        left = False
        right = False
        #check for both children
        if(self.hasLeftChild(index) and self.hasRightChild(index)):
            #if left is valid set up flag for call
            if(self.getLeftChild(index) != None):
                left = True
            #if right is valid set right flag
            if(self.getRightChild(index) != None):
                right = True
        #move up our self  and clear our spot
        self.data[self.getParent(index)- offset] = self.data[index]
        self.data[index] = None
        #recursive calls based of set flags
        if(left):
            self.trav = self.trav +1
            self.moveUpRec(self.getLeftChild(index),-1)
        if(right):
            self.trav = self.trav +1
            self.moveUpRec(self.getRightChild(index))
    def moveUpIter(self,index):
        children = []
        run = True
        #Start with the current index to find children
        current = [[index, 'r']]
        #build a list of nodes that need to be moved
        while(run):
            #auto exit if no children found
            run = False
            temp = []
            #for ever node to find children for
            for i in current:
                # check if node has valid children
                if(self.hasLeftChild(i[0]) and self.hasRightChild(i[0])):
                    if(self.data[self.getLeftChild(i[0])] != None):
                        #adds left child to list to search through
                        self.trav = self.trav +1
                        temp.append([self.getLeftChild(i[0]),'l'])
                        run = True
                    if(self.data[self.getRightChild(i[0])] != None):
                        #add right child to list to search through
                        self.trav = self.trav +1
                        temp.append([self.getRightChild(i[0]),'r'])
                        run = True
                #add the indexes we just searched through to the movind list
                children.extend(current)
                #update list to search through
                current = temp
        #iterate through the build up list
        for i in children:
            #move up based on if left or right child
            if(i[1] == 'r'):
                self.data[self.getParent(index)] = self.data[i[0]]
            else:
                self.data[self.getParent(index)-1] = self.data[i[0]]
    def sort(self,index=0):
        # set up a string io to catch self.traversial output
        f = io.StringIO()
        with redirect_stdout(f):
            # call a inorder self.traversal
            self.inOrder(0)
        #split caught output into a list and retun the sorted array
        ret = f.getvalue().split()
        return ret
    def inOrder(self, index):
        #standard self.traversal
        if (self.hasLeftChild(index)):
            if(self.data[self.getLeftChild(index)] != None):
                self.inOrder(self.getLeftChild(index))
        print(self.data[index], end=' ')
        if (self.hasRightChild(index)):
            if(self.data[self.getRightChild(index)] != None):
                self.inOrder(self.getRightChild(index))
    def printTrav(self):
        print(self.trav)
class BBST:
    def __init__(self):
        self.data = []
        self.trav = 0
    def insertIter(self,item):
        #create tree if empty
        if(len(self.data) == 0):
            self.data.append(item)
            self.data.append(None)
            self.data.append(None)
        #insert in tree if exists
        else:
            index = 0
            #interate down the tree untill we get to where we need
            while(True):
                self.trav = self.trav +1
                #go left if item is less than current node
                if(self.data[index] > item):
                    #check if left node exists
                    if(self.hasLeftChild(index)):
                        #if empty insert
                        if(self.data[self.getLeftChild(index)] == None):
                            self.data[self.getLeftChild(index)] = item
                            break
                        else:
                            #update current index if slot is full
                            index = self.getLeftChild(index)
                            continue
                    # left node doesnt exist add level and insert
                    else:
                        for i in range(len(self.data)+1):
                            self.data.append(None)
                        self.data[self.getLeftChild(index)] = item
                        break
                #go right because node is greater than current
                else:
                    #check if current node has children
                    if(self.hasRightChild(index)):
                        #if child is empty insert
                        if(self.data[self.getRightChild(index)] == None):
                            self.data[self.getRightChild(index)] = item
                            break
                        #update index if child has value
                        else:
                            index = self.getRightChild(index)
                            continue
                    # next level of tree doesnt exist, generate and insert
                    else:
                        for i in range(len(self.data)+1):
                            self.data.append(None)
                        self.data[self.getRightChild(index)] = item
                        break
        self.balanceTree()  
        
    def deleteIter(self, item):
        #find the index of the item to remove
        index = self.findItemIter(item)
        #if the item is in the tree
        if(index > -1):
            #check if node has 2 childres
            if(self.hasLeftChild(index) and self.hasRightChild(index)):
                #if both are valid find min value in right subtree and swap
                if(self.getLeftChild(index) != None and self.getLeftChild(index) != None):
                    self.trav = self.trav +1
                    mindex = self.findItemIter(self.findMinIter(self.getRightChild(index)))
                    self.data[index] = self.data[mindex]
                    self.data[mindex] = None
                #  check if one is valid
                elif(self.getLeftChild(index) != None or self.getLeftChild(index) != None):
                    #if its left child
                    if(self.getLeftChild(index) != None):
                        # if left child has sub tree, iterate it up
                        if(self.getLeftChild(self.getLeftChild(index)) != None or self.getRightChild(self.getLeftChild(index)) != None):
                            self.trav = self.trav +1
                            self.moveUpIter(self.getLeftChild(index))
                        #swap and remove if no sub child
                        else:
                            self.trav = self.trav +1
                            self.data[index] = self.data[self.getLeftChild(index)]
                            self.data[self.getLeftChild(index)] = None
                    #else its right child
                    else:
                        #move up iteratively if right child has a sub tree
                        if(self.getLeftChild(self.getRightChild(index)) != None or self.getRightChild(self.getRightChild(index)) != None):
                            self.trav = self.trav +1
                            self.moveUpIter(self.getRightChild(index))
                        #swap and remove if no sub tree
                        else:
                            self.trav = self.trav +1
                            self.data[index] = self.data[self.getRightChild(index)]
                            self.data[self.getRightChild(index)] = None
                #remove as we have no children
                else:
                    self.data[index] = None
            #we are at the bottom of a tree just remove
            else:
                self.data[index] = None
    def findNextIter(self,search):
        #iterate through the whole list comparing values to find andreturn the closest value over
        closest = math.inf
        index = None
        for i in self.data:
            self.trav = self.trav +1
            #skip if empty
            if(i == None):
                continue
            #skip if lesser
            if (i <= search):
                continue
            diff = i-search
            if (diff < closest):
                closest = diff
                index = i
        return index         
    def findPrevIter(self,search):
        #iterate through the whole list comparing list to find and return the cloest value under
        closest = math.inf
        index = None
        for i in self.data:
            self.trav = self.trav +1
            #skip empty
            if (i == None):
                continue
            #skip greater values
            if (i >= search):
                continue
            diff = search - i
            if (diff < closest):
                closest = diff
                index = i
        return index           
    def findMinIter(self):
        #iterate through tree list and return smallest
        min = math.inf
        for i in self.data:
            self.trav = self.trav +1
            #skip empty values 
            if (i == None):
                continue
            if (i < min):
                min = i
        return min
    def findMaxIter(self):
        #iterate through list and return largest
        max = -math.inf
        for i in self.data:
            self.trav = self.trav +1
            #skip empty
            if (i == None):
                continue
            if (i > max):
                max = i
        return max
    def hasLeftChild(self,index):
        #check if the list is long enough to have a  left child
        return(len(self.data) > (2*(index)+1))
    def hasRightChild(self,index):
        #check if the list is long enough to have a right child
        return(len(self.data) > (2*(index)+2))
    def getLeftChild(self,index):
        # returns the index of a c left hild if it exists
        if(self.hasLeftChild):
            return (2*index+1)
    def getRightChild(self,index):
        #returns the right child of a index if it exists
        if(self.hasRightChild):
            return (2*index+2)
    def printTree(self):
        #prints the values of the tree
        print (self.data)
    def findItemIter(self,item):
        #search through the list to find the index of a specfic item
        for i in range(len(self.data)):
            self.trav = self.trav +1
            #skip if empty
            if(self.data[i] == None):
                continue
            #exit on found
            if(self.data[i] == item):
                return i
        #item isnt in tree
        return -1
    def getParent(self, item):
        #root doesnt have a parent
        if (item == 0):
            return 0
        #return parent index otherwise
        else:
            return ((item -1)//2)
    def moveUpIter(self,index):
        children = []
        run = True
        #Start with the current index to find children
        current = [[index, 'r']]
        #build a list of nodes that need to be moved
        while(run):
            #auto exit if no children found
            run = False
            temp = []
            #for ever node to find children for
            for i in current:
                # check if node has valid children
                if(self.hasLeftChild(i[0]) and self.hasRightChild(i[0])):
                    if(self.data[self.getLeftChild(i[0])] != None):
                        self.trav = self.trav +1
                        #adds left child to list to search through
                        temp.append([self.getLeftChild(i[0]),'l'])
                        run = True
                    if(self.data[self.getRightChild(i[0])] != None):
                        self.trav = self.trav +1
                        #add right child to list to search through
                        temp.append([self.getRightChild(i[0]),'r'])
                        run = True
                #add the indexes we just searched through to the movind list
                children.extend(current)
                #update list to search through
                current = temp
        #iterate through the build up list
        for i in children:
            #move up based on if left or right child
            if(i[1] == 'r'):
                self.data[self.getParent(index)] = self.data[i[0]]
            else:
                self.data[self.getParent(index)-1] = self.data[i[0]]
    def balanceTree(self):
        #lets play with fire here
        while(not(self.checkBalance())):
            for i in range(len(self.data)-1,-1,-1):
                self.trav = self.trav +1
                if(self.data[i] != None):
                    if(abs(self.getBalance(i)) > 1):
                        if(self.getBalance(i) > 0):
                            self.rightRotate(i)
                            break
                        else:
                            self.leftRotate(i)
                            break
                    #we must break a rotate to mantain intergraty of the for loop
            break
    def getHeight(self, index):
        index = index +1
        return int(math.floor(math.log2(index)))
    def checkBalance(self):
        for i in range(len(self.data)):
            self.trav = self.trav +1
            if (self.data[i] != None):
                if(abs(self.getBalance(i)) > 1):
                    return False
        return True
    def getBalance(self, index):
        left = 0
        right = 0
        leftChildren = []
        rightChildren = []
        if(self.hasLeftChild(index)):
            if(self.data[self.getLeftChild(index)] != None):
                height = 1
                run = True
                #Start with the current index to find children
                current = [[self.getLeftChild(index), height]]
                #build a list of nodes that need to be moved
                while(run):
                #auto exit if no children found
                    run = False
                    temp = []
                    height = height + 1
                    #for ever node to find children for
                    for i in current:
                        # check if node has valid children
                        if(self.hasLeftChild(i[0]) and self.hasRightChild(i[0])):
                            if(self.data[self.getLeftChild(i[0])] != None):
                            #adds left child to list to search through
                                self.trav = self.trav +1
                                temp.append([self.getLeftChild(i[0]),height])
                                run = True
                            if(self.data[self.getRightChild(i[0])] != None):
                            #add right child to list to search through
                                self.trav = self.trav +1
                                temp.append([self.getRightChild(i[0]), height])
                                run = True
                        #add the indexes we just searched through to the movind list
                        leftChildren.extend(current)
                        #update list to search through
                        current = temp
                #print('left children')
                #print(leftChildren)
                if(len(leftChildren) > 0):
                    #print('value of deepest left child')
                    #print(leftChildren[-1])
                    left = leftChildren[-1][1]
            if(self.hasRightChild(index)):
                if(self.data[self.getRightChild(index)] != None):
                    height = 1
                    run = True
                    #Start with the current index to find children
                    current = [[self.getRightChild(index), height]]
                    #build a list of nodes that need to be moved
                    while(run):
                    #auto exit if no children found
                        run = False
                        temp = []
                        height = height + 1
                        #for ever node to find children for
                        for i in current:
                            # check if node has valid children
                            if(self.hasLeftChild(i[0]) and self.hasRightChild(i[0])):
                                if(self.data[self.getLeftChild(i[0])] != None):
                                    #adds left child to list to search through
                                    self.trav = self.trav +1
                                    temp.append([self.getLeftChild(i[0]),height])
                                    run = True
                                if(self.data[self.getRightChild(i[0])] != None):
                                    #add right child to list to search through
                                    self.trav = self.trav +1
                                    temp.append([self.getRightChild(i[0]), height])
                                    run = True
                            #add the indexes we just searched through to the movind list
                            rightChildren.extend(current)
                            #update list to search through
                            current = temp
                    #print('right children')
                    #print(rightChildren)    
                    if(len(rightChildren) > 0):
                        #print('value of deepest right child')
                        #print(rightChildren[-1])
                        right = rightChildren[-1][1]
        #print('value of return')
        #print(left-right)
        return (left - right)
    def leftRotate(self,index, first=True):
        #check for double rotate condition
        dbl = False
        if(first):
            if(self.hasRightChild(index)):
                if(self.data[self.getRightChild(index)] != None):
                    if(self.getBalance(self.getRightChild(index)) > 0):
                        self.trav = self.trav +1
                        self.rightRotate(self.getRightChild(index),False)
        leftChildren = []
        rightRChildren = []
        rightLChildren = []
        if(self.hasLeftChild(index)):
            if(self.data[self.getLeftChild(index)] != None):
                run = True
                #Start with the current index to find children
                current = [[self.getLeftChild(index),'l']]
                #build a list of nodes that need to be moved
                while(run):
                #auto exit if no children found
                    run = False
                    temp = []
                    #for ever node to find children for
                    for i in current:
                        # check if node has valid children
                        if(self.hasLeftChild(i[0]) and self.hasRightChild(i[0])):
                            if(self.data[self.getLeftChild(i[0])] != None):
                            #adds left child to list to search through
                                self.trav = self.trav +1
                                temp.append([self.getLeftChild(i[0]),'l'])
                                run = True
                            if(self.data[self.getRightChild(i[0])] != None):
                            #add right child to list to search through
                                self.trav = self.trav +1
                                temp.append([self.getRightChild(i[0]),'r'])
                                run = True
                        #add the indexes we just searched through to the movind list
                        leftChildren.extend(current)
                        #update list to search through
                        current = temp
                        temp = []
        if(self.hasRightChild(index)):
            if(self.data[self.getRightChild(index)] != None):
                #not typing this out so much
                rindex = self.getRightChild(index)
                if(self.hasLeftChild(rindex)):
                    if(self.data[self.getLeftChild(rindex)] != None):
                        run = True
                        #Start with the current index to find children
                        current = [[self.getLeftChild(rindex),'l']]
                        #build a list of nodes that need to be moved
                        while(run):
                        #auto exit if no children found
                            run = False
                            temp = []
                            #for ever node to find children for
                            for i in current:
                                # check if node has valid children
                                if(self.hasLeftChild(i[0]) and self.hasRightChild(i[0])):
                                    if(self.data[self.getLeftChild(i[0])] != None):
                                        #adds left child to list to search through
                                        self.trav = self.trav +1
                                        temp.append([self.getLeftChild(i[0]),'l'])
                                        run = True
                                    if(self.data[self.getRightChild(i[0])] != None):
                                        #add right child to list to search through
                                        self.trav = self.trav +1
                                        temp.append([self.getRightChild(i[0]),'r'])
                                        run = True
                                #add the indexes we just searched through to the movind list
                                rightLChildren.extend(current)
                                #update list to search through
                                current = temp
                                temp = []
                if(self.hasRightChild(rindex)):
                    if(self.data[self.getRightChild(rindex)] != None):
                        run = True
                        #Start with the current index to find children
                        current = [[self.getRightChild(rindex),'r']]
                        #build a list of nodes that need to be moved
                        while(run):
                        #auto exit if no children found
                            run = False
                            temp = []
                            #for ever node to find children for
                            for i in current:
                                # check if node has valid children
                                if(self.hasLeftChild(i[0]) and self.hasRightChild(i[0])):
                                    if(self.data[self.getLeftChild(i[0])] != None):
                                        #adds left child to list to search through
                                        self.trav = self.trav +1
                                        temp.append([self.getLeftChild(i[0]),'l'])
                                        run = True
                                    if(self.data[self.getRightChild(i[0])] != None):
                                        #add right child to list to search through
                                        self.trav = self.trav +1
                                        temp.append([self.getRightChild(i[0]),'r'])
                                        run = True
                                #add the indexes we just searched through to the movind list
                                rightRChildren.extend(current)
                                #update list to search through
                                current = temp
                                temp = []
            #move left children down
            if(len(leftChildren) > 0):
                for i in range(len(leftChildren)-1,-1,-1):
                    self.trav = self.trav +1
                    if(self.hasLeftChild(leftChildren[i][0])):
                        if(leftChildren[i][1] == "r"):
                            self.data[self.getLeftChild(leftChildren[i][0])-1] = self.data[leftChildren[i][0]]
                            self.data[leftChildren[i][0]] = None
                        else:
                            self.data[self.getLeftChild(leftChildren[i][0])] = self.data[leftChildren[i][0]]
                            self.data[leftChildren[i][0]] = None
                    else:
                        for j in range(len(self.data)+1):
                            self.data.append(None)
                        self.data[self.getLeftChild(leftChildren[i][0])] = self.data[leftChildren[i][0]]
                        self.data[leftChildren[i][0]] = None
            #move Root down
            self.data[self.getLeftChild(index)] = self.data[index]
            self.data[index] = None
            #move right's left sub tree left
            for i in rightLChildren:
                self.trav = self.trav +1
                loc = int(i[0] - (math.pow(2,(self.getHeight(i[0]) - self.getHeight(index) -2))))
                self.data[loc] = self.data[i[0]]
                self.data[i[0]] = None
            #move right up   
            self.trav = self.trav +1
            self.data[index] = self.data[self.getRightChild(index)]
            self.data[self.getRightChild(index)] = None
            # move subtre right up a level
            for i in rightRChildren:
                self.trav = self.trav +1
                #move up based on if left or right child
                if(i[1] == 'r'):
                    self.data[self.getParent(i[0])] = self.data[i[0]]
                    self.data[i[0]] = None
                else:
                    self.data[self.getParent(i[0])-1] = self.data[i[0]]
                    self.data[i[0]] = None
    def rightRotate(self,index,first=True):
        dbl = False
        if(first):
            if(self.hasLeftChild(index)):
                if(self.data[self.getLeftChild(index)] != None):
                    if(self.getBalance(self.getLeftChild(index)) < 0):
                        self.trav = self.trav +1
                        self.leftRotate(self.getLeftChild(index),False)
        #build list of left and right children
        leftLChildren = []
        leftRChildren = []
        rightChildren = []
        if(self.hasLeftChild(index)):
            if(self.data[self.getLeftChild(index)] != None):
                 #not typing this out so much
                lindex = self.getLeftChild(index)
                if(self.hasLeftChild(lindex)):
                    if(self.data[self.getLeftChild(lindex)] != None):
                        run = True
                        #Start with the current index to find children
                        current = [[self.getLeftChild(lindex),'l']]
                        #build a list of nodes that need to be moved
                        while(run):
                        #auto exit if no children found
                            run = False
                            temp = []
                            #for ever node to find children for
                            for i in current:
                                # check if node has valid children
                                if(self.hasLeftChild(i[0]) and self.hasRightChild(i[0])):
                                    if(self.data[self.getLeftChild(i[0])] != None):
                                        #adds left child to list to search through
                                        self.trav = self.trav +1
                                        temp.append([self.getLeftChild(i[0]),'l'])
                                        run = True
                                    if(self.data[self.getRightChild(i[0])] != None):
                                        #add right child to list to search through
                                        self.trav = self.trav +1
                                        temp.append([self.getRightChild(i[0]),'r'])
                                        run = True
                                #add the indexes we just searched through to the movind list
                                leftLChildren.extend(current)
                                #update list to search through
                                current = temp
                                temp = []
                if(self.hasRightChild(lindex)):
                    if(self.data[self.getRightChild(lindex)] != None):
                        run = True
                        #Start with the current index to find children
                        current = [[self.getRightChild(lindex),'r']]
                        #build a list of nodes that need to be moved
                        while(run):
                        #auto exit if no children found
                            run = False
                            temp = []
                            #for ever node to find children for
                            for i in current:
                                # check if node has valid children
                                if(self.hasLeftChild(i[0]) and self.hasRightChild(i[0])):
                                    if(self.data[self.getLeftChild(i[0])] != None):
                                        #adds left child to list to search through
                                        self.trav = self.trav +1
                                        temp.append([self.getLeftChild(i[0]),'l'])
                                        run = True
                                    if(self.data[self.getRightChild(i[0])] != None):
                                        #add right child to list to search through
                                        self.trav = self.trav +1
                                        temp.append([self.getRightChild(i[0]),'r'])
                                        run = True
                            #add the indexes we just searched through to the movind list
                            leftRChildren.extend(current)
                            #update list to search through
                            current = temp
                            temp = []
        if(self.hasRightChild(index)):
            if(self.data[self.getRightChild(index)] != None):
                run = True
                #Start with the current index to find children
                current = [[self.getRightChild(index),'r']]
                #build a list of nodes that need to be moved
                while(run):
                #auto exit if no children found
                    run = False
                    temp = []
                    #for ever node to find children for
                    for i in current:
                        # check if node has valid children
                        if(self.hasLeftChild(i[0]) and self.hasRightChild(i[0])):
                            if(self.data[self.getLeftChild(i[0])] != None):
                                #adds left child to list to search through
                                self.trav = self.trav +1
                                temp.append([self.getLeftChild(i[0]),'l'])
                                run = True
                            if(self.data[self.getRightChild(i[0])] != None):
                                #add right child to list to search through
                                self.trav = self.trav +1
                                temp.append([self.getRightChild(i[0]),'r'])
                                run = True
                            #add the indexes we just searched through to the movind list
                            rightChildren.extend(current)
                            #update list to search through
                            current = temp
                            temp = []
        #move whole right sub tree down
        if(len(rightChildren) > 0):
            for i in range(len(rightChildren)-1,-1,-1):
                self.trav = self.trav +1
                if(self.hasRightChild(rightChildren[i][0])):
                    if(rightChildren[i][1] == 'r'):
                        self.data[self.getRightChild(rightChildren[i][0])] = self.data[rightChildren[i][0]]
                        self.data[rightChildren[i][0]] = None
                    else:
                        self.data[self.getRightChild(rightChildren[i][0])+1] = self.data[rightChildren[i][0]]
                        self.data[rightChildren[i][0]] = None
                else:
                    for j in range(len(self.data)+1):
                        self.data.append(None)
                    self.data[self.getRightChild(rightChildren[i][0])] = self.data[rightChildren[i][0]]
                    self.data[rightChildren[i][0]] = None
        #move root down
        self.trav = self.trav +1
        self.data[self.getRightChild(index)] = self.data[index]
        self.data[index] = None
        #move left's right sub tree over
        for i in leftRChildren:
            self.trav = self.trav +1
            if (index > 0):
                loc = int(i[0] + math.pow(2,(self.getHeight(i[0])- self.getHeight(index)-1))-1)
            else:
                loc = int(i[0] + math.pow(2,(math.floor(math.log2(i[0]))-1) -1))
            self.data[loc] = self.data[i[0]]
            self.data[i[0]] = None
        #move left to root
        self.trav = self.trav +1
        self.data[index] = self.data[self.getLeftChild(index)]
        self.data[self.getLeftChild(index)] = None
        # move subtre right up a level
        for i in leftLChildren:
            self.trav = self.trav +1
            #move up based on if left or right child
            if(i[1] == 'r'):
                self.data[self.getParent(i[0])+1] = self.data[i[0]]
                self.data[i[0]] = None
            else:
                self.data[self.getParent(i[0])] = self.data[i[0]]
                self.data[i[0]] = None
    def printTrav(self):
        print(self.trav)
def getRandomArray(n):
    #generate a range as a list and shuffle it
    ret = list(range(n))
    random.shuffle(ret)
    return ret
def getSortedArray(n):
    #build a list from a range and return
    ret = list(range(n,-1,-1))
    return ret
itertree = BST()
rectree = BST()
avltree = BBST()

items = getRandomArray(2500)
start = time.time()
for i in items:
    itertree.insertIter(i)
print("--- %s seconds ---" % (time.time() - start))
itertree.printTrav()
print('for iter Bst')
start = time.time()
for i in items: 
    rectree.insertRec(i)
print("--- %s seconds ---" % (time.time() - start))
rectree.printTrav()
print('for rec Bst')
start = time.time()
for i in items:
    avltree.insertIter(i)
print("--- %s seconds ---" % (time.time() - start))
avltree.printTrav()
print('for Avl') 

itertree2 = BST()
rectree2 = BST()
avltree2 = BBST()
items = getSortedArray(20)
start = time.time()
for i in items:
    itertree2.insertIter(i)
print("--- %s seconds ---" % (time.time() - start))
itertree2.printTrav()
print('for iter Bst')
start = time.time()
for i in items: 
    rectree2.insertRec(i)
print("--- %s seconds ---" % (time.time() - start))
rectree2.printTrav()
print('for rec Bst')
start = time.time()
for i in items:
    avltree2.insertIter(i)
print("--- %s seconds ---" % (time.time() - start))
avltree2.printTrav()
print('for Avl')   
print('finished')

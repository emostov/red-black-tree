# -*- coding: utf-8 -*-
"""
Created on Wed Oct 17 19:16:20 2018

@author: ZekeMostov

This implementation of a red black tree has 3 classes - TNil which is representive
of the sentinal in our text, Node which represents a node of the tree with all
its pointers and key, and RBT which stores the root of the tree and I definie
everything but drawing the tree and searching. Built into RBT are the user friendly
functions RBT.myinsert(key), RBT.mysearch(key), and RBT.mydelete(key). 
These are desinged
so the user does not have to make a node or specify a node and can just enter
a key that represents the node. The user must first though create a tree object
and then they can use the desired functions on. All the algorithms closely follow
our book

All keys given to the program must be an int

Also, cannot handle the insertion of multiple keys with the same value

For drawing, I have built setup(root), which takes a root node and recursively
draws the tree with recurse() in a turtle window. After the first call to setup()
everytime after setup() is called  again (which includes 
every delete and insert) you must close the existing turtle window so
turtle can redraw an updated tree 
"""
import turtle
BLACK = "BLACK"
RED = "RED"

class TNil:
    #equivalent t.Nill in text
    def __init__(self):
        self.color = BLACK
        

#initializing T.nil
TNIL = TNil()

class Node(object):
    # creates a node with attributes as described in textbook
    def __init__(self, key, color=RED, left=TNIL, right=TNIL, p=TNIL):
       
        self.color = color
        self.key = key
        self.left = left
        self.right = right
        self.p = p
        
    def inorder(self):
        #prints out the tree in order using the given node as a root
        #example would be to do T.root.inorder()
        if self.left != TNIL:
            self.left.inorder()
        print (self.key)
        if self.right != TNIL:
            self.right.inorder()
            

class RBT:
    '''
    class describing a red black tree and operations as described in our 
    textbook
    red black tree that is initialized witb a root of T.nil
    user interface function are RBT.myinsert(key), RBT.mydelete(key), and
    RBT.mysearch(key) which prints wether or not the key is in the tree

    '''
    def __init__(self):
        self.root = TNIL
        
    def leftrotate(self, x):
        '''
        left rotate are and right rotate are coded as described in our textbook
        and take a node as input
        '''
        y = x.right
        x.right = y.left
        if (y.left != TNIL):
            y.left.p = x
        y.p = x.p
        if (x.p == TNIL):
            self.root = y
        elif (x == x.p.left):
            x.p.left = y
        else:
            x.p.right = y
        y.left = x
        x.p = y

    def rightrotate(self, x):
        y = x.left
        x.left = y.right
        if x.right != TNIL:
            y.right.p = x
        y.p = x.p
        if x.p == TNIL:
            self.root = y
        elif (x == x.p.right):
            x.p.right = y
        else:
            x.p.left = y
        y.right = x
        x.p = y

    def insert(self, z):
        '''
        insert takes a node z as input and closely follows the algorithm of 
        rbt insert and rbt fixup as describbed in our text book
        '''
        y = TNIL
        x = self.root
        while x != TNIL:
            y = x
            if z.key < x.key:
                x = x.left
            else:
                x = x.right
        z.p = y

        if y == TNIL:
            self.root = z
        elif z.key < y.key:
            y.left = z
        else:
            y.right = z
        z.left = TNIL
        z.right = TNIL

        z.color = RED
        while z.p.color == RED and z != self.root:
            if z.p == z.p.p.left:
                y = z.p.p.right
                if y.color == RED:
                    z.p.color = BLACK
                    y.color = BLACK 
                    z.p.p.color = RED
                    z = z.p.p
                else:
                    if z == z.p.right:
                        z = z.p
                        self.leftrotate(z)
                    z.p.color = BLACK
                    z.p.p.color = RED
                    self.rightrotate(z.p.p)
            else:
                y = z.p.p.left
                if y.color == RED:
                    z.p.color = BLACK
                    y.color = BLACK 
                    z.p.p.color = RED
                    z = z.p.p
                else:
                    if z == z.p.left:
                        z = z.p
                        self.rightrotate(z)
                    z.p.color = BLACK
                    z.p.p.color = RED
                    self.leftrotate(z.p.p)
        self.root.color = BLACK
        
    def transplant(self, u, v):
        #as described in textbook
        if u.p == TNIL:
            self.root = v
        elif u == u.p.left:
            u.p.left = v
        else:
            u.p.right = v
        v.p = u.p
    
    def minimum(self, x):
        #as described in textbook
        while x.left != TNIL:
            x = x.left
        return x
        
    def delete_fixup(self, x):
        #coded as described in our text book
        while x != self.root and x.color == BLACK:
            if x == x.p.left:
                w = x.p.right
                if w.color == RED:
                    w.color = BLACK
                    x.p.color = RED
                    self.leftrotate(x.p)
                    w = x.p.right
                    
                if w.left.color == BLACK and w.right.color == BLACK:
                    w.color = RED
                    x = x.p
                else:
                    if w.right.color == BLACK:
                        w.left.color = BLACK
                        w.color = RED
                        self.rightrotate(w)
                        w = x.p.right
                    w.color = x.p.color
                    x.p.color = BLACK
                    w.right.color = BLACK
                    self.leftrotate(x.p)
                    x = self.root
                
            else:
                w = x.p.left
                if w.color == RED:
                    w.color = BLACK
                    x.p.color = RED
                    self.rightrotate(x.p)
                    w = x.p.left
                if w.right.color == BLACK and w.left.color == BLACK:
                    w.color = RED
                    x = x.p
                else:
                    if w.left.color == BLACK:
                        w.right.color = BLACK
                        w.color = RED
                        self.leftrotate(w)
                        w = x.p.left
                    w.color = x.p.color
                    x.p.color = BLACK
                    w.left.color = BLACK
                    self.rightrotate(x.p)
                    x = self.root
        x.color = BLACK

            
    
    def delete(self, z):
        y=z
        y_original_color = y.color
        if z.left == TNIL:
            x = z.right
            self.transplant(z, z.right)
        elif (z.right == TNIL):
                x = z.left
                self.transplant(z, z.left)
        else: 
            y = self.minimum(z.right)
            y_original_color = y.color
            x = y.right
            if y.p == z:
                x.p = y
            else:
                self.transplant(y, y.right)
                y.right = z.right
                y.right.p = y
            self.transplant(z,y)
            y.left = z.left
            y.left.p = y
            y.color = z.color
        if y_original_color == BLACK:
            self.delete_fixup(x)
    
    def myinsert(self, key):
        #creates a node using the specified key and then inserts into tree
        x = Node(key)
        self.insert(x)
        setup(self.root)
    
    def mydelete(self, key):
        #searches to verify key exists, and if does it will delete node associated
        #with that key. If not it will print a message that key could not be found
        if search(self.root, key) == TNIL:
            print("This key does not exist in the tree - will not delete")
        else:
            x = search(self.root, key)
            self.delete(x)
            setup(self.root)
    
    def mysearch(self, key):
        #calls search starting from the root of the tree and prints a message
        #saying wether or not a node with the entered key is found
        if search(self.root, key) == TNIL:
            print("This key does not exist in the tree")
            
        else:
            print("A node with key: " + str(key) + " was found in the tree")
        
    
        
  
def search(x, k):
    '''
    takes a root node and key k. if it does not found a node with key a key =
    to k it will return a TNil object - the equivalent of t.Nil in our text
    '''
    if x == TNIL or k == x.key:
        return x
    if k < x.key:
        return search(x.left, k)
    else:
        return search(x.right, k)
 
def setup(root):
    '''
    Takes a node and uses it as a root to draw the tree with turtle
    by calling the recrusive function recurse. This function setups
    turtle so it does not freeze once recurse is dones
    Also sets up var, which decreases whith each level so node width decreases
    Currently this is optimized for drawing trees of height 7 or less
    Would have to increase var if wanted to draw a higher tree and not
    have nodes overlap
    Note that the Nil nodes are not represented in the drawing but are assumed
    '''
    var = 300 #variable that gets smaller with each level so tree draws correctly

    turtle.screensize(1100, 1100)
    recurse(root, var)
    turtle.screen.exitonclick()
    

def recurse(z, var):
    '''
    This function recursively draws the tree by draw the right subtree
    and then the left subtree. It takes node z, which is the root of the tree
    being drawn and var, which controls how far the nodes are apart on the x
    axis and decrease by .5 with each call so the nodes dont overlap
    It must be called using setup() in order to work properly
    '''
    if z == TNIL:
        return
        
    pos = turtle.position()
    turtle.pendown()
    if z.color == RED:
        turtle.color("red")
    else:
        turtle.color("black")
    turtle.dot(size=8)
    turtle.penup
    
    turtle.goto(pos)
    turtle.setheading(90)
    turtle.forward(3)
    if z.color == RED:
        turtle.color("red")
    else:
        turtle.color("black")
    turtle.write(z.key, True, align="center", font=("Arial", 10, "normal"))
    turtle.color("black")
    
    if z.right != TNIL:
        turtle.pendown()
        turtle.goto((pos[0]+var),(pos[1]-25))
        recurse(z.right, (var*.5))
        turtle.penup()
        turtle.goto(pos)
        
    if z.left != TNIL:
        turtle.pendown()
        turtle.goto((pos[0]-var),(pos[1]-25))
        recurse(z.left, (var*.5))
        turtle.penup()
        turtle.goto(pos)
        

    

 







    
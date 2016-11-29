#!/usr/bin/python
# -*- coding: utf-8 -*-
#title           :plotlety.py
#author:         :Lawrence Fernandes
#copyright       :(C) 2016 Lawrence Fernandes <lawrencefernandes@acm.org>
#date            :2016/11/29
#version         :1.0
#usage           :python plotlety.py [function]
#python_version  :2.7.12 and 3.5.2
#description     :plotlety is a very simple pure Python math graphics plotter capable of 
#                 drawing 2D and 3D graphics. It requires PyOpenGL and numpy.
#========================================================================================

#-----------------------
# IMPORT PYTHON MODULES
#-----------------------
import os, sys
from math import *
from time import localtime, strftime
#-------------------------
# IMPORT EXTERNAL MODULES
#-------------------------
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from numpy import *

#------------------
# GLOBAL VARIABLES
#------------------
display_width = 800
display_height = 600

minX = -5.0
maxX = 5.0
stepX = 0.5
minY = -5.0
maxY = 5.0
stepY = 0.5

g_fViewDistance = 9.0
g_nearPlane = 1.0
g_farPlane = 1000.0

action = ""
xStart = yStart = 0.0
zoom = 65.0

xRotate = 0.0
yRotate = 0.0
zRotate = 0.0

xTrans = 0.0
yTrans = 0.0

#-----------------------
# OPENGL INITIALIZATION
#-----------------------
def init2D():
    """ OpenGL initialization function for 2D graphics."""
    glClearColor(0.0, 0.0, 0.0, 0.0)
    gluOrtho2D(-5.0, 5.0, -5.0, 5.0)

def init3D():
    """ OpenGL initialization function for 3D graphics."""
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)
    glShadeModel(GL_SMOOTH)
    resetView()

#----------------------
# FUNCTION CONSTRUCTOR
#----------------------
def f(x,y):
    """ Specify the 3D math function."""
    return eval(sys.argv[1])

#--------------------
# SCENE CONSTRUCTORS
#--------------------
def plotFunction2D():
    """ Scene constructor for 2D graphics."""
    glClear(GL_COLOR_BUFFER_BIT) # Clear frame buffer
    glColor3f(0.0, 0.0, 0.0)
    glPointSize(3.0)
    glBegin(GL_LINES)
    glColor3f(0.4,0.7,0)
    glVertex2f(-5.0,0.0)
    glColor3f(0.4,0.7,0)
    glVertex2f(5.0, 0.0)
    glColor3f(0.4,0.7,0)
    glVertex2f(0.0, 5.0)
    glColor3f(0.4,0.7,0)
    glVertex2f(0.0,-5.0)
    glEnd()
    for x in arange(-5.0, 5.0, 0.05):
        y = eval(sys.argv[1])
        glBegin(GL_POINTS)
        glVertex2f(x, y)
        glColor3f(0.4,0.7,0)
        glEnd()
    glFlush() # It could be substituted by glutSwapBuffers()

def plotFunction3D():
    """ Scene constructor for 3D graphics."""
    global minX, maxX, stepX, minY, maxY, stepY, xRotate, yRotate, zRotate
    # Clear frame buffer and depth buffer
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    # Set up viewing transformation, looking down -Z axis
    glLoadIdentity()
    gluLookAt(20, -50, -g_fViewDistance, 0, 0, 0, -0.1, 0, 0)
    # Set perspective (also zoom)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(zoom, float(display_width)/float(display_height), g_nearPlane, g_farPlane)
    glMatrixMode(GL_MODELVIEW)
    polarView()
    glRotate(90,0.0,0.0,1.0)
    # Viewing transformation
    gluLookAt(0, 0, 0, 1, 1, 1, 0, 1, 1)
    # Modeling transformation 
    glScalef(1.0, 2.0, 1.0)
    glBegin(GL_LINES)
    glColor3f(0.4,0.7,0)
    for x in arange(minX, maxX, stepX):
        for y in arange(minY, maxY, stepY):
            glVertex3f(x,y,f(x,y))
            glVertex3f(x,y+stepY,f(x,y+stepY))
            glVertex3f(x,y,f(x,y))
            glVertex3f(x+stepX,y,f(x+stepX,y))
    # Draw axis x,y,z
    glColor3f(1, 0, 0)
    glVertex3f(-50, -2, -20)
    glVertex3f(50, -2, -20)
    glColor3f(0, 1, 0)
    glVertex3f(0, -50, -20)
    glVertex3f(0, 50, -20)
    glColor3f(0, 0, 1)
    glVertex3f(0, -2, -100)
    glVertex3f(0, -2, 10)
    glEnd()
    glutSwapBuffers()

#--------
# VIEWER
#--------
def printHelp():
    """ This function prints the command options avaiable for 3D graphics."""
    print("""\n
         -------------------------------------------------------------------\n
         Left Mousebutton   - move eye position (+ Shift for third axis)\n
         Middle Mousebutton - translate the scene\n
         Right Mousebutton  - move up / down to zoom in / out\n
         Key 'R'            - reset viewpoint\n
         Key 'Q'            - exit the program\n
         -------------------------------------------------------------------\n
         """)

def resetView():
    """ This function is used to reset the view in the 3D graphics mode."""
    global zoom, xRotate, yRotate, zRotate, xTrans, yTrans
    zoom = 65.0
    xRotate = 0.0
    yRotate = 0.0
    zRotate = 0.0
    xTrans = 0.0
    yTrans = 0.0
    glutPostRedisplay()

def reshape(width, height):
    """ This function is used to reshape/resize the glut window."""
    global display_width, display_height
    if height == 0:       # Prevent A Divide By Zero If The Window Is Too Small 
        height = 1
    display_width = width
    display_height = height
    glViewport(0, 0, display_width, display_height)

def polarView():
    """ This function enables the orbit moviments in the 3D scene."""
    glTranslatef(yTrans/100.0, 0.0, 0.0)
    glTranslatef(0.0, -xTrans/100.0, 0.0)
    glRotatef(-zRotate, 0.0, 0.0, 1.0)
    glRotatef(-xRotate, 1.0, 0.0, 0.0)
    glRotatef(-yRotate, 0.0, 1.0, 0.0)

def keyboard(key, x, y):
    """ This function specifies the mouse commands."""
    global zTr, yTr, xTr
    if(key=='r'): resetView()
    if(key=='q'): exit(0)
    glutPostRedisplay()

def mouse(button, state, x, y):
    """ This function specifies the mouse commands."""
    global action, xStart, yStart
    if (button==GLUT_LEFT_BUTTON):
        if (glutGetModifiers() == GLUT_ACTIVE_SHIFT):
            action = "MOVE_EYE_2"
        else:
            action = "MOVE_EYE"
    elif (button==GLUT_MIDDLE_BUTTON):
        action = "TRANS"
    elif (button==GLUT_RIGHT_BUTTON):
        action = "ZOOM"
    xStart = x
    yStart = y

def motion(x, y):
    """ This function evaluates the mouse commands."""
    global zoom, xStart, yStart, xRotate, yRotate, zRotate, xTrans, yTrans
    if (action=="MOVE_EYE"):
        xRotate += x - xStart
        yRotate -= y - yStart
    elif (action=="MOVE_EYE_2"):
        zRotate += y - yStart
    elif (action=="TRANS"):
        xTrans += x - xStart
        yTrans += y - yStart
    elif (action=="ZOOM"):
        zoom -= y - yStart
        if zoom > 150.0:
            zoom = 150.0
        elif zoom < 1.1:
            zoom = 1.1
    else:
        print("unknown action\n", action)
    xStart = x
    yStart = y 
    glutPostRedisplay()

#------
# MENU
#------
def menu():
    """ This function creates an options menu."""
    print('\nUsage: %s [function]' % sys.argv[0])
    print('\nExamples:')
    print('  %s x**2' % sys.argv[0])
    print('  %s 2*x**3-x**2+5' % sys.argv[0])
    print('  %s x**2+y**2/4**2' % sys.argv[0])
    print('\n')

#------
# MAIN
#------
def main():
    """ This is the main function of the module."""
    print('\n\nStarting Plotlety 1.0 at %s' % strftime("%Y-%m-%d %H:%M:%S", localtime()))
    print('(c) 2016 Lawrence Fernandes')
    if len(sys.argv) > 1:
        function = sys.argv[1]
        if "help" in function:
            menu()
        else:
            # GLUT Window Initialization
            glutInit()
            glutInitWindowSize(display_width,display_height)
            glutInitWindowPosition((glutGet(GLUT_SCREEN_WIDTH)-display_width)/2,(glutGet(GLUT_SCREEN_HEIGHT)-display_height)/2)
            glutCreateWindow("Plotlety")
            if "y" not in function:
                # Initialize OpenGL graphics state for 2D graphics
                init2D()
                # Register callbacks
                glutDisplayFunc(plotFunction2D)
                glutKeyboardFunc(keyboard)
            else:
                # Initialize OpenGL graphics state for 3D graphics
                init3D()
                # Register callbacks
                glutReshapeFunc(reshape)
                glutDisplayFunc(plotFunction3D)
                glutMouseFunc(mouse)
                glutMotionFunc(motion)
                glutKeyboardFunc(keyboard)
                printHelp()
            # Turn the flow of control over to GLUT
            glutMainLoop()
    else:
        print("\nInvalid usage! Needs to specify a function.")
        print("Hint: Use 'help' for more information.\n")

# Standard boilerplate to call the main function to begin the program.
if __name__ == '__main__':
    main()

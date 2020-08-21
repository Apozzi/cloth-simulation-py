import math
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

w,h= 650,650

bounce = 0.9
gravity = 0.9
friction = .99

sticks = []
points = []

class Point:
    x, y = 0.0, 0.0
    oldx, oldy = 0.0, 0.0
    bounce, gravity, friction = 0.0, 0.0, 0.0

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.oldx = x-5
        self.oldy = y-5


class Stick:
    p0, p1 = None, None
    distancev = 0.0

    def __init__(self, p0, p1):
        self.p0 = p0
        self.p1 = p1
        self.distancev = self.distance(p0, p1)


    def distance (self, p0, p1):
        dx = p1.x - p0.x
        dy = p1.y - p0.y
        return (dx * dx + dy * dy)**(1/2)


def updatePoints():
    for p in points:
        vx = (p.x - p.oldx) * friction
        vy = (p.y - p.oldy) * friction

        p.oldx = p.x
        p.oldy = p.y

        p.x += vx
        p.y += vy
        p.y += gravity

        if (p.x > w):
            p.x = w
            p.oldx = p.x + vx * bounce
        if (p.x < 0):
            p.x = 0
            p.oldx = p.x + vx * bounce
        if (p.y > h):
            p.y = h
            p.oldy = p.y + vy * bounce
        if (p.y < 0):
            p.y = 0
            p.oldy = p.y + vy * bounce


def updateSticks():
	for stick in sticks:
		dx = stick.p1.x - stick.p0.x
		dy = stick.p1.y - stick.p0.y

		distance = math.sqrt(dx * dx + dy * dy)
		difference = stick.distancev
		percent = (difference - distance) / 1000 ## idk this works?
		print(" distance " + str(distance) )
		print(" difference " + str(difference))
		print(" percent " + str(percent))
		adjustX = dx * percent
		adjustY = dy * percent

		stick.p0.x -= adjustX
		stick.p0.y -= adjustY
		stick.p1.x += adjustX
		stick.p1.y += adjustY


def renderPoint(x , y):
    glPointSize(8)
    glBegin( GL_POINTS )
    glColor3f(1,0,0)
    glVertex2d(x, h - y)
    glEnd()


def renderLine(x0 , y0 , x1, y1):
    glLineWidth(3)
    glBegin( GL_LINES )
    glColor3f(0,0,0)
    glVertex2d(x0, h - y0)
    glVertex2d(x1, h - y1)
    glEnd()

        

def loop():
    for stick in sticks:
        renderLine(stick.p0.x, stick.p0.y ,stick.p1.x ,stick.p1.y)
    for point in points:
        renderPoint(point.x , point.y)
    updatePoints()
    updateSticks()

    points[0].x = 100
    points[0].y = 0
    
    points[9].x = 500
    points[9].y = 0


def load():
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-1.0, w, 0.0, h, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()

def showScreen():
    glClearColor(1, 1, 1, 1)
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    load()
    glColor3f(1.0, 0.0, 3.0)
    loop()
    glutSwapBuffers()

def mouseClick(button, state, x, y):
    if(button == GLUT_LEFT_BUTTON and state == GLUT_DOWN):
        points[90].x -= 70
        points[90].y -= 70


for k in range(2, 12):
   for i in range(2, 12):
     points.append(Point(i*20, k*20))

kold = 0
iold = 0
for k in range(0, 10):
    for i in range(0, 10):
        if (i != 0 and iold != 9):
            sticks.append(Stick(points[i + 10*k] , points[iold + 10*k]))
        sticks.append(Stick(points[i + 10*k] , points[i + 10*kold]))
        iold = i
    kold = k

glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(650, 650)
glutInitWindowPosition(0, 0)
wind = glutCreateWindow("Verlet Integration")
glutMouseFunc(mouseClick)
glutDisplayFunc(showScreen)
glutIdleFunc(showScreen)
glutMainLoop()

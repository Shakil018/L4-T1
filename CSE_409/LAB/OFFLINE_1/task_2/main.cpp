
#include<stdio.h>
#include<stdlib.h>
#include<math.h>

#include <windows.h>
#include <GL/glut.h>

#define pi (2*acos(0.0))
#define UPPER 1
#define LOWER 2

double cameraHeight;
double cameraAngle;
int drawgrid;
int drawaxes;
double angle;
double cylHeight, sphereRadius, MaxRadius, squareLen;


struct point
{
	double x,y,z;
};

struct point pos, up, right, looking;


void drawAxes()
{
	if(drawaxes==1)
	{
		glColor3f(1.0, 1.0, 1.0);
		glBegin(GL_LINES);{
			glVertex3f( 100,0,0);
			glVertex3f(-100,0,0);

			glVertex3f(0,-100,0);
			glVertex3f(0, 100,0);

			glVertex3f(0,0, 100);
			glVertex3f(0,0,-100);
		}glEnd();
	}
}


void drawGrid()
{
	int i;
	if(drawgrid==1)
	{
		glColor3f(0.6, 0.6, 0.6);	//grey
		glBegin(GL_LINES);{
			for(i=-8;i<=8;i++){

				if(i==0)
					continue;	//SKIP the MAIN axes

				//lines parallel to Y-axis
				glVertex3f(i*10, -90, 0);
				glVertex3f(i*10,  90, 0);

				//lines parallel to X-axis
				glVertex3f(-90, i*10, 0);
				glVertex3f( 90, i*10, 0);
			}
		}glEnd();
	}
}

void drawSquare(double a)
{
    //glColor3f(1.0,0.0,0.0);

	glBegin(GL_QUADS);{
		glVertex3f( a, a, 0);
		glVertex3f( a,-a, 0);
		glVertex3f(-a,-a, 0);
		glVertex3f(-a, a, 0);
	}glEnd();

    /*
	glBegin(GL_QUADS);{
		glVertex3f( first.x, first.y, first.z);
		glVertex3f( second.x, second.y, second.z);
        glVertex3f( second.x, second.y, -second.z);
		glVertex3f( first.x, first.y, -first.z);

	}glEnd();
	*/

}


void drawCircle(double radius,int segments)
{
    int i;
    struct point points[100];
    glColor3f(0.7,0.7,0.7);
    //generate points
    for(i=0;i<=segments;i++)
    {
        points[i].x=radius*cos(((double)i/(double)segments)*2*pi);
        points[i].y=radius*sin(((double)i/(double)segments)*2*pi);
    }
    //draw segments using generated points
    for(i=0;i<segments;i++)
    {
        glBegin(GL_LINES);
        {
			glVertex3f(points[i].x,points[i].y,0);
			glVertex3f(points[i+1].x,points[i+1].y,0);
        }
        glEnd();
    }
}

void drawOneFourthCyllinder(double radius, double height, int slices, int stacks, double offsetX, double offsetY)
{

    struct point points[100][100];
	int i,j;
	double h,r;
	//generate points
    r = radius;

	for(i=0; i<=stacks; i++)
	{
        h = ((double)height/2)*((double)i/(double)stacks);

		for(j=0; j<=slices; j++)
		{
		    if(offsetX > 0 && offsetY > 0)
            {
                points[i][j].x = r*cos(((double)j/(double)slices)*pi/2) + offsetX;
                points[i][j].y = r*sin(((double)j/(double)slices)*pi/2) + offsetY;

		    }
		    else if(offsetX < 0 && offsetY > 0)
            {
                points[i][j].x = -r*cos(((double)j/(double)slices)*pi/2) + offsetX;
                points[i][j].y = r*sin(((double)j/(double)slices)*pi/2) + offsetY;

            }
            else if(offsetX < 0 && offsetY < 0)
            {
                points[i][j].x = -r*cos(((double)j/(double)slices)*pi/2) + offsetX;
                points[i][j].y = -r*sin(((double)j/(double)slices)*pi/2) + offsetY;

            }
            else if(offsetX > 0 && offsetY < 0)
            {
                points[i][j].x = r*cos(((double)j/(double)slices)*pi/2) + offsetX;
                points[i][j].y = -r*sin(((double)j/(double)slices)*pi/2) + offsetY;

            }


		    /*
			points[i][j].x = r*cos(((double)j/(double)slices)*pi/2) + offsetX;
			points[i][j].y = r*sin(((double)j/(double)slices)*pi/2) + offsetY;
			*/

			points[i][j].z = h;
		}
	}


    for(i=0; i<stacks; i++)
    {
        //glColor3f((double)i/(double)stacks,(double)i/(double)stacks,(double)i/(double)stacks);
		for(j=0;j<slices;j++)
		{
			glBegin(GL_QUADS);{
			    //upper hemisphere
				glVertex3f(points[i][j].x,points[i][j].y,points[i][j].z);
				glVertex3f(points[i][j+1].x,points[i][j+1].y,points[i][j+1].z);
				glVertex3f(points[i+1][j+1].x,points[i+1][j+1].y,points[i+1][j+1].z);
				glVertex3f(points[i+1][j].x,points[i+1][j].y,points[i+1][j].z);
                //lower hemisphere
                glVertex3f(points[i][j].x,points[i][j].y,-points[i][j].z);
				glVertex3f(points[i][j+1].x,points[i][j+1].y,-points[i][j+1].z);
				glVertex3f(points[i+1][j+1].x,points[i+1][j+1].y,-points[i+1][j+1].z);
				glVertex3f(points[i+1][j].x,points[i+1][j].y,-points[i+1][j].z);
			}glEnd();
		}
    }
}

void drawCone(double radius,double height,int segments)
{
    int i;
    double shade;
    struct point points[100];
    //generate points
    for(i=0;i<=segments;i++)
    {
        points[i].x=radius*cos(((double)i/(double)segments)*2*pi);
        points[i].y=radius*sin(((double)i/(double)segments)*2*pi);
    }
    //draw triangles using generated points
    for(i=0;i<segments;i++)
    {
        //create shading effect
        if(i<segments/2)shade=2*(double)i/(double)segments;
        else shade=2*(1.0-(double)i/(double)segments);
        glColor3f(shade,shade,shade);

        glBegin(GL_TRIANGLES);
        {
            glVertex3f(0,0,height);
			glVertex3f(points[i].x,points[i].y,0);
			glVertex3f(points[i+1].x,points[i+1].y,0);
        }
        glEnd();
    }
}

void drawOneEighthSphere(double radius, int slices, int stacks, int direction)
{
    struct point points[100][100];
    int i, j;
    double h, r;

    for(i=0;i<=stacks;i++)
	{
		h=radius*sin(((double)i/(double)stacks)*(pi/2));
		r=radius*cos(((double)i/(double)stacks)*(pi/2));
		for(j=0;j<=slices;j++)
		{
			points[i][j].x = r*cos(((double)j/(double)slices)*pi/2);
			points[i][j].y = r*sin(((double)j/(double)slices)*pi/2);
			points[i][j].z = h;
		}
	}

	for(i=0;i<stacks;i++)
	{
        //glColor3f((double)i/(double)stacks,(double)i/(double)stacks,(double)i/(double)stacks);
		for(j=0;j<slices;j++)
		{
			glBegin(GL_QUADS);{
			    if(direction == UPPER)
                {
                    //upper hemisphere
                    glVertex3f(points[i][j].x,points[i][j].y,points[i][j].z);
                    glVertex3f(points[i][j+1].x,points[i][j+1].y,points[i][j+1].z);
                    glVertex3f(points[i+1][j+1].x,points[i+1][j+1].y,points[i+1][j+1].z);
                    glVertex3f(points[i+1][j].x,points[i+1][j].y,points[i+1][j].z);
                }
                else{

                    //lower hemisphere

                    glVertex3f(points[i][j].x,points[i][j].y,-points[i][j].z);
                    glVertex3f(points[i][j+1].x,points[i][j+1].y,-points[i][j+1].z);
                    glVertex3f(points[i+1][j+1].x,points[i+1][j+1].y,-points[i+1][j+1].z);
                    glVertex3f(points[i+1][j].x,points[i+1][j].y,-points[i+1][j].z);

                }

                //lower hemisphere
                /*
                glVertex3f(points[i][j].x,points[i][j].y,-points[i][j].z);
				glVertex3f(points[i][j+1].x,points[i][j+1].y,-points[i][j+1].z);
				glVertex3f(points[i+1][j+1].x,points[i+1][j+1].y,-points[i+1][j+1].z);
				glVertex3f(points[i+1][j].x,points[i+1][j].y,-points[i+1][j].z);
				*/
			}glEnd();
		}
	}

}


void drawSphere(double radius,int slices,int stacks)
{
	struct point points[100][100];
	int i,j;
	double h,r;
	//generate points
	for(i=0;i<=stacks;i++)
	{
		h=radius*sin(((double)i/(double)stacks)*(pi/2));
		r=radius*cos(((double)i/(double)stacks)*(pi/2));
		for(j=0;j<=slices;j++)
		{
			points[i][j].x=r*cos(((double)j/(double)slices)*2*pi);
			points[i][j].y=r*sin(((double)j/(double)slices)*2*pi);
			points[i][j].z=h;
		}
	}
	//draw quads using generated points
	for(i=0;i<stacks;i++)
	{
        glColor3f((double)i/(double)stacks,(double)i/(double)stacks,(double)i/(double)stacks);
		for(j=0;j<slices;j++)
		{
			glBegin(GL_QUADS);{
			    //upper hemisphere
				glVertex3f(points[i][j].x,points[i][j].y,points[i][j].z);
				glVertex3f(points[i][j+1].x,points[i][j+1].y,points[i][j+1].z);
				glVertex3f(points[i+1][j+1].x,points[i+1][j+1].y,points[i+1][j+1].z);
				glVertex3f(points[i+1][j].x,points[i+1][j].y,points[i+1][j].z);
                //lower hemisphere
                glVertex3f(points[i][j].x,points[i][j].y,-points[i][j].z);
				glVertex3f(points[i][j+1].x,points[i][j+1].y,-points[i][j+1].z);
				glVertex3f(points[i+1][j+1].x,points[i+1][j+1].y,-points[i+1][j+1].z);
				glVertex3f(points[i+1][j].x,points[i+1][j].y,-points[i+1][j].z);
			}glEnd();
		}
	}
}


void drawSS()
{

    //side 4 cylinders
    glColor3f(0, 1, 0);
    //drawOneEighthSphere(40, 50, 30, 0);

    //drawOneFourthCyllinder(double radius, double height, int slices, int stacks, double offsetX, double offsetY)

    drawOneFourthCyllinder(sphereRadius, cylHeight, 30, 20, squareLen, squareLen);
    drawOneFourthCyllinder(sphereRadius, cylHeight, 30, 20, -squareLen, squareLen);
    drawOneFourthCyllinder(sphereRadius, cylHeight, 30, 20, -squareLen, -squareLen);
    drawOneFourthCyllinder(sphereRadius, cylHeight, 30, 20, squareLen, -squareLen);

    //upper 4 cylinders

    glPushMatrix();
    glRotatef(90, 1, 0, 0);
    //glTranslatef(0,20,0);
    drawOneFourthCyllinder(sphereRadius, cylHeight, 30, 20, squareLen, squareLen);

    glPopMatrix();
    glPushMatrix();
    glRotatef(90, 1, 0, 0);
    //glTranslatef(0,20,0);
    drawOneFourthCyllinder(sphereRadius, cylHeight, 30, 20, -squareLen, squareLen);

    glPopMatrix();
    glPushMatrix();
    glRotatef(90, 1, 0, 0);
    //glTranslatef(0,20,0);
    drawOneFourthCyllinder(sphereRadius, cylHeight, 30, 20, -squareLen, -squareLen);

    glPopMatrix();
    glPushMatrix();
    glRotatef(90, 1, 0, 0);
    //glTranslatef(0,20,0);
    drawOneFourthCyllinder(sphereRadius, cylHeight, 30, 20, squareLen, -squareLen);

    //glRotatef(angle,0,0,1);


    //lower 4 cylinders

    glPopMatrix();
    glPushMatrix();
    glRotatef(90, 0, 1, 0);
    //glTranslatef(0,20,0);
    drawOneFourthCyllinder(sphereRadius, cylHeight, 30, 20, squareLen, squareLen);

    glPopMatrix();
    glPushMatrix();
    glRotatef(90, 0, 1, 0);
    //glTranslatef(0,20,0);
    drawOneFourthCyllinder(sphereRadius, cylHeight, 30, 20, -squareLen, squareLen);

    glPopMatrix();
    glPushMatrix();
    glRotatef(90, 0, 1, 0);
    //glTranslatef(0,20,0);
    drawOneFourthCyllinder(sphereRadius, cylHeight, 30, 20, -squareLen, -squareLen);

    glPopMatrix();
    glPushMatrix();
    glRotatef(90, 0, 1, 0);
    //glTranslatef(0,20,0);
    drawOneFourthCyllinder(sphereRadius, cylHeight, 30, 20, squareLen, -squareLen);


    //drawing squares

    glColor3f(1, 1, 1);

    glPopMatrix();
    glPushMatrix();
    glRotatef(90, 0, 1, 0);
    glTranslatef(0, 0, sphereRadius + squareLen);
    drawSquare(squareLen);


    glPopMatrix();
    glPushMatrix();
    glRotatef(90, 0, 1, 0);
    glTranslatef(0, 0, -(sphereRadius + squareLen));
    drawSquare(squareLen);

    glPopMatrix();
    glPushMatrix();
    glRotatef(90, 1, 0, 0);
    glTranslatef(0, 0, sphereRadius + squareLen);
    drawSquare(squareLen);


    glPopMatrix();
    glPushMatrix();
    glRotatef(90, 1, 0, 0);
    glTranslatef(0, 0, -(sphereRadius + squareLen));
    drawSquare(squareLen);


    glPopMatrix();
    glPushMatrix();
    glRotatef(90, 0, 0, 1);
    glTranslatef(0, 0, sphereRadius + squareLen);
    drawSquare(squareLen);


    glPopMatrix();
    glPushMatrix();
    glRotatef(90, 0, 0, 1);
    glTranslatef(0, 0, -(sphereRadius + squareLen));
    drawSquare(squareLen);



    // drawing spheres:

    //drawOneEighthSphere(double radius, int slices, int stacks)

    // drawing upper spheres:
    glColor3f(1, 0, 0);

    glPopMatrix();
    glPushMatrix();
    glRotatef(90, 0, 0, 1);
    glTranslatef(squareLen, squareLen, squareLen);
    drawOneEighthSphere(sphereRadius, 30, 20, UPPER);

    glPopMatrix();
    glPushMatrix();
    glRotatef(270, 0, 0, 1);
    glTranslatef(squareLen, squareLen, squareLen);
    drawOneEighthSphere(sphereRadius, 30, 20, UPPER);

    glPopMatrix();
    glPushMatrix();
    glRotatef(180, 0, 0, 1);
    glTranslatef(squareLen, squareLen, squareLen);
    drawOneEighthSphere(sphereRadius, 30, 20, UPPER);

    glPopMatrix();
    glPushMatrix();
    glRotatef(0, 0, 0, 1);
    glTranslatef(squareLen, squareLen, squareLen);
    drawOneEighthSphere(sphereRadius, 30, 20, UPPER);


    // drawing lower spheres:

    glPopMatrix();
    glPushMatrix();
    glRotatef(90, 0, 0, 1);
    glTranslatef(squareLen, squareLen, -squareLen);
    drawOneEighthSphere(sphereRadius, 30, 20, LOWER);

    glPopMatrix();
    glPushMatrix();
    glRotatef(270, 0, 0, 1);
    glTranslatef(squareLen, squareLen, -squareLen);
    drawOneEighthSphere(sphereRadius, 30, 20, LOWER);

    glPopMatrix();
    glPushMatrix();
    glRotatef(180, 0, 0, 1);
    glTranslatef(squareLen, squareLen, -squareLen);
    drawOneEighthSphere(sphereRadius, 30, 20, LOWER);

    glPopMatrix();
    glPushMatrix();
    glRotatef(0, 0, 0, 1);
    glTranslatef(squareLen, squareLen, -squareLen);
    drawOneEighthSphere(sphereRadius, 30, 20, LOWER);

    glPopMatrix();

    //drawSquare(20);
    //drawSphere(30,24,20);
    //drawCone(20,50,24);



    //glPopMatrix();
    //glPushMatrix();

    //drawCone(10, 20, 50);
    //glPopMatrix();

    /*
    glRotatef(angle,0,0,1);
    glTranslatef(110,0,0);
    glRotatef(angle,0,0,1);
    glColor3f(0,1,0);
    */


    //drawSquare(15);

    glPushMatrix();
    {
        glRotatef(angle,0,0,1);
        glTranslatef(60,0,0);
        glRotatef(angle,0,0,1);
        glColor3f(0,0,1);
        //drawSquare(10);
    }
    glPopMatrix();

    glRotatef(angle,0,0,1);
    glTranslatef(40,0,0);

    glRotatef(10*angle,0,0,1);

    glColor3f(1,1,0);
    //drawSquare(5);
}

void keyboardListener(unsigned char key, int x,int y){
	switch(key){

		case '1':
			drawgrid=1-drawgrid;
			break;

		default:
			break;
	}
}


void specialKeyListener(int key, int x,int y){

    struct point forward_move;
    double factor = 5.0;

	switch(key){
		case GLUT_KEY_DOWN:		//down arrow key
			//cameraHeight -= 3.0;
			//gluLookAt(0,0,200,	0,0,0,	0,1,0);
			forward_move.x = up.y*right.z - up.z*right.y;
			forward_move.y = up.z*right.x - up.x*right.z;
			forward_move.z = up.x*right.y - up.y*right.x;

			pos.x += factor*forward_move.x;
			pos.y += factor*forward_move.y;
			pos.z += factor*forward_move.z;

			break;
		case GLUT_KEY_UP:		// up arrow key
			//cameraHeight += 3.0;

			struct point forward_move;
			forward_move.x = up.y*right.z - up.z*right.y;
			forward_move.y = up.z*right.x - up.x*right.z;
			forward_move.z = up.x*right.y - up.y*right.x;

			pos.x -= factor*forward_move.x;
			pos.y -= factor*forward_move.y;
			pos.z -= factor*forward_move.z;
			//pos.x -= 5.0;
			break;

		case GLUT_KEY_RIGHT:
			//cameraAngle += 0.03;
			pos.x += factor*right.x;
			pos.y += factor*right.y;
			pos.z += factor*right.z;

			//pos.y += 5.0;
			break;
		case GLUT_KEY_LEFT:
			//cameraAngle -= 0.03;
			//pos.y -= 5.0;

			pos.x -= factor*right.x;
			pos.y -= factor*right.y;
			pos.z -= factor*right.z;

			break;

		case GLUT_KEY_PAGE_UP:

            pos.x += factor*up.x;
            pos.y += factor*up.y;
            pos.z += factor*up.z;

		    //pos.z += 5.0;
			break;
		case GLUT_KEY_PAGE_DOWN:
		    //pos.z -= 5.0;

            pos.x -= factor*up.x;
            pos.y -= factor*up.y;
            pos.z -= factor*up.z;

			break;

		case GLUT_KEY_INSERT:
			break;

		case GLUT_KEY_HOME:
		    if(sphereRadius < MaxRadius)
            {
                sphereRadius += 1.0;

                cylHeight = 2*MaxRadius - 2*sphereRadius;
                squareLen = cylHeight/2;
		    }


			break;
		case GLUT_KEY_END:
		    if(sphereRadius > 0)
            {
                sphereRadius -= 1.0;

                cylHeight = 2*MaxRadius - 2*sphereRadius;
                squareLen = cylHeight/2;
		    }



		    /*
		    if(cylHeight < MaxRadius)
            {
                cylHeight += 10;
            }
            if(squareLen < MaxRadius/2)
            {
                squareLen += 10;
            }
            */

			break;

		default:
			break;
	}
}


void mouseListener(int button, int state, int x, int y){	//x, y is the x-y of the screen (2D)
	switch(button){
		case GLUT_LEFT_BUTTON:
			if(state == GLUT_DOWN){		// 2 times?? in ONE click? -- solution is checking DOWN or UP
				drawaxes=1-drawaxes;
			}
			break;

		case GLUT_RIGHT_BUTTON:
			//........
			break;

		case GLUT_MIDDLE_BUTTON:
			//........
			break;

		default:
			break;
	}
}



void display(){

	//clear the display
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
	glClearColor(0,0,0,0);	//color black
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

	/********************
	/ set-up camera here
	********************/
	//load the correct matrix -- MODEL-VIEW matrix
	glMatrixMode(GL_MODELVIEW);

	//initialize the matrix
	glLoadIdentity();

	//now give three info
	//1. where is the camera (viewer)?
	//2. where is the camera looking?
	//3. Which direction is the camera's UP direction?

	//gluLookAt(100,100,100,	0,0,0,	0,0,1);
	//gluLookAt(200*cos(cameraAngle), 200*sin(cameraAngle), cameraHeight,		0,0,0,		0,0,1);
	//gluLookAt(0,0,200,	0,0,0,	0,1,0);
	gluLookAt(pos.x, pos.y, pos.z, looking.x, looking.y, looking.z,	up.x, up.y, up.z);


	//again select MODEL-VIEW
	glMatrixMode(GL_MODELVIEW);


	/****************************
	/ Add your objects from here
	****************************/
	//add objects

	drawAxes();
	drawGrid();

    //glColor3f(1,0,0);
    //drawSquare(10);

    drawSS();

    //drawOneEighthSphere(40, 50, 30, 0);
    //drawOneFourthCyllinder(20, 50, 30, 20, 0);


    //drawCircle(30,24);

    //drawCone(20,50,24);

	//drawSphere(30,24,20);




	//ADD this line in the end --- if you use double buffer (i.e. GL_DOUBLE)
	glutSwapBuffers();
}


void animate(){
	angle+=0.01;
	//codes for any changes in Models, Camera
	glutPostRedisplay();
}

void init(){
	//codes for initialization
	drawgrid=0;
	drawaxes=1;
	cameraHeight=150.0;
	cameraAngle=1.0;
	angle=0;

	// initializing global vars
    //cylHeight, sphereRadius, squareLen;

    MaxRadius = 70;
    cylHeight = 100;
    sphereRadius = 20;
    squareLen = 50;


	pos.x = 100;
	pos.y = 100;
	pos.z = 100;

	up.x = 0;
	up.y = 0;
	up.z = 1;

	right.x = -1/sqrt(2);
	right.y = 1/sqrt(2);
	right.z = 0;

	looking.x = -1/sqrt(2);
	looking.y = -1/sqrt(2);
	looking.z = 0;


	//clear the screen
	glClearColor(0,0,0,0);

	/************************
	/ set-up projection here
	************************/
	//load the PROJECTION matrix
	glMatrixMode(GL_PROJECTION);

	//initialize the matrix
	glLoadIdentity();

	//give PERSPECTIVE parameters
	gluPerspective(100,	1,	1,	1000.0);
	//field of view in the Y (vertically)
	//aspect ratio that determines the field of view in the X direction (horizontally)
	//near distance
	//far distance
}

int main(int argc, char **argv){
	glutInit(&argc,argv);
	glutInitWindowSize(500, 500);
	glutInitWindowPosition(0, 0);
	glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB);	//Depth, Double buffer, RGB color

	glutCreateWindow("My OpenGL Program");

	init();

	glEnable(GL_DEPTH_TEST);	//enable Depth Testing

	glutDisplayFunc(display);	//display callback function
	glutIdleFunc(animate);		//what you want to do in the idle time (when no drawing is occuring)

	glutKeyboardFunc(keyboardListener);
	glutSpecialFunc(specialKeyListener);
	glutMouseFunc(mouseListener);

	glutMainLoop();		//The main loop of OpenGL

	return 0;
}

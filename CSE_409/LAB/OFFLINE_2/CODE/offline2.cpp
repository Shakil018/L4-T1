#include <iostream>
#include <fstream>
#include <vector>
#include <stack>
#include <cmath>
#include <iomanip>
#include "bitmap_image.hpp"

using namespace std;

#define PI acos(-1.0)
#define INF 100000000.0
// #define INF numeric_limits<double>::infinity()
struct Vector
{
    double x, y, z, w;

    Vector()
    {
        this->x = 0.0;
        this->y = 0.0;
        this->z = 0.0;
        this->w = 1.0;
    }

    Vector(double paramX, double paramY, double paramZ)
    {
        this->x = paramX;
        this->y = paramY;
        this->z = paramZ;
        this->w = 1.0;
    }

    Vector(double paramX, double paramY, double paramZ, double paramW)
    {
        this->x = paramX;
        this->y = paramY;
        this->z = paramZ;
        this->w = paramW;
    }

    void Normalize()
    {
        double resultant = sqrt(x * x + y * y + z * z);

        this->x /= resultant;
        this->y /= resultant;
        this->z /= resultant;
        this->w /= resultant;
    }

    void scale()
    {
        this->x /= w;
        this->y /= w;
        this->z /= w;
        this->w /= w;
    }
};

struct Intersection_Point
{
    Vector point;
    int idx1, idx2;
};

struct Matrix
{
    string name = "";
    double matrix[4][4];

    Matrix()
    {
        for (int i = 0; i < 4; i++)
        {
            for (int j = 0; j < 4; j++)
            {
                matrix[i][j] = 0;
            }
            matrix[i][i] = 1;
        }
    }
};

struct Color
{
    int redVal;
    int greenVal;
    int blueVal;

    Color()
    {
        this->redVal = 0;
        this->greenVal = 0;
        this->blueVal = 0;
    }

    Color(int redVal, int greenVal, int blueVal)
    {
        this->redVal = redVal;
        this->greenVal = greenVal;
        this->blueVal = blueVal;
    }
};

struct Triangle
{
    Vector points[3];
    Color rgb_value;
};

void printMatrix(Matrix myMatrix)
{

    for (int i = 0; i < 4; i++)
    {
        for (int j = 0; j < 4; j++)
        {
            printf("%lf ", myMatrix.matrix[i][j]);
        }
        printf("\n");
    }
}

Matrix transposeMatrix(Matrix myMatrix)
{
    Matrix temp;

    for (int i = 0; i < 4; i++)
    {
        for (int j = 0; j < 4; j++)
        {
            temp.matrix[i][j] = myMatrix.matrix[j][i];
        }
    }

    return temp;
}

double vectorDotProduct(Vector a, Vector b)
{
    double result;
    result = a.x * b.x + a.y * b.y + a.z * b.z;

    return result;
}

Vector vectorCrossProduct(Vector a, Vector b)
{
    Vector result;

    result.x = a.y * b.z - a.z * b.y;
    result.y = a.z * b.x - a.x * b.z;
    result.z = a.x * b.y - a.y * b.x;

    return result;
}

Matrix makeTranslationMatrix(double tx, double ty, double tz)
{
    Matrix temp;
    temp.matrix[0][3] = tx;
    temp.matrix[1][3] = ty;
    temp.matrix[2][3] = tz;

    return temp;
}

Matrix makeScaleMatrix(double sx, double sy, double sz)
{
    Matrix temp;
    temp.matrix[0][0] = sx;
    temp.matrix[1][1] = sy;
    temp.matrix[2][2] = sz;
    return temp;
}

Vector Rotate(Vector X, Vector A, double angle)
{
    double term1, term2, term3;
    Vector result;

    term1 = cos(angle * PI / 180);
    term2 = (1.0 - cos(angle * PI / 180)) * vectorDotProduct(A, X);
    term3 = sin(angle * PI / 180);

    Vector crossVector = vectorCrossProduct(A, X);

    result.x = term1 * X.x + term2 * A.x + term3 * crossVector.x;
    result.y = term1 * X.y + term2 * A.y + term3 * crossVector.y;
    result.z = term1 * X.z + term2 * A.z + term3 * crossVector.z;

    return result;
}

Matrix makeRotationMatrix(double angle, Vector axis)
{
    axis.Normalize();
    Vector I(1.0, 0.0, 0.0), J(0.0, 1.0, 0.0), K(0.0, 0.0, 1.0);
    Vector c1 = Rotate(I, axis, angle);
    Vector c2 = Rotate(J, axis, angle);
    Vector c3 = Rotate(K, axis, angle);

    Matrix result;

    result.matrix[0][0] = c1.x;
    result.matrix[0][1] = c2.x;
    result.matrix[0][2] = c3.x;

    result.matrix[1][0] = c1.y;
    result.matrix[1][1] = c2.y;
    result.matrix[1][2] = c3.y;

    result.matrix[2][0] = c1.z;
    result.matrix[2][1] = c2.z;
    result.matrix[2][2] = c3.z;

    return result;
}

Vector transformPoint(Matrix top, Vector point)
{
    double arr[4], temp[4];
    arr[0] = point.x;
    arr[1] = point.y;
    arr[2] = point.z;
    arr[3] = 1.0;

    for (int i = 0; i < 4; i++)
    {
        temp[i] = 0.0;
        for (int j = 0; j < 4; j++)
        {
            temp[i] += top.matrix[i][j] * arr[j];
        }
    }

    Vector result(temp[0], temp[1], temp[2], temp[3]);
    result.scale();

    return result;
}

Matrix matrixProduct(Matrix a, Matrix b)
{
    Matrix result;

    for (int i = 0; i < 4; i++)
    {
        for (int j = 0; j < 4; j++)
        {
            result.matrix[i][j] = 0.0;
            for (int k = 0; k < 4; k++)
            {
                result.matrix[i][j] += a.matrix[i][k] * b.matrix[k][j];
            }
        }
    }

    return result;
}

stack<Matrix> state;

Vector eye, up, look;
int screenWidth, screenHeight;
double fovY, aspectRatio, near, far;
double leftLimitX, rightLimitX, bottomLimitY, topLimitY, frontLimitZ, rearLimitZ;

void readWritePoint(ifstream &inputFile, ofstream &stageFile, Matrix transformer)
{
    Vector pointA, pointB, pointC;

    inputFile >> pointA.x >> pointA.y >> pointA.z;
    inputFile >> pointB.x >> pointB.y >> pointB.z;
    inputFile >> pointC.x >> pointC.y >> pointC.z;

    Vector p1 = transformPoint(transformer, pointA);
    Vector p2 = transformPoint(transformer, pointB);
    Vector p3 = transformPoint(transformer, pointC);

    stageFile << std::fixed << setprecision(7);

    stageFile << p1.x << " " << p1.y << " " << p1.z << endl;
    stageFile << p2.x << " " << p2.y << " " << p2.z << endl;
    stageFile << p3.x << " " << p3.y << " " << p3.z << endl;
    stageFile << endl;
}

Matrix ViewTransformation()
{
    Vector l;

    l.x = look.x - eye.x;
    l.y = look.y - eye.y;
    l.z = look.z - eye.z;

    l.Normalize();

    Vector r = vectorCrossProduct(l, up);

    r.Normalize();

    Vector u = vectorCrossProduct(r, l);

    Matrix T;

    T.matrix[0][3] = -eye.x;
    T.matrix[1][3] = -eye.y;
    T.matrix[2][3] = -eye.z;

    Matrix R;

    R.matrix[0][0] = r.x;
    R.matrix[0][1] = r.y;
    R.matrix[0][2] = r.z;

    R.matrix[1][0] = u.x;
    R.matrix[1][1] = u.y;
    R.matrix[1][2] = u.z;

    R.matrix[2][0] = -l.x;
    R.matrix[2][1] = -l.y;
    R.matrix[2][2] = -l.z;

    Matrix product = matrixProduct(R, T);

    return product;
}

Matrix ProjectionTransformation()
{
    double fovX, t, r;
    fovX = fovY * aspectRatio;
    t = near * tan((fovY * PI) / (180 * 2));
    r = near * tan((fovX * PI) / (180 * 2));

    Matrix P;

    P.matrix[0][0] = near / r;

    P.matrix[1][1] = near / t;

    P.matrix[2][2] = -(far + near) / (far - near);
    P.matrix[2][3] = -(2 * far * near) / (far - near);

    P.matrix[3][2] = -1.0;
    P.matrix[3][3] = 0.0;

    return P;
}

int main()
{
    Matrix identity;
    state.push(identity);
    int totalTriangles = 0;

    string command;
    ifstream sceneFile, configFile, commandFile, stage1_file_in, stage2_file_in, stage3_file_in;
    ofstream stage1_file_out, stage2_file_out, stage3_file_out, z_buffer_file;

    printf("enter test case no. inside test_case directory: \n");
    string folderName;
    cin>>folderName;

    sceneFile.open("test_case/" + folderName + "/scene.txt");
    configFile.open("test_case/" + folderName + "/config.txt");
    stage1_file_out.open("output/stage1.txt");
    stage1_file_in.open("output/stage1.txt");

    stage2_file_out.open("output/stage2.txt");
    stage2_file_in.open("output/stage2.txt");

    stage3_file_out.open("output/stage3.txt");
    stage3_file_in.open("output/stage3.txt");
    z_buffer_file.open("output/z_buffer.txt");

    double tempX, tempY, tempZ;

    sceneFile >> eye.x >> eye.y >> eye.z;
    sceneFile >> look.x >> look.y >> look.z;
    sceneFile >> up.x >> up.y >> up.z;
    sceneFile >> fovY >> aspectRatio >> near >> far;

    // printf("fovY: %lf, aspectRatio: %lf, near: %lf, far: %lf\n", fovY, aspectRatio, near, far);

    double tx, ty, tz;
    double sx, sy, sz;
    double rotationAngle;
    Vector pointA, pointB, pointC;

    while (true)
    {
        sceneFile >> command;

        if (command == "triangle")
        {
            // cout << "triangle command" << endl;

            totalTriangles++;
            readWritePoint(sceneFile, stage1_file_out, state.top());
        }

        else if (command == "translate")
        {
            // cout << "translate ccommand" << endl;
            sceneFile >> tx >> ty >> tz;
            Matrix translationMatrix = makeTranslationMatrix(tx, ty, tz);

            Matrix topMatrix = state.top();
            state.pop();
            state.push(matrixProduct(topMatrix, translationMatrix));
        }
        else if (command == "scale")
        {
            // cout << "scale command" << endl;
            sceneFile >> sx >> sy >> sz;
            Matrix scaleMatrix = makeScaleMatrix(sx, sy, sz);

            Matrix topMatrix = state.top();
            state.pop();
            state.push(matrixProduct(topMatrix, scaleMatrix));
        }
        else if (command == "rotate")
        {
            // cout << "rotate" << endl;
            Vector rotationAxis;
            sceneFile >> rotationAngle >> rotationAxis.x >> rotationAxis.y >> rotationAxis.z;
            Matrix rotationMatrix = makeRotationMatrix(rotationAngle, rotationAxis);

            Matrix topMatrix = state.top();
            state.pop();
            state.push(matrixProduct(topMatrix, rotationMatrix));
        }
        else if (command == "push")
        {
            // cout << "push" << endl;
            state.push(state.top());
        }
        else if (command == "pop")
        {
            // cout << "pop" << endl;
            state.pop();
        }
        else if (command == "end")
        {
            // cout << "end";
            break;
        }
    }

    // View Transformation:

    Matrix V = ViewTransformation();

    int cnt = totalTriangles;
    while (cnt--)
    {
        readWritePoint(stage1_file_in, stage2_file_out, V);
    }

    // Projection Transformation:

    Matrix P = ProjectionTransformation();

    cnt = totalTriangles;
    while (cnt--)
    {
        readWritePoint(stage2_file_in, stage3_file_out, P);
    }

    // Stage 4:

    configFile >> screenWidth >> screenHeight;
    configFile >> leftLimitX;
    configFile >> bottomLimitY;
    configFile >> frontLimitZ >> rearLimitZ;

    rightLimitX = -leftLimitX;
    topLimitY = -bottomLimitY;

    // double z_max = abs(rearLimitZ - frontLimitZ);
    double z_max = rearLimitZ;

    Triangle allTriangle[totalTriangles];
    srand(time(0));

    for (int i = 0; i < totalTriangles; i++)
    {
        stage3_file_in >> allTriangle[i].points[0].x >> allTriangle[i].points[0].y >> allTriangle[i].points[0].z;
        stage3_file_in >> allTriangle[i].points[1].x >> allTriangle[i].points[1].y >> allTriangle[i].points[1].z;
        stage3_file_in >> allTriangle[i].points[2].x >> allTriangle[i].points[2].y >> allTriangle[i].points[2].z;

        allTriangle[i].rgb_value.redVal = rand() % 256;
        allTriangle[i].rgb_value.greenVal = rand() % 256;
        allTriangle[i].rgb_value.blueVal = rand() % 256;
    }

    stage3_file_in.close();

    double dx, dy, top_Y, bottom_Y, left_X, right_X;

    dx = (rightLimitX - leftLimitX) / screenWidth;
    dy = (topLimitY - bottomLimitY) / screenHeight;
    left_X = leftLimitX + dx / 2.0;
    right_X = rightLimitX - dx / 2.0;
    top_Y = topLimitY - dy / 2.0;
    bottom_Y = bottomLimitY + dy / 2.0;

    Color zero_color(0, 0, 0);
    vector<vector<double>> z_buffer(screenHeight, vector<double>(screenWidth, z_max));
    vector<vector<Color>> frame_buffer(screenHeight, vector<Color>(screenWidth, zero_color));

    // printf("dx: %lf, dy: %lf, left_X: %lf, right_X: %lf, top_Y: %lf, bottom_Y: %lf\n", dx, dy, left_X, right_X, top_Y, bottom_Y);

    // Procedure:
    double max_Y, min_Y;
    for (int i = 0, top_scanline, bottom_scanline; i < totalTriangles; i++)
    {
        double max_Y = max(allTriangle[i].points[2].y, max(allTriangle[i].points[0].y, allTriangle[i].points[1].y));
        double min_Y = min(allTriangle[i].points[2].y, min(allTriangle[i].points[0].y, allTriangle[i].points[1].y));
        double diff;
        if (max_Y >= top_Y)
        {
            top_scanline = 0;
        }
        else
        {
            diff = (top_Y - max_Y) / dy;
            top_scanline = (int)round(diff);
        }

        if (min_Y <= bottom_Y)
        {
            bottom_scanline = screenHeight - 1;
        }
        else
        {
            diff = abs(bottom_Y - min_Y) / dy;
            bottom_scanline = screenHeight - ((int)round(diff)) - 1;
        }

        for (int rowNum = top_scanline, leftInterCol, rightInterCol; rowNum <= bottom_scanline; rowNum++)
        {
            double ys = top_Y - rowNum * dy;

            // Intersection_Point intersections[3];
            Vector intersections[3];
            intersections[0] = Vector(INF, ys, 0, 1);
            intersections[1] = Vector(INF, ys, 1, 2);
            intersections[2] = Vector(INF, ys, 2, 0);

            for (int k = 0; k < 3; k++)
            {
                Vector point1 = allTriangle[i].points[(int)intersections[k].z];
                Vector point2 = allTriangle[i].points[(int)intersections[k].w];

                if (point1.y != point2.y)
                {
                    intersections[k].x = point1.x + (ys - point1.y) * (point1.x - point2.x) / (point1.y - point2.y);
                }
            }

            for (int k = 0; k < 3; k++)
            {
                Vector point1 = allTriangle[i].points[(int)intersections[k].z];
                Vector point2 = allTriangle[i].points[(int)intersections[k].w];

                if (intersections[k].x != INF)
                {
                    bool x_invalid_condition = intersections[k].x > max(point1.x, point2.x) || intersections[k].x < min(point1.x, point2.x);
                    bool y_invalid_condition = intersections[k].y > max(point1.y, point2.y) || intersections[k].y < min(point1.y, point2.y);

                    if (x_invalid_condition || y_invalid_condition)
                    {
                        intersections[k].x = INF;
                    }
                }
            }

            // Left & Right intersecting points:

            int min_idx = -1, max_idx = -1;

            double max_X, min_X;

            for (int k = 0; k < 3; k++)
            {
                if (min_idx == -1 && max_idx == -1)
                {
                    if (intersections[k].x != INF)
                    {
                        min_idx = k;
                        max_idx = k;

                        max_X = intersections[k].x;
                        min_X = intersections[k].x;
                    }
                }
                else
                {
                    if (intersections[k].x != INF)
                    {
                        if (intersections[k].x < min_X)
                        {
                            min_idx = k;
                            min_X = intersections[k].x;
                        }
                        if (intersections[k].x > max_X)
                        {
                            max_idx = k;
                            max_X = intersections[k].x;
                        }
                    }
                }
            }

            // Left & Right intersecting column:

            if (intersections[min_idx].x <= left_X)
            {
                leftInterCol = 0;
            }
            else
            {
                leftInterCol = (int)round((intersections[min_idx].x - left_X) / dx);
            }

            if (intersections[max_idx].x >= right_X)
            {
                rightInterCol = screenWidth - 1;
            }
            else
            {
                rightInterCol = screenWidth - (1 + ((int)round((right_X - intersections[max_idx].x) / dx)));
            }

            // za & zb values:

            Vector point1 = allTriangle[i].points[(int)intersections[min_idx].z];
            Vector point2 = allTriangle[i].points[(int)intersections[min_idx].w];

            double za = point1.z + (intersections[min_idx].y - point1.y) * (point2.z - point1.z) / (point2.y - point1.y);

            point1 = allTriangle[i].points[(int)intersections[max_idx].z];
            point2 = allTriangle[i].points[(int)intersections[max_idx].w];

            double zb = point1.z + (intersections[max_idx].y - point1.y) * (point2.z - point1.z) / (point2.y - point1.y);

            // Scanning :

            double zp;
            double constTerm = dx * (zb - za) / (intersections[max_idx].x - intersections[min_idx].x);

            for (int colNum = leftInterCol; colNum <= rightInterCol; colNum++)
            {
                if (colNum == leftInterCol)
                {
                    zp = za + ((left_X + leftInterCol * dx) - intersections[min_idx].x) * (zb - za) / (intersections[max_idx].x - intersections[min_idx].x);
                }
                else
                {
                    zp = zp + constTerm;
                }

                if (zp > frontLimitZ && zp < z_buffer[rowNum][colNum])
                {
                    z_buffer[rowNum][colNum] = zp;

                    frame_buffer[rowNum][colNum].redVal = allTriangle[i].rgb_value.redVal;
                    frame_buffer[rowNum][colNum].greenVal = allTriangle[i].rgb_value.greenVal;
                    frame_buffer[rowNum][colNum].blueVal = allTriangle[i].rgb_value.blueVal;
                }
            }
        }
    }

    bitmap_image bitImg(screenWidth, screenHeight);

    for (int rowNum = 0; rowNum < screenHeight; rowNum++)
    {
        for (int colNum = 0; colNum < screenWidth; colNum++)
        {

            if (z_buffer[rowNum][colNum] < z_max)
            {
                z_buffer_file << z_buffer[rowNum][colNum] << '\t';
            }

            Color ch = frame_buffer[rowNum][colNum];
            bitImg.set_pixel(colNum, rowNum, ch.redVal, ch.greenVal, ch.blueVal);
        }
        z_buffer_file << endl;
    }
    bitImg.save_image("output/out.bmp");
    z_buffer_file.close();

    std::vector<vector<double>>().swap(z_buffer);
    std::vector<vector<Color>>().swap(frame_buffer);

    return 0;
}

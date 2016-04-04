from __future__ import print_function
from PIL import Image
from math import sqrt
from math import acos
from math import trunc

pi=3.1415

def get_RGBvalue(t) :
    return t[0]+t[1]+t[2]

##

im=Image.open("cervello.tif")
x=im.size[0]
y=im.size[1]
O=(x/2,y/2)



#########################
lower_threshold=25      #
upper_threshold=90      #
#########################





#Left Occipital Pole  ///  Lpole
Left=False
Lbox=0
Lc=0
j=y-1
while (j>=0 and Left==False) :
    for i in range(O[0]) :
        t=im.getpixel((i,j))
        val=get_RGBvalue(t)
        if val>lower_threshold :
            Left=True
            Lbox+=(i*val)
            Lc+=val
            Ly=j
    j-=1
    
if Lc : Lx=Lbox/Lc
Lpole=(Lx,Ly)
im.putpixel(Lpole,(255,0,255))




#Right Occipital Pole  ///  Rpole
Right=False
Rbox=0
Rc=0
j=y-1
while (j>=0 and Right==False) :
    for i in range(O[0],x) :
        t=im.getpixel((i,j))
        val=get_RGBvalue(t)
        if val>lower_threshold :
            Right=True
            Rbox+=(i*val)
            Rc+=val
            Ry=j
    j-=1

if Rc : Rx=Rbox/Rc
Rpole=(Rx,Ry)
im.putpixel(Rpole,(255,0,255))



print ("Left occipital pole:",Lpole)
print ("Right occipital pole:",Rpole)



####################################BISECTOR_APPROXIMATION##########################################
#############
Vertx=80    #
Verty=116   #
#############
Vertex=(Vertx,Verty)
im.putpixel(Vertex,(255,0,0))    #red pixel marks the user-selected vertex
print("-------------------------------------------------------------------------------")
print("User-selected Vertex:",Vertex)

Lx=Lpole[0]-Vertex[0]
Ly=Lpole[1]-Vertex[1]
Rx=Rpole[0]-Vertex[0]
Ry=Rpole[1]-Vertex[1]

cos_angle=(Lx*Rx+Ly*Ry)/(sqrt(Lx**2+Ly**2)*sqrt(Rx**2+Ry**2))
angle=acos(cos_angle)

Ay=y-O[1]
Rx=Rpole[0]-O[0]
Ry=Rpole[1]-O[1]
cos_BAOB=(Ay*Ry)/(sqrt(Ay**2)*sqrt(Rx**2+Ry**2))    # cos of BisectorApproximation-calculated Occipital Bending
BAOB=acos(cos_BAOB)-(angle/2)
print ("Bisector-Approximated Occipital Bending [BAOB]: %f randians" %BAOB)
print ("                                              ~ %f degrees" %((BAOB*180)/pi))



####################################AVERAGE_POLE##########################################
Apole=((Lpole[0]+Rpole[0])/2,(Lpole[1]+Rpole[1])/2)
im.putpixel(Apole,(0,255,0))    #green pixel marks the average pole

Px=Apole[0]-O[0]
Py=Apole[1]-O[1]
cos_OBAM=(Ay*Py)/(sqrt(Ay**2)*sqrt(Px**2+Py**2))    # cos of Occipital Bending with Average-pole Method
OBAM=acos(cos_OBAM)
print("-------------------------------------------------------------------------------")
print("Average Pole:",Apole)
print("Occipital Bending with Average-pole Method [OBAM]: %f randians" %OBAM)
print("                                                 ~ %f degrees" %((OBAM*180)/pi))




#uncomment this to show axes
""" #show axes
for i in range(y) :
    if i%10==0 : im.putpixel((O[0],i),(0,0,255))
for i in range(x) :
    if i%10==0 : im.putpixel((i,O[1]),(0,0,255))
"""

""" #calcolo vertex sbagliato
#Central point  ///  Cpoint
j=y-1
while (j) :
    t=im.getpixel((O[0],j))
    val=get_RGBvalue(t)
    if val<lower_threshold : j-=1
    else : break

while (j) :                     #edge here
    t=im.getpixel((O[0],j))
    val=get_RGBvalue(t)
    if val>upper_threshold : j-=1
    else :
        Cy=j
        break
        
Cpoint=(O[0],Cy)
im.putpixel(Cpoint,(255,0,255))
"""

im.save("cervelloMarcato.tif")









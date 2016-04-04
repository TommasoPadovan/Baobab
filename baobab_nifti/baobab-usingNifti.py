from nifti import NiftiImage
from datetime import datetime
prima=datetime.now()
#FLAGS
#############################
background_threshold=25     #
reverse_YAxis=True          #
#############################



nim=NiftiImage("cervello")
print "Processing '%s'" %nim.filename,
nim.load()

d=nim.extent #genearatin a 4-uple containing the dimension of nifti image (x,y,z,time)
O=(d[0]/2,d[1]/2)
print "(%dx%dx%d)\n" %(d[0],d[1],d[2])
print "--------------------------------------------------------------------------------"
print

bb=nim.bbox


#ASSUMING IMAGE HAS TIME SIZE=1  -> program will work just on first istant on 4-dimensional images
print "\tLeft Pole\tRight Pole\tAverage Pole"


for z in range(bb[0][0],bb[0][1]) : #bottom-up scroll
    y=bb[1][0]
    found=False
    maximum=background_threshold
    while (y<bb[1][1] and found==False) :
        for x in range(bb[2][0],O[0]) :
            val=nim.data[0,z,y,x]
            if val>background_threshold :
                found=True
                if val>=maximum :
                    maximum=val
                    Lx=x
        y+=1
    if found : Lpole=[Lx,y-1,z]
    else : Lpole=None


    y=bb[1][0]
    found=False
    maximum=background_threshold
    while (y<bb[1][1] and found==False) :
        for x in range(O[0],bb[2][1]) :
            val=nim.data[0,z,y,x]
            if val>background_threshold :
                found=True
                if val>=maximum :
                    maximum=val
                    Rx=x
        y+=1
    if found : Rpole=[Rx,y-1,z]
    else : Rpole=None

    if Lpole and Rpole :
        Apole=[(Lpole[0]+Rpole[0])/2.0,(Lpole[1]+Rpole[1])/2.0,z]
        if reverse_YAxis :                  #reversing y-axis
            Lpole[1]= -(Lpole[1]-d[1]+1)
            Rpole[1]= -(Rpole[1]-d[1]+1)
            Apole[1]= -(Apole[1]-d[1]+1)
    else :
        Apole=None


    
    print "%d)\t" %z,Lpole,"\t",Rpole,"\t",Apole


dopo=datetime.now()

print
print "--------------------------------------------------------------------------------"
print
print "total time",dopo-prima









    
    

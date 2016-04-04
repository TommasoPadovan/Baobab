from nifti import NiftiImage
from datetime import datetime
from xlwt import Workbook
prima=datetime.now()
#FLAGS
#############################
background_threshold=25     #
reverse_YAxis=True          #
print_on_shell=False        #
#############################


#   NOME FILE QUA ↓↓↓↓
nim=NiftiImage("cervello")
nim.load()
d=nim.extent #genearatin a 4-uple (or a 3-uple) containing the dimension of nifti image (x,y,z,(time))
O=(d[0]/2,d[1]/2)

dimension=len(d)
print "Processing '%s'" %nim.filename,"(%dx%dx%d) %d-dimensional\n" %(d[0],d[1],d[2],dimension)
print "--------------------------------------------------------------------------------\n"
bb=nim.bbox


#creating workbook
book=Workbook()
s=book.add_sheet(nim.filename)
s.write(0,1,"Left Pole")
s.write(0,3,"Right Pole")
s.write(0,5,"Average Pole")
s.write(1,0,"z")
s.write(1,1,"x")
s.write(1,2,"y")
s.write(1,3,"x")
s.write(1,4,"y")
s.write(1,5,"x")
s.write(1,6,"y")
row=2

#ASSUMING IMAGE HAS 3 OR 4 DIMENSIONS
#if 4 dimension ASSUMING IMAGE HAS TIME SIZE=1  -> program will work just on first istant on 4-dimensional images
if print_on_shell : print "\tLeft Pole\tRight Pole\tAverage Pole"


for z in range(bb[0][0],bb[0][1]) : #bottom-up scroll
    y=bb[1][0]
    found=False
    maximum=background_threshold
    while (y<bb[1][1] and found==False) :
        for x in range(bb[2][0],O[0]) :
            if dimension==4 : val=nim.data[0,z,y,x]
            elif dimension==3 : val=nim.data[z,y,x]
            else :
                print "unknown dimension format"
                break
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
            if dimension==4 : val=nim.data[0,z,y,x]
            elif dimension==3 : val=nim.data[z,y,x]
            else :
                print "unknown dimension format"
                break
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


    
    if print_on_shell : print "%d)\t" %z,Lpole,"\t",Rpole,"\t",Apole
    elif z%5==1 : print "..",

    s.write(row,0,str(z))
    if Lpole :
        s.write(row,1,str(Lpole[0]))
        s.write(row,2,str(Lpole[1]))
    else :
        s.write(row,1,"None")
        s.write(row,2,"None")
    if Rpole :
        s.write(row,3,str(Rpole[0]))
        s.write(row,4,str(Rpole[1]))
    else :
        s.write(row,3,"None")
        s.write(row,4,"None")
    if Rpole and Lpole :
        s.write(row,5,str(Apole[0]))
        s.write(row,6,str(Apole[1]))
    else :
        s.write(row,5,"None")
        s.write(row,6,"None")
    row+=1


dopo=datetime.now()

print "\n--------------------------------------------------------------------------------\n"
print "---DONE---"
print "total time",dopo-prima


book.save("output.xls")






    
    

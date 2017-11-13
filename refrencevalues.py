# This is my main code for my final project for 15-112 Intro to programming.
# File Created: November 1 , 12:49 p.m
# Name: Kenana Dalle
# Andrew ID: kdalle
# Project name: Electronic text writer.
# Libraries used: ImageWriter.py 
# This code is for generating reference values needed for the main code.

from ImageWriter import *
''' This code generates the reference values for the 8 parts for each capital and small letters From A to Z. It follows the same algorithem as my main with the
    difference of just generating the percentages for each part.'''


# Taking the image and converting it to black and white
def convertBlackWhite(pic):
    
    rows = getHeight(pic)
    columns = getWidth(pic)
    for i in range(0,rows):
        for j in range(0,columns):
            c = getColor(pic,j,i)
            if sum(c)/3 >= 100:
                setColor(pic,j,i,[255,255,255])
            else:
                setColor(pic,j,i,[0,0,0])
    showPicture(pic)

def detectline(pic):
    
    rows= getHeight(pic)
    columns=getWidth(pic)
    isLine=False
    startOfLine=[]
    endOfLine=[]
    result=[]
    linestart=[]
    for r in range(rows): # Going through the whole picture, if one black pixel is found in one row, then it breaks the loop (by setting isLine to True) and goes
                          # through the next row.
        isLine=False
        for c in range(columns):
            g=getColor(pic,c,r)
            
            if g==[0,0,0] and not isLine :
                isLine=True
                linestart.append(r)
                
              
    for r in range(len(linestart)-1): # Here I checked the starts and ends of the lines by checking the rows that are not consecutive.
        if linestart[r+1]-linestart[r]>1:
            startOfLine.append(linestart[r+1])
            endOfLine.append(linestart[r])
              
    startOfLine=[linestart[0]]+startOfLine
    endOfLine=endOfLine+[linestart[len(linestart)-1]]
    for i in range(len(endOfLine)):
        result.append((startOfLine[i],endOfLine[i]))

    return result

def detectletter(pic,startrow,endrow,col):
    rows=getHeight(pic)
    columns=getWidth(pic)
    width=[]
    firstcol=[]
    lastcol=[]
    for c in range(col,columns): # This checks for the columns that include black pixels.
        isblack=True
        for r in range(startrow,endrow):
            g=getColor(pic,c,r)
            if g==[0,0,0] and isblack:
               width.append(c)
               isblack=False
    pixels=width[:]
           
    if ',' in pixels:
        if len(pixels[:pixels.index(',')])<1: # This checks if the pixels detected are actualy just noise by checking if their width is less than 2.
            del width[:pixels.index(',')]
        
        for p in range(len(width)-1):
            if width[p]-width[p-1]!=1:
                firstcol.append(width[p])
                
        
        for p in range(len(width)-1):
            if width[p+1]-width[p]!=1:
                
                lastcol.append(width[p])
                
        

        for i in range(len(lastcol)):
            if lastcol[i]-firstcol[i]>1:
                return [firstcol[i], lastcol[i]]
    else: # If there was no noise , it will simply return the first column and the last column with black pixels detected.
        
        return [width[0],width[len(width)-1]]
def letterlimit(pic,startrow,endrow,col):

    letterborders=[]
    rows=getHeight(pic)
    columns=getWidth(pic)
    column1=detectletter(pic,startrow,endrow,col)[0]
    column2=detectletter(pic,startrow,endrow,col)[1]
    for r in range(startrow,endrow):
        isEnd=False
        for c in range(column1,column2):
            g=getColor(pic,c,r)
            
            if g==[0,0,0] and not isEnd :
                isEnd=True
                letterborders.append(r)
    return [letterborders[0],letterborders[len(letterborders)-1]]

def readLetter(pic,startrow,endrow,startcol,endcol):
    count=0
    part1=0
    part2=0
    part3=0
    part4=0
    part5=0
    part6=0
    part7=0
    part8=0
    rows=getHeight(pic)
    columns=getWidth(pic)
    midrow=range(startrow,endrow)[len(range(startrow,endrow))/2] # This is to seperate the picture into four quadrents
    midcolumn=range(startcol,endcol)[len(range(startcol,endcol))/2]
    Q1_pixels=((endcol-midcolumn)*(midrow-startrow))# These are the total number of pixel for each quadrent
    Q2_pixels=((midcolumn-startcol)*(midrow-startrow))
    Q3_pixels=((midcolumn-startcol)*(endrow-midrow))
    Q4_pixels=((endcol-midcolumn)*(endrow-midrow))
    
    for r in range(startrow,midrow):
        i=endcol-count
        count=count+1
        for c in range(midcolumn,i):
            g=getColor(pic,c,r)
            
            if g==[0,0,0]:
                part1=part1+1
    count=1
    for r in range(startrow,midrow):
        i=endcol-count
        count=count+1
        for c in range(i,endcol):
            if i>=midcolumn:
                g=getColor(pic,c,r)
                
                
                if g==[0,0,0]:
                    part2=part2+1
    count=0
    for r in range(midrow,endrow):
        i=midcolumn+count
        count=count+1
        for c in range(i,endcol):
            g=getColor(pic,c,r)
            if g==[0,0,0]:
                part3=part3+1
    count=1
    for r in range(midrow,endrow):
        i=midcolumn+count
        count=count+1
        for c in range(midcolumn,i):
            if i<= endcol:
                g=getColor(pic,c,r)
                
                if g==[0,0,0]:
                    part4=part4+1
    count=1
    for r in range(midrow,endrow):
        i=midcolumn-count
        count=count+1
        for c in range(i,midcolumn):
            if i>=startcol:
                g=getColor(pic,c,r)
                if g==[0,0,0]:
                    part5=part5+1
    count=0
    for r in range(midrow,endrow):
        i=midcolumn-count
        count=count+1
        for c in range(startcol,i):
            g=getColor(pic,c,r)
            if g==[0,0,0]:
                part6=part6+1
    count=1
    for r in range(startrow,midrow):
        i=startcol+count
        count=count+1
        for c in range(startcol,i):
            if i<=midcolumn:
                g=getColor(pic,c,r)
                if g==[0,0,0]:
                    part7=part7+1
    count=0
    for r in range(startrow,midrow):
        i=startcol+count
        count=count+1
        for c in range(i,midcolumn):
            g=getColor(pic,c,r)
            if g==[0,0,0]:
                part8=part8+1           
    
    #These are the %'s of black to total for each of the 8 parts
    part1_p=float(part1)/float(Q1_pixels/2)
    part2_p=float(part2)/float(Q1_pixels/2)
    part3_p=float(part3)/float(Q4_pixels/2)
    part4_p=float(part4)/float(Q4_pixels/2)
    part5_p=float(part5)/float(Q3_pixels/2)
    part6_p=float(part6)/float(Q3_pixels/2)
    part7_p=float(part7)/float(Q2_pixels/2)
    part8_p=float(part8)/float(Q2_pixels/2)
    return [part1_p,part2_p,part3_p,part4_p,part5_p,part6_p,part7_p,part8_p]        
def readAll(filename):
    lst=[]
    d={}
    pic=loadPicture(filename)
    convertBlackWhite(pic)
    lines=detectline(pic)
    line1start=lines[0][0]
    line1end=lines[0][1]
    letterend=0
    l='AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz'
    for i in range(16):
        col=detectletter(pic,line1start,line1end,letterend)
        letterstartrow=letterlimit(pic,line1start,line1end,letterend)[0]
        letterendrow=letterlimit(pic,line1start,line1end,letterend)[1]
        letterstart=col[0]+1
        letterend=col[1]+1
        
        letters1=readLetter(pic,letterstartrow,letterendrow,letterstart,letterend)
        d[l[i]]=letters1
        
        
    line2start=lines[1][0]
    line2end=lines[1][1]
    letterend=0
    for i in range(16):
        col=detectletter(pic,line2start,line2end,letterend)
        letterstartrow=letterlimit(pic,line2start,line2end,letterend)[0]
        letterendrow=letterlimit(pic,line2start,line2end,letterend)[1]
        letterstart=col[0]+1
        letterend=col[1]+1
        
        letters2=readLetter(pic,letterstartrow,letterendrow,letterstart,letterend)
        d[l[i+16]]=letters2
        
    line3start=lines[2][0]
    line3end=lines[2][1]
    letterend=0
    for i in range(16):
        col=detectletter(pic,line3start,line3end,letterend)
        letterstartrow=letterlimit(pic,line3start,line3end,letterend)[0]
        letterendrow=letterlimit(pic,line3start,line3end,letterend)[1]
        letterstart=col[0]+1
        letterend=col[1]+1
        
        letters3=readLetter(pic,letterstartrow,letterendrow,letterstart,letterend)
        d[l[i+32]]=letters3

    line4start=lines[3][0]
    line4end=lines[3][1]
    letterend=0
    for i in range(4):
        col=detectletter(pic,line4start,line4end,letterend)
        letterstartrow=letterlimit(pic,line4start,line4end,letterend)[0]
        letterendrow=letterlimit(pic,line4start,line4end,letterend)[1]
        letterstart=col[0]+1
        letterend=col[1]+1
        
        letters4=readLetter(pic,letterstartrow,letterendrow,letterstart,letterend)
        d[l[i+48]]=letters4
       

    File=open('Reference values for TNR format','w')
    for letter in d:
        File.write(letter+str(d[letter])+'\n')

    File.close()
    



    
print readAll('ref3.jpg')

# This is my main code for my final project for 15-112 Intro to programming.
# File Created: November 1 , 12:49 p.m
# Name: Kenana Dalle
# Andrew ID: kdalle
# Project name: Electronic text writer and dictionary
# Libraries used: ImageWriter.py , urllib.py
#

from ImageWriter import *
from urllib import *


d={}
f=open('Reference values for TNR format','r')
line=f.readline()
while line:
    d[line[0]]=eval(line[1:])
    line=f.readline()


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
    #pic=loadPicture(pic)
    #convertBlackWhite(pic)
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
                
              
    for r in range(len(linestart)-1): # Here I checked the starts and ends of the blobs by checking the rows that are not consecutive.
        if linestart[r+1]-linestart[r]>1:
            startOfLine.append(linestart[r+1])
            endOfLine.append(linestart[r])
              
    startOfLine=[linestart[0]]+startOfLine
    endOfLine=endOfLine+[linestart[len(linestart)-1]]
    for i in range(len(endOfLine)):
        result.append((startOfLine[i],endOfLine[i]))

    return result

def detectletter(pic,startrow,endrow,col):
    #pic=loadPicture(pic)
    #convertBlackWhite(pic)
    rows=getHeight(pic)
    columns=getWidth(pic)
    width=[]
    firstcol=[]
    lastcol=[]
    for c in range(col,columns): # This checks for the columns that include black pixels.
        isblack=True
        for r in range(startrow,endrow+1):
            g=getColor(pic,c,r)
            if g==[0,0,0] and isblack:
               width.append(c)
               isblack=False
    pixels=width[:]
    
    for p in range(len(width)-1): # This conditional seperates the columns with black noise 
        if width[p+1]-width[p]!=1:
            pixels.insert((p+1),',')
           
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
    #pic=loadPicture(pic)
    #convertBlackWhite(pic)
    letterborders=[]
    rows=getHeight(pic)
    columns=getWidth(pic)
    column1=detectletter(pic,startrow,endrow,col+1)[0]
    column2=detectletter(pic,startrow,endrow,col+1)[1]
    for r in range(startrow,endrow):
        isEnd=False
        for c in range(column1,column2):
            g=getColor(pic,c,r)
            
            if g==[0,0,0] and not isEnd :
                isEnd=True
                letterborders.append(r)
    return [letterborders[0],letterborders[len(letterborders)-1]]

def readLetter(pic,startrow,endrow,startcol,endcol,d):
    black=[]
    count=0
    part1=0
    part2=0
    part3=0
    part4=0
    part5=0
    part6=0
    part7=0
    part8=0
    for r in range(startrow,endrow): # To differintiate between i and t
        isBlack=False
        for c in range(startcol,endcol):
            g=getColor(pic,c,r)
            if g==[0,0,0] and not isBlack :
                isBlack=True
                black.append(r)
                
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
    if (Q1_pixels/2)!=0 or (Q2_pixels/2)!=0 or (Q3_pixels/2)!=0 or (Q4_pixels/2)!=0:
        
        part1_p=float(part1)/float(Q1_pixels/2)
        part2_p=float(part2)/float(Q1_pixels/2)
        part3_p=float(part3)/float(Q4_pixels/2)
        part4_p=float(part4)/float(Q4_pixels/2)
        part5_p=float(part5)/float(Q3_pixels/2)
        part6_p=float(part6)/float(Q3_pixels/2)
        part7_p=float(part7)/float(Q2_pixels/2)
        part8_p=float(part8)/float(Q2_pixels/2)
      

    # This piece of code is to find added differences between the
    # obtained letter percentages and the percentages of A
    d1_A=abs(part1_p-d['A'][0])
    d2_A=abs(part2_p-d['A'][1])
    d3_A=abs(part3_p-d['A'][2])
    d4_A=abs(part4_p-d['A'][3])
    d5_A=abs(part5_p-d['A'][4])
    d6_A=abs(part6_p-d['A'][5])
    d7_A=abs(part7_p-d['A'][6])
    d8_A=abs(part8_p-d['A'][7])
    
    A=(d1_A/8)+(d2_A/8)+(d3_A/8)+(d4_A/8)+(d5_A/8)+(d6_A/8)+(d7_A/8)+(d8_A/8)

    
    # Comparing with a
    d1_a=abs(part1_p-d['a'][0])
    d2_a=abs(part2_p-d['a'][1])
    d3_a=abs(part3_p-d['a'][2])
    d4_a=abs(part4_p-d['a'][3])
    d5_a=abs(part5_p-d['a'][4])
    d6_a=abs(part6_p-d['a'][5])
    d7_a=abs(part7_p-d['a'][6])
    d8_a=abs(part8_p-d['a'][7])
    
    a=(d1_a/8)+(d2_a/8)+(d3_a/8)+(d4_a/8)+(d5_a/8)+(d6_a/8)+(d7_a/8)+(d8_a/8)   

    
    # Comparing with B
    d1_B=abs(part1_p-d['B'][0])
    d2_B=abs(part2_p-d['B'][1])
    d3_B=abs(part3_p-d['B'][2])
    d4_B=abs(part4_p-d['B'][3])
    d5_B=abs(part5_p-d['B'][4])
    d6_B=abs(part6_p-d['B'][5])
    d7_B=abs(part7_p-d['B'][6])
    d8_B=abs(part8_p-d['B'][7])
    
    B=(d1_B/8)+(d2_B/8)+(d3_B/8)+(d4_B/8)+(d5_B/8)+(d6_B/8)+(d7_B/8)+(d8_B/8)

    
    # Comparing with b
    d1_b=abs(part1_p-d['b'][0])
    d2_b=abs(part2_p-d['b'][1])
    d3_b=abs(part3_p-d['b'][2])
    d4_b=abs(part4_p-d['b'][3])
    d5_b=abs(part5_p-d['b'][4])
    d6_b=abs(part6_p-d['b'][5])
    d7_b=abs(part7_p-d['b'][6])
    d8_b=abs(part8_p-d['b'][7])
    
    b=(d1_b/8)+(d2_b/8)+(d3_b/8)+(d4_b/8)+(d5_b/8)+(d6_b/8)+(d7_b/8)+(d8_b/8)
    
    
    # Comparing with C
    d1_C=abs(part1_p-d['C'][0])
    d2_C=abs(part2_p-d['C'][1])
    d3_C=abs(part3_p-d['C'][2])
    d4_C=abs(part4_p-d['C'][3])
    d5_C=abs(part5_p-d['C'][4])
    d6_C=abs(part6_p-d['C'][5])
    d7_C=abs(part7_p-d['C'][6])
    d8_C=abs(part8_p-d['C'][7])
    
    C=(d1_C/8)+(d2_C/8)+(d3_C/8)+(d4_C/8)+(d5_C/8)+(d6_C/8)+(d7_C/8)+(d8_C/8)

    
    # Comparing with c
    d1_c=abs(part1_p-d['c'][0])
    d2_c=abs(part2_p-d['c'][1])
    d3_c=abs(part3_p-d['c'][2])
    d4_c=abs(part4_p-d['c'][3])
    d5_c=abs(part5_p-d['c'][4])
    d6_c=abs(part6_p-d['c'][5])
    d7_c=abs(part7_p-d['c'][6])
    d8_c=abs(part8_p-d['c'][7])
    
    c=(d1_c/8)+(d2_c/8)+(d3_c/8)+(d4_c/8)+(d5_c/8)+(d6_c/8)+(d7_c/8)+(d8_c/8)

    
    # Comparing with D
    
    d1_D=abs(part1_p-d['D'][0])
    d2_D=abs(part2_p-d['D'][1])
    d3_D=abs(part3_p-d['D'][2])
    d4_D=abs(part4_p-d['D'][3])
    d5_D=abs(part5_p-d['D'][4])
    d6_D=abs(part6_p-d['D'][5])
    d7_D=abs(part7_p-d['D'][6])
    d8_D=abs(part8_p-d['D'][7])
    
    D=(d1_D/8)+(d2_D/8)+(d3_D/8)+(d4_D/8)+(d5_D/8)+(d6_D/8)+(d7_D/8)+(d8_D/8)

    
    # Comparing with d
    d1_d=abs(part1_p-d['d'][0])
    d2_d=abs(part2_p-d['d'][1])
    d3_d=abs(part3_p-d['d'][2])
    d4_d=abs(part4_p-d['d'][3])
    d5_d=abs(part5_p-d['d'][4])
    d6_d=abs(part6_p-d['d'][5])
    d7_d=abs(part7_p-d['d'][6])
    d8_d=abs(part8_p-d['d'][7])
    
    dletter=(d1_d/8)+(d2_d/8)+(d3_d/8)+(d4_d/8)+(d5_d/8)+(d6_d/8)+(d7_d/8)+(d8_d/8)
    
    # Comparing with E
    d1_E=abs(part1_p-d['E'][0])
    d2_E=abs(part2_p-d['E'][1])
    d3_E=abs(part3_p-d['E'][2])
    d4_E=abs(part4_p-d['E'][3])
    d5_E=abs(part5_p-d['E'][4])
    d6_E=abs(part6_p-d['E'][5])
    d7_E=abs(part7_p-d['E'][6])
    d8_E=abs(part8_p-d['E'][7])
    
    E=(d1_E/8)+(d2_E/8)+(d3_E/8)+(d4_E/8)+(d5_E/8)+(d6_E/8)+(d7_E/8)+(d8_E/8)

    
    # Comparing with e
    d1_e=abs(part1_p-d['e'][0])
    d2_e=abs(part2_p-d['e'][1])
    d3_e=abs(part3_p-d['e'][2])
    d4_e=abs(part4_p-d['e'][3])
    d5_e=abs(part5_p-d['e'][4])
    d6_e=abs(part6_p-d['e'][5])
    d7_e=abs(part7_p-d['e'][6])
    d8_e=abs(part8_p-d['e'][7])
    
    e=(d1_e/8)+(d2_e/8)+(d3_e/8)+(d4_e/8)+(d5_e/8)+(d6_e/8)+(d7_e/8)+(d8_e/8)

    # Comparing with F
    d1_F=abs(part1_p-d['F'][0])
    d2_F=abs(part2_p-d['F'][1])
    d3_F=abs(part3_p-d['F'][2])
    d4_F=abs(part4_p-d['F'][3])
    d5_F=abs(part5_p-d['F'][4])
    d6_F=abs(part6_p-d['F'][5])
    d7_F=abs(part7_p-d['F'][6])
    d8_F=abs(part8_p-d['F'][7])
    
    F=(d1_F/8)+(d2_F/8)+(d3_F/8)+(d4_F/8)+(d5_F/8)+(d6_F/8)+(d7_F/8)+(d8_F/8)

    # Comparing with f
    d1_f=abs(part1_p-d['f'][0])
    d2_f=abs(part2_p-d['f'][1])
    d3_f=abs(part3_p-d['f'][2])
    d4_f=abs(part4_p-d['f'][3])
    d5_f=abs(part5_p-d['f'][4])
    d6_f=abs(part6_p-d['f'][5])
    d7_f=abs(part7_p-d['f'][6])
    d8_f=abs(part8_p-d['f'][7])
    
    f=(d1_f/8)+(d2_f/8)+(d3_f/8)+(d4_f/8)+(d5_f/8)+(d6_f/8)+(d7_f/8)+(d8_f/8)

    # Comparing with G
    d1_G=abs(part1_p-d['G'][0])
    d2_G=abs(part2_p-d['G'][1])
    d3_G=abs(part3_p-d['G'][2])
    d4_G=abs(part4_p-d['G'][3])
    d5_G=abs(part5_p-d['G'][4])
    d6_G=abs(part6_p-d['G'][5])
    d7_G=abs(part7_p-d['G'][6])
    d8_G=abs(part8_p-d['G'][7])
    
    G=(d1_G/8)+(d2_G/8)+(d3_G/8)+(d4_G/8)+(d5_G/8)+(d6_G/8)+(d7_G/8)+(d8_G/8)

     # Comparing with g
    d1_g=abs(part1_p-d['g'][0])
    d2_g=abs(part2_p-d['g'][1])
    d3_g=abs(part3_p-d['g'][2])
    d4_g=abs(part4_p-d['g'][3])
    d5_g=abs(part5_p-d['g'][4])
    d6_g=abs(part6_p-d['g'][5])
    d7_g=abs(part7_p-d['g'][6])
    d8_g=abs(part8_p-d['g'][7])
    
    g=(d1_g/8)+(d2_g/8)+(d3_g/8)+(d4_g/8)+(d5_g/8)+(d6_g/8)+(d7_g/8)+(d8_g/8)

    # Comparing with H
    d1_H=abs(part1_p-d['H'][0])
    d2_H=abs(part2_p-d['H'][1])
    d3_H=abs(part3_p-d['H'][2])
    d4_H=abs(part4_p-d['H'][3])
    d5_H=abs(part5_p-d['H'][4])
    d6_H=abs(part6_p-d['H'][5])
    d7_H=abs(part7_p-d['H'][6])
    d8_H=abs(part8_p-d['H'][7])
    
    H=(d1_H/8)+(d2_H/8)+(d3_H/8)+(d4_H/8)+(d5_H/8)+(d6_H/8)+(d7_H/8)+(d8_H/8)

     # Comparing with h
    d1_h=abs(part1_p-d['h'][0])
    d2_h=abs(part2_p-d['h'][1])
    d3_h=abs(part3_p-d['h'][2])
    d4_h=abs(part4_p-d['h'][3])
    d5_h=abs(part5_p-d['h'][4])
    d6_h=abs(part6_p-d['h'][5])
    d7_h=abs(part7_p-d['h'][6])
    d8_h=abs(part8_p-d['h'][7])
    
    h=(d1_h/8)+(d2_h/8)+(d3_h/8)+(d4_h/8)+(d5_h/8)+(d6_h/8)+(d7_h/8)+(d8_h/8)

    # Comparing with I
    d1_I=abs(part1_p-d['I'][0])
    d2_I=abs(part2_p-d['I'][1])
    d3_I=abs(part3_p-d['I'][2])
    d4_I=abs(part4_p-d['I'][3])
    d5_I=abs(part5_p-d['I'][4])
    d6_I=abs(part6_p-d['I'][5])
    d7_I=abs(part7_p-d['I'][6])
    d8_I=abs(part8_p-d['I'][7])
    
    I=(d1_I/8)+(d2_I/8)+(d3_I/8)+(d4_I/8)+(d5_I/8)+(d6_I/8)+(d7_I/8)+(d8_I/8)

     # Comparing with i
    d1_i=abs(part1_p-d['i'][0])
    d2_i=abs(part2_p-d['i'][1])
    d3_i=abs(part3_p-d['i'][2])
    d4_i=abs(part4_p-d['i'][3])
    d5_i=abs(part5_p-d['i'][4])
    d6_i=abs(part6_p-d['i'][5])
    d7_i=abs(part7_p-d['i'][6])
    d8_i=abs(part8_p-d['i'][7])
    
    i=(d1_i/8)+(d2_i/8)+(d3_i/8)+(d4_i/8)+(d5_i/8)+(d6_i/8)+(d7_i/8)+(d8_i/8)

     # Comparing with J
    d1_J=abs(part1_p-d['J'][0])
    d2_J=abs(part2_p-d['J'][1])
    d3_J=abs(part3_p-d['J'][2])
    d4_J=abs(part4_p-d['J'][3])
    d5_J=abs(part5_p-d['J'][4])
    d6_J=abs(part6_p-d['J'][5])
    d7_J=abs(part7_p-d['J'][6])
    d8_J=abs(part8_p-d['J'][7])
    
    J=(d1_J/8)+(d2_J/8)+(d3_J/8)+(d4_J/8)+(d5_J/8)+(d6_J/8)+(d7_J/8)+(d8_J/8)

     # Comparing with j
    d1_j=abs(part1_p-d['j'][0])
    d2_j=abs(part2_p-d['j'][1])
    d3_j=abs(part3_p-d['j'][2])
    d4_j=abs(part4_p-d['j'][3])
    d5_j=abs(part5_p-d['j'][4])
    d6_j=abs(part6_p-d['j'][5])
    d7_j=abs(part7_p-d['j'][6])
    d8_j=abs(part8_p-d['j'][7])
    
    j=(d1_j/8)+(d2_j/8)+(d3_j/8)+(d4_j/8)+(d5_j/8)+(d6_j/8)+(d7_j/8)+(d8_j/8)
    
     # Comparing with K
    d1_K=abs(part1_p-d['K'][0])
    d2_K=abs(part2_p-d['K'][1])
    d3_K=abs(part3_p-d['K'][2])
    d4_K=abs(part4_p-d['K'][3])
    d5_K=abs(part5_p-d['K'][4])
    d6_K=abs(part6_p-d['K'][5])
    d7_K=abs(part7_p-d['K'][6])
    d8_K=abs(part8_p-d['K'][7])
    
    K=(d1_K/8)+(d2_K/8)+(d3_K/8)+(d4_K/8)+(d5_K/8)+(d6_K/8)+(d7_K/8)+(d8_K/8)

    # Comparing with k
    d1_k=abs(part1_p-d['k'][0])
    d2_k=abs(part2_p-d['k'][1])
    d3_k=abs(part3_p-d['k'][2])
    d4_k=abs(part4_p-d['k'][3])
    d5_k=abs(part5_p-d['k'][4])
    d6_k=abs(part6_p-d['k'][5])
    d7_k=abs(part7_p-d['k'][6])
    d8_k=abs(part8_p-d['k'][7])
    
    k=(d1_k/8)+(d2_k/8)+(d3_k/8)+(d4_k/8)+(d5_k/8)+(d6_k/8)+(d7_k/8)+(d8_k/8)

     # Comparing with L
    d1_L=abs(part1_p-d['L'][0])
    d2_L=abs(part2_p-d['L'][1])
    d3_L=abs(part3_p-d['L'][2])
    d4_L=abs(part4_p-d['L'][3])
    d5_L=abs(part5_p-d['L'][4])
    d6_L=abs(part6_p-d['L'][5])
    d7_L=abs(part7_p-d['L'][6])
    d8_L=abs(part8_p-d['L'][7])
    
    L=(d1_L/8)+(d2_L/8)+(d3_L/8)+(d4_L/8)+(d5_L/8)+(d6_L/8)+(d7_L/8)+(d8_L/8)

    # Comparing with l
    d1_l=abs(part1_p-d['l'][0])
    d2_l=abs(part2_p-d['l'][1])
    d3_l=abs(part3_p-d['l'][2])
    d4_l=abs(part4_p-d['l'][3])
    d5_l=abs(part5_p-d['l'][4])
    d6_l=abs(part6_p-d['l'][5])
    d7_l=abs(part7_p-d['l'][6])
    d8_l=abs(part8_p-d['l'][7])
    
    l=(d1_l/8)+(d2_l/8)+(d3_l/8)+(d4_l/8)+(d5_l/8)+(d6_l/8)+(d7_l/8)+(d8_l/8)

    # Comparing with M
    d1_M=abs(part1_p-d['M'][0])
    d2_M=abs(part2_p-d['M'][1])
    d3_M=abs(part3_p-d['M'][2])
    d4_M=abs(part4_p-d['M'][3])
    d5_M=abs(part5_p-d['M'][4])
    d6_M=abs(part6_p-d['M'][5])
    d7_M=abs(part7_p-d['M'][6])
    d8_M=abs(part8_p-d['M'][7])
    
    M=(d1_M/8)+(d2_M/8)+(d3_M/8)+(d4_M/8)+(d5_M/8)+(d6_M/8)+(d7_M/8)+(d8_M/8)

    # Comparing with m
    d1_m=abs(part1_p-d['m'][0])
    d2_m=abs(part2_p-d['m'][1])
    d3_m=abs(part3_p-d['m'][2])
    d4_m=abs(part4_p-d['m'][3])
    d5_m=abs(part5_p-d['m'][4])
    d6_m=abs(part6_p-d['m'][5])
    d7_m=abs(part7_p-d['m'][6])
    d8_m=abs(part8_p-d['m'][7])
    
    m=(d1_m/8)+(d2_m/8)+(d3_m/8)+(d4_m/8)+(d5_m/8)+(d6_m/8)+(d7_m/8)+(d8_m/8)

    # Comparing with N
    d1_N=abs(part1_p-d['N'][0])
    d2_N=abs(part2_p-d['N'][1])
    d3_N=abs(part3_p-d['N'][2])
    d4_N=abs(part4_p-d['N'][3])
    d5_N=abs(part5_p-d['N'][4])
    d6_N=abs(part6_p-d['N'][5])
    d7_N=abs(part7_p-d['N'][6])
    d8_N=abs(part8_p-d['N'][7])
    
    N=(d1_N/8)+(d2_N/8)+(d3_N/8)+(d4_N/8)+(d5_N/8)+(d6_N/8)+(d7_N/8)+(d8_N/8)

    # Comparing with n
    d1_n=abs(part1_p-d['n'][0])
    d2_n=abs(part2_p-d['n'][1])
    d3_n=abs(part3_p-d['n'][2])
    d4_n=abs(part4_p-d['n'][3])
    d5_n=abs(part5_p-d['n'][4])
    d6_n=abs(part6_p-d['n'][5])
    d7_n=abs(part7_p-d['n'][6])
    d8_n=abs(part8_p-d['n'][7])
    
    n=(d1_n/8)+(d2_n/8)+(d3_n/8)+(d4_n/8)+(d5_n/8)+(d6_n/8)+(d7_n/8)+(d8_n/8)

    # Comparing with O
    d1_O=abs(part1_p-d['O'][0])
    d2_O=abs(part2_p-d['O'][1])
    d3_O=abs(part3_p-d['O'][2])
    d4_O=abs(part4_p-d['O'][3])
    d5_O=abs(part5_p-d['O'][4])
    d6_O=abs(part6_p-d['O'][5])
    d7_O=abs(part7_p-d['O'][6])
    d8_O=abs(part8_p-d['O'][7])
    
    O=(d1_O/8)+(d2_O/8)+(d3_O/8)+(d4_O/8)+(d5_O/8)+(d6_O/8)+(d7_O/8)+(d8_O/8)

    # Comparing with o
    d1_o=abs(part1_p-d['o'][0])
    d2_o=abs(part2_p-d['o'][1])
    d3_o=abs(part3_p-d['o'][2])
    d4_o=abs(part4_p-d['o'][3])
    d5_o=abs(part5_p-d['o'][4])
    d6_o=abs(part6_p-d['o'][5])
    d7_o=abs(part7_p-d['o'][6])
    d8_o=abs(part8_p-d['o'][7])
    
    o=(d1_o/8)+(d2_o/8)+(d3_o/8)+(d4_o/8)+(d5_o/8)+(d6_o/8)+(d7_o/8)+(d8_o/8)

    # Comparing with p
    d1_p=abs(part1_p-d['p'][0])
    d2_p=abs(part2_p-d['p'][1])
    d3_p=abs(part3_p-d['p'][2])
    d4_p=abs(part4_p-d['p'][3])
    d5_p=abs(part5_p-d['p'][4])
    d6_p=abs(part6_p-d['p'][5])
    d7_p=abs(part7_p-d['p'][6])
    d8_p=abs(part8_p-d['p'][7])
    
    p=(d1_p/8)+(d2_p/8)+(d3_p/8)+(d4_p/8)+(d5_p/8)+(d6_p/8)+(d7_p/8)+(d8_p/8)

    # Comparing with P
    d1_P=abs(part1_p-d['P'][0])
    d2_P=abs(part2_p-d['P'][1])
    d3_P=abs(part3_p-d['P'][2])
    d4_P=abs(part4_p-d['P'][3])
    d5_P=abs(part5_p-d['P'][4])
    d6_P=abs(part6_p-d['P'][5])
    d7_P=abs(part7_p-d['P'][6])
    d8_P=abs(part8_p-d['P'][7])
    
    P=(d1_P/8)+(d2_P/8)+(d3_P/8)+(d4_P/8)+(d5_P/8)+(d6_P/8)+(d7_P/8)+(d8_P/8)

    # Comparing with Q
    d1_Q=abs(part1_p-d['Q'][0])
    d2_Q=abs(part2_p-d['Q'][1])
    d3_Q=abs(part3_p-d['Q'][2])
    d4_Q=abs(part4_p-d['Q'][3])
    d5_Q=abs(part5_p-d['Q'][4])
    d6_Q=abs(part6_p-d['Q'][5])
    d7_Q=abs(part7_p-d['Q'][6])
    d8_Q=abs(part8_p-d['Q'][7])
    
    Q=(d1_Q/8)+(d2_Q/8)+(d3_Q/8)+(d4_Q/8)+(d5_Q/8)+(d6_Q/8)+(d7_Q/8)+(d8_Q/8)

    # Comparing with q
    d1_q=abs(part1_p-d['q'][0])
    d2_q=abs(part2_p-d['q'][1])
    d3_q=abs(part3_p-d['q'][2])
    d4_q=abs(part4_p-d['q'][3])
    d5_q=abs(part5_p-d['q'][4])
    d6_q=abs(part6_p-d['q'][5])
    d7_q=abs(part7_p-d['q'][6])
    d8_q=abs(part8_p-d['q'][7])
    
    q=(d1_q/8)+(d2_q/8)+(d3_q/8)+(d4_q/8)+(d5_q/8)+(d6_q/8)+(d7_q/8)+(d8_q/8)

    # Comparing with R
    d1_R=abs(part1_p-d['R'][0])
    d2_R=abs(part2_p-d['R'][1])
    d3_R=abs(part3_p-d['R'][2])
    d4_R=abs(part4_p-d['R'][3])
    d5_R=abs(part5_p-d['R'][4])
    d6_R=abs(part6_p-d['R'][5])
    d7_R=abs(part7_p-d['R'][6])
    d8_R=abs(part8_p-d['R'][7])
    
    R=(d1_R/8)+(d2_R/8)+(d3_R/8)+(d4_R/8)+(d5_R/8)+(d6_R/8)+(d7_R/8)+(d8_R/8)
        
    # Comparing with r
    d1_r=abs(part1_p-d['r'][0])
    d2_r=abs(part2_p-d['r'][1])
    d3_r=abs(part3_p-d['r'][2])
    d4_r=abs(part4_p-d['r'][3])
    d5_r=abs(part5_p-d['r'][4])
    d6_r=abs(part6_p-d['r'][5])
    d7_r=abs(part7_p-d['r'][6])
    d8_r=abs(part8_p-d['r'][7])
    
    r=(d1_r/8)+(d2_r/8)+(d3_r/8)+(d4_r/8)+(d5_r/8)+(d6_r/8)+(d7_r/8)+(d8_r/8)

    # Comparing with S
    d1_S=abs(part1_p-d['S'][0])
    d2_S=abs(part2_p-d['S'][1])
    d3_S=abs(part3_p-d['S'][2])
    d4_S=abs(part4_p-d['S'][3])
    d5_S=abs(part5_p-d['S'][4])
    d6_S=abs(part6_p-d['S'][5])
    d7_S=abs(part7_p-d['S'][6])
    d8_S=abs(part8_p-d['S'][7])
    
    S=(d1_S/8)+(d2_S/8)+(d3_S/8)+(d4_S/8)+(d5_S/8)+(d6_S/8)+(d7_S/8)+(d8_S/8)

    # Comparing with s
    d1_s=abs(part1_p-d['s'][0])
    d2_s=abs(part2_p-d['s'][1])
    d3_s=abs(part3_p-d['s'][2])
    d4_s=abs(part4_p-d['s'][3])
    d5_s=abs(part5_p-d['s'][4])
    d6_s=abs(part6_p-d['s'][5])
    d7_s=abs(part7_p-d['s'][6])
    d8_s=abs(part8_p-d['s'][7])
    
    s=(d1_s/8)+(d2_s/8)+(d3_s/8)+(d4_s/8)+(d5_s/8)+(d6_s/8)+(d7_s/8)+(d8_s/8)

    # Comparing with T
    d1_T=abs(part1_p-d['T'][0])
    d2_T=abs(part2_p-d['T'][1])
    d3_T=abs(part3_p-d['T'][2])
    d4_T=abs(part4_p-d['T'][3])
    d5_T=abs(part5_p-d['T'][4])
    d6_T=abs(part6_p-d['T'][5])
    d7_T=abs(part7_p-d['T'][6])
    d8_T=abs(part8_p-d['T'][7])
    
    T=(d1_T/8)+(d2_T/8)+(d3_T/8)+(d4_T/8)+(d5_T/8)+(d6_T/8)+(d7_T/8)+(d8_T/8)

    # Comparing with t
    d1_t=abs(part1_p-d['t'][0])
    d2_t=abs(part2_p-d['t'][1])
    d3_t=abs(part3_p-d['t'][2])
    d4_t=abs(part4_p-d['t'][3])
    d5_t=abs(part5_p-d['t'][4])
    d6_t=abs(part6_p-d['t'][5])
    d7_t=abs(part7_p-d['t'][6])
    d8_t=abs(part8_p-d['t'][7])
    
    t=(d1_t/8)+(d2_t/8)+(d3_t/8)+(d4_t/8)+(d5_t/8)+(d6_t/8)+(d7_t/8)+(d8_t/8)

    # Comparing with U
    d1_U=abs(part1_p-d['U'][0])
    d2_U=abs(part2_p-d['U'][1])
    d3_U=abs(part3_p-d['U'][2])
    d4_U=abs(part4_p-d['U'][3])
    d5_U=abs(part5_p-d['U'][4])
    d6_U=abs(part6_p-d['U'][5])
    d7_U=abs(part7_p-d['U'][6])
    d8_U=abs(part8_p-d['U'][7])
    
    U=(d1_U/8)+(d2_U/8)+(d3_U/8)+(d4_U/8)+(d5_U/8)+(d6_U/8)+(d7_U/8)+(d8_U/8)

    # Comparing with u
    d1_u=abs(part1_p-d['u'][0])
    d2_u=abs(part2_p-d['u'][1])
    d3_u=abs(part3_p-d['u'][2])
    d4_u=abs(part4_p-d['u'][3])
    d5_u=abs(part5_p-d['u'][4])
    d6_u=abs(part6_p-d['u'][5])
    d7_u=abs(part7_p-d['u'][6])
    d8_u=abs(part8_p-d['u'][7])
    
    u=(d1_u/8)+(d2_u/8)+(d3_u/8)+(d4_u/8)+(d5_u/8)+(d6_u/8)+(d7_u/8)+(d8_u/8)

    # Comparing with V
    d1_V=abs(part1_p-d['V'][0])
    d2_V=abs(part2_p-d['V'][1])
    d3_V=abs(part3_p-d['V'][2])
    d4_V=abs(part4_p-d['V'][3])
    d5_V=abs(part5_p-d['V'][4])
    d6_V=abs(part6_p-d['V'][5])
    d7_V=abs(part7_p-d['V'][6])
    d8_V=abs(part8_p-d['V'][7])
    
    V=(d1_V/8)+(d2_V/8)+(d3_V/8)+(d4_V/8)+(d5_V/8)+(d6_V/8)+(d7_V/8)+(d8_V/8)

    # Comparing with v
    d1_v=abs(part1_p-d['v'][0])
    d2_v=abs(part2_p-d['v'][1])
    d3_v=abs(part3_p-d['v'][2])
    d4_v=abs(part4_p-d['v'][3])
    d5_v=abs(part5_p-d['v'][4])
    d6_v=abs(part6_p-d['v'][5])
    d7_v=abs(part7_p-d['v'][6])
    d8_v=abs(part8_p-d['v'][7])
    
    v=(d1_v/8)+(d2_v/8)+(d3_v/8)+(d4_v/8)+(d5_v/8)+(d6_v/8)+(d7_v/8)+(d8_v/8)

    # Comparing with W
    d1_W=abs(part1_p-d['W'][0])
    d2_W=abs(part2_p-d['W'][1])
    d3_W=abs(part3_p-d['W'][2])
    d4_W=abs(part4_p-d['W'][3])
    d5_W=abs(part5_p-d['W'][4])
    d6_W=abs(part6_p-d['W'][5])
    d7_W=abs(part7_p-d['W'][6])
    d8_W=abs(part8_p-d['W'][7])
    
    W=(d1_W/8)+(d2_W/8)+(d3_W/8)+(d4_W/8)+(d5_W/8)+(d6_W/8)+(d7_W/8)+(d8_W/8)

    # Comparing with w
    d1_w=abs(part1_p-d['w'][0])
    d2_w=abs(part2_p-d['w'][1])
    d3_w=abs(part3_p-d['w'][2])
    d4_w=abs(part4_p-d['w'][3])
    d5_w=abs(part5_p-d['w'][4])
    d6_w=abs(part6_p-d['w'][5])
    d7_w=abs(part7_p-d['w'][6])
    d8_w=abs(part8_p-d['w'][7])
    
    w=(d1_w/8)+(d2_w/8)+(d3_w/8)+(d4_w/8)+(d5_w/8)+(d6_w/8)+(d7_w/8)+(d8_w/8)

    # Comparing with X

    d1_X=abs(part1_p-d['X'][0])
    d2_X=abs(part2_p-d['X'][1])
    d3_X=abs(part3_p-d['X'][2])
    d4_X=abs(part4_p-d['X'][3])
    d5_X=abs(part5_p-d['X'][4])
    d6_X=abs(part6_p-d['X'][5])
    d7_X=abs(part7_p-d['X'][6])
    d8_X=abs(part8_p-d['X'][7])
    
    X=(d1_X/8)+(d2_X/8)+(d3_X/8)+(d4_X/8)+(d5_X/8)+(d6_X/8)+(d7_X/8)+(d8_X/8)

    # COmparing with x

    d1_x=abs(part1_p-d['x'][0])
    d2_x=abs(part2_p-d['x'][1])
    d3_x=abs(part3_p-d['x'][2])
    d4_x=abs(part4_p-d['x'][3])
    d5_x=abs(part5_p-d['x'][4])
    d6_x=abs(part6_p-d['x'][5])
    d7_x=abs(part7_p-d['x'][6])
    d8_x=abs(part8_p-d['x'][7])
    
    x=(d1_x/8)+(d2_x/8)+(d3_x/8)+(d4_x/8)+(d5_x/8)+(d6_x/8)+(d7_x/8)+(d8_x/8)

    # Comparing with Y

    d1_Y=abs(part1_p-d['Y'][0])
    d2_Y=abs(part2_p-d['Y'][1])
    d3_Y=abs(part3_p-d['Y'][2])
    d4_Y=abs(part4_p-d['Y'][3])
    d5_Y=abs(part5_p-d['Y'][4])
    d6_Y=abs(part6_p-d['Y'][5])
    d7_Y=abs(part7_p-d['Y'][6])
    d8_Y=abs(part8_p-d['Y'][7])
    
    Y=(d1_Y/8)+(d2_Y/8)+(d3_Y/8)+(d4_Y/8)+(d5_Y/8)+(d6_Y/8)+(d7_Y/8)+(d8_Y/8)

    # Comparing with y

    d1_y=abs(part1_p-d['y'][0])
    d2_y=abs(part2_p-d['y'][1])
    d3_y=abs(part3_p-d['y'][2])
    d4_y=abs(part4_p-d['y'][3])
    d5_y=abs(part5_p-d['y'][4])
    d6_y=abs(part6_p-d['y'][5])
    d7_y=abs(part7_p-d['y'][6])
    d8_y=abs(part8_p-d['y'][7])
    
    y=(d1_y/8)+(d2_y/8)+(d3_y/8)+(d4_y/8)+(d5_y/8)+(d6_y/8)+(d7_y/8)+(d8_y/8)

    # Comparing with Z

    d1_Z=abs(part1_p-d['Z'][0])
    d2_Z=abs(part2_p-d['Z'][1])
    d3_Z=abs(part3_p-d['Z'][2])
    d4_Z=abs(part4_p-d['Z'][3])
    d5_Z=abs(part5_p-d['Z'][4])
    d6_Z=abs(part6_p-d['Z'][5])
    d7_Z=abs(part7_p-d['Z'][6])
    d8_Z=abs(part8_p-d['Z'][7])
    
    Z=(d1_Z/8)+(d2_Z/8)+(d3_Z/8)+(d4_Z/8)+(d5_Z/8)+(d6_Z/8)+(d7_Z/8)+(d8_Z/8)

    # Comparing with z

    d1_z=abs(part1_p-d['z'][0])
    d2_z=abs(part2_p-d['z'][1])
    d3_z=abs(part3_p-d['z'][2])
    d4_z=abs(part4_p-d['z'][3])
    d5_z=abs(part5_p-d['z'][4])
    d6_z=abs(part6_p-d['z'][5])
    d7_z=abs(part7_p-d['z'][6])
    d8_z=abs(part8_p-d['z'][7])
    
    z=(d1_z/8)+(d2_z/8)+(d3_z/8)+(d4_z/8)+(d5_z/8)+(d6_z/8)+(d7_z/8)+(d8_z/8)
    
             
    possible=[A,a,B,b,C,c,D,dletter,E,e,F,f,G,g,H,h,I,i,J,j,K,k,L,l,M,m,N,n,O,o,P,p,Q,q,R,r,S,s,T,t,U,u,V,v,W,w,X,x,Y,y,Z,z]
    possible.sort()# This sorts the list so that the first element is the smallest
    #print possible
    
    
    if possible[0]==A: # These conditionals checks for which number the proccesed one corresponds 
        return 'A'
    if possible[0]==a:
        return 'a'
    if possible[0]==B:
        return 'B'
    if possible[0]==b:
        return 'b'
    if possible[0]==C:
        return 'C'
    if possible[0]==c:
        return 'c'
    if possible[0]==D:
        return 'D'
    if possible[0]==dletter:
        return 'd'
    if possible[0]==E:
        return 'E'
    if possible[0]==e:
        return 'e'
    if possible[0]==F:
        return 'F'
    if possible[0]==f:
        return 'f'
    if possible[0]==G:
        return 'G'
    if possible[0]==g:
        return 'g'
    if possible[0]==H:
        return 'H'
    if possible[0]==h:
        return 'h'
    if possible[0]==I:
        return 'I'
    if possible[0]==i:
        return 'i'
    if possible[0]==J:
        return 'J'
    if possible[0]==j:
        return 'j'
    if possible[0]==K:
        return 'K'
    if possible[0]==k:
        return 'k'
    if possible[0]==L:
        return 'L'
    if possible[0]==l:
        return 'l'
    if possible[0]==M:
        return 'M'
    if possible[0]==m:
        return 'm'
    if possible[0]==N:
        return 'N'
    if possible[0]==n:
        return 'n'
    if possible[0]==O:
        return 'O'
    if possible[0]==o:
        return 'o'
    if possible[0]==P:
        return 'P'
    if possible[0]==p:
        return 'p'
    if possible[0]==Q:
        return 'Q'
    if possible[0]==q:
        return 'q'
    if possible[0]==R:
        return 'R'
    if possible[0]==r:
        return 'r'
    if possible[0]==S:
        return 'S'
    if possible[0]==s:
        return 's'
    if possible[0]==T:
        return 'T'
    if possible[0]==t:
        return 't'
    if possible[0]==U:
        return 'U'
    if possible[0]==u:
        return 'u'
    if possible[0]==V:
        return 'V'
    if possible[0]==v:
        return 'v'
    if possible[0]==W:
        return 'W'
    if possible[0]==w:
        return 'w'
    if possible[0]==X:
        return 'X'
    if possible[0]==x:
        return 'x'
    if possible[0]==Y:
        return 'Y'
    if possible[0]==y:
        return 'y'
    if possible[0]==Z:
        return 'Z'
    if possible[0]==z:
        return 'z'

def lastcolumn(pic,startrow,endrow):
    
    rows=getHeight(pic)
    columns=getWidth(pic)
    for c in range(columns):
        islast=False
        for r in range(startrow,endrow):
            g=getColor(pic,c,r)
            if g==[0,0,0] and not islast:
                last=c
                islast=True
    return last

def readAll(filename,d):
    lst=[]
    
    word=''
    pic=loadPicture(filename)
    convertBlackWhite(pic)
    lines=detectline(pic)
    print lines
    for line in lines:
        line1start=line[0]
        line1end=line[1]
        letterend=0
        word+='\n'
        while letterend<lastcolumn(pic,line[0],line[1]):
            col=detectletter(pic,line1start,line1end,letterend)
            letterstartrow=letterlimit(pic,line1start,line1end,letterend)[0]
            letterendrow=letterlimit(pic,line1start,line1end,letterend)[1]
            letterstart=col[0]
            if letterstart-letterend > 5:
                word+=' '
            letterend=col[1]+1
            #print letterend
            #print letterstartrow , letterendrow ,letterstart, letterend
            letters1=readLetter(pic,letterstartrow,letterendrow,letterstart,letterend,d)
            word+=letters1
    F=open('name','w')
    F.write(word)
    F.close()
    print word    
print readAll('test11.jpg',d)


import imp
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

import galois
import numpy as np
import string
allVals= ["^","x","+"," ","   ","  ","    "]

for i in range(0,500):
    allVals.append(str(i))

#utility function to build arrays of size 500 of all 0's
def arr(c):
    for i in range(0,500):
        c.append(0)
    return c

#x and xErr will be used for error handling
x="x^"
xErr=[]
xErr.append("1")
xErr.append("x")
xErr.append(" ")
for i in range(2,499):
    conv=str(i)
    xErr.append(x+conv)
    xErr.append(x+conv+" ")
    xErr.append(" "+x+conv)
    xErr.append(x+conv+"  ")
    xErr.append("  "+x+conv)
    xErr.append(x+conv+"   ")
    xErr.append("   "+x+conv)
    xErr.append(x+conv+"    ")
    xErr.append("    "+x+conv)


#building the irreducible polynomials
irr1=arr([])
irr2=arr([])
irr1[0]=1
irr1[3]=1
irr1[6]=1
irr1[7]=1
irr2[0]=1
irr2[3]=1
irr2[6]=1
irr2[7]=1
irr2[163]=1

#setting up the 2 formats of the irreducible polynomial that we will be using

def getPoly(poly):      #get array format of polynomial from string format
    coeffs=arr([])
    
    ss=poly.split("+")
    
    for j in ss:
        if j=="1":
            coeffs[0]=1
        else:
            if j=="x":
                    coeffs[1]=1
            else:
                    for i in range(0,len(j)):
                        if j[i]=="^":
                            sss=j[i+1:len(j)]
                            conv=int(sss)
                            if conv>0:
                                
                                if coeffs[conv]==1: 
                                    coeffs[conv]=0
                                else:
                                    coeffs[conv]=1
                            else:
                                if coeffs[-conv]==1:
                                    coeffs[-conv]=0
                                else:
                                    coeffs[-conv]=1 
    return coeffs

#takes 2 arrays polynomials and xor them
def xor(a,b):
    
    c=arr([])
    for i in range(0,500):     
        if (a[i]==0 and b[i]==0 ) or (a[i]==1 and b[i]==1):
            c[i]=0
        else:
            c[i]=1
    return c
    
#takes string poly and gives the order of the polynomial
def order(poly):
    max=0
    for i in range(0,len(poly)):
        if poly[i]==1:
            max=i
    return max
    
def add(poly1,poly2):
    coeffs=xor(poly1,poly2)
    return modReduc(coeffs)
   
#takes string polynomial

def polystr(a):     #get string format of polynomial from array format
    
    s=""
    for i in range(len(a)-1,1,-1):
        if a[i]==1:
            s=s+"x^"+str(i)+"+"
    s=s[:-1]
    if(a[1]==1):
        if(s==""):
            s=s+"x"
        else:
            s=s+"+x"
    if(a[0]==1):
        if(s==""):
            s=s+"1"
        else:
            s=s+"+1"
    if(s==""):
       s="0"
    return s
#takes string polynomial

#mutliply a poly by a poly of the form x^o
def mult2(pol1,o):
    if o==0:
        return pol1
    else:
        for i in range(0,o):
            pol1=shiftright(pol1)
    return pol1
            
    
#takes 2 strings 
def mult(poly1,poly2):
    result=[arr([])]
    for i in range(0,len(poly2)):
        if poly2[i]==1:
            b=mult2(poly1,i)
            result.append(b)
    c=arr([])
    for i in result:
       c=xor(c,i)
    return modReduc(c)

def sub(poly1,poly2):
    coeffs=xor(poly1,poly2)
    return coeffs

def shiftright(poly):
    c=arr([])
    for i in range(1,len(poly)):
        c[i]=poly[i-1]
    return c

def modReduc(poly1):
    quotient=arr([])
    remainder=arr([])
    result=[quotient,remainder]
    o1=order(poly1)
    o2=order(irr2)
    if(o1<o2):
            result[1]=(poly1)
            remainder=(poly1)
    else:
        
        while(o1>=o2):
            o=o1-o2
            quotient[o]=1
            temp=arr([])
            temp[o]=quotient[o]
            temp2=mult2(irr2,o)
            temp3=add(temp2,poly1)
            poly1=temp3     #update poly1 to be the remainder
            o1=order(poly1)
    return poly1

#takes 2 polynomials, find the quotiend and remainder after dividing poly1 by poly2 
def div(poly1,poly2):
    temp=inverse(poly2)
    return mult(temp,poly1)

def quotRem(poly1,poly2):
    o1=order(poly1)
    o2=order(poly2)
    quotient=arr([])
    remainder=arr([])
    if(o1>o2):
       while(o1>=o2):
           o=o1-o2
           quotient[o]=1
           temp1=mult2(poly2, o)
           temp2=add(temp1,poly1)
           poly1=temp2
           o1=order(poly1)
           remainder=poly1
    else:
        remainder=poly1
        
    return [quotient,remainder]


def inverse(poly):      #we will be using euclid's extended algo to find the inverse of polynomial "poly"
        if order(poly)==163:
            poly=modReduc(poly)
        a1=arr([])
        a2=arr([])
        a2[0]=1
        BB=[a1,a2,poly]
        AA=[a2,a1,irr2]
        i=0
        while(BB[2]!=a2):
            poly1=AA[2]
            poly2=BB[2]  
            temp=quotRem(poly1,poly2)
            temp2=[modReduc(add((AA[0]),mult((BB[0]),(temp[0])))),modReduc(add((AA[1]),mult((BB[1]),(temp[0])))),temp[1]]
            AA[0]=BB[0]
            AA[1]=BB[1]
            AA[2]=BB[2]
            BB[0]=temp2[0]
            BB[1]=temp2[1]
            BB[2]=temp2[2]

        if BB[2]==getPoly(""):
            return "No inverse"
        if BB[2]==getPoly("x^0"):
            return BB[1]
def split(word):
    return [char for char in word]

#function to handle all wrong format inputs
def errorHandling(poly):
    f1=arr([])
    f2=arr([])
    errors=[]
    s=poly.split("+")
    ss=split(poly)
    for i in range(0,len(ss)):
        f1[i]=False
        for j in allVals:
            if ss[i]==j:
                f1[i]=True
        if f1[i]==False:
             errors.append(ss[i])
    for i in range(0,len(s)):
        f2[i]=False
        for j in xErr:
            if s[i]==j:
                f2[i]=True
        if f2[i]==False:
            errors.append(s[i])
        
    return errors

                    
# x^163 + x^7 + x^6 + x^3 + 1


#######TESTING THE FUNCTIONS

# print("Note: All results are modulo GF(2**163)")
# pol1=input("Please enter the first polynomial (Enter the polynomial and all the remaining in the following format: x^43 +x^21+...+x^1+x^0 as an example): ")
# pol2=input("Please enter the second polynomial: ")
# print(errorHandling(pol1))
# print(pol1.split("+"))
# ee1=errorHandling(pol1)
# ee2=errorHandling(pol2)
# if len(ee1)>0 or len(ee2)>0:
#        raise Exception("Sorry, wrong input format")
# poly1=getPoly(pol1)
# poly2=getPoly(pol2)
# pol3=add(poly1,poly2)
# pol4=mult(poly1,poly2)

# pol9=sub(poly1,poly2)
# pol10=div(poly1,poly2)
# print("Addition of first 2 polynomials: ",polystr(pol3))
# print("Multiplication of first 2 polynomials: ",polystr(pol4))
# print("Substration of first 2 polynomials: ",polystr(pol9))
# print("Division of first 2 polynomials: ",polystr(pol10))
# pol5=input("Please enter a third polynomial whose inverse is to be found: ")
# ee5=errorHandling(pol5)
# if len(ee5)>0:
#        raise Exception("Sorry, wrong input format")
# poly5=getPoly(pol5)
# pol6=inverse(poly5)

# print("Inverse of third polynomial: ",polystr(pol6))
# print("Verification that inverse is correct: ",polystr(mult(pol6,poly5)))
# pol7=input("Please enter a polynomial of degree larger than 163 to show its reduction in GF(2^8): ")
# ee7=errorHandling(pol7)
# if len(ee7)>0:
#        raise Exception("Sorry, wrong input format")
# poly7=getPoly(pol7)
# pol8=modReduc(poly7)
# print("reduction to: ",polystr(pol8))



@app.route('/getPolyOperations', methods=['POST'])
def getPolyOperations():
    
    ee1=errorHandling(request.json["firstOperand"])
    ee2=errorHandling(request.json["secondOperand"])
    if len(ee1)>0 or len(ee2)>0:
        return jsonify(result="Sorry, wrong input format")

    firstOperand = getPoly(request.json["firstOperand"])
    secondOperand = getPoly(request.json["secondOperand"])
    operation = request.json["operation"]

    if operation == '+':
        return jsonify(result=polystr(add(firstOperand, secondOperand)))
    elif operation == '-':
        return jsonify(result=polystr(sub(firstOperand, secondOperand)))
    elif operation == '*':
        return jsonify(result=polystr(mult(firstOperand, secondOperand)))
    elif operation == '/':
        return jsonify(result=polystr(div(firstOperand, secondOperand)))
    else:
        return jsonify(result='Error')

@app.route('/getPolyInverse', methods=['POST'])
def getPolyInverse():

    ee3=errorHandling(request.json["thirdOperand"])
    if len(ee3)>0:
        return jsonify(result="Sorry, wrong input format")
    
    thridOperand = getPoly(request.json["thirdOperand"])
    return jsonify(result=polystr(inverse(thridOperand)))

@app.route('/getPolyModulo', methods=['POST'])
def getPolyModulo():
    ee4=errorHandling(request.json["forthOperand"])
    if len(ee4)>0:
        return jsonify(result="Sorry, wrong input format")

    forthOperand = getPoly(request.json["forthOperand"])
    return jsonify(result=polystr(modReduc(forthOperand)))


if __name__ == "__main__":
    app.run(debug=True)
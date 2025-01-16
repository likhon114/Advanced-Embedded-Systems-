def series(r1,r2):
    Rs=r1+r2
    return Rs

def parallel(r1,r2):
    Rp = 1/(1/r1 + 1/r2)
    return Rp

R1= series(30,400)
r2 = parallel(200,300)
R2= parallel(r2,R1)

R3= series(R2,20)

I1= R3*10/(100+R3)
i2= 100*10/(100+R3)

I2=parallel(300,430)*i2/(200+parallel(300,430))
I3=parallel(200,430)*i2/(300+parallel(200,430))
I4=parallel(200,300)*i2/(430+parallel(200,300))

print(f"the current I1 is ",I1)
print(f"the current I2 is ",I2)
print(f"the current I3 is ",I3)
print(f"the current I4 is ",I4)
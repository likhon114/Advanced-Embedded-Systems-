def series(r1,r2):
    Rs=r1+r2
    return Rs

def parallel(r1,r2):
    Rp = 1/(1/r1 + 1/r2)
    return Rp

R1= series(400,30)
r2=parallel(R1,300)
R2=parallel(r2,200)

R3= series(R2,20)
R4=parallel(R3,100)

V0=10
V1=R4*10/(10+R4)
V2=R2*V1/(R2+20)
V3=400*V2/(400+30)


print(f'Volatage is V0 ', V0)
print(f'Volatage is V1 ', V1)
print(f'Volatage is V2 ', V2)
print(f'Volatage is V3 ', V3)
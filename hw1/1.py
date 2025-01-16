def series(r1,r2):
    Rs=r1+r2
    return Rs

def parallel(r1,r2):
    Rp = 1/(1/r1 + 1/r2)
    return Rp

R1= parallel(500,600)
R2 = series(R1,400)
R3=parallel(R2,100)
r4= series(200,300)
R4=series(r4,R3)
R5= parallel(R4,700)

print(f"The equivalent resistance is ", R5)
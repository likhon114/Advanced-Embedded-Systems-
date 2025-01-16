def series(r1,r2):
    Rs=r1+r2
    return Rs

def parallel(r1,r2):
    Rp = 1/(1/r1 + 1/r2)
    return Rp

Z1=series(400,30j)
z2=parallel(Z1,300)
Z2=parallel(z2,-200j)
Z3=series(Z2,20)
Z4=parallel(Z3,100)
Z5=series(Z4,10j)

print(f'the impedance is ', Z5)
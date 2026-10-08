def gcd(a,b):
    while a != 0:
        r = b % a
        b = a
        a = r
    return b

def lcm(a,b):
    return a*b//gcd(a,b)

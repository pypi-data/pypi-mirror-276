# input a,b mit sign(f(a)) != sign(f(b)), Funktion f(x), iterations to do
def bisection(a,b,f,i):
    if(f(a) * f(b) > 0):
        print("Falsche Inputwerte")
        return
    if(f(a) > 0):
        os = a
        us = b
    else:
        os = b
        us = a
    for j in range(i):
        v = f((1/2)*(os+us))
        #print(f"Akutelle Lösung x = {(1/2)*(os+us)} mit f(x) {abs(v)}")
        print(f"Iteration:{j} \t I [{us};{os}] \t\t  x = {(1/2)*(os+us)} \t f(x) = {v}")
        if (v>0):
            os = (1/2)*(os+us)
        else:
            us = (1/2)*(os+us)
    return ((1/2)*(os+us), v)

    
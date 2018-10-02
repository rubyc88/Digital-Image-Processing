rf = [2000, 2200, 2400, 2700, 3000, 3300, 3600, 3900, 4300, 4700, 5100, 5600, 6200, 6800, 7500, 8200, 9100, 10000, 11000, 12000, 13000, 15000, 16000, 18000, 20000, 22000, 24000, 27000, 30000, 33000]
ri = rf
for i in range (0, len(ri),1):
    for j in range(0, len(rf),1):
        ratio = rf[i]/ri[j]
        if ratio >3.8  and ratio < 4.1:
            a = (rf[i]/ri[j])/23.39
            #gain = rf[i]/(r[i]*a)
            if a > 0.169:# and gain < 26 and gain >20:
                print("rf : " + str(rf[i]) +", ri: " + str(ri[j]) +", a: "+ str(a))
# gain max = 26 linear           
gain = rf/(ri*a)
fl=1/(2*pi*ri*Cb) 
fh = A/(2*pi*rf*Cint)




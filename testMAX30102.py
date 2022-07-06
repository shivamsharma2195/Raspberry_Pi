import max30102
import hrcalc

m = max30102.MAX30102()
sumHR = 0
sumSPO2 = 0
hr2 = 0
sp2 = 0
pos=0
# for better results we use HR and SPO2 averaging you can remove averaging
# below array will get replaced by every new value using queue concept
HR=[75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75]
SPO2=[100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100]

while True:
    red, ir = m.read_sequential()
    
    hr,hrb,sp,spb = hrcalc.calc_hr_and_spo2(ir, red)

    if(hrb == True and hr != -999):
        HR[pos]=int(hr)
        for i in HR:
            sumHR=sumHR+i
        hr2 = sumHR/30
        sumHR = 0
        print("Heart Rate : ",int(hr2))
    if(spb == True and sp != -999):
        SPO2[pos]=int(sp)
        for i in SPO2:
            sumSPO2 = sumSPO2+i
        sp2 = sumSPO2/30
        sumSPO2 = 0
        print("SPO2       : ",int(sp2))
    pos += 1
    pos %= 30

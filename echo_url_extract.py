from structureReader import structureReader as sr
import os
import sys
import csv
import pandas as pd

def get_url(path):
    cs = sr.cref(["magic","version","urllength","md5"],[8,4,4,4],[False,False,False,False],None,"Cache_Header") << sr.cref.structure
    with  open(str(path), 'rb') as file:
        buffer = file.read(1024)
        if(buffer==b''):
            print("EOF")
            sys.exit()
    cs << buffer
    length = cs.byte2int((cs >> ("urllength",)))
    return buffer[cs.sizeof():cs.sizeof()+length].decode('utf-8').strip()

def csv_write(path, _list):
    df = pd.DataFrame(_list, columns=['a','b'])
    df.to_csv(path,index=False,mode="w")

if __name__ == '__main__':

    basepath = "\\org.chromium.android_webview"
    data = []
    for file_name in os.listdir(basepath) :
        target = os.path.join(basepath, file_name)
        data.append(file_name)
        data.append(get_url(target))
        
    n=2
    result = [data[i * n:(i + 1) * n] for i in range((len(data) + n - 1) // n )] 
    
    csv_write("firefox_test.csv",data)



    
    
    
    
    

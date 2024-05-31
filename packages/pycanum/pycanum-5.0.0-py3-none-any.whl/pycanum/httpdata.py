
import requests
import struct
import numpy as np

class HttpData:
    def __init__(self,url):
        self.url = url
        self.data = b''
        self.response = b''
        self.responseDataPos = 0

    def initData(self):
        self.data = b''

    def writeInt8(self,x,signed=True):
        if signed: fmt = '<b'
        else: fmt = '<B'
        bts = struct.pack(fmt,x)
        for b in bts:
            self.data += (b).to_bytes(1,byteorder='little')

    def writeInt16(self,x,signed=True):
        if signed: fmt = '<h'
        else: fmt = '<H'
        bts = struct.pack(fmt,x)
        for b in bts:
            self.data += (b).to_bytes(1,byteorder='little')

    def writeInt32(self,x,signed=True):
        if signed: fmt = '<i'
        else: fmt = '<I'
        bts = struct.pack(fmt,x)
        for b in bts:
            self.data += (b).to_bytes(1,byteorder='little')

    def writeFloat(self,x):
        bts = struct.pack('<f',x)
        for b in bts:
            self.data += (b).to_bytes(1,byteorder='little')

    def writeDouble(self,x):
        bts = struct.pack('<d',x)
        for b in bts:
            self.data += (b).to_bytes(1,byteorder='little')

    def writeFloatArray(self,a):
        a = np.array(a,dtype=np.float32)
        for i in range(len(a)):
            bts = struct.pack('<f',a[i])
            for b in bts:
                self.data += (b).to_bytes(1,byteorder='little')

    def writeDoubleArray(self,a):
        a = np.array(a,dtype=np.float64)
        for i in range(len(a)):
            bts = struct.pack('<d',a[i])
            for b in bts:
                self.data += (b).to_bytes(1,byteorder='little')


    def readInt8(self,signed=True):
        if signed : fmt = '<b'
        else : fmt = '<B'
        x = struct.unpack(fmt,self.responseData[self.responseDataPos:self.responseDataPos+1])
        self.responseDataPos += 1
        return x[0]

    def readInt16(self,signed=True):
        if signed : fmt = '<h'
        else : fmt = '<H'
        x = struct.unpack(fmt,self.responseData[self.responseDataPos:self.responseDataPos+2])
        self.responseDataPos += 2
        return x[0]

    def readInt32(self,signed=True):
        if signed : fmt = '<l'
        else : fmt = '<L'
        x = struct.unpack(fmt,self.responseData[self.responseDataPos:self.responseDataPos+4])
        self.responseDataPos += 4
        return x[0]

    def readFloat(self):
        x = struct.unpack('<f',self.responseData[self.responseDataPos:self.responseDataPos+4])
        self.responseDataPos += 4
        return np.float32(x[0])

    def readDouble(self):
        x = struct.unpack('<d',self.responseData[self.responseDataPos:self.responseDataPos+8])
        self.responseDataPos += 8
        return np.float64(x[0])

    def readFloatArray(self,size):
        a = np.zeros(size,dtype=np.float32)
        for k in range(size):
            a[k] = self.readFloat()
        return a

    def readDoubleArray(self,size):
        a = np.zeros(size,dtype=np.float64)
        for k in range(size):
            a[k] = self.readDouble()
        return a

    def readInt8Array(self,size,signed=True):
        a = np.zeros(size,dtype=np.int8)
        for k in range(size):
            a[k] = self.readInt8(signed)
        return a

    def readFloatNdArray(self,size):
        a = np.frombuffer(self.responseData[self.responseDataPos:self.responseDataPos+4*size],dtype=np.float32)
        self.responseDataPos += 4*size
        return a

    def readDoubleNdArray(self,size):
        a = np.frombuffer(self.responseData[self.responseDataPos:self.responseDataPos+8*size],dtype=np.float64)
        self.responseDataPos += 8*size
        return a
        

    def sendRequest(self,name):
        success = False
        while not(success):
            response = requests.post(self.url+name,data=self.data)
            success = response.status_code==200
        if response.reason=="ERROR":
            self.initData()
            self.sendRequest("terminate")
            raise Exception(response.text)
        self.responseData = bytes(response.text,response.encoding)
        self.responseDataPos = 0
        return response.text

    

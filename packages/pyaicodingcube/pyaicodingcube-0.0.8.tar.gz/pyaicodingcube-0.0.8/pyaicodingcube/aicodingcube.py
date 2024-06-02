import time
import threading
# import datetime
# from gtts import gTTS
# import playsound
# import random
# import os
# import keyboard
# import speech_recognition as sr
import serial

class protocol:
    global ser
    global gRxCmd
    global gRxCount
    global gRxRecord    

    def __init__(self):
        self.buffers = []
        for i in range(11):
            self.buffers.append(0)

    def open_port(self, portname):
        global ser
        ser = serial.Serial(portname, 115200)
        return ser

    def make_packet(self, index, para1, para2, para3, para4):  
        self.buffers[0] = 0
        self.buffers[1] = index
        self.buffers[2] = para1
        self.buffers[3] = para2
        self.buffers[4] = para3
        self.buffers[5] = para4
        self.buffers[6] = 90
        self.buffers[7] = 7
        self.buffers[8] = 253
        self.buffers[9] = 254
        self.buffers[10] = 254 

    def send_packet(self, main, sub):   
        self.make_packet(0, 11, main, sub, 0xff)
        return self.buffers

    def select_mode(self, Main, Sub, DelayTime):         
        global ser
        packet = self.send_packet(Main, Sub)
        print(packet)
        ser.write(packet)
        time.sleep(DelayTime) 
        return self.buffers    

    def turn_face(self, facechar, turnCnt, delaytime):
        global ser
        if facechar == 'W': faceid = 0
        elif facechar == 'Y' : faceid = 1
        elif facechar == 'G' : faceid = 2
        elif facechar == 'B' : faceid = 3
        elif facechar == 'R' : faceid = 4
        elif facechar == 'P' : faceid = 5                

        if turnCnt == -1 : turnCnt = 11
        elif turnCnt == -2 : turnCnt = 14            
        elif turnCnt == 1 : turnCnt = 3
        elif turnCnt == 2 : turnCnt = 6
        else : turnCnt = 0

        result = divmod(faceid, 2)

        if result[1] == 0 :
            turnCnt = turnCnt* 16 * (1- result[1] )  

        if faceid <= 1   : 
            self.make_packet(7, 3, turnCnt, 0, 0 )
        elif faceid <= 3 :
            self.make_packet(7, 3, 0, turnCnt, 0 )
        elif faceid <= 5 :
            self.make_packet(7, 3, 0, 0, turnCnt)            

        print(self.buffers)       
        ser.write(self.buffers)      
        time.sleep(delaytime)
        return self.buffers       

    def cellcolor2val(self, LedValue): 
        WriteLedValue = None
        if LedValue == "RED" : WriteLedValue = 1
        elif LedValue == "GREEN" : WriteLedValue = 2
        elif LedValue == "BLUE" : WriteLedValue = 3
        elif LedValue == "YELLOW" : WriteLedValue = 4
        elif LedValue == "PINK" : WriteLedValue = 6
        elif LedValue == "WHITE" : WriteLedValue = 7
        elif LedValue == "SKIP" : WriteLedValue = 8
        elif LedValue == "OFF" : WriteLedValue = 0      
        return WriteLedValue    
    
    def change_centercell(self, facechar, LedValue, delaytime):  
        global ser
        if facechar =='W': faceid = 0
        elif facechar == 'Y': faceid = 1
        elif facechar == 'G': faceid = 2
        elif facechar == 'B': faceid = 3
        elif facechar == 'R': faceid = 4
        elif facechar == 'P': faceid = 5
        self.make_packet(faceid*32 + 9, self.cellcolor2val(LedValue), 0xff , 0xff, 0xff)
        print(self.buffers)
        ser.write(self.buffers)
        time.sleep(delaytime)
        return self.buffers
    
    def change_edgecornercell(self, facechar, LedVal1, LedVal2, LedVal3, LedVal4, LedVal5, LedVal6, LedVal7, LedVal8, delaytime):  
        global ser
        if facechar =='W':faceid = 0
        elif facechar == 'Y': faceid = 1
        elif facechar == 'G': faceid = 2
        elif facechar == 'B': faceid = 3
        elif facechar == 'R': faceid = 4
        elif facechar == 'P': faceid = 5
        self.make_packet(faceid*32 + 11,self.cellcolor2val(LedVal1)*16+self.cellcolor2val(LedVal2), self.cellcolor2val(LedVal3)*16+self.cellcolor2val(LedVal4),self.cellcolor2val(LedVal5)*16+self.cellcolor2val(LedVal6),self.cellcolor2val(LedVal7)*16+self.cellcolor2val(LedVal8))
        print(self.buffers)
        ser.write(self.buffers)
        time.sleep(delaytime)
        return self.buffers

    def turn_notation(self, facechar):       
        if facechar == "U": 
            faceid = 'W'
            turnCnt = 1
        elif facechar == "U'": 
            faceid = 'W'
            turnCnt = -1            
        elif facechar == "U2": 
            faceid = 'W'
            turnCnt = 2                  
        elif facechar == "F": 
            faceid = 'G'
            turnCnt = 1
        elif facechar == "F'": 
            faceid = 'G'
            turnCnt = -1          
        elif facechar == "L": 
            faceid = 'P'
            turnCnt = 1
        elif facechar == "L'": 
            faceid = 'P'
            turnCnt = -1
        elif facechar == "R": 
            faceid = 'R'
            turnCnt = 1
        elif facechar == "R'": 
            faceid = 'R'
            turnCnt = -1
        elif facechar == "B": 
            faceid = 'B'
            turnCnt = 1
        elif facechar == "B'": 
            faceid = 'B'
            turnCnt = -1
        elif facechar == "D": 
            faceid = 'Y'
            turnCnt = 1
        elif facechar == "D'": 
            faceid = 'Y'
            turnCnt = -1

        self.turn_face( faceid, turnCnt, 0.5)
        return self.buffers   

    def run_dice (self, dicecnt): # 40<= dicent <=100        
        global ser
        if dicecnt <= 40: dicecnt = 40
        elif dicecnt >= 100: dicecnt = 100
        self.make_packet (0, 0x15, dicecnt, 0xff ,0xff)
        ser.write(self.buffers)
        return self.buffers
        
    def set_brake(self, value): 
        if value == 0 : aicodingcube.select_mode(self, 13, 4, 1.0)  #non brake
        elif value == 1 : aicodingcube.select_mode(self, 9, 3, 1.0)  # basic brake 0
        elif value == 2 : aicodingcube.select_mode(self, 13, 5, 1.0)  # basic brake 1
        elif value == 3 : aicodingcube.select_mode(self, 9, 4, 1.0)  # speed brake 0
        elif value == 4 : aicodingcube.select_mode(self, 13, 6, 1.0)  # speed brake 1        
        return self.buffers   
    
    def control_faceangle(self, facechar, goalpos, state, torq): # control_faceangle after setbrake(0)  
        global ser    
        if facechar =='W':faceid = 0
        elif facechar == 'Y': faceid = 1
        elif facechar == 'G': faceid = 2
        elif facechar == 'B': faceid = 3
        elif facechar == 'R': faceid = 4
        elif facechar == 'P': faceid = 5
                
        if goalpos >= 120: dicecnt = 120  # 0~120  , control angle 1unit 2.73degree, each corner angle = 13,47,82, 116  
        if state > 3 : state = 3   #// CW  , 0-Brak, 2-CCW, 3-Passive
        if torq > 4 : torq = 4  # 0~4
        
        self.make_packet(faceid*32 + 12, goalpos, state, torq, 0xff)
        ser.write(self.buffers)
        return self.buffers
        
    def make_clear(self):		
        self.make_packet(7, 2, 0xff, 0xff, 0xff)			
        return self.buffers

    def clear_allfaces(self, DelayTime):	
        global ser
        packet = self.make_clear()		
        ser.write(packet)		
        time.sleep(DelayTime)		
        return self.buffers	

    def change_musicalscales(self, index, delaytime):
        global ser
        if index == 8:
            self.make_packet(0, 0x1e, 3, 0, 0xff)
        elif index == 12:
            self.make_packet(0, 0x1e, 3, 1, 0xff)
        ser.write(self.buffers)
        time.sleep(delaytime)
        return self.buffers	
   
    def num2color(self, Num):
        if Num == 0 : Color = "W_U"
        elif Num == 1 : Color = "Y_D"
        elif Num == 2 : Color = "G_F"
        elif Num == 3 : Color = "B_B"
        elif Num == 4 : Color = "R_R"
        elif Num == 5 : Color = "P_L"
        return Color
    
    def get_message(self):
        global gRxCmd
        return gRxCmd
    
    def clear_message(self):
        global gRxCmd
        gRxCmd = "none"
        return self.buffers
    
    def get_message_record(self):
        global gRxRecord
        return gRxRecord
    
    def clear_message_record(self):
        global gRxRecord
        gRxRecord = 0.0
        return self.buffers

    def exit_mode(self):
       self.select_mode(10, 10, 0.3)

    # import threading
    gRxRecord = -1       
    def begin_checkmessage(self):   
        global ser 
        ser.timeout = 0.01 #sec
        #rx_data = ser.readline().decode('cp437','strict') #ser.readall() 
        rx_data = ser.readall().decode('cp437', 'strict') #ser.readall() 
        rx_size = len(rx_data)
        global gRxCmd
        global gRxCount
        global gRxRecord
        gRxCount = 0
        gRxCount = gRxCount + rx_size
 
        if rx_size >= 7 :      
            rx_byte = bytearray(rx_data, 'cp437' )    
            #for i in range(rx_size):
                #print("Rx %d" %rx_byte[i])    
            if rx_byte[0] == 0 and rx_byte[6] == 0x5a :
                if rx_byte[1] == 7 and rx_byte[2] == 1 :
                    #gRxCmd = "Rotate"    
                    faceCnt = bytearray([0, 0, 0, 0, 0, 0])
                    faceCnt[0] = (rx_byte[3] >> 4 )
                    faceCnt[1] = (rx_byte[3] & 0x0f)
                    faceCnt[2] = (rx_byte[4] >> 4)
                    faceCnt[3] = (rx_byte[4] & 0x0f)                
                    faceCnt[4] = (rx_byte[5] >>4)
                    faceCnt[5] = (rx_byte[5] & 0x0f)    
                    for i in range(6):
                        if faceCnt[i]>0 :
                            if faceCnt[i] == 3: faceRotR ="Face"+aicodingcube.num2color(self, i)+ "+CW"  #"Face"+str(i)+ "+CW"
                            elif faceCnt[i] == 11: faceRotR = "Face"+aicodingcube.num2color(self, i)+ "CCW" #"Face"+str(i)+ "CCW"
                            else : faceRotR = "FaceNo"
                    gRxCmd = faceRotR
                    #print("RX Rotate:"+ faceRotR )      
                elif rx_byte[1] == 7 and rx_byte[2] == 2 :    
                    gRxCmd = "ResetAllFace"
                elif rx_byte[1] == 7 and rx_byte[2] == 4 :    
                    gRxCmd = "FinshedScrambele"
                elif rx_byte[1] == 7 and rx_byte[2] == 5 :    
                    gRxCmd = "TimeoutExploreScramble"
                elif rx_byte[1] == 200 and rx_byte[2] == 0  : 
                    gRxCmd = "Mode3XRecordTime"
                    chkrecord = (float)(rx_byte[3] * 256 * 256 + rx_byte[4] * 256 + rx_byte[5] ) / 1000.0
                    gRxRecord = chkrecord
                    #print("Mode3x RecordTime: %.3f sec" %chkrecord )      
                elif rx_byte[1] == 169 and rx_byte[2] == 0  : 
                    gRxCmd = "Mode2XRecordTime"
                    chkrecord = (float)(rx_byte[3] * 256 * 256 + rx_byte[4] * 256 + rx_byte[5] ) / 1000.0
                    gRxRecord = chkrecord
                    #print("Mode2x RecordTime: %.3f sec" %chkrecord )  
                elif rx_byte[1] == 233 and rx_byte[2] == 0  : 
                    gRxCmd = "Mode02RecordTime"
                    chkrecord = (float)(rx_byte[3] * 256 * 256 + rx_byte[4] * 256 + rx_byte[5] ) / 1000.0
                    gRxRecord = chkrecord
                   # print("Mode02 RecordTime: %.3f sec" %chkrecord )  
                elif rx_byte[1] == 0  and rx_byte[2] == 11  :
                    if rx_byte[3] == 10  and rx_byte[4] == 10:  gRxCmd = "ModeExit"                       
                    elif rx_byte[3]== 5 and rx_byte[4]== 0 :   gRxCmd = "EndCmd"
                    else :  gRxCmd = "Mode" + str(rx_byte[3]) + str(rx_byte[4])
                    #print("RX Mode: %d %d  "  %(rx_byte[3],rx_byte[4])  )         
                elif rx_byte [1] == 0xe9 and rx_byte [2] == 0:
                    chkrecord = (float)(rx_byte[3] * 256 * 256 + rx_byte[4] * 256 + rx_byte [5] ) / 1000.0 #1~6
                    if chkrecord == 1.0 or chkrecord == 2.0 or chkrecord == 3.0 or chkrecord == 4.0 or chkrecord == 5.0 or chkrecord == 6.0:
                        gRxCmd = "DiceNumber"
                        gRxRecord = chkrecord
                        print("DiceNumber: %.0f " % chkrecord)
                    elif chkrecord > 10 :
                        gRxCmd = "Mode02RecordTime"
                        gRxRecord = chkrecord
                        print ("Mode02RecordTime: %.3f sec" % chkrecord)
                    else : gRxCmd = "OtherCmd"
                else :
                    gRxCmd = "OtherCmd"
                    #print("RX Other: %d %d "  %(rx_byte[3],rx_byte[4])  )  
                    #for i in range(7):
                        #print("%d" %rx_byte[i])      
                #ser.reset_input_buffer()                 
                gRxCount = 0
            else :
                print("No Cmd " + str(rx_size)  )
                for i in range(7):
                    print("%d" %rx_byte[i])    
                gRxCount = 0
        elif rx_size >= 6 :   
            rx_byte =bytearray(rx_data, 'cp437' )
            print("No Cmd " + str(rx_size)  )
            for i in range(rx_size):
                print("%d" %rx_byte[i])    
        #else:   
            #print(".")
                            
   # print( datetime.datetime.now())
        thread1 = threading.Timer(0.03, self.begin_checkmessage)
        thread1.daemon = True
        thread1.start()
#######################################################################################





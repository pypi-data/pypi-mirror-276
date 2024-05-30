from pyaicodingcube import *



######################################################################################

if __name__ == "__main__":
    cube = aicodingcube()
    ser = cube.open_port('COM8')   
    packet = cube.gotomode(10,10,0.2)
    packet = cube.gotomode(0, 0, 3.0)

   

    gRxCmd = "none"
    gRxCount = 0
    if ser.is_open :
        cube.Timer_RxCheck()
        # thread1 = threading.Thread(target=cube.Timer_RxCheck)
        
        
        #thread1 = threading.Timer(0.03, cube.Timer_RxCheck)
        #thread1.daemon = True
        #thread1.start()
   
    ser.reset_input_buffer()   
    
    #cube.make_onescramble('U')

    cube.clearMessage()
    loopCnt =0
    while ser.is_open :
       # packet = pro.gotomode(10,10, 3.0)
       # packet = pro.gotomode(2,0, 3.0)
        
        # if gRxCmd != "none": 
        #     if gRxCmd == "EndCmd" : break
        #     elif gRxCmd == "Mode2XRcordTime":
        #         print("Mode2x RecodTime: %.3f sec" %gRxRecord )  
        #     elif gRxCmd == "Mode3XRcordTime":
        #         print("Mode3x RecodTime: %.3f sec" %gRxRecord ) 
        #     elif gRxCmd == "FaceW_U+CW":  
        #         print(gRxCmd)
        #     elif gRxCmd == "FaceW_UCCW":  
        #         print(gRxCmd)

        #     else : print(gRxCmd)

        #     gRxCmd = "none"
        Msg = cube.getMessage()
        if Msg != "none": 
            print(Msg)
            cube.clearMessage()

        if loopCnt % 30 ==0 : print("Hello")
        loopCnt = loopCnt+1
        if loopCnt > 1000000 : break
        time.sleep(0.03)



    # good = ["좋음", "사랑", "예쁨", "즐거움","천재", "멋지다","고마워", "잘했어"]
    # bad = ["싫음", "나빠","미움","불만","짜증","바보","못생겼어","잘난척이야"]

    # command = recognize_speech()
    
    # if command in good:
    #     speak("네 좋아요")
    #     packet = pro.WriteLedCellsCen('R','OFF', 1.0 )
        
    # elif command in bad:
    #     speak("싫어요")
    #     packet = pro.WriteLedCellsCen('R','RED', 0.2 )
    #     packet = pro.WriteLedCellSide('R','OFF','RED','OFF','RED','OFF','RED','OFF','RED',1.0)

    # else:
    #     speak("몰라요")













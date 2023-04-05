# Simple tests for an Sequence generator module

import cocotb
from cocotb.triggers import Timer
from cocotb.triggers import FallingEdge
from cocotb.clock import Clock
from cocotb.result import TestFailure
import random
import wavedrom
import json

# @cocotb.test()
# async def adder_basic_test(dut):
#     """Test for 5 + 10"""

#     en_=1
#     in_ = 2

#     # input driving
#     dut.en.value = en_
#     dut.inp.value = in_

#     await Timer(2, units='ns')

#     assert dut.out.value == pow(2,in_), f"Encoder result is incorrect: {dut.out.value} != 4"

def TransformContinousString(s):
    transformed_str = ""
    for i in range(len(s)-1, 0, -1):
        if s[i] == s[i-1]:
            transformed_str = "." + transformed_str
        else:
            transformed_str = s[i] + transformed_str
    transformed_str = s[0] + transformed_str
    return transformed_str

@cocotb.test()
async def adder_randomised_test(dut):
    """Test for sequence detector multiple times"""

    cocotb.fork(Clock(dut.clk,10,'ns').start())

    data = {'signal1': [], 'signal2': [], 'signal3':[], 'signal3': []}
    myoutput = []
    exp_out = []
    myInput1 = []   #reset
    myInput2 = []   #serial input
    timeString = ""
    equalString = ""
    Mismatch_string = ""

    arr = []
    seq = [1,0,1,1]
    for i in range(5):
        if i>0:
            timeString += "."
        equalString += "="

        reset_ = 1
        in_ = random.randint(0,1)
        dut.reset.value = reset_
        dut.in_vl.value = in_
        
        myInput1.append(int(reset_))
        myInput2.append(int(in_))
        if arr[-4:]==seq :
            exp_out.append(0)
        else:
            exp_out.append(0)

        await FallingEdge(dut.clk)
        
        myoutput.append(dut.out.value)
        
        if (int(dut.out.value) == 0):
            Mismatch_string+='0'
           
        else:
            Mismatch_string+='1'
        


        #if dut.out.value == 1 :
        #    raise TestFailure('Test Failure occured output=1 when reset is active')

    
    for i in range(50):

        timeString += "."
        equalString += "="
        
        reset_ = 0
        in_ = random.randint(0,1)
        dut.reset.value = reset_
        dut.in_vl.value = in_

        arr.append(in_)

        myInput1.append(int(reset_))
        myInput2.append(int(in_))
        if arr[-4:]==seq :
            exp_out.append(1)
        else:
            exp_out.append(0)

        await FallingEdge(dut.clk)

        myoutput.append(dut.out.value)
        
        # if (arr[-4:] == seq and dut.out.value == 0) :
        #     raise TestFailure('Test Failure occured when last 4 elements = ' , arr[-4:], 'and output of dsn=0')
        
        # if (arr[-4:] != seq and dut.out.value == 1) :
        #     raise TestFailure('Test Failure occured when last 4 elements = ' , arr[-4:],'and output of dsn=1')
        
        if (int(dut.out.value) == (arr[-4:] == seq)):
            Mismatch_string+='0'
           
        else:
            Mismatch_string+='1'
    
    
    # wd = waveDrom()
    s = " "
    Input1_string = s.join([str(elem) for elem in myInput1])
    Input2_String = s.join([str(elem) for elem in myInput2])
    #Input3_string = s.join([str(elem) for elem in myInput3])
    Output_String = s.join([str(elem) for elem in myoutput])
    Exp_output_String = s.join([str(elem) for elem in exp_out])
    Mismatch_string=TransformContinousString(Mismatch_string)
    print(equalString, timeString)
    # print(Input1_string,"\n",Input2_String,"\n",Output_String)
    data = {
        "signal": [
            {"name": "Clk", "wave": "P"+timeString},
            {"name": "Signal1",  "wave": equalString, "data": Input1_string},
            {"name": "Signal2",  "wave": equalString, "data": Input2_String},
            #{"name": "Signal3",  "wave": equalString, "data": Input3_string},
            {"name": "Output",  "wave": equalString, "data": Output_String},
            {"name": "Exp_Output",  "wave": equalString, "data": Exp_output_String},
            {"name": "Mismatch",  "wave": Mismatch_string }




        ]
    }
    data_str = json.dumps(data)
    svg = wavedrom.render(data_str)
    svg.saveas("demo1.svg")    


@cocotb.test()
async def adder_randomised_test2(dut):
    """Test for sequence detector single time"""

    cocotb.fork(Clock(dut.clk,10,'ns').start())
    data = {'signal1': [], 'signal2': [], 'signal3':[], 'signal3': []}
    myoutput = []
    exp_out = []
    myInput1 = []   #reset
    myInput2 = []   #serial input
    timeString = ""
    equalString = ""
    Mismatch_string = ""

    seq=[0,1,0,1,1,0]
    for i in range(len(seq)):
        if i>0:
            timeString += "."
            reset_=0
        else: reset_=1
        equalString += "="

        dut.reset.value = reset_
        dut.in_vl.value = seq[i]

        myInput1.append(int(reset_))
        myInput2.append(int(seq[i]))

        if(i!=(len(seq)-2)):
            exp_out.append(0)
        else: exp_out.append(1)

        await FallingEdge(dut.clk)
        myoutput.append(dut.out.value)

        if (int(dut.out.value) == exp_out[i]):
            Mismatch_string+='0'   
        else:
            Mismatch_string+='1'

    
     # wd = waveDrom()
    s = " "
    Input1_string = s.join([str(elem) for elem in myInput1])
    Input2_String = s.join([str(elem) for elem in myInput2])
    #Input3_string = s.join([str(elem) for elem in myInput3])
    Output_String = s.join([str(elem) for elem in myoutput])
    Exp_output_String = s.join([str(elem) for elem in exp_out])
    Mismatch_string=TransformContinousString(Mismatch_string)
    print(equalString, timeString)
    # print(Input1_string,"\n",Input2_String,"\n",Output_String)
    data = {
        "signal": [
            {"name": "Clk", "wave": "P"+timeString},
            {"name": "Signal1",  "wave": equalString, "data": Input1_string},
            {"name": "Signal2",  "wave": equalString, "data": Input2_String},
            #{"name": "Signal3",  "wave": equalString, "data": Input3_string},
            {"name": "Output",  "wave": equalString, "data": Output_String},
            {"name": "Exp_Output",  "wave": equalString, "data": Exp_output_String},
            {"name": "Mismatch",  "wave": Mismatch_string }




        ]
    }
    data_str = json.dumps(data)
    svg = wavedrom.render(data_str)
    svg.saveas("demo2.svg")   
        





    
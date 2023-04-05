# Sequence Detector

Consider a finite state machine with inputs reset and in_vl, which are an asynchronous high reset input and a 1-bit input value, respectively. You need to design a Moore machine to detect a sequence of [1,0,1,1]. Keep in mind that the sequences can be overlapping as well. The output signal out should be driven.

Write Verilog code for the Moore machine, taking care not to change the name of input or output registers and wires.

**complete the function below**

```
module seq_dec(input wire clk,
                input wire reset,
                input wire in_vl,
                output wire out);
    
   //your code here

endmodule

```


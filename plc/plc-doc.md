l

## Commands

| Code | Function                             | DATA BYTE TO PLC / FROM PLC |
| :--: | :----------------------------------- | :-------------------------: |
| 0x00 | No Command                           | 0/0                         |
| 0x01 | PLC Reset                            | 0/0                         |
| 0x02 | Basic Parameters                     | 14/0                        |
| 0x03 | Modify Gain                          | 1/0                         |
| 0x04 | Set Length                           | 4/0                         |
| 0x05 | Feed Start                           | 0/0                         |
| 0x06 | Feed Stop                            | 0/0                         |
| 0x07 | Software Speed                       | 1/0                         |
| 0x08 | No Software Speed                    | 0/0                         |
| 0x09 | Tacho Adjust                         | 0/0                         |
| 0x0A | No Tacho Adjust                      | 0/0                         |
| 0x0B | Trapezoid Function                   | 0/0                         |
| 0x0C | No Trapezoid Function                | 0/0                         |
| 0x0D | Trim Function                        | 5/0                         |
| 0x0E | Read Trim Measured Length            | 0/4                         |
| 0x0F | Jog Forward                          | 0/0                         |
| 0x10 | Jog Reverse                          | 0/0                         |
| 0x11 | Jog Stop                             | 0/0                         |
| 0x12 | No Loop                              | 0/0                         |
| 0x13 | Closed Loop                          | 0/0                         |
| 0x14 | Set Time A Time B                    | 4/0                         |
| 0x15 | Set Delay                            | 1/0                         |
| 0x16 | Length Add                           | 0/0                         |
| 0x17 | Search Forward                       | 0/0                         |
| 0x18 | Search Reverse                       | 0/0                         |
| 0x19 | Read Error Code                      | 0/4                         |
| 0x1A | Write S-position                     | 4/0                         |
| 0x1B | Read S-position                      | 0/4                         |
| 0x1C | Factor for Encoder 1                 | 3/0                         |
| 0x1D | Factor for Encoder 2                 | 3/0                         |
| 0x1E | Set External Time Base               | 0/0                         |
| 0x1F | Clear Position Error                 | 0/0                         |
| 0x20 | Disable Track/Encoder Error          | 0/0                         |
| 0x21 | Enable Track/Encoder Error           | 0/0                         |
| 0x22 | Transfer of Error Code Finished      | 0/0                         |
| 0x23 | Flying Start After Trigger           | 1/0                         |
| 0x24 | Read ADC Value                       | 0/1                         |
| 0x25 | Write DAC Value                      | 2/0                         |
| 0x26 | Feed Start to S-position             | 0/0                         |
| 0x27 | Set Comparators for S-position       | 8/0                         |
| 0x28 | Read Position Error                  | 0/2                         |
| 0x29 | Jog-speed Factor                     | 1/0                         |
| 0x2A | Set Length Correction Factor         | 8/0                         |
| 0x2B | Read Length After Correction         | 0/4                         |
| 0x2C | Trapezoid Function Alternating       | 0/0                         |
| 0x2D | Divide Two int32_t Values            | 8/0                         |
| 0x2E | Multiply Result of div by Factor 8   | 8/0                         |
| 0x2F | Read 64 bit Fixed Point Result       | 0/8                         |
| 0x30 | New Cycle for Length Correction      | 0/0                         |
| 0x31 | Read Pulse Counting of Encoder 2     | 0/4                         |

## Status

### Status Byte Mask

| Bit | Name   | Description            |
| :-: | :----: | :--------------------- |
|  7  | FIOURY | FIFO Output Ready      | 
|  6  | FIINRY | FIFO Input Ready       |
|  5  | CMDBSY | Command Busy           |
|  4  | ERRST  | Error Status           |
|  3  | INTM   | Interrupt to Multybus  |
|  2  | FEEDPE | Feeding Position Error |
|  1  | CLOOP  | Closed Loop            |
|  0  |  ---   | Not Used               |

### General

Before transmitting data, ensure the following conditions are met:

- The "ERRST" bit is set high, indicating an "Interface Transmission Fail" error.
- If the number of data bytes is too low, the "FIINRY" bit will not be set high.
- If too many data bytes are sent, the error message "Interface Transmission Fail" will be triggered.

### Status Message

#### (BIT7) FIFO Output Ready
When data can be read from the FIFO, "FIOURY" is set high. The bit goes low when no more data is available in the FIFO.

#### (BIT6) FIFO Input Ready
If this bit is high, a new command plus data byte may be written to the FIFO; otherwise, ANY transmission to the PLC is not permitted. The first byte transmitted from the Multybus to the FIFO sets this bit low. After this, for new commands, "FIINRY" will be set high again.

#### (BIT5) Command Busy
This indicates that the PLC is busy executing a command.
The PLC sets "CMDBSY" for the following commands: 02, 05, 09, 0B, 0F, 10, 12, 13, 14, 16, 17, 18, 23, 26, 2C (in hex).

For the following commands, "CMDBSY" must have cleared; otherwise, an "Interface Error" will be triggered: 02, 05, 09, 0B, 0E, 0F, 10, 14, 18, 26, 2C (in hex).

#### (BIT4) Error Status
Error message, see error code.

#### (BIT3) Interrupt to Multybus
Indicates in the status whether the interrupt "/INTM" pin: C8A has become active (open collector). "/INTM" is automatically reset during a hardware reset or when reading the status.
Alternatively, the status can also be queried by polling.
Status changes that activate "/INTM":
 - Rising edge of "FIINRY"
 - Falling edge of "CMDBSY"
 - Rising edge of "ERRST"

#### (BIT2) Feeding Position Error
For the following commands: 05, 0F, 10, 16, 17, 18, 23, 26 (in hex)

#### (BIT1) Closed Loop
The following commands are only permitted in "Closed Loop" mode: 05, 0D, 0F, 10, 16, 17, 18, 23, 26 (in hex).  
The following commands are only permitted in "No Loop" mode: 09, 0B, 25, 2C (in hex).  
Otherwise, an "Interface Error" will occur.  

### Status Changes Depending on Command

#### 0x00 No Command
| Data byte to/from PLC | FIOURY | FIINRY | CMDBSY | ERRST  | INTM   | FEEDPE | CLOOP  |                             | 
| :-------------------: | :----: | :----: | :----: | :----: | :----: | :----: | :----: | :-------------------------- | 
| 0/0                   | X      | H      | X      | X      | X      | X      | X      | Precondition                | 
| 0/0                   | X      | L      | X      | X      | X      | X      | X      | Command transfer            | 
| 0/0                   | X      | H      | X      | X      | X      | X      | X      | Transfer completed          | 

#### 0x01 PLC Reset
| Data byte to/from PLC | FIOURY | FIINRY | CMDBSY | ERRST  | INTM   | FEEDPE | CLOOP  |                             |
| :-------------------: | :----: | :----: | :----: | :----: | :----: | :----: | :----: | :-------------------------- |
| 0/0                   | X      | H      | X      | X      | X      | X      | X      | Precondition                |
| 0/0                   | X      | L      | X      | X      | X      | X      | X      | Command transfer            |
| 0/0                   | X      | H      | X      | X      | X      | X      | X      | Transfer completed          |

#### 0x02 Basic Parameter
| Data byte to/from PLC | FIOURY | FIINRY | CMDBSY | ERRST  | INTM   | FEEDPE | CLOOP  |                             |
| :-------------------: | :----: | :----: | :----: | :----: | :----: | :----: | :----: | :-------------------------- |
| 0/0                   | X      | H      | L      | X      | X      | X      | X      | Precondition                |
| 0/0                   | X      | L      | L      | X      | X      | X      | X      | Command transfer            |
| 14/0                  | X      | L      | L      | X      | X      | X      | X      | Data transfer               |
| 0/0                   | X      | H      | H      | X      | X      | X      | X      | Transfer completed          |
| 0/0                   | X      | X      | L      | X      | X      | X      | X      | Command finished            |

#### 0x03 Modify Gain
| Data byte to/from PLC | FIOURY | FIINRY | CMDBSY | ERRST  | INTM   | FEEDPE | CLOOP  |                             |
| :-------------------: | :----: | :----: | :----: | :----: | :----: | :----: | :----: | :-------------------------- |
| 0/0                   | X      | H      | X      | X      | X      | X      | X      | Precondition                |
| 0/0                   | X      | L      | X      | X      | X      | X      | X      | Command transfer            |
| 1/0                   | X      | L      | X      | X      | X      | X      | X      | Data transfer               |
| 0/0                   | X      | H      | X      | X      | X      | X      | X      | Transfer completed          |

#### 0x04 Set Length
| Data byte to/from PLC | FIOURY | FIINRY | CMDBSY | ERRST  | INTM   | FEEDPE | CLOOP  |                             |
| :-------------------: | :----: | :----: | :----: | :----: | :----: | :----: | :----: | :-------------------------- |
| 0/0                   | X      | H      | X      | X      | X      | X      | X      | Precondition                |
| 0/0                   | X      | L      | X      | X      | X      | X      | X      | Command transfer            |
| 4/0                   | X      | L      | X      | X      | X      | X      | X      | Data transfer               |
| 0/0                   | X      | H      | X      | X      | X      | X      | X      | Transfer completed          |

#### 0x05 Feed Start
| Data byte to/from PLC | FIOURY | FIINRY | CMDBSY | ERRST  | INTM   | FEEDPE | CLOOP  |                             |
| :-------------------: | :----: | :----: | :----: | :----: | :----: | :----: | :----: | :-------------------------- |
| 0/0                   | X      | H      | L      | X      | X      | X      | H      | Precondition                |
| 0/0                   | X      | L      | L      | X      | X      | X      | H      | Command transfer            |
| 0/0                   | X      | H      | H      | X      | X      | H      | H      | Transfer completed          |
| 0/0                   | X      | X      | L      | X      | X      | L      | H      | Command finished            |

#### 0x06 Feed Stop
| Data byte to/from PLC | FIOURY | FIINRY | CMDBSY | ERRST  | INTM   | FEEDPE | CLOOP  |                             |
| :-------------------: | :----: | :----: | :----: | :----: | :----: | :----: | :----: | :-------------------------- |
| 0/0                   | X      | H      | X      | X      | X      | X      | X      | Precondition                |
| 0/0                   | X      | L      | X      | X      | X      | X      | X      | Command transfer            |
| 0/0                   | X      | H      | X      | X      | X      | X      | X      | Transfer completed          |

#### 0x07 Software Speed
| Data byte to/from PLC | FIOURY | FIINRY | CMDBSY | ERRST  | INTM   | FEEDPE | CLOOP  |                             |
| :-------------------: | :----: | :----: | :----: | :----: | :----: | :----: | :----: | :-------------------------- |
| 0/0                   | X      | H      | X      | X      | X      | X      | X      | Precondition                |
| 0/0                   | X      | L      | X      | X      | X      | X      | X      | Command transfer            |
| 1/0                   | X      | L      | X      | X      | X      | X      | X      | Data transfer               |
| 0/0                   | X      | H      | X      | X      | X      | X      | X      | Transfer completed          |

#### 0x08 No Software Speed (hardware speed from tacho)
| Data byte to/from PLC | FIOURY | FIINRY | CMDBSY | ERRST  | INTM   | FEEDPE | CLOOP  |                             |
| :-------------------: | :----: | :----: | :----: | :----: | :----: | :----: | :----: | :-------------------------- |
| 0/0                   | X      | H      | X      | X      | X      | X      | X      | Precondition                |
| 0/0                   | X      | L      | X      | X      | X      | X      | X      | Command transfer            |
| 0/0                   | X      | H      | X      | X      | X      | X      | X      | Transfer completed          |

#### 0x09 Tacho Adjust
| Data byte to/from PLC | FIOURY | FIINRY | CMDBSY | ERRST  | INTM   | FEEDPE | CLOOP  |                             |
| :-------------------: | :----: | :----: | :----: | :----: | :----: | :----: | :----: | :-------------------------- |
| 0/0                   | X      | H      | L      | X      | X      | L      | X      | Precondition                |
| 0/0                   | X      | L      | L      | X      | X      | L      | X      | Command transfer            |
| 0/0                   | X      | H      | H      | X      | X      | L      | X      | Transfer completed          |
| 0/0                   | X      | X      | L      | X      | X      | X      | X      | Command finished            |

#### 0x0A No Tacho Adjust
| Data byte to/from PLC | FIOURY | FIINRY | CMDBSY | ERRST  | INTM   | FEEDPE | CLOOP  |                             |
| :-------------------: | :----: | :----: | :----: | :----: | :----: | :----: | :----: | :-------------------------- |
| 0/0                   | X      | H      | X      | X      | X      | X      | X      | Precondition                |
| 0/0                   | X      | L      | X      | X      | X      | X      | X      | Command transfer            |
| 0/0                   | X      | H      | X      | X      | X      | X      | X      | Transfer completed          |

#### 0x0B Trapezoid Function
| Data byte to/from PLC | FIOURY | FIINRY | CMDBSY | ERRST  | INTM   | FEEDPE | CLOOP  |                             |
| :-------------------: | :----: | :----: | :----: | :----: | :----: | :----: | :----: | :-------------------------- |
| 0/0                   | X      | H      | L      | X      | X      | L      | X      | Precondition                |
| 0/0                   | X      | L      | L      | X      | X      | L      | X      | Command transfer            |
| 0/0                   | X      | H      | H      | X      | X      | L      | X      | Transfer completed          |
| 0/0                   | X      | X      | L      | X      | X      | X      | X      | Command finished            |

#### 0x0C No Trapezoid Function
| Data byte to/from PLC | FIOURY | FIINRY | CMDBSY | ERRST  | INTM   | FEEDPE | CLOOP  |                             |
| :-------------------: | :----: | :----: | :----: | :----: | :----: | :----: | :----: | :-------------------------- |
| 0/0                   | X      | H      | X      | X      | X      | X      | X      | Precondition                |
| 0/0                   | X      | L      | X      | X      | X      | X      | X      | Command transfer            |
| 0/0                   | X      | H      | X      | X      | X      | X      | X      | Transfer completed          |

#### 0x0D Trim Function
| Data byte to/from PLC | FIOURY | FIINRY | CMDBSY | ERRST  | INTM   | FEEDPE | CLOOP  |                             |
| :-------------------: | :----: | :----: | :----: | :----: | :----: | :----: | :----: | :-------------------------- |
| 0/0                   | X      | H      | X      | X      | X      | H      | X      | Precondition                |
| 0/0                   | X      | L      | X      | X      | X      | H      | X      | Command transfer            |
| 5/0                   | X      | L      | X      | X      | X      | H      | X      | Data transfer               |
| 0/0                   | X      | H      | X      | X      | X      | H      | X      | Transfer completed          |

#### 0x0E Read Trim Measured Length
| Data byte to/from PLC | FIOURY | FIINRY | CMDBSY | ERRST  | INTM   | FEEDPE | CLOOP  |                             |
| :-------------------: | :----: | :----: | :----: | :----: | :----: | :----: | :----: | :-------------------------- |
| 0/0                   | L*     | H      | L      | X      | X      | H      | X      | Precondition                |
| 0/0                   | X      | L      | X      | X      | X      | H      | X      | Command transfer            |
| 0/4                   | X      | L      | X      | X      | X      | H      | X      | Data transfer               |
| 0/0                   | X      | H      | X      | X      | X      | H      | X      | Transfer completed          |

---
\* If "FIOURY" is not low, reading must continue.

#### 0x0F Jog Forward
| Data byte to/from PLC | FIOURY | FIINRY | CMDBSY | ERRST  | INTM   | FEEDPE | CLOOP  |                             |
| :-------------------: | :----: | :----: | :----: | :----: | :----: | :----: | :----: | :-------------------------- |
| 0/0                   | X      | H      | L      | X      | X      | X      | H      | Precondition                |
| 0/0                   | X      | L      | L      | X      | X      | X      | H      | Command transfer            |
| 0/0                   | X      | H      | H      | X      | X      | H      | H      | Transfer completed          |
| 0/0                   | X      | X      | L      | X      | X      | L      | X      | Command finished            |

End the command using "JOG STOP", "NO LOOP", or "PLC RESET".

#### 0x10 Jog Reverse
| Data byte to/from PLC | FIOURY | FIINRY | CMDBSY | ERRST  | INTM   | FEEDPE | CLOOP  |                             |
| :-------------------: | :----: | :----: | :----: | :----: | :----: | :----: | :----: | :-------------------------- |
| 0/0                   | X      | H      | L      | X      | X      | X      | H      | Precondition                |
| 0/0                   | X      | L      | L      | X      | X      | X      | H      | Command transfer            |
| 0/0                   | X      | H      | H      | X      | X      | H      | H      | Transfer completed          |
| 0/0                   | X      | X      | L      | X      | X      | L      | X      | Command finished            |

End the command using "JOG STOP", "NO LOOP", or "PLC RESET".

#### 0x11 Jog Stop
| Data byte to/from PLC | FIOURY | FIINRY | CMDBSY | ERRST  | INTM   | FEEDPE | CLOOP  |                             |
| :-------------------: | :----: | :----: | :----: | :----: | :----: | :----: | :----: | :-------------------------- | 
| 0/0                   | X      | H      | X      | X      | X      | X      | X      | Precondition                | 
| 0/0                   | X      | L      | X      | X      | X      | X      | X      | Command transfer            | 
| 0/0                   | X      | H      | X      | X      | X      | L      | X      | Transfer completed          | 

#### 0x12 No Loop
| Data byte to/from PLC | FIOURY | FIINRY | CMDBSY | ERRST  | INTM   | FEEDPE | CLOOP  |                             |
| :-------------------: | :----: | :----: | :----: | :----: | :----: | :----: | :----: | :-------------------------- |
| 0/0                   | X      | H      | X      | X      | X      | X      | X      | Precondition                | 
| 0/0                   | X      | L      | X      | X      | X      | X      | X      | Command transfer            | 
| 0/0                   | X      | H      | X      | X      | X      | L      | L      | Transfer completed          | 

#### 0x13 Closed Loop
| Data byte to/from PLC | FIOURY | FIINRY | CMDBSY | ERRST  | INTM   | FEEDPE | CLOOP  |                             |
| :-------------------: | :----: | :----: | :----: | :----: | :----: | :----: | :----: | :-------------------------- |
| 0/0                   | X      | H      | L      | X      | X      | X      | X      | Precondition                |
| 0/0                   | X      | L      | L      | X      | X      | X      | X      | Command transfer            |
| 0/0                   | X      | H      | H      | X      | X      | X      | X      | Transfer completed          |
| 0/0                   | X      | X      | L      | X      | X      | X      | H      | Command finished            |

#### 0x14 Set Time A Time B
| Data byte to/from PLC | FIOURY | FIINRY | CMDBSY | ERRST  | INTM   | FEEDPE | CLOOP  |                             |
| :-------------------: | :----: | :----: | :----: | :----: | :----: | :----: | :----: | :-------------------------- |
| 0/0                   | X      | H      | L      | X      | X      | X      | X      | Precondition                |
| 0/0                   | X      | L      | L      | X      | X      | X      | X      | Command transfer            |
| 4/0                   | X      | L      | L      | X      | X      | X      | X      | Data transfer               |
| 0/0                   | X      | H      | H      | X      | X      | X      | X      | Transfer completed          |
| 0/0                   | X      | X      | L      | X      | X      | X      | X      | Command finished            |

#### 0x15 Set Delay
| Data byte to/from PLC | FIOURY | FIINRY | CMDBSY | ERRST  | INTM   | FEEDPE | CLOOP  |                             |
| :-------------------: | :----: | :----: | :----: | :----: | :----: | :----: | :----: | :-------------------------- |
| 0/0                   | X      | H      | X      | X      | X      | X      | X      | Precondition                |
| 0/0                   | X      | L      | X      | X      | X      | X      | X      | Command transfer            |
| 1/0                   | X      | L      | X      | X      | X      | X      | X      | Data transfer               |
| 0/0                   | X      | H      | X      | X      | X      | X      | X      | Transfer completed          |

#### 0x16 Length Add
| Data byte to/from PLC | FIOURY | FIINRY | CMDBSY | ERRST  | INTM   | FEEDPE | CLOOP  |                             |
| :-------------------: | :----: | :----: | :----: | :----: | :----: | :----: | :----: | :-------------------------- |
| 0/0                   | X      | H      | X      | X      | X      | X      | H      | Precondition                |
| 0/0                   | X      | L      | X      | X      | X      | X      | H      | Command transfer            |
| 1/0                   | X      | H      | H      | X      | X      | H      | H      | Data transfer               |
| 0/0                   | X      | X      | L      | X      | X      | L      | X      | Command finished            |

#### 0x17 Search Forward
| Data byte to/from PLC | FIOURY | FIINRY | CMDBSY | ERRST  | INTM   | FEEDPE | CLOOP  |                             |
| :-------------------: | :----: | :----: | :----: | :----: | :----: | :----: | :----: | :-------------------------- |
| 0/0                   | X      | H      | L      | X      | X      | X      | H      | Precondition                |
| 0/0                   | X      | L      | L      | X      | X      | X      | H      | Command transfer            |
| 0/0                   | X      | H      | H      | X      | X      | H      | H      | Transfer completed          |
| 0/0                   | X      | X      | L      | X      | X      | L      | X      | Command finished            |

#### 0x18 Search Reverse
| Data byte to/from PLC | FIOURY | FIINRY | CMDBSY | ERRST  | INTM   | FEEDPE | CLOOP  |                             |
| :-------------------: | :----: | :----: | :----: | :----: | :----: | :----: | :----: | :-------------------------- |
| 0/0                   | X      | H      | L      | X      | X      | X      | H      | Precondition                |
| 0/0                   | X      | L      | L      | X      | X      | X      | H      | Command transfer            |
| 0/0                   | X      | H      | H      | X      | X      | H      | H      | Transfer completed          |
| 0/0                   | X      | X      | L      | X      | X      | L      | X      | Command finished            |

#### 0x19 Read Error Code
| Data byte to/from PLC | FIOURY | FIINRY | CMDBSY | ERRST  | INTM   | FEEDPE | CLOOP  |                             |
| :-------------------: | :----: | :----: | :----: | :----: | :----: | :----: | :----: | :-------------------------- |
| 0/0                   | L      | H      | X      | H      | X      | X      | X      | Precondition                |
| 0/0                   | H      | L      | X      | H      | X      | X      | X      | Command transfer            |
| 0/0                   | H      | H      | X      | L      | X      | X      | X      | Transfer completed          |
| 0/4                   | H      | X      | X      | L      | X      | X      | X      | Data transfer               |
| 0/0                   | L      | X      | X      | L      | X      | X      | X      | Transfer completed          |

The data must be read immediately after this command. It is mandatory to acknowledge that the error code has been read. 
This is done using the "Error code transfer finished" command (0x22). Otherwise, the error code will not be updated.

#### 0x1A Write S-position
| Data byte to/from PLC | FIOURY | FIINRY | CMDBSY | ERRST  | INTM   | FEEDPE | CLOOP  |                             |
| :-------------------: | :----: | :----: | :----: | :----: | :----: | :----: | :----: | :-------------------------- |
| 0/0                   | X      | H      | X      | X      | X      | X      | X      | Precondition                |
| 0/0                   | X      | L      | X      | X      | X      | X      | X      | Command transfer            |
| 4/0                   | X      | L      | X      | X      | X      | X      | X      | Data transfer               |
| 0/0                   | X      | H      | X      | X      | X      | X      | X      | Transfer completed          |

#### 0x1B Read S-position
| Data byte to/from PLC | FIOURY | FIINRY | CMDBSY | ERRST  | INTM   | FEEDPE | CLOOP  |                             |
| :-------------------: | :----: | :----: | :----: | :----: | :----: | :----: | :----: | :-------------------------- |
| 0/0                   | L      | H      | X      | X      | X      | X      | X      | Precondition                |
| 0/0                   | H      | L      | X      | X      | X      | X      | X      | Command transfer            |
| 0/0                   | H      | H      | X      | X      | X      | X      | X      | Transfer completed          |
| 0/4                   | H      | X      | X      | X      | X      | X      | X      | Data transfer               |
| 0/0                   | L      | X      | X      | X      | X      | X      | X      | Transfer completed          |

#### 0x1C Factor for Encoder 1
| Data byte to/from PLC | FIOURY | FIINRY | CMDBSY | ERRST  | INTM   | FEEDPE | CLOOP  |                             |
| :-------------------: | :----: | :----: | :----: | :----: | :----: | :----: | :----: | :-------------------------- |
| 0/0                   | X      | H      | X      | X      | X      | X      | X      | Precondition                |
| 0/0                   | X      | L      | X      | X      | X      | X      | X      | Command transfer            |
| 4/0                   | X      | L      | X      | X      | X      | X      | X      | Data transfer               |
| 0/0                   | X      | H      | X      | X      | X      | X      | X      | Transfer completed          |

#### 0x1D Factor for Encoder 2
| Data byte to/from PLC | FIOURY | FIINRY | CMDBSY | ERRST  | INTM   | FEEDPE | CLOOP  |                             |
| :-------------------: | :----: | :----: | :----: | :----: | :----: | :----: | :----: | :-------------------------- |
| 0/0                   | X      | H      | X      | X      | X      | X      | X      | Precondition                |
| 0/0                   | X      | L      | X      | X      | X      | X      | X      | Command transfer            |
| 4/0                   | X      | L      | X      | X      | X      | X      | X      | Data transfer               |
| 0/0                   | X      | H      | X      | X      | X      | X      | X      | Transfer completed          |

#### 0x1E Set External Time Base
| Data byte to/from PLC | FIOURY | FIINRY | CMDBSY | ERRST  | INTM   | FEEDPE | CLOOP  |                             |
| :-------------------: | :----: | :----: | :----: | :----: | :----: | :----: | :----: | :-------------------------- |
| 0/0                   | X      | H      | X      | X      | X      | X      | X      | Precondition                |
| 0/0                   | X      | L      | X      | X      | X      | X      | X      | Command transfer            |
| 0/0                   | X      | H      | X      | X      | X      | X      | X      | Transfer completed          |

Returns to the internal timer only by using the "PLC RESET" command (0x01).

#### 0x1F Clear Position Error
| Data byte to/from PLC | FIOURY | FIINRY | CMDBSY | ERRST  | INTM   | FEEDPE | CLOOP  |                             |
| :-------------------: | :----: | :----: | :----: | :----: | :----: | :----: | :----: | :-------------------------- |
| 0/0                   | X      | H      | X      | X      | X      | X      | X      | Precondition                |
| 0/0                   | X      | L      | X      | X      | X      | X      | X      | Command transfer            |
| 0/0                   | X      | H      | X      | X      | X      | X      | X      | Transfer completed          |

#### 0x20 Disable Track-error and encoder-error
| Data byte to/from PLC | FIOURY | FIINRY | CMDBSY | ERRST  | INTM   | FEEDPE | CLOOP  |                             |
| :-------------------: | :----: | :----: | :----: | :----: | :----: | :----: | :----: | :-------------------------- |
| 0/0                   | X      | H      | X      | X      | X      | X      | X      | Precondition                |
| 0/0                   | X      | L      | X      | X      | X      | X      | X      | Command transfer            |
| 0/0                   | X      | H      | X      | X      | X      | X      | X      | Transfer completed          |

#### 0x21 Enable Track-error and encoder-error
| Data byte to/from PLC | FIOURY | FIINRY | CMDBSY | ERRST  | INTM   | FEEDPE | CLOOP  |                             |
| :-------------------: | :----: | :----: | :----: | :----: | :----: | :----: | :----: | :-------------------------- |
| 0/0                   | X      | H      | X      | X      | X      | X      | X      | Precondition                |
| 0/0                   | X      | L      | X      | X      | X      | X      | X      | Command transfer            |
| 0/0                   | X      | H      | X      | X      | X      | X      | X      | Transfer completed          |

#### 0x22 Error Code Transfer Finished
| Data byte to/from PLC | FIOURY | FIINRY | CMDBSY | ERRST  | INTM   | FEEDPE | CLOOP  |                             |
| :-------------------: | :----: | :----: | :----: | :----: | :----: | :----: | :----: | :-------------------------- |
| 0/0                   | X      | H      | X      | L      | X      | X      | X      | Precondition                |
| 0/0                   | X      | L      | X      | X      | X      | X      | X      | Command transfer            |
| 0/0                   | X      | H      | X      | X      | X      | X      | X      | Transfer completed          |

#### 0x23 Fling Start after Trigger
| Data byte to/from PLC | FIOURY | FIINRY | CMDBSY | ERRST  | INTM   | FEEDPE | CLOOP  |                             |
| :-------------------: | :----: | :----: | :----: | :----: | :----: | :----: | :----: | :-------------------------- |
| 0/0                   | X      | H      | H      | X      | X      | H      | H      | Precondition                |
| 0/0                   | X      | L      | H      | X      | X      | H      | H      | Command transfer            |
| 1/0                   | X      | L      | H      | X      | X      | H      | H      | Data transfer               |
| 0/0                   | X      | H      | H      | X      | X      | H      | H      | Transfer completed          |
| 0/0                   | X      | X      | L      | X      | X      | L      | H      | Command finished            |

#### 0x24 Read ADC Value
| Data byte to/from PLC | FIOURY | FIINRY | CMDBSY | ERRST  | INTM   | FEEDPE | CLOOP  |                             |
| :-------------------: | :----: | :----: | :----: | :----: | :----: | :----: | :----: | :-------------------------- |
| 0/0                   | L      | H      | X      | X      | X      | X      | X      | Precondition                |
| 0/0                   | H      | L      | X      | X      | X      | X      | X      | Command transfer            |
| 0/0                   | H      | H      | X      | X      | X      | X      | X      | Transfer completed          |
| 0/1                   | H      | X      | X      | X      | X      | X      | X      | Data transfer               |
| 0/0                   | L      | X      | X      | X      | X      | X      | X      | Transfer completed          |

#### 0x25 Write DAC Value
| Data byte to/from PLC | FIOURY | FIINRY | CMDBSY | ERRST  | INTM   | FEEDPE | CLOOP  |                             |
| :-------------------: | :----: | :----: | :----: | :----: | :----: | :----: | :----: | :-------------------------- |
| 0/0                   | X      | H      | H      | X      | X      | X      | L      | Precondition                |
| 0/0                   | X      | L      | H      | X      | X      | X      | L      | Command transfer            |
| 2/0                   | X      | L      | H      | X      | X      | X      | L      | Data transfer               |
| 0/0                   | X      | H      | H      | X      | X      | X      | L      | Transfer completed          |
| 0/0                   | X      | X      | L      | X      | X      | X      | X      | Command finished            |

#### 0x26 Start S-position
| Data byte to/from PLC | FIOURY | FIINRY | CMDBSY | ERRST  | INTM   | FEEDPE | CLOOP  |                             |
| :-------------------: | :----: | :----: | :----: | :----: | :----: | :----: | :----: | :-------------------------- |
| 0/0                   | X      | H      | L      | X      | X      | X      | H      | Precondition                |
| 0/0                   | X      | L      | L      | X      | X      | X      | H      | Command transfer            |
| 0/0                   | X      | H      | H      | X      | X      | H      | H      | Transfer completed          |
| 0/0                   | X      | X      | L      | X      | X      | L      | H      | Command finished            |

#### 0x27 Set Comparators for S-position
| Data byte to/from PLC | FIOURY | FIINRY | CMDBSY | ERRST  | INTM   | FEEDPE | CLOOP  |                             |
| :-------------------: | :----: | :----: | :----: | :----: | :----: | :----: | :----: | :-------------------------- |
| 0/0                   | X      | H      | X      | X      | X      | X      | X      | Precondition                |
| 0/0                   | X      | L      | X      | X      | X      | X      | X      | Command transfer            |
| 8/0                   | X      | L      | X      | X      | X      | X      | X      | Data transfer               |
| 0/0                   | X      | H      | X      | X      | X      | X      | X      | Transfer completed          |
| 0/0                   | X      | X      | X      | X      | X      | X      | X      | Command finished            |

#### 0x28 Read Position Error
| Data byte to/from PLC | FIOURY | FIINRY | CMDBSY | ERRST  | INTM   | FEEDPE | CLOOP  |                             |
| :-------------------: | :----: | :----: | :----: | :----: | :----: | :----: | :----: | :-------------------------- |
| 0/0                   | L      | H      | X      | X      | X      | X      | X      | Precondition                |
| 0/0                   | H      | L      | X      | X      | X      | X      | X      | Command transfer            |
| 0/0                   | H      | H      | X      | X      | X      | X      | X      | Transfer completed          |
| 0/2                   | H      | X      | X      | X      | X      | X      | X      | Data transfer               |
| 0/0                   | L      | X      | X      | X      | X      | X      | X      | Transfer completed          |

#### 0x29 Jog Speed Factor
| Data byte to/from PLC | FIOURY | FIINRY | CMDBSY | ERRST  | INTM   | FEEDPE | CLOOP  |                             |
| :-------------------: | :----: | :----: | :----: | :----: | :----: | :----: | :----: | :-------------------------- |
| 0/0                   | X      | H      | X      | X      | X      | X      | X      | Precondition                |
| 0/0                   | X      | L      | X      | X      | X      | X      | X      | Command transfer            |
| 1/0                   | X      | L      | X      | X      | X      | X      | X      | Data transfer               |
| 0/0                   | X      | H      | X      | X      | X      | X      | X      | Transfer completed          |

#### 0x2A Set Length Correction Factor
| Data byte to/from PLC | FIOURY | FIINRY | CMDBSY | ERRST  | INTM   | FEEDPE | CLOOP  |                             |
| :-------------------: | :----: | :----: | :----: | :----: | :----: | :----: | :----: | :-------------------------- |
| 0/0                   | X      | H      | X      | X      | X      | X      | X      | Precondition                |
| 0/0                   | X      | L      | X      | X      | X      | X      | X      | Command transfer            |
| 8/0                   | X      | L      | X      | X      | X      | X      | X      | Data transfer               |
| 0/0                   | X      | H      | X      | X      | X      | X      | X      | Transfer completed          |

#### 0x2B Read Length After Correction
| Data byte to/from PLC | FIOURY | FIINRY | CMDBSY | ERRST  | INTM   | FEEDPE | CLOOP  |                             |
| :-------------------: | :----: | :----: | :----: | :----: | :----: | :----: | :----: | :-------------------------- |
| 0/0                   | L      | H      | X      | X      | X      | X      | X      | Precondition                |
| 0/0                   | L      | L      | X      | X      | X      | X      | X      | Command transfer            |
| 0/0                   | H      | H      | X      | X      | X      | X      | X      | Transfer completed          |
| 0/4                   | H      | X      | X      | X      | X      | X      | X      | Data transfer               |
| 0/0                   | L      | X      | X      | X      | X      | X      | X      | Transfer completed          |

#### 0x2C Trapez Function Alternating
| Data byte to/from PLC | FIOURY | FIINRY | CMDBSY | ERRST  | INTM   | FEEDPE | CLOOP  |                             |
| :-------------------: | :----: | :----: | :----: | :----: | :----: | :----: | :----: | :-------------------------- |
| 0/0                   | X      | H      | L      | X      | X      | L      | X      | Precondition                |
| 0/0                   | X      | L      | L      | X      | X      | L      | X      | Command transfer            |
| 0/0                   | X      | H      | H      | X      | X      | L      | X      | Transfer completed          |
| 0/0                   | X      | X      | L      | X      | X      | X      | X      | Command finished            |

#### 0x2D Divide Two 32-bit Integers Values
| Data byte to/from PLC | FIOURY | FIINRY | CMDBSY | ERRST  | INTM   | FEEDPE | CLOOP  |                             |
| :-------------------: | :----: | :----: | :----: | :----: | :----: | :----: | :----: | :-------------------------- |
| 0/0                   | X      | H      | X      | X      | X      | X      | X      | Precondition                |
| 0/0                   | X      | L      | X      | X      | X      | X      | X      | Command transfer            |
| 8/0                   | X      | L      | X      | X      | X      | X      | X      | Data transfer               |
| 0/0                   | X      | H      | X      | X      | X      | X      | X      | Transfer completed          |

#### 0x2E Multiply Result of Divide with 64-bit Fixed Point
| Data byte to/from PLC | FIOURY | FIINRY | CMDBSY | ERRST  | INTM   | FEEDPE | CLOOP  |                             |
| :-------------------: | :----: | :----: | :----: | :----: | :----: | :----: | :----: | :-------------------------- |
| 0/0                   | X      | H      | X      | X      | X      | X      | X      | Precondition                |
| 0/0                   | X      | L      | X      | X      | X      | X      | X      | Command transfer            |
| 8/0                   | X      | L      | X      | X      | X      | X      | X      | Data transfer               |
| 0/0                   | X      | H      | X      | X      | X      | X      | X      | Transfer completed          |

#### 0x2F Read 64-bit Fixed Point Result
| Data byte to/from PLC | FIOURY | FIINRY | CMDBSY | ERRST  | INTM   | FEEDPE | CLOOP  |                             |
| :-------------------: | :----: | :----: | :----: | :----: | :----: | :----: | :----: | :-------------------------- |
| 0/0                   | L      | H      | X      | X      | X      | X      | X      | Precondition                |
| 0/0                   | L      | L      | X      | X      | X      | X      | X      | Command transfer            |
| 0/0                   | H      | H      | X      | X      | X      | X      | X      | Transfer completed          |
| 0/8                   | H      | X      | X      | X      | X      | X      | X      | Data transfer               |
| 0/0                   | L      | X      | X      | X      | X      | X      | X      | Transfer completed          |

#### 0x30 New Cycle of Length Correction
| Data byte to/from PLC | FIOURY | FIINRY | CMDBSY | ERRST  | INTM   | FEEDPE | CLOOP  |                             |
| :-------------------: | :----: | :----: | :----: | :----: | :----: | :----: | :----: | :-------------------------- |
| 0/0                   | X      | H      | X      | L      | X      | X      | X      | Precondition                |
| 0/0                   | X      | L      | X      | X      | X      | X      | X      | Command transfer            |
| 0/0                   | X      | H      | X      | X      | X      | X      | X      | Transfer completed          |

#### 0x31 Read Pulses of Encoder 2
| Data byte to/from PLC | FIOURY | FIINRY | CMDBSY | ERRST  | INTM   | FEEDPE | CLOOP  |                             |
| :-------------------: | :----: | :----: | :----: | :----: | :----: | :----: | :----: | :-------------------------- |
| 0/0                   | L      | H      | X      | X      | X      | X      | X      | Precondition                |
| 0/0                   | H      | L      | X      | X      | X      | X      | X      | Command transfer            |
| 0/0                   | H      | H      | X      | X      | X      | X      | X      | Transfer completed          |
| 0/4                   | H      | X      | X      | X      | X      | X      | X      | Data transfer               |
| 0/0                   | L      | X      | X      | X      | X      | X      | X      | Transfer completed          |

#### 0x32..0xFF Reserved for future use

These codes are not yet assigned. After the transfer is completed, "ERRST" is set high, and the error code "INTERFACE TRANSMISSION ERROR" is returned.

## Error Codes

### Overview

#### 00000001 - ECRAM - RAMTEST Failed  
**Cause:** RAM faulty  
**Remedy:** Replace RAM or PLC card  
**Note:** PLC status: "ERRST"=high, all others low. PLC is not ready to accept commands; LEDs indicate the type of error.

#### 00000002 - ECROM - PROMTEST Failed
**Cause:** PROM faulty  
**Remedy:** Replace PROM or PLC card  
**Note:** PLC status: "ERRST"=high, all others low. PLC is not ready to accept commands; LEDs indicate the type of error.

#### 00000004 - ECBMIS - Basic Parameter Missing
**Cause:** The commands "SLOOP", "TCHSET", or "TPZSET" are issued without prior transmission of the basic parameters.
**Reaction:** "CLOSED LOOP" not possible, commands ignored  
**Remedy:** Transmit basic parameters

#### 00000008 - 


### Error Display on the LEDs

Only in "No Loop" mode and if error codes are not read via the interface, multiple errors may occur; in this case, only the last error is displayed.

```
LED          -  -  -  -  -  -  -  -     +  +  +  +  +  +  +  +
Error code   7  6  5  4  3  2  1  0  G  0  1  2  3  4  5  6  7  Description
00000001     X  -  -  -  -  -  -  -  X  X  -  -  -  -  -  -  -  RAM Test Fail
00000002     X  -  -  -  -  -  -  -  X  -  X  -  -  -  -  -  -  PROM Test Fail
00000004     X  -  -  -  -  -  -  -  X  -  -  X  -  -  -  -  -  Basic Parameter Missing
00000008     X  -  -  -  -  -  -  -  X  -  -  -  X  -  -  -  -  Expected Position Error too High
00000010     X  -  -  -  -  -  -  -  X  -  -  -  -  X  -  -  -  SQR Table not Calculated
00000020     X  -  -  -  -  -  -  -  X  -  -  -  -  -  X  -  -  Encoder Compare Error
00000040     X  -  -  -  -  -  -  -  X  -  -  -  -  -  -  X  -  Track Error
00000080     X  -  -  -  -  -  -  -  X  -  -  -  -  -  -  -  X  Safety Limits Exceeded
00000100     X  -  -  -  -  -  -  X  X  X  -  -  -  -  -  -  -  Position Error Overflow
00000200     X  -  -  -  -  -  -  X  X  -  X  -  -  -  -  -  -  Arithmetic Processor Unit Fail
00000400     X  -  -  -  -  -  -  X  X  -  -  X  -  -  -  -  -  Trim-function Improper Terminated
00000800     X  -  -  -  -  -  -  X  X  -  -  -  X  -  -  -  -  Control Voltage Missing
00001000     X  -  -  -  -  -  -  X  X  -  -  -  -  X  -  -  -  Trap Interrupt
00002000     X  -  -  -  -  -  -  X  X  -  -  -  -  -  X  -  -  Interface Fail
00004000     X  -  -  -  -  -  -  X  X  -  -  -  -  -  -  X  -  Transfered Length Ignore
00008000     X  -  -  -  -  -  -  X  X  -  -  -  -  -  -  -  X  Basic Parameter Value Wrong
00010000     X  -  -  -  -  -  X  -  X  X  -  -  -  -  -  -  -  Flying Start Fail
00020000     X  -  -  -  -  -  X  -  X  -  X  -  -  -  -  -  -  Search Improper Terminated
00040000     X  -  -  -  -  -  X  -  X  -  -  X  -  -  -  -  -  Length Correction Fail
00080000     X  -  -  -  -  -  X  -  X  -  -  -  X  -  -  -  -  Length Correction not Terminated
00100000     X  -  -  -  -  -  X  -  X  -  -  -  -  X  -  -  -  Calculation Fail

X: LED on
-: LED off
```

### Read Error Code Command 0x19

When the status bit "ERRST" has been set, the error code should be read as soon as possible so that appropriate measures can be taken.
The "READ ERROR CODE" command starts the transfer of the 4 bytes to the FIFO and resets the "ERRST" bit in the status. Further error reports are temporarily blocked.
All 4 data bytes must be read.
Afterwards the command "ERROR CODE TRANSFER FINISHED" must be sent as an acknowledgment so that further errors can be reported.

### Error Code Transfer Finished Command 0x22

Serves as acknowledgment; only after this command can the PLC set the status bit "ERRST" again.

### 
# ovmslogs
VW e-Up OVMS logs, T26 comfort CAN

# Maps+More Commands
All M+M commands are sent to ID 0x69D

## Connect M+M

At initial connect, two commands are sent. 
This example was run on on Nov 07 15:45:45:
```
24 50 15 0b 07 
```
`15 0b 07` is the date:
0x15 = 21
0x0b = 11
0x07 = 7

```
24 51 0e 2d 00 
```
`0e 2d` is the time:
0x0e = 14(+1)
0x2d = 45

Additional 69D commands seen at M+M connect:
```
Nov 08 11:39:57 80 04 19 59 11 00 00 04
Nov 08 11:39:57 80 04 19 5a 11 00 00 04
```
(functionality not known yet)

## Modify Charge Current
Modification of immediate charge current ("Sofortladen") leads to four different commands:
```
80 14 29 59 13 45 00 01
c0 00 02 00 0a 00 00 00
c1 08 4f 70 74 69 6f 6e
c2 65 6e
```

In details:
```
80 14 29 59 13 45 00 01
```
`80 14` is possibly the command indicator,\
`59` (fixed ?),\
`13` is a counter that's incremented for each packet,\
`45 00 01` (fixed ?)
```
c0 00 02 00 0a 00 00 00
```
`c0` (and `c1`, `c2`) are additional parameters for the initial `80` command\
`02` seems to be "climate w/o batt only" (06 is with batt)\
`0a` is the current parameter (10A - other values:
0x0d=13A, 0x05=5A, 0x20=max)

```
c1 08 4f 70 74 69 6f 6e
```
(no details known yet)


```
c2 65 6e
```
(no details known yet)

c1 and c2 contain the same data as in the 69E c2/c3 OCU commands for climate control (see end of this text):
```
C2 1E 1E 0A 00 00 08 4F
C3 70 74 69 6F 6E 65 6E
```


## Seen commands:
### Climate change to 21 deg, w/o battery
```
Nov 07 15:50:41 80 0e 29 59 1b 47 00 01
Nov 07 15:50:41 c0 00 02 00 20 50 6e 00  #6e = 21, 02 = climate w/o batt?
Nov 07 15:50:41 c1 00 1e 0a
```

### Enable battery-only climate
```
Nov 07 15:51:21 80 14 29 59 1c 45 00 01     
Nov 07 15:51:21 c0 00 06 00 20 00 00 00  # 06 = climate with batt? Zeroes mean no temperature change?
Nov 07 15:51:21 c1 08 4f 70 74 69 6f 6e
Nov 07 15:51:21 c2 65 6e
```

### Modify charge current to 5A
```
Nov 07 15:47:21 80 14 29 59 14 45 00 01
Nov 07 15:47:21 c0 00 02 00 05 00 00 00 # 05 = 5A
Nov 07 15:47:21 c1 08 4f 70 74 69 6f 6e
Nov 07 15:47:21 c2 65 6e
```

### Charge minimum SOC to 90%
```
Nov 07 15:53:01 80 0e 29 59 11 47 00 01
Nov 07 15:53:01 c0 00 02 00 20 5a 5f 00  # 0x5a = 90
Nov 07 15:53:01 c1 00 1e 0a
```

### Climate timer 1 to Sunday, no repetition
```
Nov 06 14:45:31 80 08 29 54 15 0b 07 0c # Sunday is 2021-11-07, i.e. 15 0b 07; 0c is hour-1
Nov 06 14:45:31 c0 32 81 03 00 # 32 is minute; 81 is 0x80 (sunday) | 1 (no repeat)
```

### Activate timer 3 (1 & 2 already active)
```
Nov 06 14:47:01 29 53 07 00 -> 7 is 1 | 2 | 4
```


### At start and end of M+M connect
Several of these:
```
Nov 08 11:44:16 19 42
Nov 08 11:44:16 19 42
Nov 08 11:44:16 14 42
Nov 08 11:44:17 19 42
Nov 08 11:44:17 14 42
```


### 80 Commands
`80 14 29 59 14 45 00 01` # charge current ... c0, c1, c2\
`80 0e 29 59 11 47 00 01` # charge min. SOC ... c0, c1\
`80 08 29 54 15 0b 07 0c` # climate timer, 15-0c is date+hour, ... c0\
`80 14 29 59 1c 45 00 01` # enable bat-only climate ... c0, c1, c2\
`80 0e 29 59 1b 47 00 01` # climate change w/o bat ... c0, c1\
`80 04 19 59 11 00 00 04` # at start ???\
`80 04 19 5a 11 00 00 04` # at ???

| 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
| - | - | - | - | - | - | - | - |
| 80 |14 |29| 59| 14| 45| 00| 01|
| ID1 | ID2| Fix? | 59,54,5a? | Cnt. | D0 | D1 | D2


### C0 Command Parameters

`c0 00 02 00 20 50 6e 00`  #800e, +c1, 20=32A, 6e = 21deg, 02 = climate w/o batt?\
`c0 00 06 00 20 00 00 00`  #8014, +c1,c2, 06 = climate with batt? Zeroes mean no temperature change?\
`c0 00 02 00 05 00 00 00`  #8014, +c1,c2, 05 = 5A\
`c0 32 81 03 00` #8008 32 is minute; 81 is 0x80 (sunday) | 1 (no repeat)

### OCU commands climate on
(taken from OVMS source)
`5A7 60 16 00 00 00 00 00 00`

`69E 80 20 29 59 21 00 00 01`\
`69E C0 06 00 10 1E FF FF 00`\
`69E C1 FF FF FF FF 01 78 00`  # 78 = 22 deg\
`69E C2 1E 1E 0A 00 00 08 4F`\
`69E C3 70 74 69 6F 6E 65 6E`

`5A7 60 16 00 00 00 00 00 00`

`69E 29 58 00 01            `  # 01 = on, 00 = off?

These OCU commands seem to have an effect on the following parameters:
 - min. SOC to 30% (0x1E?)
 - charge current to 5A (?)
 - 22 deg (0x78) climate with battery (06?)
 - start climate *now* 



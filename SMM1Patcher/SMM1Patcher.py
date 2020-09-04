#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# SMM1Patcher
# A Code Patcher For The Super Mario Maker Binary.
# Version 0.2
# Created By MarioPossamato And System46

# This File Is Part Of SMM1Patcher.

# All Modifications In This Script Are For Version 1.47 Of Super Mario Maker.
# To Apply Modifications Manually, I Recommend Using HxD Hex Editor <https://mh-nexus.de/downloads/HxDSetup.zip>.

# To Find These Offsets Using HxD, Use Ctrl+G (Goto), And Paste In The Offset.  Then, Copy The Data Press Ctrl+B (Paste Overrite).
# Alternatively, You Can Use HxD's Ctrl+E (Select Block), Paste In The Start And End Offsets, Then Right Click On The Selected Block, Click Fill Selection, Then Place The Data In There To Fill The Selection.

# Please Note That None Of The Modifications In This Script Will Work If Your Copy Of Block.rpx Is Not Decompressed!  Use wiiurpxtool <https://github.com/0CBH0/wiiurpxtool/releases>.


# Examples:

"""
> Python -i SMM1Patcher.py Block.rpx
SMM1Patcher (Version 0.2)
Created By MarioPossamato And System46
>>>
>>> x = Read(dict_0, 0x4)
3f800000
1.0
Ok
>>> x = x[1]*2
>>> Write(dict_0, int.from_bytes(bytes.fromhex(FloatToHex(x)), 'big'), 0x4)
Ok
>>> ChangeWingedSolidBlockSize(ApplicableBlockTypes['HardBlock'], 2.0)
Ok
>>> ChangeWingedSolidBlockSize(ApplicableBlockTypes['IceBlock'], 0.5)
Ok
>>> ChangeLargeDokanEnemySize(2.0)
Ok
"""


SMM1PatcherVersion = '0.2'


import sys
import struct
import binascii
import time


# Dictionaries

# Useful Known Variables, Found By Mario Possamato

"MarioRelated"
dict_0 = {'StartOffset':0xCC0E0, 'EndOffset':0xCC0E4, 'Size':0x4, 'Default':0x3F800000, 'Description':'Carry displacement, horizontal', 'AffectedModes':['M1','M3','MW']}
dict_1 = {'StartOffset':0xCC16C, 'EndOffset':0xCC170, 'Size':0x4, 'Default':0x40000000, 'Description':'Carry displacement vertical, small Mario', 'AffectedModes':['M1','M3','MW']}
dict_2 = {'StartOffset':0xCE7BC, 'EndOffset':0xCE7C0, 'Size':0x4, 'Default':0x40400000, 'Description':'Carry displacement vertical, large Mario', 'AffectedModes':['M1','M3','MW']}
dict_3 = {'StartOffset':0xCE29C, 'EndOffset':0xCE2A0, 'Size':0x4, 'Default':0x3F800000, 'Description':'Run speed, right', 'AffectedModes':['M1','M3','MW','WU']}
dict_4 = {'StartOffset':0xCE2B0, 'EndOffset':0xCE2B4, 'Size':0x4, 'Default':0x40400000, 'Description':'Run speed, right and left', 'AffectedModes':['M1','M3','MW','WU']}
dict_5 = {'StartOffset':0xB1180, 'EndOffset':0xB1184, 'Size':0x4, 'Default':0x40400000, 'Description':'Throw speed while not moving', 'AffectedModes':['M1','M3','MW','WU']}
dict_6 = {'StartOffset':0xB1178, 'EndOffset':0xB117C, 'Size':0x4, 'Default':0x3F800000, 'Description':'Throw speed while turning around', 'AffectedModes':['M1','M3','MW','WU']}
dict_7 = {'StartOffset':0xB11C8, 'EndOffset':0xB11CC, 'Size':0x4, 'Default':0x3f8CCCCD, 'Description':'Throw speed while crouching, right', 'AffectedModes':['M1','M3','MW','WU']}
dict_8 = {'StartOffset':0xB11C4, 'EndOffset':0xB11C8, 'Size':0x4, 'Default':0xBF8CCCCD, 'Description':'Throw speed while crouching, left', 'AffectedModes':['M1','M3','MW','WU']}
dict_9 = {'StartOffset':0xB11CC, 'EndOffset':0xB11D0, 'Size':0x4, 'Default':0x3E99999A, 'Description':'Throw speed upwards', 'AffectedModes':['M1','M3','MW','WU']}
dict_10 = {'StartOffset':0xCE58C, 'EndOffset':0xCE590, 'Size':0x4, 'Default':0x40200000, 'Description':'Jump gravity', 'AffectedModes':['M1','M3','MW','WU']}
dict_11 = {'StartOffset':0xC4DE8, 'EndOffset':0xC4DEC, 'Size':0x4, 'Default':0x40000000, 'Description':'Bounce velocity off bumper side', 'AffectedModes':['M1','M3','MW','WU']}
dict_12 = {'StartOffset':0xD034C, 'EndOffset':0xD0350, 'Size':0x4, 'Default':0x3F800000, 'Description':'Cloud ride scale', 'AffectedModes':['M1','M3','MW','WU']}
dict_13 = {'StartOffset':0xD1260, 'EndOffset':0xD1264, 'Size':0x4, 'Default':0xBE23D70A, 'Description':'Gravity when falling offscreen after dying', 'AffectedModes':['M1','M3','MW','WU']}
dict_14 = {'StartOffset':0xD2574, 'EndOffset':0xD2578, 'Size':0x4, 'Default':0x40400000, 'Description':'Upward propeller velocity', 'AffectedModes':['M1','M3','MW','WU']}
dict_15 = {'StartOffset':0xD2548, 'EndOffset':0xD254C, 'Size':0x4, 'Default':0xBfA00000, 'Description':'Propeller gravity when floating down', 'AffectedModes':['M1','M3','MW','WU']}
dict_16 = {'StartOffset':0xD2598, 'EndOffset':0xD259C, 'Size':0x4, 'Default':0xBF800000, 'Description':'Propeller gravity when twirling', 'AffectedModes':['M1','M3','MW','WU']}
dict_17 = {'StartOffset':0xD25A8, 'EndOffset':0xD25AC, 'Size':0x4, 'Default':0xC0C00000, 'Description':'Propeller gravity when drilling', 'AffectedModes':['M1','M3','MW','WU']}
dict_18 = {'StartOffset':0xD2584, 'EndOffset':0xD2588, 'Size':0x4, 'Default':0xBDCCCCCD, 'Description':'Unknown propeller gravity related variable', 'AffectedModes':['M1','M3','MW','WU']}
dict_19 = {'StartOffset':0x19C30, 'EndOffset':0x19C50, 'Size':0x4, 'Default':0x3F800000, 'Description':'Fireball model size', 'AffectedModes':['M1','M3','MW','WU']}
dict_20 = {'StartOffset':0x19A98, 'EndOffset':0x19A9C, 'Size':0x4, 'Default':0x3F800000, 'Description':'Fireball speed, right', 'AffectedModes':['M1','M3','MW','WU']}
dict_21 = {'StartOffset':0x19A9C, 'EndOffset':0x19AA0, 'Size':0x4, 'Default':0xBF800000, 'Description':'Fireball speed, left', 'AffectedModes':['M1','M3','MW','WU']}
dict_22 = {'StartOffset':0x19C38, 'EndOffset':0x19C3C, 'Size':0x4, 'Default':0x40680000, 'Description':'Fireball speed, forward', 'AffectedModes':['M1','M3','MW','WU']}
dict_23 = {'StartOffset':0x19C3C, 'EndOffset':0x19C40, 'Size':0x4, 'Default':0x40800000, 'Description':'Upward bounce velocity of fireball', 'AffectedModes':['M1','M3','MW','WU']}
dict_24 = {'StartOffset':0x19C44, 'EndOffset':0x19C48, 'Size':0x4, 'Default':0xBEE00000, 'Description':'Gravity of fireball', 'AffectedModes':['M1','M3','MW','WU']}
dict_25 = {'StartOffset':0x19C48, 'EndOffset':0x19C4C, 'Size':0x4, 'Default':0xC0800000, 'Description':'Upward fireball velocity', 'AffectedModes':['M1','M3','MW','WU']}

"SenkanHoudaiRelated"
dict_26 = {'StartOffset':0x1A504, 'EndOffset':0x1A508, 'Size':0x4, 'Default':0xBF800000, 'Description':'Bounce velocity off SenkanHoudaiBall', 'AffectedModes':['M1','M3','MW','WU']}
dict_27 = {'StartOffset':0x1A518, 'EndOffset':0x1A51C, 'Size':0x4, 'Default':0x3F800000, 'Description':'SenkanHoudaiBall model size and speed', 'AffectedModes':['M1','M3','MW','WU']}
dict_28 = {'StartOffset':0x1A4B4, 'EndOffset':0x1A4B8, 'Size':0x4, 'Default':0x40800000, 'Description':'SenkanHoudaiBall hitbox width', 'AffectedModes':['M1','M3','MW','WU']}
dict_29 = {'StartOffset':0x1A4B8, 'EndOffset':0x1A4BC, 'Size':0x4, 'Default':0x40800000, 'Description':'SenkanHoudaiBall hitbox height, top', 'AffectedModes':['M1','M3','MW','WU']}
dict_30 = {'StartOffset':0x1A4B0, 'EndOffset':0x1A4B4, 'Size':0x4, 'Default':0x41000000, 'Description':'SenkanHoudaiBall hitbox height, bottom', 'AffectedModes':['M1','M3','MW','WU']}
dict_31 = {'StartOffset':0x648E4, 'EndOffset':0x648E8, 'Size':0x4, 'Default':0x80000000, 'Description':'SenkanHoudaiBall shoot direction', 'AffectedModes':['M1','M3','MW','WU']}
dict_32 = {'StartOffset':0x64AB8, 'EndOffset':0x64ABC, 'Size':0x4, 'Default':0xC1000000, 'Description':'SenkanHoudai hitbox width', 'AffectedModes':['M1','M3','MW','WU']}
dict_33 = {'StartOffset':0x64ABC, 'EndOffset':0x64AC0, 'Size':0x4, 'Default':0x41800000, 'Description':'SenkanHoudai hitbox height', 'AffectedModes':['M1','M3','MW','WU']}
dict_34 = {'StartOffset':0x648CC, 'EndOffset':0x648D0, 'Size':0x4, 'Default':0x00000000, 'Description':'Speed SenkanHoudais move left/right in play mode', 'AffectedModes':['M1','M3','MW','WU']}

"KillerHoudaiRelated"
dict_35 = {'StartOffset':0x49828, 'EndOffset':0x4982C, 'Size':0x4, 'Default':0x3F000000, 'Description':'Upward bounce velocity of objects shot out of KillerHoudais', 'AffectedModes':['M1','M3','MW','WU']}
dict_36 = {'StartOffset':0x49800, 'EndOffset':0x49804, 'Size':0x4, 'Default':0x3F800000, 'Description':'Enemy model and hitbox size when first shot out of a KillerHoudai', 'AffectedModes':['M1','M3','MW','WU']}
dict_37 = {'StartOffset':0x49818, 'EndOffset':0x4981C, 'Size':0x4, 'Default':0x41800000, 'Description':'Enemy model and hitbox size when shot out of a KillerHoudai', 'AffectedModes':['M1','M3','MW','WU']}
dict_38 = {'StartOffset':0x55E34, 'EndOffset':0x55E38, 'Size':0x4, 'Default':0xC1800000, 'Description':'Vertical displacement of objects when shot from a KillerHoudai', 'AffectedModes':['M1','M3','MW','WU']}
dict_39 = {'StartOffset':0x55E44, 'EndOffset':0x55E48, 'Size':0x4, 'Default':0x41000000, 'Description':'KillerHoudai hitbox width, right', 'AffectedModes':['M1','M3','MW','WU']}
dict_40 = {'StartOffset':0x55E70, 'EndOffset':0x55E74, 'Size':0x4, 'Default':0xC1000000, 'Description':'KillerHoudai hitbox width, left', 'AffectedModes':['M1','M3','MW','WU']}
dict_41 = {'StartOffset':0x55E68, 'EndOffset':0x55E6C, 'Size':0x4, 'Default':0x42000000, 'Description':'KillerHoudai hitbox height', 'AffectedModes':['M1','M3','MW','WU']}
dict_42 = {'StartOffset':0x686C4, 'EndOffset':0x686C8, 'Size':0x4, 'Default':0xBE400000, 'Description':'KillerHoudai gravity', 'AffectedModes':['M1','M3','MW','WU']}
dict_43 = {'StartOffset':0x55E30, 'EndOffset':0x55E34, 'Size':0x4, 'Default':0x3F800000, 'Description':'KillerHoudai bounce velocity off of Mario', 'AffectedModes':['M1','M3','MW','WU']}

"LargeEnemyLinkedToDokanRelated"
dict_44 = {'StartOffset':0x48FD0, 'EndOffset':0x48FD4, 'Size':0x4, 'Default':0x3F333333, 'Description':'Model and hitbox size of large enemies when spawned in a Dokan', 'AffectedModes':['M1','M3','MW','WU']}
dict_45 = {'StartOffset':0x49078, 'EndOffset':0x4907C, 'Size':0x4, 'Default':0x3F000000, 'Description':'Model and hitbox size of large enemies when spawned in a Dokan', 'AffectedModes':['M1','M3','MW','WU']}
dict_46 = {'StartOffset':0x49034, 'EndOffset':0x49038, 'Size':0x4, 'Default':0x3F800000, 'Description':'Model and hitbox size of large enemies immediately after exiting a Dokan', 'AffectedModes':['M1','M3','MW','WU']}
dict_47 = {'StartOffset':0x49098, 'EndOffset':0x4909C, 'Size':0x4, 'Default':0x40400000, 'Description':'Velocity at which large enemies shoot out of pipes', 'AffectedModes':['M1','M3','MW','WU']}

"WingedSolidBlockModelHitboxFormat"
ApplicableBlockTypes = {'HardBlock':{'StartOffset':0xB41A4, 'EndOffset':0xB41CC},'IceBlock':{'StartOffset':0xB4FD0, 'EndOffset':0xB4FF8}}
ObjectBlockFormat = {
'Solid block model size':0x4,
'Model placement over solid block hitbox':0x8,
'Unknown 1':0x4,
'Winged solid block velocity, horizontal':0xC,
'Winged solid block velocity, vertical':0x10,
'Unknown 2':0x14,
'Solid block hitbox width right, height':0x18,
'Unknown 3':0x1C,
'Unknown 4':0x20,
'Solid block hitbox width, left':0x24
}


# Function To Change The Model And Hitbox Size Of Winged Solid Blocks

"""
>>> ChangeWingedSolidBlockSize(ApplicableBlockTypes[BlockType], Size)
Ok
Replace BlockType With The Type Of Block You Want (HardBlock, IceBlock)
"""

def ChangeWingedSolidBlockSize(x, y, model=True, velocityHorizontal=True, velocityVertical=True, hitbox=True):
    with open(File,'rb') as file:
        data = bytearray(file.read())
        data[x['StartOffset']:x['StartOffset']+0x4] = bytes.fromhex(FloatToHex(y)) # Model Size
        data[x['StartOffset']+0xC:x['StartOffset']+0x10] = bytes.fromhex(FloatToHex(48.0*y)) # Horizontal Velocity
        data[x['StartOffset']+0x10:x['StartOffset']+0x14] = bytes.fromhex(FloatToHex(16.0*y)) # Vertical Velocity"
        data[x['StartOffset']+0x18:x['StartOffset']+0x1C] = bytes.fromhex(FloatToHex(8.0*y)) # Hitbox Width Right, Height
        data[x['StartOffset']+0x24:x['StartOffset']+0x28] = bytes.fromhex(FloatToHex(-8.0*y)) # Hitbox Width Left
        with open(File,'wb') as file:
            file.write(data)
        print('Ok')


# Function To Change The Model And Hitbox Size Of Large Enemies Linked To Dokans

"""
>>> ChangeLargeDokanEnemySize(Size)
Ok
"""

def ChangeLargeDokanEnemySize(x):
    with open(File,'rb') as file:
        data = bytearray(file.read())
        data[dict_44['StartOffset']:dict_44['StartOffset']+0x4] = bytes.fromhex(FloatToHex(0.7*x))
        data[dict_45['StartOffset']:dict_45['StartOffset']+0x4] = bytes.fromhex(FloatToHex(0.5*x))
        data[dict_46['StartOffset']:dict_46['StartOffset']+0x4] = bytes.fromhex(FloatToHex(1.0*x))
        with open(File,'wb') as file:
            file.write(data)
        print('Ok')


# Function To Write Data

"""
>>> Write(Dictionary, Data, Length)
Ok
"""

def Write(x, y, z):
    with open(File,'rb') as file:
        data = bytearray(file.read())
        data[x['StartOffset']:x['EndOffset']] = int.to_bytes(y, z, 'big')
        with open(File,'wb') as file:
            file.write(data)
        print('Ok')


# Function To Read Data

"""
>>> Read(Dictionary, Length)
Ok
"""

def Read(x, y):
    with open(File,'rb') as file:
        file.seek(x['StartOffset'])
        data = file.read(y)
        print(bytes.hex(data))
        print(HexToFloat(int.from_bytes(data, 'big')))
        print('Ok')
        return [bytes.hex(data), HexToFloat(int.from_bytes(data, 'big'))]

# Function To Replace Data

"""
>>> Replace('3f800000', '40400000', 0x4, 0x00, 10)
Ok
"""

def Replace(x, y, z, start, a):
	with open(File, 'rb') as file:
		b = bytearray(file.read(start))
		file.seek(start)
		c = bytearray(file.read())
		for i in range(int(a)):
			c[c.find(bytes.fromhex(x)):c.find(bytes.fromhex(x))+z] = bytes.fromhex(y)
		with open(File, 'wb') as file:
			file.write(b+c)
		print('Ok')


# Function To Convert Float To Hex

"""
>>> FloatToHex(1.0)
'3f800000'
"""

def FloatToHex(f):
    return hex(struct.unpack('<I', struct.pack('<f', f))[0])[2:]


# Function To Convert Hex To Float

"""
>>> HexToFloat(0x3f800000)
1.0
"""

def HexToFloat(i):
    return struct.unpack('!f', int.to_bytes(i, 0x4, 'big'))[0]


# Script Name, Script Version, And Script Creators

print('SMM1Patcher (Version 0.2)')
print('Created By MarioPossamato And System46')


if len(sys.argv) <= 1:
    File = False
if len(sys.argv) >= 2:
    File = sys.argv[1]

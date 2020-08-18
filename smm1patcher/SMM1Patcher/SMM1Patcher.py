#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# SMM1Patcher
# A Code Patcher For The Super Mario Maker Binary.
# Version 0.2
# Created by MarioPossamato

# This file is part of SMM1Patcher.

# All Modifications In This Script Are For Version 1.47 Of Super Mario Maker.
# To Apply Modifications Manually, I Recommend Using HxD Hex Editor <https://mh-nexus.de/downloads/HxDSetup.zip>.

# To Find These Offsets Using HxD, Use Ctrl+G (Goto), And Paste In The Offset.  Then, Copy The Data Press Ctrl+B (Paste Overrite).
# Alternatively, You Can Use HxD's Ctrl+E (Select Block), Paste In The Start And End Offsets, Then Right Click On The Selected Block, Click Fill Selection, Then Place The Data In There To Fill The Selection.

# Please Note That None Of The Modifications In This Script Will Work If Your Copy Of Block.rpx Is Not Decompressed!  Use wiiurpxtool <https://github.com/0CBH0/wiiurpxtool/releases>.

SMM1PatcherVersion = '0.2'

import sys
import struct



# Function To Convert Float To Hex
def float_to_hex(f):
    return hex(struct.unpack('<I', struct.pack('<f', f))[0])[2:]

# Function To Convert Hex To Float
def hex_to_float(i):
    return struct.unpack('!f', int.to_bytes(i, 0x4, 'big'))[0]

# Create Dictionaries

# Useful Known Variables, Found By Mario Possamato

"MarioRelated"
dict_0 = {'start_offset':0xCC0E0, 'end_offset':0xCC0E4, 'size':0x4, 'default':0x3F800000, 'description':'Carry displacement, horizontal', 'affected_modes':['M1','M3','MW']}
dict_1 = {'start_offset':0xCC16C, 'end_offset':0xCC170, 'size':0x4, 'default':0x40000000, 'description':'Carry displacement vertical, small Mario', 'affected_modes':['M1','M3','MW']}
dict_2 = {'start_offset':0xCE7BC, 'end_offset':0xCE7C0, 'size':0x4, 'default':0x40400000, 'description':'Carry displacement vertical, large Mario', 'affected_modes':['M1','M3','MW']}
dict_3 = {'start_offset':0xCE29C, 'end_offset':0xCE2A0, 'size':0x4, 'default':0x3F800000, 'description':'Run speed, right', 'affected_modes':['M1','M3','MW','WU']}
dict_4 = {'start_offset':0xCE2B0, 'end_offset':0xCE2B4, 'size':0x4, 'default':0x40400000, 'description':'Run speed, right and left', 'affected_modes':['M1','M3','MW','WU']}
dict_5 = {'start_offset':0xB1180, 'end_offset':0xB1184, 'size':0x4, 'default':0x40400000, 'description':'Throw speed while not moving', 'affected_modes':['M1','M3','MW','WU']}
dict_6 = {'start_offset':0xB1178, 'end_offset':0xB117C, 'size':0x4, 'default':0x3F800000, 'description':'Throw speed while turning around', 'affected_modes':['M1','M3','MW','WU']}
dict_7 = {'start_offset':0xB11C8, 'end_offset':0xB11CC, 'size':0x4, 'default':0x3f8CCCCD, 'description':'Throw speed while crouching, right', 'affected_modes':['M1','M3','MW','WU']}
dict_8 = {'start_offset':0xB11C4, 'end_offset':0xB11C8, 'size':0x4, 'default':0xBF8CCCCD, 'description':'Throw speed while crouching, left', 'affected_modes':['M1','M3','MW','WU']}
dict_9 = {'start_offset':0xB11CC, 'end_offset':0xB11D0, 'size':0x4, 'default':0x3E99999A, 'description':'Throw speed upwards', 'affected_modes':['M1','M3','MW','WU']}
dict_10 = {'start_offset':0xCE58C, 'end_offset':0xCE590, 'size':0x4, 'default':0x40200000, 'description':'Jump gravity', 'affected_modes':['M1','M3','MW','WU']}
dict_11 = {'start_offset':0xC4DE8, 'end_offset':0xC4DEC, 'size':0x4, 'default':0x40000000, 'description':'Bounce velocity off bumper side', 'affected_modes':['M1','M3','MW','WU']}
dict_12 = {'start_offset':0xD034C, 'end_offset':0xD0350, 'size':0x4, 'default':0x3F800000, 'description':'Cloud ride scale', 'affected_modes':['M1','M3','MW','WU']}
dict_13 = {'start_offset':0xD1260, 'end_offset':0xD1264, 'size':0x4, 'default':0xBE23D70A, 'description':'Gravity when falling offscreen after dying', 'affected_modes':['M1','M3','MW','WU']}
dict_14 = {'start_offset':0xD2574, 'end_offset':0xD2578, 'size':0x4, 'default':0x40400000, 'description':'Upward propeller velocity', 'affected_modes':['M1','M3','MW','WU']}
dict_15 = {'start_offset':0xD2548, 'end_offset':0xD254C, 'size':0x4, 'default':0xBfA00000, 'description':'Propeller gravity when floating down', 'affected_modes':['M1','M3','MW','WU']}
dict_16 = {'start_offset':0xD2598, 'end_offset':0xD259C, 'size':0x4, 'default':0xBF800000, 'description':'Propeller gravity when twirling', 'affected_modes':['M1','M3','MW','WU']}
dict_17 = {'start_offset':0xD25A8, 'end_offset':0xD25AC, 'size':0x4, 'default':0xC0C00000, 'description':'Propeller gravity when drilling', 'affected_modes':['M1','M3','MW','WU']}
dict_18 = {'start_offset':0xD2584, 'end_offset':0xD2588, 'size':0x4, 'default':0xBDCCCCCD, 'description':'Unknown propeller gravity related variable', 'affected_modes':['M1','M3','MW','WU']}
dict_19 = {'start_offset':0x19C30, 'end_offset':0x19C50, 'size':0x4, 'default':0x3F800000, 'description':'Fireball model size', 'affected_modes':['M1','M3','MW','WU']}
dict_20 = {'start_offset':0x19A98, 'end_offset':0x19A9C, 'size':0x4, 'default':0x3F800000, 'description':'Fireball speed, right', 'affected_modes':['M1','M3','MW','WU']}
dict_21 = {'start_offset':0x19A9C, 'end_offset':0x19AA0, 'size':0x4, 'default':0xBF800000, 'description':'Fireball speed, left', 'affected_modes':['M1','M3','MW','WU']}
dict_22 = {'start_offset':0x19C38, 'end_offset':0x19C3C, 'size':0x4, 'default':0x40680000, 'description':'Fireball speed, forward', 'affected_modes':['M1','M3','MW','WU']}
dict_23 = {'start_offset':0x19C3C, 'end_offset':0x19C40, 'size':0x4, 'default':0x40800000, 'description':'Upward bounce velocity of fireball', 'affected_modes':['M1','M3','MW','WU']}
dict_24 = {'start_offset':0x19C44, 'end_offset':0x19C48, 'size':0x4, 'default':0xBEE00000, 'description':'Gravity of fireball', 'affected_modes':['M1','M3','MW','WU']}
dict_25 = {'start_offset':0x19C48, 'end_offset':0x19C4C, 'size':0x4, 'default':0xC0800000, 'description':'Upward fireball velocity', 'affected_modes':['M1','M3','MW','WU']}

"CannonRelated"
dict_26 = {'start_offset':0x1A504, 'end_offset':0x1A508, 'size':0x4, 'default':0xBF800000, 'description':'Bounce velocity off cannonball', 'affected_modes':['M1','M3','MW','WU']}
dict_27 = {'start_offset':0x1A518, 'end_offset':0x1A51C, 'size':0x4, 'default':0x3F800000, 'description':'Cannonball model size and speed', 'affected_modes':['M1','M3','MW','WU']}
dict_28 = {'start_offset':0x1A4B4, 'end_offset':0x1A4B8, 'size':0x4, 'default':0x40800000, 'description':'Cannonball hitbox width', 'affected_modes':['M1','M3','MW','WU']}
dict_29 = {'start_offset':0x1A4B8, 'end_offset':0x1A4BC, 'size':0x4, 'default':0x40800000, 'description':'Cannonball hitbox height, top', 'affected_modes':['M1','M3','MW','WU']}
dict_30 = {'start_offset':0x1A4B0, 'end_offset':0x1A4B4, 'size':0x4, 'default':0x41000000, 'description':'Cannonball hitbox height, bottom', 'affected_modes':['M1','M3','MW','WU']}
dict_31 = {'start_offset':0x64AB8, 'end_offset':0x64ABC, 'size':0x4, 'default':0xC1000000, 'description':'Cannon hitbox width', 'affected_modes':['M1','M3','MW','WU']}
dict_32 = {'start_offset':0x64ABC, 'end_offset':0x64AC0, 'size':0x4, 'default':0x41800000, 'description':'Cannon hitbox height', 'affected_modes':['M1','M3','MW','WU']}
dict_33 = {'start_offset':0x648CC, 'end_offset':0x648D0, 'size':0x4, 'default':0x00000000, 'description':'Speed cannons move left/right in play mode', 'affected_modes':['M1','M3','MW','WU']}
dict_34 = {'start_offset':0x648E4, 'end_offset':0x648E8, 'size':0x4, 'default':0x80000000, 'description':'Cannonball shoot direction', 'affected_modes':['M1','M3','MW','WU']}

"BulletBlasterRelated"
dict_35 = {'start_offset':0x49828, 'end_offset':0x4982C, 'size':0x4, 'default':0x3F000000, 'description':'Upward bounce velocity of objects shot out of bullet blasters', 'affected_modes':['M1','M3','MW','WU']}
dict_37 = {'start_offset':0x49800, 'end_offset':0x49804, 'size':0x4, 'default':0x3F800000, 'description':'Enemy model and hitbox size when first shot out of a bullet blaster', 'affected_modes':['M1','M3','MW','WU']}
dict_36 = {'start_offset':0x49818, 'end_offset':0x4981C, 'size':0x4, 'default':0x41800000, 'description':'Enemy model and hitbox size when shot out of a bullet blaster', 'affected_modes':['M1','M3','MW','WU']}
dict_38 = {'start_offset':0x55E34, 'end_offset':0x55E38, 'size':0x4, 'default':0xC1800000, 'description':'Vertical displacement of objects when shot from a bullet blaster', 'affected_modes':['M1','M3','MW','WU']}
dict_39 = {'start_offset':0x55E44, 'end_offset':0x55E48, 'size':0x4, 'default':0x41000000, 'description':'Bullet blaster hitbox width, right', 'affected_modes':['M1','M3','MW','WU']}
dict_40 = {'start_offset':0x55E70, 'end_offset':0x55E74, 'size':0x4, 'default':0xC1000000, 'description':'Bullet blaster hitbox width, left', 'affected_modes':['M1','M3','MW','WU']}
dict_41 = {'start_offset':0x55E68, 'end_offset':0x55E6C, 'size':0x4, 'default':0x42000000, 'description':'Bullet blaster hitbox height', 'affected_modes':['M1','M3','MW','WU']}
dict_42 = {'start_offset':0x686C4, 'end_offset':0x686C8, 'size':0x4, 'default':0xBE400000, 'description':'Bullet blaster gravity', 'affected_modes':['M1','M3','MW','WU']}
dict_43 = {'start_offset':0x55E30, 'end_offset':0x55E34, 'size':0x4, 'default':0x3F800000, 'description':'Bullet blaster bounce velocity off of mario', 'affected_modes':['M1','M3','MW','WU']}

"WingedSolidBlockModelHitboxFormat"
ApplicableBlockTypes = {'hardblock':{'start_offset':0xB41A4, 'end_offset':0xB41CC},'iceblock':{'start_offset':0xB4FD0, 'end_offset':0xB4FF8}}
ObjectBlockFormat = {
'solid block model size':0x4,
'model placement over solid block hitbox':0x8,
'unknown 1':0x4,
'winged solid block velocity, horizontal':0xC,
'winged solid block velocity, vertical':0x10,
'unknown 2':0x14,
'solid block hitbox width right, height':0x18,
'unknown 3':0x1C,
'unknown 4':0x20,
'solid block hitbox width, left':0x24
}

# Create Function To Change Block Model And Hitbox Size
def ChangeObjectBlockSize(x, y):
    with open(sys.argv[1],'rb') as file:
        data = bytearray(file.read())
        data[x['start_offset']:x['start_offset']+0x4] = bytes.fromhex(float_to_hex(y)) # Model Size
        data[x['start_offset']+0xC:x['start_offset']+0x10] = bytes.fromhex(float_to_hex(48.0*y)) # Horizontal Velocity
        data[x['start_offset']+0x10:x['start_offset']+0x14] = bytes.fromhex(float_to_hex(16.0*y)) # Vertical Velocity"
        data[x['start_offset']+0x18:x['start_offset']+0x1C] = bytes.fromhex(float_to_hex(8.0*y)) # Hitbox Width Right, Height
        data[x['start_offset']+0x24:x['start_offset']+0x28] = bytes.fromhex(float_to_hex(-8.0*y)) # Hitbox Width Left
        with open(sys.argv[1],'wb') as file:
            file.write(data)
    
# Create Function To Write Data
def Modify(x, y):
    with open(sys.argv[1],'rb') as file:
        data = bytearray(file.read())
        data[x['start_offset']:x['end_offset']] = int.to_bytes(y)
        with open(sys.argv[1],'wb') as file:
            file.write(data)


print('SMM1Patcher (Version 0.2)')

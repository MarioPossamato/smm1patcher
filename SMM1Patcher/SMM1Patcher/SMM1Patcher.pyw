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


filename = ''
SMM1PatcherVersion = '0.2'


import sys
import struct
from PyQt5 import QtCore, QtGui, QtWidgets


dict_0 = {'StartOffset':0x48FD0, 'EndOffset':0x48FD4, 'Size':0x4, 'Default':0x3F333333, 'Description':'Model and hitbox size of large enemies when spawned in a Dokan', 'AffectedModes':['M1','M3','MW','WU']}
dict_1 = {'StartOffset':0x49078, 'EndOffset':0x4907C, 'Size':0x4, 'Default':0x3F000000, 'Description':'Model and hitbox size of large enemies when spawned in a Dokan', 'AffectedModes':['M1','M3','MW','WU']}
dict_2 = {'StartOffset':0x49034, 'EndOffset':0x49038, 'Size':0x4, 'Default':0x3F800000, 'Description':'Model and hitbox size of large enemies immediately after exiting a Dokan', 'AffectedModes':['M1','M3','MW','WU']}
dict_3 = {'StartOffset':0x49098, 'EndOffset':0x4909C, 'Size':0x4, 'Default':0x40400000, 'Description':'Velocity at which large enemies shoot out of pipes', 'AffectedModes':['M1','M3','MW','WU']}

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


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__(None)
        self.setWindowTitle('SMM1Patcher (Version 0.2)')
        self.setMinimumSize(QtCore.QSize(1621, 671))
        self.setMaximumSize(QtCore.QSize(1621, 671))

        self.Open = QtWidgets.QPushButton(self)
        self.Open.setGeometry(QtCore.QRect(10, 10, 93, 31))
        self.Open.setObjectName('Open')
        self.Open.setText('Open')
        self.Open.clicked.connect(self.HandleOpenFile)

        self.Save = QtWidgets.QPushButton(self)
        self.Save.setGeometry(QtCore.QRect(10, 630, 93, 31))
        self.Save.setObjectName('Save')
        self.Save.setText('Save')
        self.Save.clicked.connect(self.HandleSaveFileAs)

        self.FilenameLabel = QtWidgets.QLabel(self)
        self.FilenameLabel.setGeometry(QtCore.QRect(110, 15, 1061, 21))
        self.FilenameLabel.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.FilenameLabel.setObjectName('FilenameLabel')
        self.FilenameLabel.setText('No File Selected')

        self.GroupBox1 = QtWidgets.QGroupBox(self)
        self.GroupBox1.setGeometry(QtCore.QRect(9, 49, 1161, 571))
        self.GroupBox1.setTitle('')
        self.GroupBox1.setObjectName('GroupBox1')

        self.GroupBox2 = QtWidgets.QGroupBox(self)
        self.GroupBox2.setGeometry(QtCore.QRect(1180, 50, 431, 571))
        self.GroupBox2.setTitle('')
        self.GroupBox2.setObjectName('GroupBox2')

        self.BackgroundLabel = QtWidgets.QLabel(self.GroupBox1)
        self.BackgroundLabel.setGeometry(QtCore.QRect(10, 10, 1141, 511))
        self.BackgroundLabel.setStyleSheet('background-color: rgb(119, 136, 153);')
        self.BackgroundLabel.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.BackgroundLabel.setText('')
        self.BackgroundLabel.setObjectName('BackgroundLabel')

        self.DoubleSpinBox1 = QtWidgets.QDoubleSpinBox(self.GroupBox1)
        self.DoubleSpinBox1.setGeometry(QtCore.QRect(10, 531, 171, 31))
        self.DoubleSpinBox1.setDecimals(4)
        self.DoubleSpinBox1.setMaximum(8.0)
        self.DoubleSpinBox1.setProperty('value', 1.0)
        self.DoubleSpinBox1.setObjectName('DoubleSpinBox1')
        self.DoubleSpinBox1.valueChanged.connect(self.ScaleHardBlock)

        self.DoubleSpinBox2 = QtWidgets.QDoubleSpinBox(self.GroupBox1)
        self.DoubleSpinBox2.setGeometry(QtCore.QRect(510, 531, 171, 31))
        self.DoubleSpinBox2.setDecimals(4)
        self.DoubleSpinBox2.setMaximum(8.0)
        self.DoubleSpinBox2.setProperty('value', 1.0)
        self.DoubleSpinBox2.setObjectName('DoubleSpinBox2')
        self.DoubleSpinBox2.valueChanged.connect(self.ScaleIceBlock)

        self.Label1 = QtWidgets.QLabel(self.GroupBox1)
        self.Label1.setGeometry(QtCore.QRect(190, 530, 61, 31))
        self.Label1.setObjectName('Label1')
        self.Label1.setText('Hard Block')

        self.Label2 = QtWidgets.QLabel(self.GroupBox1)
        self.Label2.setGeometry(QtCore.QRect(690, 530, 51, 31))
        self.Label2.setObjectName('Label2')
        self.Label2.setText('Ice Block')

        self.Mario = QtWidgets.QLabel(self.GroupBox1)
        self.Mario.setGeometry(QtCore.QRect(20, 480, 32, 32))
        self.Mario.setText('')
        self.Mario.setPixmap(QtGui.QPixmap('SMM1PatcherData/Sprites/20151007040718!SMM-SMB-Mario.png'))
        self.Mario.setScaledContents(True)
        self.Mario.setWordWrap(False)
        self.Mario.setObjectName('Mario')

        self.SuperMario = QtWidgets.QLabel(self.GroupBox1)
        self.SuperMario.setGeometry(QtCore.QRect(60, 448, 32, 64))
        self.SuperMario.setText('')
        self.SuperMario.setPixmap(QtGui.QPixmap('SMM1PatcherData/Sprites/SMM-SMB-SuperMario.png'))
        self.SuperMario.setScaledContents(True)
        self.SuperMario.setWordWrap(False)
        self.SuperMario.setObjectName('SuperMario')

        self.HardBlock = QtWidgets.QLabel(self.GroupBox1)
        self.HardBlock.setGeometry(QtCore.QRect(110, 480, 64, 32))
        self.HardBlock.setText('')
        self.HardBlock.setPixmap(QtGui.QPixmap('SMM1PatcherData/Sprites/SMM-SMB-HardBlock-Winged.png'))
        self.HardBlock.setScaledContents(True)
        self.HardBlock.setWordWrap(False)
        self.HardBlock.setObjectName('HardBlock')

        self.IceBlock = QtWidgets.QLabel(self.GroupBox1)
        self.IceBlock.setGeometry(QtCore.QRect(630, 480, 64, 32))
        self.IceBlock.setText('')
        self.IceBlock.setPixmap(QtGui.QPixmap('SMM1PatcherData/Sprites/SMM-SMB-IceBlock-Winged.png'))
        self.IceBlock.setScaledContents(True)
        self.IceBlock.setWordWrap(False)
        self.IceBlock.setObjectName('IceBlock')

        self.Label2 = QtWidgets.QLabel(self.GroupBox2)
        self.Label2.setGeometry(QtCore.QRect(10, 10, 411, 511))
        self.Label2.setStyleSheet('background-color: rgb(119, 136, 153);')
        self.Label2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.Label2.setText('')
        self.Label2.setObjectName('Label2')
        self.Label2.raise_()

        self.DoubleSpinBox3 = QtWidgets.QDoubleSpinBox(self.GroupBox2)
        self.DoubleSpinBox3.setGeometry(QtCore.QRect(10, 530, 171, 31))
        self.DoubleSpinBox3.setDecimals(4)
        self.DoubleSpinBox3.setMaximum(6.0)
        self.DoubleSpinBox3.setProperty('value', 1.0)
        self.DoubleSpinBox3.setObjectName('DoubleSpinBox3')
        self.DoubleSpinBox3.raise_()
        self.DoubleSpinBox3.valueChanged.connect(self.ScalePipeEnemy)

        self.Label5 = QtWidgets.QLabel(self.GroupBox2)
        self.Label5.setGeometry(QtCore.QRect(190, 529, 71, 31))
        self.Label5.setObjectName('Label5')
        self.Label5.setText('Pipe Enemy')
        self.Label5.raise_()

        self.Mario = QtWidgets.QLabel(self.GroupBox2)
        self.Mario.setGeometry(QtCore.QRect(20, 480, 32, 32))
        self.Mario.setText('')
        self.Mario.setPixmap(QtGui.QPixmap('SMM1PatcherData/Sprites/20151007040718!SMM-SMB-Mario.png'))
        self.Mario.setScaledContents(True)
        self.Mario.setWordWrap(False)
        self.Mario.setObjectName('Mario')

        self.SuperMario = QtWidgets.QLabel(self.GroupBox2)
        self.SuperMario.setGeometry(QtCore.QRect(60, 448, 32, 64))
        self.SuperMario.setText('')
        self.SuperMario.setPixmap(QtGui.QPixmap('SMM1PatcherData/Sprites/SMM-SMB-SuperMario.png'))
        self.SuperMario.setScaledContents(True)
        self.SuperMario.setWordWrap(False)
        self.SuperMario.setObjectName('SuperMario')

        self.Pipe = QtWidgets.QLabel(self.GroupBox2)
        self.Pipe.setGeometry(QtCore.QRect(180, 448, 64, 64))
        self.Pipe.setText('')
        self.Pipe.setPixmap(QtGui.QPixmap('SMM1PatcherData/Sprites/SMM-SMB-PipeTop.png'))
        self.Pipe.setScaledContents(True)
        self.Pipe.setWordWrap(False)
        self.Pipe.setObjectName('Pipe')
        self.Pipe.raise_()

        self.Goomba = QtWidgets.QLabel(self.GroupBox2)
        self.Goomba.setGeometry(QtCore.QRect(180, 400, 64, 64))
        self.Goomba.setText('')
        self.Goomba.setPixmap(QtGui.QPixmap('SMM1PatcherData/Sprites/GoombaSMM.png'))
        self.Goomba.setScaledContents(True)
        self.Goomba.setWordWrap(False)
        self.Goomba.setObjectName('Goomba')
        self.Goomba.raise_()

    def __init2__(self):
        return

    def HandleOpenFile(self):
        global filename
        filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Open', '', 'Block.rpx (*.rpx)')[0]
        if filename:
            self.FilenameLabel.setText(filename)
            return True

        return

    def HandleSaveFileAs(self):
        global filename
        if filename:
            filename = QtWidgets.QFileDialog.getSaveFileName(self, 'Save As', '', 'Block.rpx (*.rpx)')[0]
            with open(filename,'rb') as file:
                data = bytearray(file.read())

                x = ApplicableBlockTypes['HardBlock']
                data[x['StartOffset']:x['StartOffset']+0x4] = bytes.fromhex(self.FloatToHex(float(self.DoubleSpinBox1.text())))
                data[x['StartOffset']+0xC:x['StartOffset']+0x10] = bytes.fromhex(self.FloatToHex(48.0*float(self.DoubleSpinBox1.text())))
                data[x['StartOffset']+0x10:x['StartOffset']+0x14] = bytes.fromhex(self.FloatToHex(16.0*float(self.DoubleSpinBox1.text())))
                data[x['StartOffset']+0x18:x['StartOffset']+0x1C] = bytes.fromhex(self.FloatToHex(8.0*float(self.DoubleSpinBox1.text())))
                data[x['StartOffset']+0x24:x['StartOffset']+0x28] = bytes.fromhex(self.FloatToHex(-8.0*float(self.DoubleSpinBox1.text())))

                x = ApplicableBlockTypes['IceBlock']
                data[x['StartOffset']:x['StartOffset']+0x4] = bytes.fromhex(self.FloatToHex(float(self.DoubleSpinBox2.text())))
                data[x['StartOffset']+0xC:x['StartOffset']+0x10] = bytes.fromhex(self.FloatToHex(48.0*float(self.DoubleSpinBox2.text())))
                data[x['StartOffset']+0x10:x['StartOffset']+0x14] = bytes.fromhex(self.FloatToHex(16.0*float(self.DoubleSpinBox2.text())))
                data[x['StartOffset']+0x18:x['StartOffset']+0x1C] = bytes.fromhex(self.FloatToHex(8.0*float(self.DoubleSpinBox2.text())))
                data[x['StartOffset']+0x24:x['StartOffset']+0x28] = bytes.fromhex(self.FloatToHex(-8.0*float(self.DoubleSpinBox2.text())))

                data[dict_0['StartOffset']:dict_0['StartOffset']+0x4] = bytes.fromhex(self.FloatToHex(0.7*float(self.DoubleSpinBox3.text())))
                data[dict_1['StartOffset']:dict_1['StartOffset']+0x4] = bytes.fromhex(self.FloatToHex(0.5*float(self.DoubleSpinBox3.text())))
                data[dict_2['StartOffset']:dict_2['StartOffset']+0x4] = bytes.fromhex(self.FloatToHex(1.0*float(self.DoubleSpinBox3.text())))

                with open(filename,'wb') as file:
                    file.write(data)

                return True
        else:
            return

    def ScaleHardBlock(self):
        self.HardBlock.setGeometry(QtCore.QRect(110, 480-32*(float(self.DoubleSpinBox1.text())-1), 64*float(self.DoubleSpinBox1.text()), 32*float(self.DoubleSpinBox1.text())))

    def ScaleIceBlock(self):
        self.IceBlock.setGeometry(QtCore.QRect(630, 480-32*(float(self.DoubleSpinBox2.text())-1), 64*float(self.DoubleSpinBox2.text()), 32*float(self.DoubleSpinBox2.text())))

    def ScalePipeEnemy(self):
        self.Goomba.setGeometry(QtCore.QRect(180-32*(float(self.DoubleSpinBox3.text())-1), 400-64*(float(self.DoubleSpinBox3.text())-1), 64*float(self.DoubleSpinBox3.text()), 64*float(self.DoubleSpinBox3.text())))

    def FloatToHex(self, f):
        return hex(struct.unpack('<I', struct.pack('<f', f))[0])[2:]

    def HexToFloat(self, i):
        return struct.unpack('!f', int.to_bytes(i, 0x4, 'big'))[0]


def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationDisplayName('Created By MarioPossamato And System46')

    mainWindow = MainWindow()
    mainWindow.__init2__()
    mainWindow.show()
    app.exec_()
    sys.exit()


if __name__ == '__main__': main()

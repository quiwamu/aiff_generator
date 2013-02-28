#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from struct import pack
from random import randint
from math import sin,cos,pi

# h:整数2bytes, l:long整数4bytes, c:1byte文字
# >はビッグエンディアンの意

frames = 1000000
ssnd_size = 2 * 2 * frames # 16bit(2bytes)*2ch(stereo)*frames
comment_size = 10 # bytes
file_size = ssnd_size + comment_size + 54 # FORMヘッダ12, COMMチャンク26, SSNDヘッダ16

# FORMチャンク
outfile = open(sys.argv[1], 'w')
odata = pack("cccc","F","O","R","M")
odata += pack(">l",file_size - 8) # FORMチャンクサイズ
odata += pack("4c","A","I","F","F")

# COMMチャンク
odata += pack("4c","C","O","M","M")
odata += pack(">l",18) # COMMチャックのバイト長(=18)
odata += pack(">h",2) # channel数(=2:ステレオ)
odata += pack(">l",frames) # frame数
odata += pack(">h",16) # bits/samples 1..32
# sample rate (extended 80-bit floating-point format)
# 10bytesの型がないので、4+4+2でやってる
# 実際はextend floatで44100
odata += pack(">l",0x400EAC44)
odata += pack(">l",0x00000000)
odata += pack(">h",0x0000) 
# ここまでsample rate

# SSNDチャンク
odata += pack("cccc","S","S","N","D")
odata += pack(">l", ssnd_size + comment_size + 8) # SSNDチャンクサイズ
odata += pack(">l", comment_size) # コメントサイズ
odata += pack(">l", 0) # block size (=0)
odata += pack("10c", "s","u","c","k","m","y","d","i","c","k") # comment
for f in range(frames):
	t = f / 44100.0 # pythonは通常の割り算では整数解になってしまうので、小数点以下をつけておく
	#hz = 4000 * sin(t/100.0*2*pi) + 3000 # 可聴域20..16000
	#hz = randint(1,2)+160
	hz = 160
	amp = 10000 * sin(t/0.8 * 2 * pi) + 10000
	#amp = 3000
	subsubval = 5000 * sin(t * hz*3 * 2 * pi)+5000  # 0 < val < 65535 
	subval = amp/2.0 * sin(t * hz*2 * 2 * pi) + amp/2.0 # 0 < val < 65535 
	val = subval + subsubval + amp/2.0 * sin(t * hz * 2 * pi) + amp/2.0 # 0 < val < 65535 
	odata += pack(">H", int(val)) 
	odata += pack(">H", int(val))
outfile.write(odata)
outfile.close()

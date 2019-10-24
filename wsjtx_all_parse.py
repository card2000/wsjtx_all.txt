# -*- coding: utf-8 -*-
import re
import ctypes
import os
fname=os.path.normpath("C:\WSJT\wsjtx\ALL.TXT")
DXCALL='VP6R'
qso_list = {}
count=0

def qrg_to_band(qrg):
	band = None
	freq = int(qrg.replace('.',''))
	if ((freq >= 1800) and (freq <= 2000)):
		band = 160
	elif ((freq >= 3500) and (freq <= 4000)):
		band = 80
	elif ((freq >= 5000) and (freq <= 5500)):
		band = 60
	elif ((freq >= 7000) and (freq <= 7300)):
		band = 40
	elif ((freq >= 10100) and (freq <= 10150)):
		band = 30
	elif ((freq >= 14000) and (freq <= 14350)):
		band = 20
	elif ((freq >= 18068) and (freq <= 18268)):
		band = 17
	elif ((freq >= 21000) and (freq <= 21450)):
		band = 15
	elif ((freq >= 24890) and (freq <= 24990)):
		band = 12
	elif ((freq >= 28000) and (freq <= 29700)):
		band = 10
	elif ((freq >= 50000) and (freq <= 54000)):
		band = 6
	elif ((freq >= 70000) and (freq <= 71000)):
		band = 4
	elif ((freq >= 144000) and (freq <= 148000)):
		band = 2
	else:
		raise KeyError
	return str(band)+ 'm'
    	
def swap_date( word ):
	l = word[0].split("_")
	return '20'+l[0] , l[1]
	

def doadifline( call , param ):
	day, utc = swap_date(param)
	band = qrg_to_band(param[1])
	adif= '<call:' + str(len(call)) + '>' + call + ' <mode:' + str(len(param[3])) + '>' + param[3] + ' <rst_sent:3>' +  qso_list[call] + ' <rst_rcvd:3>+00 <qso_date:8>' + day  + ' <time_on:6>' + utc + ' <qso_date_off:8>' + day + ' <time_off:6>' + utc + ' <band:' + str(len(band)) +'>' + band + '<freq:' + str(len(param[1] )+3) + '>' + param[1] + param[6] +' <station_callsign:' + str(len(DXCALL)) + '>' + DXCALL + ' <eor>'
	print adif
	
with open(fname, "r") as f:
	currentdone=''
	for line in f:
		if not ' Transmitting ' in line:
			oldline=line
		if not ' ~' in line:
			currentdone=''
			if ' Rx' in line and DXCALL in line and 'RR73;' in line:
				rxwords=line.split()
				#if rxwords[8] in "RR73;" and rxwords[10] in DXCALL:
				currentdone = rxwords[9]
				qso_list[ rxwords[9] ] = rxwords[11]
				
				if currentdone in qso_list:
					doadifline( currentdone, rxwords )
					count+=1
			elif ' Rx' in line and DXCALL in line and 'RR73' in line:
				rxwords=line.split()
				#print rxwords 
				if rxwords[7] in qso_list:
					doadifline( rxwords[7], rxwords )
					count+=1
			elif ' Rx' in line and DXCALL in line and not 'RR73' in line:
				# only raport
				rxraports=line.split()
				if rxraports[8]==DXCALL:
					qso_list[rxwords[7] ] = rxwords[9]
					#print rxraports
			elif ' Tx' in line and DXCALL in line:
				txwords=line.split()
				#print txwords  
print count

f.close()

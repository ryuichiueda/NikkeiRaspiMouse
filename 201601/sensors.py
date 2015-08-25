#!/usr/bin/python
# vim:fileencoding=utf-8
import time, fcntl, glob, sys, threading

class Sensor:
	def __init__(self):
		with open("/tmp/lock","w") as lock:
			lock.write("")

	def _readline(self,filename):
		with open("/tmp/lock","r") as lock:
			fcntl.flock(lock,fcntl.LOCK_EX)
			with open(filename,"r") as f:
				line = f.readline()
			fcntl.flock(lock,fcntl.LOCK_UN)

			return line.rstrip()
#		with open(filename,"r") as f:
#			fcntl.flock(f,fcntl.LOCK_EX)
#			line = f.readline()
#			fcntl.flock(f,fcntl.LOCK_UN)
#			return line.rstrip()
			
class Buttons(Sensor):
	def __init__(self):
		Sensor.__init__(self)
		self.__files = sorted(glob.glob("/dev/rtswitch[0-2]"))
		self.__pushed = [False,False,False]
		self.__values = ["1","1","1"]

	def __check_pushed(self,num):
		if self.__values[num] == "0": #now pushing
			return False

		if self.__pushed[num]:
			self.__pushed[num] = False 
			return True
		else:
			return False

	#デバイスファイルからのデータ読み込み
	def update(self):
		#現在の値の取得
		self.__values = map(self._readline,self.__files)
		#押されたら*_pushedが呼ばれるまでTrueを保持するリスト
		self.__pushed = [ v == "0" or past for (v,past) in zip(self.__values,self.__pushed)]

	#公開するボタンの状態取得メソッド
	def front_pushed(self):    return self.__check_pushed(0)
	def center_pushed(self):   return self.__check_pushed(1)
	def back_pushed(self):     return self.__check_pushed(2)
	def front_pushed_now(self):    return self.__values[0] == "0"
	def center_pushed_now(self):   return self.__values[1] == "0"
	def back_pushed_now(self):     return self.__values[2] == "0"

	def all_pushed_now(self):
		return self.__values == ["0","0","0"]

	def get_values(self):	return self.__values
	def get_pushed(self):	return self.__pushed

if __name__ == '__main__':
	num = 100
	btns = []
	for i in range(num):
		btns.append(Buttons())

	th = []
	for i in range(num):
		th.append(threading.Thread(target=btns[i].update))

	for i in range(num):
		th[i].start()

	for i in range(num):
		th[i].join()
	
		print btns[i].get_values()
		print btns[i].get_pushed()

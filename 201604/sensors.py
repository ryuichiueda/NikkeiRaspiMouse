#!/usr/bin/python
# vim:fileencoding=utf-8
import time, fcntl, glob, sys, threading

# 参考: http://blog.livedoor.jp/tmako123-programming/archives/41536599.html
#       http://qiita.com/wwacky/items/98d8be2844fa1b778323

class Sensor:
	def __init__(self):
		pass

	def _readline(self,f):
            if isinstance(f,basestring) :
                return self._readline_filename(f)
            else:
                return self._readline_fileobj(f)

	def _readline_filename(self,filename):
		with open(filename,"r") as f:
			fcntl.flock(f,fcntl.LOCK_EX)
			line = f.readline()
			fcntl.flock(f,fcntl.LOCK_UN)
			return line.rstrip()

	def _readline_fileobj(self,f):
		fcntl.flock(f,fcntl.LOCK_EX)
		line = f.readline()
		fcntl.flock(f,fcntl.LOCK_UN)
		return line.rstrip()


class Yaw(Sensor):
	def __init__(self):
		Sensor.__init__(self)
                self.__value = 0.0
                self.__init_value = 0.0
                self.__time = 0.0

        def on(self):
		self.__run = True
                threading.Thread(target=self.__update).start()

        def off(self):
		self.__run = False

	def __update(self):
                with open("/dev/ttyACM0","r") as f:
		    self.__init_value = float(self._readline(f))
                    time.sleep(0.3)
		    self.__init_value = float(self._readline(f))
                    while self.__run:
                        time.sleep(0.03)
		        self.__value = float(self._readline(f))
		        self.__time = time.time()

	def get_value(self):
            v = self.__value - self.__init_value
            if v > 180.0:   v -= 360.0
            elif v < -180.0:    v += 360.0
            return v

	def get_time(self): return self.__time
			
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
            time.sleep(0.3)
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

import picamera,os,cv2,io
import numpy as np
class PiCamera(Sensor):
	def __init__(self):
		Sensor.__init__(self)
		self.camera = picamera.PiCamera()
		self.camera.hflip = True
		self.camera.vflip = True

	def capture(self,filename,resolution=(2592/4,1944/4)):
                self.camera.resolution = resolution
		self.camera.capture(filename + "_tmp.jpg")
		os.rename(filename + "_tmp.jpg",filename)

	def face_pos_on_img(self):
                #画像の取得
                stream = io.BytesIO()
                width,height = 600,400
                self.camera.resolution = (width,height)
                self.camera.capture(stream,'jpeg')
                data = np.fromstring(stream.getvalue(), np.uint8)
                img = cv2.imdecode(data,1)

                #OpenCVを使った顔検出
                gimg = cv2.cvtColor(img,cv2.cv.CV_BGR2GRAY)
                classifier = "/usr/share/opencv/haarcascades/haarcascade_frontalface_default.xml"
                cascade = cv2.CascadeClassifier(classifier)
                face = cascade.detectMultiScale(gimg,1.1,1,cv2.CASCADE_FIND_BIGGEST_OBJECT)

                #出力
                if len(face) == 0: return None
                r = face[0]
                cv2.rectangle(img,tuple(r[0:2]),tuple(r[0:2]+r[2:4]),(0,255,255),4)
                cv2.imwrite("/var/www/tmp.image.jpg",img)
                os.rename("/var/www/tmp.image.jpg","/var/www/image.jpg")
                h = r[0] + r[2]/2 - width/2
		#画角が53.5度なので、(幅のピクセル数/53.5)[pixel]が1度に相当
		return -h/(width/53.5)  

if __name__ == '__main__':
    yaw = Yaw()
    while True:
        v,t = yaw.get_value(),yaw.get_time()
        print v
    

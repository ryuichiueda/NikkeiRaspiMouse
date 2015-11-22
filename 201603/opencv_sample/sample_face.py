#!/usr/bin/python
#vim:fileencoding=utf-8
#参考: 「python+OpenCVで顔認識をやってみる」
#	http://qiita.com/wwacky/items/98d8be2844fa1b778323

import cv2, sys

#画像を読み込む
img = cv2.imread("/home/pi/fool.jpg")
#処理用に変換
gimg = cv2.cvtColor(img,cv2.cv.CV_BGR2GRAY)

#顔識別用のデータをロード
classifier = "/usr/share/opencv/haarcascades/haarcascade_frontalface_default.xml"
cascade = cv2.CascadeClassifier(classifier)
#認識
face = cascade.detectMultiScale(gimg,1.1,1,cv2.CASCADE_FIND_BIGGEST_OBJECT)

if len(face) == 0: sys.exit(1) #検出失敗したら出る

#検出結果
r = face[0] 
print "左上の座標:",r[0:2]
print "横幅,縦幅:",r[2:4]

#顔の部分に枠を描いてファイルに書き出す
cv2.rectangle(img,tuple(r[0:2]),tuple(r[0:2]+r[2:4]),(0,255,255),4)
cv2.imwrite("out.jpg",img)


#!/usr/bin/python
# vim:fileencoding=utf-8

class Hoge:
	def __init__(self,v):
		self.value = v

	def out(self):
		print self.value

if __name__ == '__main__':
	a = Hoge("あああ") #インスタンスaの作成
	b = Hoge(1) #インスタンスbの作成

	b.out() #bのoutメソッドを実行
	a.out() #aのoutメソッドを実行

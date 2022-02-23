
import numpy as np
import os
import shutil
import sys
import unittest

sys.path.append('.')
import jpeglib

class TestFlags(unittest.TestCase):
	def setUp(self):
		try: shutil.rmtree("tmp")
		except: pass
		finally: os.mkdir("tmp")
	def tearDown(self):
		shutil.rmtree("tmp")
	
	def test_fancy_upsampling(self):
		
		jpeglib.version.set('9e')
		with jpeglib.JPEG("examples/IMG_0791.jpeg") as im:
			x_def = im.read_spatial(flags = [])
			x_fu = im.read_spatial(flags = ['+DO_FANCY_UPSAMPLING'])
			x_ss = im.read_spatial(flags = ['-DO_FANCY_UPSAMPLING'])
		
		self.assertTrue((x_def == x_fu).all())
		self.assertTrue((x_def != x_ss).all())



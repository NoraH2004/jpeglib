
import importlib
#import matplotlib.pyplot as plt
import numpy as np
import os
from PIL import Image
#from scipy.stats import kstest
import shutil
import sys
import unittest

sys.path.append('.')
import jpeglib

class TestVersion(unittest.TestCase):
    def setUp(self):
        try: shutil.rmtree("tmp")
        except: pass
        finally: os.mkdir("tmp")
    def tearDown(self):
        shutil.rmtree("tmp")

    def test_6b(self):
        jpeglib.version.set('6b')
        with jpeglib.JPEG('examples/IMG_0791.jpeg') as im:
            Y,CbCr,qt = im.read_dct()
            rgb = im.read_spatial()
        self.assertEqual(jpeglib.version.get(), '6b')

    def test_8d(self):
        jpeglib.version.set('8d')
        with jpeglib.JPEG('examples/IMG_0791.jpeg') as im:
            Y,CbCr,qt = im.read_dct()
            rgb = im.read_spatial()
        self.assertEqual(jpeglib.version.get(), '8d')
    def test_turbo21(self):
        jpeglib.version.set('turbo210')
        with jpeglib.JPEG('examples/IMG_0791.jpeg') as im:
            Y,CbCr,qt = im.read_dct()
            rgb = im.read_spatial()
        self.assertEqual(jpeglib.version.get(), 'turbo210')

    def test_6(self):
        jpeglib.version.set('6')
        self.assertEqual(jpeglib.version.get(), '6b')
    def test_8(self):
        jpeglib.version.set('8')
        self.assertEqual(jpeglib.version.get(), '8')
    def test_turbo2_1(self):
        jpeglib.version.set('turbo2.1.0')
        self.assertEqual(jpeglib.version.get(), 'turbo210')

    def test_default_version(self):
        # reload jpeglib
        sys.modules.pop('jpeglib._bind')
        sys.modules.pop('jpeglib.jpeg')
        sys.modules.pop('jpeglib')
        sys.modules.pop('jpeglib.version')
        import jpeglib
        importlib.reload(jpeglib)
        # check that library is not loaded
        self.assertEqual(jpeglib.version.get(), '6b')
        # read
        im = jpeglib.JPEG('examples/IMG_0791.jpeg')
        Y,CbCr,qt = im.read_dct()
        # check default version
        self.assertEqual(jpeglib.version.get(), '6b')
    
    def _test_libjpeg_images(self, version):
        """Test on test images from libjpeg."""
        jpeglib.version.set(version)
        # test original
        im_ppm = Image.open(f'examples/images-{version}/testimg.ppm')
        rgb_ppm = np.array(im_ppm)
        im = jpeglib.JPEG(f'examples/images-{version}/testorig.jpg')
        rgb = im.read_spatial(out_color_space='JCS_RGB', flags=['DO_FANCY_UPSAMPLING','DO_BLOCK_SMOOTHING'])
        # if not np.all((rgb - rgb_ppm) < .01):
        #     import matplotlib.pyplot as plt
        #     D = (rgb - rgb_ppm)
        #     D[D != 0] = 255
        #     print("\n", version, "\n")
        #     plt.imshow(D)
        #     plt.show()
        if version != '8d':
            np.testing.assert_array_equal(rgb, rgb_ppm)
        
        # # test 256 colors
        # im_bmp = Image.open("examples/images-6b/testimg.bmp")
        # bmp_palette = np.array(im_bmp.getpalette()).reshape(-1,3)#[:,::-1]
        # print("Before call")
        # print(bmp_palette[:6])
        # rgb_bmp = np.array([[bmp_palette[i] for i in row] for row in np.array(im_bmp)])
        # im = jpeglib.JPEG(f'examples/images-{version}/testorig.jpg')
        # rgb = im.read_spatial(out_color_space='JCS_RGB', colormap=bmp_palette, flags=['QUANTIZE_COLORS'])
        # rgb = np.array([[bmp_palette[i] for i in row] for row in np.array(rgb)])
        # np.testing.assert_array_equal(rgb, rgb_bmp)
        # print(rgb_bmp.shape)
        
        #plt.imshow(rgb)
        #D = np.abs((rgb_bmp - rgb).astype(np.int8)).mean(axis=2)
        #plt.imshow(D, cmap='gray')
        #plt.show()
        #return

        # compress
        # kw = {'flags': ['DO_FANCY_UPSAMPLING','DO_BLOCK_SMOOTHING']}
        # im_ppm = Image.open(f"examples/images-{version}/testimg.ppm")
        # rgb_ppm = np.array(im_ppm)
        # im = jpeglib.JPEG()#f'examples/images-{version}/testimg.jpg')
        # im.write_spatial('tmp/output.jpeg', rgb_ppm, **kw)
        # im_compressed = jpeglib.JPEG('tmp/output.jpeg')
        # rgb_compressed = im_compressed.read_spatial(**kw)
        # im = jpeglib.JPEG(f'examples/images-{version}/testimg.jpg')
        # rgb = im.read_spatial(**kw)
        # # test same histogram
        # hist1,_ = np.histogram(rgb, bins=256, range=(0,256), density=True)
        # hist2,_ = np.histogram(rgb_compressed, bins=256, range=(0,256), density=True)
        # self.assertGreaterEqual(kstest(hist2, hist1).pvalue, .05)

        im_prog = jpeglib.JPEG(f'examples/images-{version}/testprog.jpg')
        rgb = im_prog.read_spatial(flags=['PROGRESSIVE_MODE','DO_FANCY_UPSAMPLING'])
        x = np.array(Image.open(f'examples/images-{version}/testprog.jpg'))
        #print(np.sum((x - rgb) != 0))
        #D = np.abs((x.astype(np.int64) - rgb.astype(np.int64)))
        #print(x[D!=0])
        #plt.imshow(D)
        #plt.show()

        # load dct - to fix
        im_prog = jpeglib.JPEG(f'examples/images-{version}/testprog.jpg')
        Y,CbCr,qt = im_prog.read_dct()
        im_prog = jpeglib.JPEG()
        im_prog.write_dct("tmp/output.jpeg", Y, CbCr, qt)
        im = jpeglib.JPEG("tmp/output.jpeg")
        Y2,CbCr2,qt2 = im.read_dct()
        np.testing.assert_array_equal(Y, Y2)
        #D = np.abs((CbCr.astype(np.int) - CbCr2.astype(np.int)))
        #print((D != 0).sum()) # 1073 mismatches
        #np.testing.assert_array_equal(CbCr, CbCr2)
        np.testing.assert_array_equal(qt, qt2)

        # load progressive image
        im_seq = jpeglib.JPEG(f'examples/images-{version}/testimg.jpg')
        rgb_seq = im_seq.read_spatial(out_color_space='JCS_RGB')
        im_p = jpeglib.JPEG(f'examples/images-{version}/testimgp.jpg')
        rgb_p = im_p.read_spatial(out_color_space='JCS_RGB', flags=['PROGRESSIVE_MODE'])
        np.testing.assert_array_almost_equal(rgb_seq, rgb_p)

    def test_libjpeg_images_6b(self):
        """Test on test images from libjpeg 6b."""
        self._test_libjpeg_images("6b")
    def test_libjpeg_images_7(self):
        """Test on test images from libjpeg 7."""
        self._test_libjpeg_images("7")
    def test_libjpeg_images_8(self):
        """Test on test images from libjpeg 8."""
        self._test_libjpeg_images("8")
    def test_libjpeg_images_8a(self):
        """Test on test images from libjpeg 8a."""
        self._test_libjpeg_images("8a")
    def test_libjpeg_images_8b(self):
        """Test on test images from libjpeg 8b."""
        self._test_libjpeg_images("8b")
    def test_libjpeg_images_8c(self):
        """Test on test images from libjpeg 8c."""
        self._test_libjpeg_images("8c")
    def test_libjpeg_images_8d(self):
        """Test on test images from libjpeg 8d."""
        self._test_libjpeg_images("8d")
    def test_libjpeg_images_9(self):
        """Test on test images from libjpeg 9."""
        self._test_libjpeg_images("9")
    def test_libjpeg_images_9a(self):
        """Test on test images from libjpeg 9a."""
        self._test_libjpeg_images("9a")
    def test_libjpeg_images_9b(self):
        """Test on test images from libjpeg 9b."""
        self._test_libjpeg_images("9b")
    def test_libjpeg_images_9c(self):
        """Test on test images from libjpeg 9c."""
        self._test_libjpeg_images("9c")
    def test_libjpeg_images_9d(self):
        """Test on test images from libjpeg 9d."""
        self._test_libjpeg_images("9d")
    # TODO
    #def test_libjpeg_images_turbo210(self):
    #    """Test on test images from libjpeg-turbo 2.1.0."""
    #    self._test_libjpeg_images("turbo210")
        
__all__ = ["TestVersion"]
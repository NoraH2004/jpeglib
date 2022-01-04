[![PyPI version](https://badge.fury.io/py/jpeglib.svg)](https://pypi.org/project/jpeglib/)
[![Documentation Status](https://readthedocs.org/projects/jpeglib/badge/?version=latest)](https://jpeglib.readthedocs.io/)
[![GitHub](https://img.shields.io/github/stars/martinbenes1996/jpeglib.svg)](https://GitHub.com/martinbenes1996/jpeglib)
[![PyPi license](https://badgen.net/pypi/license/pip/)](https://pypi.com/project/jpeglib/)
![Unittests](https://github.com/martinbenes1996/jpeglib/actions/workflows/unittests_on_commit.yml/badge.svg)

# jpeglib

> :warning: This is *versions* branch, containing all the libjpeg versions. The main branch only contains 6b, 8d and 9d.

Python envelope for the popular C library libjpeg for handling JPEG files.

*libjpeg* offers full control over compression and decompression and exposes DCT coefficients and quantization tables.

## Installation

Install the package with *all the libjpeg versions inside*, type

```bash
pip uninstall jpeglib
pip install -U --no-cache-dir git+https://www.github.com/martinbenes1996/jpeglib.git@versions
```

> :warning: This branch takes longer to install, as there are all the libjpeg versions to build.

The latest version of the package from pypi can be installed with

```bash
pip install jpeglib
```


## Usage

Import the library in Python 3

```python
import jpeglib
```

To install the dev version with *all the libjpeg versions inside*, type

```bash
pip uninstall jpeglib
pip install -U --no-cache-dir git+https://www.github.com/martinbenes1996/jpeglib.git@versions
```

> :warning: Branch *versions* is dev so it is less stable and takes longer to install than the package.

### DCT

Get *discrete cosine transform* (DCT) coefficients and quantization matrices as numpy array


```python
im = jpeglib.JPEG("input.jpeg") # load metadata
Y,CbCr,qt = im.read_dct() # load data
```

You get luminance DCT, chrominance DCT and quantization tables.

Write the DCT coefficients back to a file with

```python
im.write_dct("output.jpeg", Y, CbCr) # write data
```

You can also write the read-write sequence using `with` statement

```python
with jpeglib.JPEG("input.jpeg") as im:
  Y,CbCr,qt = im.read_dct()
  # modify the DCT coefficients
  im.write_dct("output.jpeg", Y, CbCr)
```

### Pixel data

Decompress the `input.jpeg` into spatial representation in numpy array with

```python
im = jpeglib.JPEG("input.jpeg")
rgb = im.read_spatial()
```

You can specify parameters such as output color space, DCT method, dithering, etc.

Write spatial representation in numpy arrray back to file with

```python
im.write_spatial("output.jpeg", spatial)
```

Here you can specify input color space, DCT method, sampling factor, output quality, smoothing factor etc.

You can find all the details in the [documentation](https://jpeglib.readthedocs.io/).

### libjpeg version

It is possible to choose, which version of libjpeg should be used.

```python
jpeglib.version.set('6b')
```

Branch *versions* supports all the versions of libjpeg from *6b* (*6b*,*7*,*8*,*8a*,*8b*,*8c*,*8d*,*9*,*9a*,*9b*,*9c*,*9d*).
Their source codes is baked inside the package and thus distributed with it, avoiding external dependency.

Get currently used libjpeg version by

```python
version = jpeglib.version.get()
```


## Credits

Developed by [Martin Benes](https://github.com/martinbenes1996).
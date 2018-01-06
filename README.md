# code_nova
Final Year Project

# Note
Please run the website under CSVPN environment. 

# Requirements:
- Django
  This project is using 1.X version, do not install 2.X version
  The latest 1.X version is 1.11.9
  ```bash
  pip install Django==1.11.9
  ```

- NumPy+mkl
  For windows: https://pypi.python.org/pypi/numpy
  Download package according to python version, install with command
  Please check your python version before install
  ```bash
  python -v
  ```

  e.g. For python 3.5.x, choose cp35
  For 32 bit python version, choose win32; 64 bit python version, choose amd64
  ```python
  pip install numpyxxxxxxxxxxx.whl
  ```

- SciPy (Require NumPy+mkl first)
  For windows:
  similar to NumPy, need to download and install by pip

- Node.js
  Download exe from official page
  https://nodejs.org/zh-cn/
  (Prefer LTS version)

- CKEditor (Require Node.js first)
  ```bash
  npm install --save @ckeditor/ckeditor5-build-classic
  ```

- Django CKEditor (Require CKEditor first)
  ```bash
  pip install django-ckeditor
  ```

- Microsoft Visual C++ Build Tools
  http://landinghub.visualstudio.com/visual-cpp-build-tools

- Django Channels (Require Microsoft Visual C++ Build Tools first)
  ```
  pip install -U channels
  ```

- Django Ace editor
  ```
  pip install django_ace
  ```

- win32api
  ```
  pip install pypiwin32
  ```

- asgi_redis
  ```
  pip install asgi_redis
  ```

- ast2json
  ```
  pip install ast2json
  ```

- Pillow
  ```
  pip install Pillow
  ```

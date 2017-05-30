# cYa

Facial recognition using OpenCV and GUI with face following eye using wxPython.

### Installation guide

The guide assumes working on Windows operating system. 

1. First install [Python2.7](<https://www.python.org/downloads/>). PIP now comes with it.
2. Add C:\Python27;C:\Python27\Scripts; to your PATH enviroment variable.
```bat 
PATH=%PATH%;C:\Python27;C:\Python27\Scripts;
```
3. Install numpy. Download the wheel from [here](<http://www.lfd.uci.edu/~gohlke/pythonlibs/#numpy>).
```bat 
pip uninstall numpy-1.11.3+mkl-cp27-cp27m-win_amd64.whl
pip install numpy-1.11.3+mkl-cp27-cp27m-win_amd64.whl
```
4. Install opencv. Download the wheel from [here](<http://www.lfd.uci.edu/~gohlke/pythonlibs/#opencv>).
```bat 
pip install opencv_python-2.4.13.2-cp27-cp27m-win_amd64.whl 
```

### Running the app

To run cYa either double click run.bat file, or type the command by yourself.
```bat 
python wxPython.py haarcascade_frontalface_default.xml
```
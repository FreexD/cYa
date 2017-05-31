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
5. Install wxPython for project's GUI. Download the installation file [here](<https://www.wxpython.org/download.php>) and follow the instructions.

### Running the app

To run cYa either double click run.bat file, or type the command by yourself from src catalogue.
```bat 
python cYa.py haarcascade_frontalface_default.xml haarcascade_smile.xml
```

### How does it work?

cYa uses wxPython for displaying GUI. On wxApp initialization it fires up a new thread used for face and smile detection using openCv together with haarcascade_frontalface_default.xml and haarcascade_smile.xml. On face found, the face detection thread posts and event to GUI thread with face position and information if it is smiling. GUI receives the event and redraws it's Panel on whitch there are eyes and mouth, so that the eyes are looking in the position you are in at the moment, and face smiles if you're smiling.

### Examples

![](https://github.com/FreexD/cYa/blob/master/examples/example.gif)
![](https://github.com/FreexD/cYa/blob/master/examples/example_jim_carrey.gif)




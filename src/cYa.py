#!/usr/bin/env python
import wx
import threading

import cv2
import sys
from cv2 import *
import math
import signal
import sys
def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

# communication event - on face found
myEVT_FOUNDFACE = wx.NewEventType()
EVT_FOUNDFACE = wx.PyEventBinder(myEVT_FOUNDFACE, 1)
class FoundFaceEvent(wx.PyCommandEvent):
    """Event to signal that a face was found on x and y coordinates"""
    def __init__(self, etype, eid, xvalue=None, yvalue=None, hasSmile=False):
        """Creates the event object"""
        wx.PyCommandEvent.__init__(self, etype, eid)
        self._xvalue = xvalue
        self._yvalue = yvalue
        self._hasSmile = hasSmile

    def GetValue(self):
        """Returns the value from the event.
        @return: the value of this event
        """
        return self._xvalue, self._yvalue, self._hasSmile
		
class FaceFindingThread(threading.Thread):
    def __init__(self, parent):
        """
        @param parent: The gui object that should recieve the coordinates
        """
        threading.Thread.__init__(self)
        self._parent = parent

    def run(self):
        """Overrides Thread.run. Don't call this directly its called internally
        when you call Thread.start().
        """
        faceCascPath = sys.argv[1]
        smileCascPath = sys.argv[2]
		# Create the haar cascade
        faceCascade = cv2.CascadeClassifier(faceCascPath)
        smileCascade = cv2.CascadeClassifier(smileCascPath)
        cam = VideoCapture(0)   # 0 -> index of camera
        while True:
            s, image = cam.read()
			
			# get vcap property 
            cam_width = cam.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)   # float
            cam_height = cam.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT) # float
			
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            # Detect faces in the image
            faces = faceCascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(90, 90), flags = cv2.cv.CV_HAAR_SCALE_IMAGE)
			# Draw a rectangle around the faces
            for (x, y, w, h) in faces:
                cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
                roi_gray = gray[y+h/2:y+h, x:x+w]
                smile = smileCascade.detectMultiScale(roi_gray, scaleFactor= 1.7, minNeighbors=22, minSize=(25, 25), flags=cv2.cv.CV_HAAR_SCALE_IMAGE)
                hasSmile = False
                for (x2, y2, w2, h2) in smile:
                    hasSmile = True
                    cv2.rectangle(image, (x + x2, y+h/2+ y2), (x+x2+w2, y+h/2+y2+h2), (0, 0, 255), 2)
                    break
                evt = FoundFaceEvent(myEVT_FOUNDFACE, -1, (((2*x+w)/2.0)/640.0), (((2*y+h)/2.0)/480.0), hasSmile)
                wx.PostEvent(self._parent, evt)
                break
            cv2.imshow("Faces found", image)
            if cv2.waitKey(1)& 0xFF == 0x1B:
                break

class View(wx.Panel):
    def __init__(self, parent):
        self._xvalue=250
        self._yvalue=250
        self._hasSmile = False
        self._shouldDrawSmile = False
        self._smileCounter = 0
        self._smileBitmap = wx.Image("smile.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self._noSmileBitmap = wx.Image("no_smile.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        super(View, self).__init__(parent)
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.Bind(wx.EVT_SIZE, self.on_size)
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(EVT_FOUNDFACE, self.on_found_face)
        worker = FaceFindingThread(self)
        worker.start()
    def on_size(self, event):
        event.Skip()
        self.Refresh()
    def on_found_face(self, event):
        w, h = self.GetClientSize()
        xvalue, yvalue, hasSmile = event.GetValue()
        self._xvalue = int(xvalue * w)
        self._yvalue = int(yvalue * h)
        if self._hasSmile != hasSmile:
            self._smileCounter = 0
        elif (self._smileCounter < 4):
            self._smileCounter += 1
        self._hasSmile = hasSmile
        if (self._hasSmile != self._shouldDrawSmile) and (self._smileCounter == 4):
            self._shouldDrawSmile = self._hasSmile
        self.Refresh()
    def on_paint(self, event):
        w, h = self.GetClientSize()
        dc = wx.AutoBufferedPaintDC(self)
        dc.Clear()
        dc.SetPen(wx.Pen(wx.BLACK, 0))
        dc.SetBrush(wx.Brush(wx.Colour(255,255,255)))
        dc.DrawRectangle(0,0,w,h)
        dc.SetPen(wx.Pen(wx.BLACK, 2))
        dc.DrawCircle(w / 4, h / 4, 100)
        dc.DrawCircle( 3* w / 4, h / 4, 100)
        dc.SetBrush(wx.Brush(wx.Colour(179, 224, 255)))
        dc.DrawCircle(w / 4, h / 4, 80)
        dc.DrawCircle(3 * w / 4, h / 4, 80)
        dc.SetBrush(wx.Brush(wx.Colour(0, 0, 0)))
        distance = math.hypot((w/2) - self._xvalue, (h/2) - self._yvalue)
        faceRadius = w/2
        if(h/2 < w/2):
            faceRadius = h/2
        if distance <= faceRadius:
            drawXValue = (w/4) + int((w/2 - self._xvalue) * 50/faceRadius);
            drawYValue = (h/4) - int((h/2 - self._yvalue) * 50/faceRadius);
            dc.DrawCircle(drawXValue, drawYValue, 30)    
            drawXValue = (3*w/4) + int((w/2 - self._xvalue) * 50/faceRadius);
            drawYValue = (h/4) - int((h/2 - self._yvalue) * 50/faceRadius);
            dc.DrawCircle(drawXValue, drawYValue, 30)  
        else:
            drawYValue = int((h/4) - ((h/2 - self._yvalue) * 50/distance))
            drawXValue = int((w/4) + ((w/2) - self._xvalue)/distance*50)
            dc.DrawCircle(drawXValue, drawYValue, 30)  
            drawYValue = int((h/4) - ((h/2 - self._yvalue) * 50/distance))
            drawXValue = int((3*w/4) + ((w/2) - self._xvalue)/distance*50)
            dc.DrawCircle(drawXValue, drawYValue, 30)  
        if self._shouldDrawSmile:
            dc.DrawBitmap(self._smileBitmap,(w-500)/2,h/2 + 25,True) 
        else:
            dc.DrawBitmap(self._noSmileBitmap,(w-500)/2,h/2 + 25,True) 
            
class Frame(wx.Frame):
    def __init__(self):
        super(Frame, self).__init__(None)
        self.SetTitle('cYa :)')
        self.SetClientSize((700, 500))
        self.Center()
        self.view = View(self)

def main():
    app = wx.App(False)
    frame = Frame()
    frame.Show()
    app.MainLoop()

if __name__ == '__main__':
    main()
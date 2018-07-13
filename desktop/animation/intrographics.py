#########################################################################
# A simple module for Python graphical displays. Version 2.
# Documentation: http://myslu.stlawu.edu/~ltorrey/intrographics2
#########################################################################

import Tkinter
import traceback
import inspect

# (Window manager)
class _system:
    def __init__(self):
        self.root = None # Primary Tk frame
        self.dependents = [] # Other windows

    # Create a Tkinter frame
    def createFrame(self, window):
        if not self.root:
            self.root = Tkinter.Tk()
            self.root.withdraw()
            return self.root
        else:
            frame = Tkinter.Toplevel(self.root)
            self.dependents.append(window)
            frame.withdraw()
            return frame

    # Show a Tkinter frame
    def showFrame(self, window):
        window._frame.update()
        window._frame.deiconify()
        if window._frame == self.root:
            self.root.mainloop()

    # Destroy a Tkinter frame
    def destroyFrame(self, window):
        if window._frame == self.root:
            for window in self.dependents: window.close()
            self.dependents = []
            self.root.destroy()
            self.root = None
        else:
            self.dependents.remove(window)
            window._frame.destroy()

    # Check for a valid RBG color
    def isRGB(self, color):
        if type(color) != tuple:
            return False
        if len(color) != 3:
            return False
        for c in color:
            if c < 0 or c > 255:
                return False
        return True

    # Convert a color from string or (r,g,b) to hex
    def toHex(self, color):
        try:
            if not self.isRGB(color):
                color = tuple(map(lambda x : x/256, self.root.winfo_rgb(color)))
            return "#%02x%02x%02x" % color
        except:
            raise Exception("Invalid color: "+str(color))

    # Provide some error messages
    def extra(self, command):
        self.error("Call to "+command+" has too many arguments.")
    def missing(self, command):
        self.error("Call to "+command+" is missing an argument.")
    def invalid(self, command):
        self.error("Call to "+command+" has an incorrect argument type.")
    def restricted(self, command):
        self.error("Call to "+command+" has an unreasonable argument value.")
    def immutable(self, attribute, item):
        self.error("The '"+attribute+"' attribute of the "+item+" is read-only.")
    def error(self, message):
        print "Traceback (most recent call last):"
        print traceback.format_stack()[0],
        print "IntrographicsError:", message
        quit()

# (Initialize tools)
_sys = _system()

# A simple graphical display
class window:
    def __init__(self, width=None, height=None, *extra):
        command = "intrographics.window(width,height)"
        if len(extra) > 0:
            return _sys.extra(command)
        if width==None or height==None:
            return _sys.missing(command)
        try:
            width, height = int(width), int(height)
        except ValueError:
            return _sys.invalid(command)
        if width < 1 or height < 1:
            return _sys.restricted(command)
        width = width + 1
        height = height + 1
        self._shapes = []
        self._timers = []
        self._opened = False
        self._closed = False
        self._frame = _sys.createFrame(self)
        self._canvas = Tkinter.Canvas(self._frame)
        self._configure(0, 0, width, height)
        self._frame.protocol("WM_DELETE_WINDOW", lambda : self.close(""))
        self._canvas.bind("<Configure>", lambda event : self._configure(self._x, self._y, self._frame.winfo_width(), self._frame.winfo_height()))
        self.fill("white")

    # (Update the window location and/or size)
    def _configure(self, x, y, width, height):
        self._x, self._y = x, y
        self.__dict__["width"] = width-1
        self.__dict__["height"] = height-1
        self._frame.wm_geometry(str(width)+"x"+str(height)+"+"+str(x)+"+"+str(y))
        self._canvas.configure(width=width, height=height, highlightthickness=0)

    # (Disallow direct changes to some attributes)
    def __setattr__(self, attribute, value):
        if attribute in ["width", "height"]:
            return _sys.immutable(attribute, "window")
        self.__dict__[attribute] = value

    # Give the window a background color
    def fill(self, color=None, *extra):
        command = "window.fill(color)"
        if len(extra) > 0:
            return _sys.extra(command)
        if color==None:
            return _sys.missing(command)
        if self._closed:
            return
        self._canvas.configure(background=_sys.toHex(color))

    # Change the location of the window
    def relocate(self, x=None, y=None, *extra):
        command = "window.relocate(x,y)"
        if len(extra) > 0:
            return _sys.extra(command)
        if x==None or y==None:
            return _sys.missing(command)
        try:
            x, y = int(x), int(y)
        except ValueError:
            return _sys.invalid(command)
        if self._closed:
            return
        self._configure(x, y, self.width, self.height)

    # Change the size of the window
    def resize(self, width=None, height=None, *extra):
        command = "window.resize(width,height)"
        if len(extra) > 0:
            return _sys.extra(command)
        if width==None or height==None:
            return _sys.missing(command)
        try:
            width, height = int(width), int(height)
        except ValueError:
            return _sys.invalid(command)
        if width < 1 or height < 1:
            return _sys.restricted(command)
        width = width + 1
        height = height + 1
        if self._closed:
            return
        self._configure(self._x, self._y, width, height)

    # Add and return a rectangle shape
    def addRectangle(self, x=None, y=None, width=None, height=None, *extra):
        command = "window.addRectangle(x,y,width,height)"
        if len(extra) > 0:
            return _sys.extra(command)
        if x==None or y==None or width==None or height==None:
            return _sys.missing(command)
        try:
            x, y, width, height = int(x), int(y), int(width), int(height)
        except ValueError:
            return _sys.invalid(command)
        if width < 1 or height < 1:
            return _sys.restricted(command)
        if self._closed:
            return None
        return self._add(rectangle(self._canvas, x, y, width, height))

    # Add and return an oval shape
    def addOval(self, x=None, y=None, width=None, height=None, *extra):
        command = "window.addOval(x,y,width,height)"
        if len(extra) > 0:
            return _sys.extra(command)
        if x==None or y==None or width==None or height==None:
            return _sys.missing(command)
        try:
            x, y, width, height = int(x), int(y), int(width), int(height)
        except ValueError:
            return _sys.invalid(command)
        if width < 1 or height < 1:
            return _sys.restricted(command)
        if self._closed:
            return None
        return self._add(oval(self._canvas, x, y, width, height))

    # Add and return a polygon shape
    def addPolygon(self, *points):
        command = "window.addPolygon( (x1,y1), (x2,y2), (x3,y3), ...)"
        if len(points) < 3:
            return _sys.missing(command)
        try:
            points = tuple([(int(x),int(y)) for (x,y) in points])
        except ValueError, TypeError:
            return _sys.invalid(command)
        if self._closed:
            return None
        return self._add(polygon(self._canvas, points))

    # Add and return a line shape
    def addLine(self, *points):
        command = "window.addLine( (x1,y1), (x2,y2), ...)"
        if len(points) < 2:
            return _sys.missing(command)
        try:
            points = tuple([(int(x),int(y)) for (x,y) in points])
        except ValueError, TypeError:
            return _sys.invalid(command)
        if self._closed:
            return None
        return self._add(line(self._canvas, points))

    # Add and return a text shape
    def addText(self, x=None, y=None, message=None, *extra):
        command = "window.addText(x,y,message)"
        if len(extra) > 0:
            return _sys.extra(command)
        if x==None or y==None or message==None:
            return _sys.missing(command)
        try:
            x, y, message = int(x), int(y), str(message)
        except ValueError:
            return _sys.invalid(command)
        if self._closed:
            return None
        return self._add(text(self._canvas, x, y, message))

    # Add and return a button shape
    def addButton(self, x=None, y=None, message=None, *extra):
        command = "window.addButton(x,y,message)"
        if len(extra) > 0:
            return _sys.extra(command)
        if x==None or y==None or message==None:
            return _sys.missing(command)
        try:
            x, y, message = int(x), int(y), str(message)
        except ValueError:
            return _sys.invalid(command)
        if self._closed:
            return None
        return self._add(button(self._canvas, x, y, message))

    # Add and return a field shape
    def addField(self, x=None, y=None, message=None, *extra):
        command = "window.addField(x,y,message?)"
        if len(extra) > 0:
            return _sys.extra(command)
        if x==None or y==None:
            return _sys.missing(command)
        if message==None:
            message = ""
        try:
            x, y, message = int(x), int(y), str(message)
        except ValueError:
            return _sys.invalid(command)
        if self._closed:
            return None
        return self._add(field(self._canvas, x, y, message))

    # Add and return an image shape
    def addImage(self, x=None, y=None, filename=None, *extra):
        command = "window.addImage(x,y,filename)"
        if len(extra) > 0:
            return _sys.extra(command)
        if x==None or y==None or filename==None:
            return _sys.missing(command)
        try:
            x, y, filename = int(x), int(y), str(filename)
        except ValueError:
            return _sys.invalid(command)
        if self._closed:
            return None
        return self._add(image(self._canvas, x, y, filename))

    # (Add and return a shape)
    def _add(self, obj):
        self._shapes.append(obj)
        return obj

    # (Allow iteration over shapes in the window)
    def __iter__(self):
        return iter(self._shapes[:])

    # Get a list of the shapes beneath this point
    def under(self, x, y):
        ids = self._canvas.find_overlapping(x,y,x,y)
        return [s for s in self._shapes if s._id in ids]

    # Get a list of the other shapes in contact with this shape
    def touching(self, shape):
        ids = self._canvas.find_overlapping(shape.left, shape.top, shape.right, shape.bottom)
        return [s for s in self._shapes if s!=shape and s._id in ids]

    # Remove shapes from the window
    def remove(self, shape=None, *otherShapes):
        command = "window.remove(shape, ...)"
        if shape==None:
            return _sys.missing(command)
        for s in list(otherShapes) + [shape]:
            if not isinstance(s, _shape):
                return _sys.invalid(command)
            if self._closed or s not in self._shapes:
                return
            self._shapes.remove(s)
            s._delete()

    # Start a timer that ticks periodically
    def startTimer(self, milliseconds=None, function=None, *extra):
        command = "window.startTimer(milliseconds,function)"
        if len(extra) > 0:
            return _sys.extra(command)
        if milliseconds==None or function==None:
            return _sys.missing(command)
        try:
            milliseconds = int(milliseconds)
        except ValueError:
            return _sys.invalid(command)
        if not hasattr(function, "__call__"):
            return _sys.invalid(command)
        if len(inspect.getargspec(function)[0]) > 0:
            return _sys.error("Handler function "+function.__name__+" should expect no arguments.")
        if self._closed:
            return
        self._timers.append(function)
        self._canvas.after(milliseconds, self._runTimer, milliseconds, function)

    # (Call a function periodically)
    def _runTimer(self, milliseconds, function):
        if self._closed:
            return
        if function not in self._timers:
            return
        if self._opened:
            function()
        self._canvas.after(milliseconds, self._runTimer, milliseconds, function)

    # Make a running timer stop
    def stopTimer(self, function=None, *extra):
        command = "window.stopTimer(function)"
        if len(extra) > 0:
            return _sys.extra(command)
        if function==None:
            return _sys.missing(command)
        if not hasattr(function, "__call__"):
            return _sys.invalid(command)
        if function in self._timers:
            self._timers.remove(function)

    # Assign a function to handle left clicks
    def onLeftClick(self, function=None, *extra):
        command = "window.onLeftClick(function)"
        if len(extra) > 0:
            return _sys.extra(command)
        if function==None:
            return _sys.missing(command)
        if not hasattr(function, "__call__"):
            return _sys.invalid(command)
        if inspect.getargspec(function)[0] != ["x","y"]:
            return _sys.error("Handler function "+function.__name__+" should expect two arguments (x,y).")
        if self._closed:
            return
        self._frame.bind("<Button-1>", lambda event,function=function:self._mouseHandler(event,function))

    # Assign a function to handle left drags
    def onLeftDrag(self, function=None, *extra):
        command = "window.onLeftDrag(function)"
        if len(extra) > 0:
            return _sys.extra(command)
        if function==None:
            return _sys.missing(command)
        if not hasattr(function, "__call__"):
            return _sys.invalid(command)
        if inspect.getargspec(function)[0] != ["x","y"]:
            return _sys.error("Handler function "+function.__name__+" should expect two arguments (x,y).")
        if self._closed:
            return
        self._frame.bind("<B1-Motion>", lambda event,function=function:self._mouseHandler(event,function))

    # Assign a function to handle right clicks
    def onRightClick(self, function=None, *extra):
        command = "window.onRightClick(function)"
        if len(extra) > 0:
            return _sys.extra(command)
        if function==None:
            return _sys.missing(command)
        if not hasattr(function, "__call__"):
            return _sys.invalid(command)
        if inspect.getargspec(function)[0] != ["x","y"]:
            return _sys.error("Handler function "+function.__name__+" should expect two arguments (x,y).")
        if self._closed:
            return
        self._frame.bind("<Button-3>", lambda event,function=function:self._mouseHandler(event,function))

    # Assign a function to handle right drags
    def onRightDrag(self, function=None, *extra):
        command = "window.onRightDrag(function)"
        if len(extra) > 0:
            return _sys.extra(command)
        if function==None:
            return _sys.missing(command)
        if not hasattr(function, "__call__"):
            return _sys.invalid(command)
        if inspect.getargspec(function)[0] != ["x","y"]:
            return _sys.error("Handler function "+function.__name__+" should expect two arguments (x,y).")
        if self._closed:
            return
        self._frame.bind("<B3-Motion>", lambda event,function=function:self._mouseHandler(event,function))

    # Assign a function to handle key presses
    def onKey(self, function=None, *extra):
        command = "window.onKey(function)"
        if len(extra) > 0:
            return _sys.extra(command)
        if function==None:
            return _sys.missing(command)
        if not hasattr(function, "__call__"):
            return _sys.invalid(command)
        if inspect.getargspec(function)[0] != ["key"]:
            return _sys.error("Handler function "+function.__name__+" should expect one argument (key).")
        if self._closed:
            return
        self._frame.bind("<KeyPress>", lambda event,function=function:self._keyHandler(event,function))

    # (Give mouse handlers simple arguments)
    def _mouseHandler(self, event, function):
        function(event.x, event.y)

    # (Give key handlers simple arguments)
    def _keyHandler(self, event, function):
        function(event.keysym)

    # Make the window visible
    def open(self, title="intrographics", *extra):
        command = "window.open(title?)"
        if len(extra) > 0:
            return _sys.extra(command)
        try:
            title = str(title)
        except ValueError:
            return _sys.invalid(command)
        if self._opened or self._closed:
            return
        self._frame.wm_title(title)
        self._canvas.pack()
        self._opened = True
        _sys.showFrame(self)

    # Close the window
    def close(self, output="", *extra):
        command = "window.close(output?)"
        if len(extra) > 0:
            return _sys.extra(command)
        try:
            output = str(output)
        except ValueError:
            return _sys.invalid(command)
        if not self._opened or self._closed:
            return
        for obj in self._shapes:
            self.remove(obj)
        self._closed = True
        _sys.destroyFrame(self)
        print output

# (Any shape displayed in a window)
class _shape(object):
    def __init__(self, canvas):
        self._canvas = canvas
        self._deleted = False

    # (Disallow direct changes to some attributes)
    def __setattr__(self, attribute, value):
        if attribute in ["left", "top", "right", "bottom"]:
            return _sys.immutable(attribute, self.__class__.__name__)
        super(_shape,self).__setattr__(attribute, value)

    # (Take this shape off the canvas)
    def _delete(self):
        self._deleted = True
        self._canvas.delete(self._id)

# (A shape specified by a bounding box)
class _boxShape(_shape):
    def __init__(self, canvas, x, y, width, height):
        super(_boxShape,self).__init__(canvas)
        self._configure(x, y, width, height)

    # (Disallow direct changes to some attributes)
    def __setattr__(self, attribute, value):
        if attribute in ["width", "height"]:
            return _sys.immutable(attribute, self.__class__.__name__)
        super(_boxShape,self).__setattr__(attribute, value)   

    # (Update the shape location and/or size)
    def _configure(self, x, y, width, height):
        self._canvas.coords(self._id, (x, y, x+width, y+height))
        self._x, self._y, self._width, self._height = x, y, width, height
        self.__dict__["width"] = width
        self.__dict__["height"] = height
        self.__dict__["left"] = x
        self.__dict__["top"] = y
        self.__dict__["right"] = x+width
        self.__dict__["bottom"] = y+height

    # Change the color scheme of this shape
    def paint(self, color=None, borderWidth=1, borderColor="black", *extra):
        command = self.__class__.__name__+".paint(color,borderWidth?,borderColor?)"
        if len(extra) > 0:
            return _sys.extra(command)
        if color==None:
            return _sys.missing(command)
        try:
            borderWidth = int(borderWidth)
        except ValueError:
            return _sys.invalid(command)
        if self._deleted:
            return
        self._canvas.itemconfig(self._id, fill=_sys.toHex(color), width=borderWidth, outline=_sys.toHex(borderColor))

    # Move this shape
    def move(self, dx=None, dy=None, *extra):
        command = self.__class__.__name__+".move(dx,dy)"
        if len(extra) > 0:
            return _sys.extra(command)
        if dx==None or dy==None:
            return _sys.missing(command)
        try:
            dx, dy = int(dx), int(dy)
        except ValueError:
            return _sys.invalid(command)
        if self._deleted:
            return
        self._configure(self._x+dx, self._y+dy, self._width, self._height)

    # Change the location of this shape
    def relocate(self, x=None, y=None, *extra):
        command = self.__class__.__name__+".relocate(x,y)"
        if len(extra) > 0:
            return _sys.extra(command)
        if x==None or y==None:
            return _sys.missing(command)
        try:
            x, y = int(x), int(y)
        except ValueError:
            return _sys.invalid(command)
        if self._deleted:
            return
        self._configure(x, y, self._width, self._height)

    # Change the size of this shape
    def resize(self, width=None, height=None, *extra):
        command = self.__class__.__name__+".resize(width,height)"
        if len(extra) > 0:
            return _sys.extra(command)
        if width==None or height==None:
            return _sys.missing(command)
        try:
            width, height = int(width), int(height)
        except ValueError:
            return _sys.invalid(command)
        if width < 1 or height < 1:
            return _sys.restricted(command)
        if self._deleted:
            return
        self._configure(self._x, self._y, width, height)

# A rectangle shape
class rectangle(_boxShape):
    def __init__(self, canvas, x, y, width, height):
        self._id = canvas.create_rectangle(0,0,0,0, width=1)
        super(rectangle,self).__init__(canvas, x, y, width, height)

# An oval shape
class oval(_boxShape):
    def __init__(self, canvas, x, y, width, height):
        self._id = canvas.create_oval(0,0,0,0, width=1)
        super(oval,self).__init__(canvas, x, y, width, height)

# (A shape specified by a list of points)
class _listShape(_shape):
    def __init__(self, canvas, points):
        super(_listShape,self).__init__(canvas)
        self._configure(points)

    # (Update the shape location)
    def _configure(self, points):
        self._canvas.coords(self._id, tuple([c for p in points for c in p]))
        self._points = points
        self.__dict__["left"] = min(x for (x,y) in points)
        self.__dict__["top"] = min(y for (x,y) in points)
        self.__dict__["right"] = max(x for (x,y) in points)
        self.__dict__["bottom"] = max(y for (x,y) in points)

    # Move this shape
    def move(self, dx=None, dy=None, *extra):
        command = self.__class__.__name__+".move(dx,dy)"
        if len(extra) > 0:
            return _sys.extra(command)
        if dx==None or dy==None:
            return _sys.missing(command)
        try:
            dx, dy = int(dx), int(dy)
        except ValueError:
            return _sys.invalid(command)
        if self._deleted:
            return
        self._configure(tuple(map(lambda p : (p[0]+dx,p[1]+dy) , self._points)))

# A polygon shape
class polygon(_listShape):
    def __init__(self, canvas, points):
        self._id = canvas.create_polygon(0,0,0,0,0,0, width=1)
        super(polygon,self).__init__(canvas, points)

    # Change the color scheme of this polygon
    def paint(self, color=None, borderWidth=1, borderColor="black", *extra):
        command = "polygon.paint(color,borderWidth?,borderColor?)"
        if len(extra) > 0:
            return _sys.extra(command)
        if color==None:
            return _sys.missing(command)
        try:
            borderWidth = int(borderWidth)
        except ValueError:
            return _sys.invalid(command)
        if self._deleted:
            return
	if borderWidth == 0:
            self._canvas.itemconfig(self._id, fill=_sys.toHex(color), width=borderWidth)
        else:
            self._canvas.itemconfig(self._id, fill=_sys.toHex(color), width=borderWidth, outline=_sys.toHex(borderColor))

# A line shape
class line(_listShape):
    def __init__(self, canvas, points):
        self._id = canvas.create_line(0,0,0,0, width=1)
        super(line,self).__init__(canvas, points)

    # Change the color scheme of this line
    def paint(self, color=None, width=1, *extra):
        command = "line.paint(color,width?)"
        if len(extra) > 0:
            return _sys.extra(command)
        if color==None:
            return _sys.missing(command)
        try:
            width = int(width)
        except ValueError:
            return _sys.invalid(command)
        if width < 1:
            return _sys.restricted(command)
        if self._deleted:
            return
        self._canvas.itemconfig(self._id, fill=_sys.toHex(color), width=width)

# (A shape specified by a single point)
class _pointShape(_shape):
    def __init__(self, canvas, x, y):
        super(_pointShape,self).__init__(canvas)
        self._configure(x, y)

    # (Update the shape location)
    def _configure(self, x, y):
        self._canvas.coords(self._id, (x, y))
        self._x, self._y = x, y
        self.__dict__["left"] = x
        self.__dict__["top"] = y
        self.__dict__["right"] = self._canvas.bbox(self._id)[2]
        self.__dict__["bottom"] = self._canvas.bbox(self._id)[3]

    # Move this shape
    def move(self, dx=None, dy=None, *extra):
        command = self.__class__.__name__+".move(dx,dy)"
        if len(extra) > 0:
            return _sys.extra(command)
        if dx==None or dy==None:
            return _sys.missing(command)
        try:
            dx, dy = int(dx), int(dy)
        except ValueError:
            return _sys.invalid(command)
        if self._deleted:
            return
        self._configure(self._x+dx, self._y+dy)

    # Change the location of this shape
    def relocate(self, x=None, y=None, *extra):
        command = self.__class__.__name__+".relocate(x,y)"
        if len(extra) > 0:
            return _sys.extra(command)
        if x==None or y==None:
            return _sys.missing(command)
        try:
            x, y = int(x), int(y)
        except ValueError:
            return _sys.invalid(command)
        if self._deleted:
            return
        self._configure(x, y)

# A text label
class text(_pointShape):
    def __init__(self, canvas, x, y, message):
        self._id = canvas.create_text(0,0, text=message, font=("Helvetica",16), fill="black", anchor="nw")
        super(text,self).__init__(canvas, x, y)

    # (Retrieve and type-convert the message)
    def __str__(self):
        return self._canvas.itemcget(self._id, "text")
    def __int__(self):
        try:
            return int(str(self))
        except ValueError:
            return _sys.error("Couldn't convert the message to an int.")
    def __float__(self):
        try:
            return float(str(self))
        except ValueError:
            return _sys.error("Couldn't convert the message to an int.")

    # Change the message of this text
    def rewrite(self, message=None, *extra):
        command = "text.rewrite(message)"
        if len(extra) > 0:
            return _sys.extra(command)
        if message==None:
            return _sys.missing(command)
        try:
            message = str(message)
        except ValueError:
            return _sys.invalid(command)
        if self._deleted:
            return
        self._canvas.itemconfig(self._id, text=message)

    # Change the text style of this text
    def format(self, font=None, size=None, color=None, *extra):
        command = "text.format(font,size,color)"
        if len(extra) > 0:
            return _sys.extra()
        if font==None or size==None or color==None:
            return _sys.missing(command)
        try:
            font, size = str(font), int(size)
        except ValueError:
            return _sys.invalid(command)
        if self._deleted:
            return
        self._canvas.itemconfig(self._id, font=(font,size), fill=_sys.toHex(color))
        self._configure(self._x, self._y)

# A clickable button
class button(_pointShape):
    def __init__(self, canvas, x, y, message):
        self._button = Tkinter.Button(canvas.master, text=message)
        self._id = canvas.create_window(x, y, anchor="nw", window=self._button)
        super(button,self).__init__(canvas, x, y)

    # (Retrieve and type-convert the message)
    def __str__(self):
        return self._button.cget("text")
    def __int__(self):
        try:
            return int(str(self))
        except ValueError:
            return _sys.error("Couldn't convert the message to an int.")
    def __float__(self):
        try:
            return float(str(self))
        except ValueError:
            return _sys.error("Couldn't convert the message to an int.")

    # Change the message of this button
    def rewrite(self, message=None, *extra):
        command = "button.rewrite(message)"
        if len(extra) > 0:
            return _sys.extra(command)
        if message==None:
            return _sys.missing(command)
        try:
            message = str(message)
        except ValueError:
            return _sys.invalid(command)
        if self._deleted:
            return
        self._button.config(text=message)

    # Assign a function to call when this button is pressed
    def onPress(self, function=None, *extra):
        command = "button.onPress(function)"
        if len(extra) > 0:
            return _sys.extra(command)
        if function==None:
            return _sys.missing(command)
        if not hasattr(function, "__call__"):
            return _sys.invalid(command)
        if len(inspect.getargspec(function)[0]) > 1:
            return _sys.error("Handler function "+function.__name__+" should expect no arguments or one (source).")
        if self._deleted:
            return
        if len(inspect.getargspec(function)[0]) > 0:
            self._button.config(command=lambda:function(self))
        else:
            self._button.config(command=lambda:function())

# An input field
class field(_pointShape):
    def __init__(self, canvas, x, y, message):
        self._message = Tkinter.StringVar(value=message)
        self._entry = Tkinter.Entry(canvas.master, textvariable=self._message, relief="sunken", background="gray99")
        self._id = canvas.create_window(x, y, anchor="nw", window=self._entry)
        self._entry.bind("<FocusIn>", lambda event : self._message.set(""))
        super(field,self).__init__(canvas, x, y)

    # (Retrieve and type-convert the message)
    def __str__(self):
        return self._message.get()
    def __int__(self):
        try:
            return int(str(self))
        except ValueError:
            return _sys.error("Couldn't convert the message to an int.")
    def __float__(self):
        try:
            return float(str(self))
        except ValueError:
            return _sys.error("Couldn't convert the message to an int.")

    # Change the message of this field
    def rewrite(self, message=None, *extra):
        command = "field.rewrite(message)"
        if len(extra) > 0:
            return _sys.extra(command)
        if message==None:
            return _sys.missing(command)
        try:
            message = str(message)
        except ValueError:
            return _sys.invalid(command)
        if self._deleted:
            return
        self._message.set(message)

# A GIF image
class image(_pointShape):
    def __init__(self, canvas, x, y, filename):
        self._image = Tkinter.PhotoImage(master=canvas.master, file=filename)
        self._label = Tkinter.Label(canvas.master, image=self._image, bd=0)
        self._id = canvas.create_window(x, y, anchor="nw", window=self._label)
        super(image,self).__init__(canvas, x, y)
        self.__dict__["columns"] = self._image.width()
        self.__dict__["rows"] = self._image.height()

    # (Disallow direct changes to some attributes)
    def __setattr__(self, attribute, value):
        if attribute in ["rows", "columns"]:
            return _sys.immutable(attribute, "image")
        super(image,self).__setattr__(attribute, value)

    # (Allow indexing like image[col,row] to get pixel colors)
    def __getitem__(self, pixel):
        command = "image[col,row]"
        try:
            (col,row) = pixel
            col = int(col)
            row = int(row)
        except:
            return _sys.invalid(command)
        if self._deleted:
            return _sys.error("Can't index into a deleted image.")
        return tuple(map(int, self._image.get(col,row).split()))

    # (Allow indexing like image[col,row] to change pixel colors)
    def __setitem__(self, pixel, color):
        command = "image[col,row]"
        try:
            (col,row) = pixel
            col = int(col)
            row = int(row)
        except:
            return _sys.invalid(command)
        if self._deleted:
            return
        self._image.put(_sys.toHex(color), (col, row))

   # Save this image to a file
    def saveAs(self, filename=None, *extra):
        command = "image.saveAs(filename)"
        if len(extra) > 0:
            return _sys.extra(command)
        if filename==None:
            return _sys.missing(command)
        try:
            filename = str(filename)
        except ValueError:
            return _sys.invalid(command)
        if self._deleted:
            _sys.error("Can't save a deleted image.")
        self._image.write(filename, format="GIF")

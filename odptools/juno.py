#!/usr/bin/python

import hashlib
import os
import shutil
import socket
import subprocess
import tempfile
import time
import uno

class juno:
    def __init__(self):
        junopipename = "juno_%u" % os.getpid()
        junosocket = juno.socketName(junopipename)

        if os.path.exists(junosocket):
            raise Exception("%s already exists" % junosocket)

        self.tempdir = tempfile.mkdtemp()

        subprocess.Popen(("/usr/bin/soffice",
                          "--accept=pipe,name=%s;urp;StarOffice.ServiceManager" % junopipename,
                          "--headless",
                          "-env:UserInstallation=%s" % juno.mkpath(self.tempdir)),
                         stderr = file("/dev/null", "w"),
                         close_fds = True)

        if not self.waitConnect(junosocket, 10):
            raise Exception("soffice socket not found after 10 seconds, giving up")
      
        l_ctx = uno.getComponentContext()
        res = l_ctx.ServiceManager.createInstance("com.sun.star.bridge.UnoUrlResolver")
        ctx = res.resolve("uno:pipe,name=%s;urp;StarOffice.ComponentContext" % junopipename)
        self.smgr = ctx.ServiceManager
        self.desktop = self.createInstance("com.sun.star.frame.Desktop")
        self.disableCairo()

    def disableCairo(self):
        # work around https://bugs.freedesktop.org/show_bug.cgi?id=38875

        configprovider = self.createInstance("com.sun.star.configuration.ConfigurationProvider")

        config = configprovider.createInstanceWithArguments( \
            "com.sun.star.configuration.ConfigurationUpdateAccess",
            (juno.PropertyValue("nodepath", "/org.openoffice.Office.Canvas/CanvasServiceList"), ))
        
        for servicename in config.getElementNames():
            service = config.getByName(servicename)
            service.PreferredImplementations = \
                tuple(filter(lambda x: "cairo" not in x.lower(),
                             map(unicode.strip, service.PreferredImplementations)))
        config.commitChanges()

    def masterSocketName(self):
        md5 = hashlib.md5()
        md5.update(juno.mkpath(self.tempdir).encode("utf_16_le"))
        _hash = "".join(map(lambda x: "%x" % ord(x), md5.digest()))
        return juno.socketName("SingleOfficeIPC_%s" % _hash)

    def waitConnect(self, name, timeout):
        s = socket.socket(socket.AF_UNIX)

        rv = False
        for i in xrange(timeout * 10):
            try:
                s.connect(name)
                rv = True
                break
            except Exception:
                time.sleep(0.1)

        s.close()
        return rv

    def waitBind(self, name, timeout):
        s = socket.socket(socket.AF_UNIX)

        rv = False
        for i in xrange(timeout * 10):
            try:
                s.bind(name)
                rv = True
                break
            except Exception:
                time.sleep(0.1)

        s.close()
        if rv: os.unlink(name)
        return rv

    def createInstance(self, name):
        return self.smgr.createInstance(name)

    def disconnect(self):
        self.desktop.terminate()
        if self.waitBind(self.masterSocketName(), 30):
            shutil.rmtree(self.tempdir)

    @staticmethod
    def socketName(name):
        return "/tmp/OSL_PIPE_%u_%s" % (os.getuid(), name)

    @staticmethod
    def mkpath(x):
        return "file://" + os.path.abspath(x)

    @staticmethod
    def Any(_type, value):
        return uno.Any(_type, value)

    @staticmethod
    def PropertyValue(name, value):
        return uno.createUnoStruct("com.sun.star.beans.PropertyValue", name, 0,
                                   value,
                                   uno.Enum("com.sun.star.beans.PropertyState",
                                            "DIRECT_VALUE"))
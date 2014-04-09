# Copyright (c) 2013 Shotgun Software Inc.
# 
# CONFIDENTIAL AND PROPRIETARY
# 
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit 
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your 
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights 
# not expressly granted therein are reserved by Shotgun Software Inc.

import tank

from .util import sanitize_qt, get_sg_data

from tank.platform.qt import QtCore, QtGui

class ShotgunStandardItem(QtGui.QStandardItem):
    """
    Special implementation of StandardItem which bridges PyQt and PySide.
    
    Do not construct this object directly - instead use the ShotgunModel.create_item() method.
    """

    ########################################################################################
    # helper methods
    
    def get_sg_data(self):
        """
        Retrieves the shotgun data associated with this item.
        
        :returns: Shotgun data or None if no data was associated        
        """
        return get_sg_data(self)
        
    ########################################################################################
    # overridden methods

    def statusTip(self, *args, **kwargs):
        """
        Base class override which runs sanitize_qt() on the returned data
        """
        val = super(ShotgunStandardItem, self).statusTip(*args, **kwargs)
        return sanitize_qt(val)
        
    def text(self, *args, **kwargs):
        """
        Base class override which runs sanitize_qt() on the returned data
        """
        val = super(ShotgunStandardItem, self).text(*args, **kwargs)
        return sanitize_qt(val)

    def toolTip(self, *args, **kwargs):
        """
        Base class override which runs sanitize_qt() on the returned data
        """
        val = super(ShotgunStandardItem, self).toolTip(*args, **kwargs)
        return sanitize_qt(val)

    def whatsThis(self, *args, **kwargs):
        """
        Base class override which runs sanitize_qt() on the returned data
        """
        val = super(ShotgunStandardItem, self).whatsThis(*args, **kwargs)
        return sanitize_qt(val)

    def accessibleDescription(self, *args, **kwargs):
        """
        Base class override which runs sanitize_qt() on the returned data
        """
        val = super(ShotgunStandardItem, self).accessibleDescription(*args, **kwargs)
        return sanitize_qt(val)

    def accessibleText(self, *args, **kwargs):
        """
        Base class override which runs sanitize_qt() on the returned data
        """
        val = super(ShotgunStandardItem, self).accessibleText(*args, **kwargs)
        return sanitize_qt(val)
        
    def data(self, *args, **kwargs):
        """
        Base class override which runs sanitize_qt() on the returned data
        """
        val = super(ShotgunStandardItem, self).data(*args, **kwargs)
        return sanitize_qt(val)

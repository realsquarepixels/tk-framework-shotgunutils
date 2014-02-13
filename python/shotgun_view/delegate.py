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
from tank.platform.qt import QtCore, QtGui


class WidgetDelegate(QtGui.QStyledItemDelegate):
    """
    Convenience wrapper that makes it straight forward to use
    widgets inside of delegates.
    
    This class is basically an adapter which lets you connect a 
    view (QAbstractItemView) with a QWidget of choice. This widget
    is used to "paint" the view when it is being rendered. 
        
    This class can be used in conjunction with the various widgets found
    as part of the framework module (for example list_widget and thumb_widget).
    """

    def __init__(self, view):
        """
        Constructor
        """
        QtGui.QStyledItemDelegate.__init__(self, view)
        self.__view = view        
        
        # set up the widget instance we will use 
        # when 'painting' large number of cells 
        self.__paint_widget = self._create_widget(view)
        
        # tracks the currently active cell
        self.__current_editor_index = None    
        
        # help the GC
        self.__editors = []
                
        self.__selection_model = self.__view.selectionModel()
        if self.__selection_model:
            # note! Need to have a model connected to the view in order
            # to have a selection model.
            self.__selection_model.selectionChanged.connect(self._on_publish_selection)
        
    ########################################################################################
    # private methods
        
    def _on_publish_selection(self, selected, deselected):
        """
        Signal triggered when someone changes the selection in the view
        """
        # clean up        
        if self.__current_editor_index:
            self.__view.closePersistentEditor(self.__current_editor_index)
            self.__current_editor_index = None
        
        selected_indexes = selected.indexes()
        
        if len(selected_indexes) > 0:
            # get the currently selected model index
            model_index = selected_indexes[0]
            # create an editor widget that we use for the selected item
            self.__current_editor_index = model_index
            # this will trigger the call to createEditor
            self.__view.openPersistentEditor(model_index)        

    def createEditor(self, parent_widget, style_options, model_index):
        """
        Subclassed implementation from QStyledItemDelegate which is
        called when an "editor" is set up - the editor is set up 
        via the openPersistentEditor call and is created upon selection
        of an item.
        
        Normally, for performance, when we draw hundreds of grid cells, 
        we use the same Qwidget as a brush and simply use it to paint.
        
        For the currently selected cell however, we need to be able to interact
        with the widget (e.g. click a button for example) and therefore we need
        to have a real widget for this. The widget  
        
        """
        w = self._create_widget(parent_widget)
        self.__editors.append(w)
        self._on_before_selection(w, model_index, style_options)
        return w
        
    def updateEditorGeometry(self, editor_widget, style_options, model_index):        
        """
        Subclassed implementation which is typically called 
        whenever a editor widget is set up and needs resizing.
        This happens immediately after creation and also for example
        if the grid element size is changing.
        """
        editor_widget.resize(style_options.rect.size())
        editor_widget.move(style_options.rect.topLeft())
        
    def paint(self, painter, style_options, model_index):
        """
        Paint method to handle all cells that are not being currently edited.
        """        
        if model_index != self.__current_editor_index:

            # for performance reasons, we are not creating a widget every time
            # but merely moving the same widget around. 
            # first call out to have the widget set the right values
            self._on_before_paint(self.__paint_widget, model_index, style_options)
                    
            # now paint!
            painter.save()
            self.__paint_widget.resize(style_options.rect.size())
            painter.translate(style_options.rect.topLeft())
            # note that we set the render flags NOT to render the background of the widget
            # this makes it consistent with the way the editor widget is mounted inside 
            # each element upon hover.
            self.__paint_widget.render(painter, 
                                      QtCore.QPoint(0,0), 
                                      renderFlags=QtGui.QWidget.DrawChildren)
            painter.restore()
        
    ########################################################################################
    # implemented by deriving classes
    
    def _create_widget(self, parent):
        """
        This needs to be implemented by any deriving classes.
        
        Should return a QWidget that will be used when normal grid cells are drawn by the delegate.
        Prior to drawing a grid cell, the _before_draw_widget method is called.
        """
        raise NotImplementedError
    
    def _on_before_paint(self, widget, model_index, style_options):
        """
        This needs to be implemented by any deriving classes.
        
        This is called just before a cell is painted. This method should configure values
        on the widget (such as labels, thumbnails etc) based on the data contained
        in the model index parameter which is being passed.
        """
        raise NotImplementedError
            
    def _on_before_selection(self, widget, model_index, style_options):
        """
        This needs to be implemented by any deriving classes.
    
        This method is being called every time an editor is being fired up.
        """
        raise NotImplementedError
            


import os
import sys
from pathlib import PureWindowsPath, PurePosixPath

from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi

from ..top_bar.top_bar import TopBar
from ..tab_widgets.tab_widgets import TabWidgets


class MainWindow(QMainWindow):
    def __init__(self, config, themes, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        loadUi("rubicon-web/widgets/mainwindow/mainwindow.ui", self)
        
        self.CONFIG = config
        self.THEME = themes[self.CONFIG["theme"]]
        self.default_qurl = QUrl(self.CONFIG["default_url"])
        
        self.relative_to_abs_path = lambda file_path: os.path.abspath(file_path)
        self.nt_to_posix_path = lambda file_path: ''.join(str(PurePosixPath(PureWindowsPath(file_path))).split("\\")[1:])
        
        self.tab_widgets = TabWidgets()
        self.main_layout.addWidget(self.tab_widgets)
        
        self.top_bar = TopBar(self)
        self.centralwidget_layout.insertWidget(0, self.top_bar)

        self.top_bar.nav_bar.default_tab()
        
        self.main_layout.setSizes([0])
        
        widgets_with_stylesheets = [self.centralwidget, self.top_bar.nav_bar, self.top_bar, self.top_bar.tab_bar]
        self.init_stylesheets(widgets_with_stylesheets)
        
        self.setWindowTitle("Rubicon Web")
    
    def init_stylesheets(self, widgets):
        for widget in widgets:
            widget.hide()
            widget_stylesheet = widget.styleSheet()
            
            for key in self.THEME["colors"].keys():
                widget_stylesheet = widget_stylesheet.replace('/' + key + '/', self.THEME["colors"][key])

            split_stylesheet = widget_stylesheet.split('*')
            for index in range(1, len(split_stylesheet), 2):
                file_path = self.relative_to_abs_path(split_stylesheet[index])
                if os.name == 'nt':
                    file_path = self.nt_to_posix_path(file_path)
                split_stylesheet[index] = file_path
                widget_stylesheet = ''.join(split_stylesheet)

            widget.show()
            widget.setStyleSheet(widget_stylesheet)
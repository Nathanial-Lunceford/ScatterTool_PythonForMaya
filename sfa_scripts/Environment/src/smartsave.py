import logging

from PySide2 import QtWidgets, QtCore
from PySide2.QtWidgets import QFileDialog
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
import maya.cmds as cmds
import pymel.core as pnc
from pymel.core.system import Path


log = logging.getLogger(__name__)


def maya_main_window():
    """return the maya main window widget"""
    main_window = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window), QtWidgets.QWidget)


class SmartSaveUI(QtWidgets.QDialog):
    """SmartSave UI Class"""
    def __init__(self):
        super(SmartSaveUI, self).__init__(parent=maya_main_window())
        self.setWindowTitle("Smart Save")
        self.setMinimumWidth(500)
        self.setMaximumHeight(200)
        self.setWindowFlags(self.windowFlags() ^
                            QtCore.Qt.WindowContextHelpButtonHint)
        self.scenefile = SceneFile()
        self.create_ui()
        self.create_connections()

    def create_ui(self):
        self.title_lbl = QtWidgets.QLabel("Smart Save")
        self.title_lbl.setStyleSheet("font: bold 28px")
        self.folder_lay = self._create_folder_ui()
        self.filename_lay = self._create_filename_ui()
        self.button_lay = self._create_button_ui()
        self.main_lay = QtWidgets.QVBoxLayout()
        self.main_lay.addWidget(self.title_lbl)
        self.main_lay.addLayout(self.folder_lay)
        self.main_lay.addLayout(self.filename_lay)
        self.main_lay.addStretch()
        self.main_lay.addLayout(self.button_lay)
        self.setLayout(self.main_lay)

    def _create_button_ui(self):
        self.save_btn = QtWidgets.QPushButton("Save")
        self.save_increment_btn = QtWidgets.QPushButton("Save Increment")
        self.cancel_btn = QtWidgets.QPushButton("Cancel")
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.save_btn)
        layout.addWidget(self.save_increment_btn)
        layout.addWidget(self.cancel_btn)
        return layout

    def _create_filename_ui(self):
        layout = self._create_filename_headers()
        self.descriptor_le = QtWidgets.QLineEdit(self.scenefile.descriptor)
        self.descriptor_le.setMinimumWidth(100)
        self.task_le = QtWidgets.QLineEdit(self.scenefile.task)
        self.task_le.setFixedWidth(50)
        self.ver_sbx = QtWidgets.QSpinBox()
        self.ver_sbx.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
        self.ver_sbx.setFixedWidth(50)
        self.ver_sbx.setValue(self.scenefile.ver)
        self.ext_lbl = QtWidgets.QLabel(".ma")
        layout.addWidget(self.descriptor_le, 1, 0)
        layout.addWidget(QtWidgets.QLabel("_"), 1, 1)
        layout.addWidget(self.task_le, 1, 2)
        layout.addWidget(QtWidgets.QLabel("_V"), 1, 3)
        layout.addWidget(self.ver_sbx, 1, 4)
        layout.addWidget(self.ext_lbl, 1, 5)
        return layout

    def _create_filename_headers(self):
        self.descriptor_header_lbl = QtWidgets.QLabel("Descriptor")
        self.descriptor_header_lbl.setStyleSheet("font: bold")
        self.task_header_lbl = QtWidgets.QLabel("Task")
        self.task_header_lbl.setStyleSheet("font: bold")
        self.ver_header_lbl = QtWidgets.QLabel("Version")
        self.ver_header_lbl.setStyleSheet("font: bold")
        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.descriptor_header_lbl, 0, 0)
        layout.addWidget(self.task_header_lbl, 0, 2)
        layout.addWidget(self.ver_header_lbl, 0, 4)
        return layout

    def _create_folder_ui(self):
        default_folder = Path(cmds.workspace(rootDirectory=True, query=True))
        default_folder = default_folder / "scenes"
        self.folder_le = QtWidgets.QLineEdit(default_folder)
        self.folder_browse_btn = QtWidgets.QPushButton("...")
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.folder_le)
        layout.addWidget(self.folder_browse_btn)
        return layout

    def create_connections(self):
        """connect our widget signals to slots"""
        self.cancel_btn.clicked.connect(self.cancel)
        self.folder_browse_btn.clicked.connect(self.browse_folder)
        self.save_btn.clicked.connect(self._save)
        self.save_increment_btn.clicked.connect(self._save_increment)

    @QtCore.Slot()
    def _save_increment(self):
        """Save an increment of the scene"""
        self._set_scenefile_properties_from_ui()
        self.scenefile.increment_save()
        self.ver_sbx.setValue(self.scenefile.ver)

    @QtCore.Slot()
    def _save(self):
        """Save the scene"""
        self._set_scenefile_properties_from_ui()
        self.scenefile.save()

    def _set_scenefile_properties_from_ui(self):
        self.scenefile.folder_path = self.folder_le.text()
        self.scenefile.descriptor = self.descriptor_le.text()
        self.scenefile.task = self.task_le.text()
        self.scenefile.ver = self.ver_sbx.value()
        self.scenefile.ext = self.ext_lbl.text()

    def browse_folder(self):
        """Open a dialogue box to browse the folder"""
        folder = QtWidgets.QFileDialog.getExistingDirectory(
            parent=self,
            caption="Select Directory",
            dir=self.folder_le.text(),
            options=QtWidgets.QFileDialog.ShowDirsOnly |
                    QtWidgets.QFileDialog.DontResolveSymlinks)
        self.folder_le.setText(folder)

    @QtCore.Slot()
    def cancel(self):
        """quits the dialogue"""
        self.close()


class SceneFile(object):
    """An abstract representation of a Scene file."""
    def __init__(self, path=None):
        self._folder_path = Path(cmds.workspace(query=True,
                                               rootDirectory=True)) / "scenes"
        self.descriptor = 'main'
        self.task = 'model'
        self.ver = 1
        self.ext = '.ma'
        scene = pnc.system.sceneName()
        if not path:
            path = scene
        if not path and not scene:
            log.info("Initialize with default properties")
            return
        self._init_from_path(path)

    @property
    def folder_path(self):
        return self._folder_path

    @folder_path.setter
    def folder_path(self, val):
        self._folder_path = Path(val)


    @property
    def filename(self):
        """returns properly formatted filename"""
        pattern = "{descriptor}_{task}_v{ver:03d}{ext}"
        return pattern.format(descriptor=self.descriptor,
                              task=self.task,
                              ver=self.ver,
                              ext=self.ext)

    @property
    def path(self):
        """returns path of file"""
        return self.folder_path / self.filename

    def _init_from_path(self, path):
        """creates the necessary variables from a path"""
        path = Path(path)
        self.folder_path = path.parent
        self.ext = path.ext
        self.descriptor, self.task, ver = path.name.stripext().split("_")
        self.ver = int(ver.split("v")[-1])

    def save(self):
        """saves current scene file"""
        try:
            return pnc.system.saveAs(self.path)
        except RuntimeError as err:
            log.warning("missing directories in path. Creating folders...")
            self.folder_path.makedirs_p()
            return pnc.system.saveAs(self.path)

    def next_avail_ver(self):
        """return next available version num in folder"""
        pattern = "{descriptor}_{task}_v*{ext}".format(
            descriptor=self.descriptor,
            task=self.task,
            ext=self.ext)
        matching_scenefiles = []
        for file_ in self.folder_path.files():
            if file_.name.fnmatch(pattern):
                matching_scenefiles.append(file_)
        if not matching_scenefiles:
            return 1
        matching_scenefiles.sort(reverse=True)
        latest_scenefile = matching_scenefiles[0]
        latest_scenefile = latest_scenefile.name.stripext()
        latest_version_num = int(latest_scenefile.split("_v")[-1])
        return latest_version_num + 1

    def increment_save(self):
        """Increments version and saves scene file
        should increment from largest version number in folder.
        Returns path of scene file if successful"""
        self.ver = self.next_avail_ver()
        self.save()


scene_file = SceneFile("C/noname_notask_v000.ma")
#print(scene_file.path())
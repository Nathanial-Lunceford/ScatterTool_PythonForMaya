import logging

from PySide2 import QtWidgets, QtCore
from PySide2.QtWidgets import QFileDialog
from shiboken2 import wrapInstance
import maya.OpenMaya as oM
import maya.OpenMayaUI as omUI
import maya.cmds as cmds
import pymel.core as pnc
import pymel.core.datatypes as dt
from pymel.core.system import Path
import random as rand

log = logging.getLogger(__name__)


def maya_main_window():
    """return the maya main window widget"""
    main_window = omUI.MQtUtil.mainWindow()
    return wrapInstance(long(main_window), QtWidgets.QWidget)


class ScatterUI(QtWidgets.QDialog):
    """ScatterTool UI Class"""

    def __init__(self):
        super(ScatterUI, self).__init__(parent=maya_main_window())
        self.scat = Scatter()
        self.setWindowTitle("Scatter Tool")
        self.setMinimumWidth(500)
        self.setMaximumHeight(300)
        self.setWindowFlags(self.windowFlags() ^
                            QtCore.Qt.WindowContextHelpButtonHint)
        self.create_ui()
        # Note: Need to code connections
        self.create_connections()

    def create_ui(self):
        self.title_lbl = QtWidgets.QLabel("Scatter Tool")
        self.title_lbl.setStyleSheet("font: bold 28px")
        self.select_note = self._create_select_note()
        self.button_lay = self._create_button_ui()
        self.objchoose = self._create_obj_choose()
        self.randomscalecheck = self._create_random_scale_check()
        self.randomscalemax = self._create_random_scale_max()
        self.randomscalemin = self._create_random_scale_min()
        self.randomrotatecheck = self._create_random_rotate_check()
        self.randomrotationmax = self._create_random_rotation_max()
        self.randomrotationmin = self._create_random_rotation_min()
        self.randompercentage = self._create_random_percentage()
        self.normalcheckbox = self._create_normal_checkbox()
        self.pushin = self._create_pushin()
        self.main_lay = QtWidgets.QVBoxLayout()
        self.main_lay.addWidget(self.title_lbl)
        self.main_lay.addStretch()
        self.main_lay.addLayout(self.select_note)
        self.main_lay.addLayout(self.objchoose)
        self.main_lay.addLayout(self.randomscalecheck)
        self.main_lay.addLayout(self.randomscalemax)
        self.main_lay.addLayout(self.randomscalemin)
        self.main_lay.addLayout(self.randomrotatecheck)
        self.main_lay.addLayout(self.randomrotationmax)
        self.main_lay.addLayout(self.randomrotationmin)
        self.main_lay.addStretch()
        self.main_lay.addLayout(self.randompercentage)
        self.main_lay.addLayout(self.normalcheckbox)
        self.main_lay.addLayout(self.pushin)
        self.main_lay.addLayout(self.button_lay)
        self.setLayout(self.main_lay)

    def _create_select_note(self):
        self.note = QtWidgets.QLabel("")
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.note)
        return layout

    def _create_random_rotate_check(self):
        self.random_rot_checkbox = QtWidgets.QCheckBox()
        self.random_rot_checkbox.setFixedWidth(15)
        self.random_rot_checkbox_label = QtWidgets.QLabel("Rotate objects "
                                                          "randomly?")
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.random_rot_checkbox)
        layout.addWidget(self.random_rot_checkbox_label)
        return layout

    def _create_random_scale_check(self):
        self.random_scale_checkbox = QtWidgets.QCheckBox()
        self.random_scale_checkbox.setFixedWidth(15)
        self.random_scale_checkbox_label = QtWidgets.QLabel("Scale objects "
                                                            "randomly?")
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.random_scale_checkbox)
        layout.addWidget(self.random_scale_checkbox_label)
        return layout

    def _create_random_rotation_max(self):
        """creates a random rotation editable text box"""
        self.random_rot_max_label_x = QtWidgets.QLabel("Random Rotation Max X")
        self.random_rot_max_label_y = QtWidgets.QLabel("Random Rotation Max Y")
        self.random_rot_max_label_z = QtWidgets.QLabel("Random Rotation Max Z")
        self.rand_rot_max_x = QtWidgets.QLineEdit("180")
        self.rand_rot_max_y = QtWidgets.QLineEdit("180")
        self.rand_rot_max_z = QtWidgets.QLineEdit("180")
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.random_rot_max_label_x)
        layout.addWidget(self.rand_rot_max_x)
        layout.addWidget(self.random_rot_max_label_y)
        layout.addWidget(self.rand_rot_max_y)
        layout.addWidget(self.random_rot_max_label_z)
        layout.addWidget(self.rand_rot_max_z)
        return layout

    def _create_random_rotation_min(self):
        self.random_rot_min_label_x = QtWidgets.QLabel("Random Rotation Min X")
        self.random_rot_min_label_y = QtWidgets.QLabel("Random Rotation Min Y")
        self.random_rot_min_label_z = QtWidgets.QLabel("Random Rotation Min Z")
        self.rand_rot_min_x = QtWidgets.QLineEdit("0")
        self.rand_rot_min_y = QtWidgets.QLineEdit("0")
        self.rand_rot_min_z = QtWidgets.QLineEdit("0")
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.random_rot_min_label_x)
        layout.addWidget(self.rand_rot_min_x)
        layout.addWidget(self.random_rot_min_label_y)
        layout.addWidget(self.rand_rot_min_y)
        layout.addWidget(self.random_rot_min_label_z)
        layout.addWidget(self.rand_rot_min_z)
        return layout

    def _create_random_scale_max(self):
        """creates a random scale editable text box"""
        self.random_scale_max_label_x = QtWidgets.QLabel("Random Scale Max X")
        self.random_scale_max_label_y = QtWidgets.QLabel("Random Scale Max Y")
        self.random_scale_max_label_z = QtWidgets.QLabel("Random Scale Max Z")
        self.rand_scale_max_x = QtWidgets.QLineEdit("2")
        self.rand_scale_max_y = QtWidgets.QLineEdit("2")
        self.rand_scale_max_z = QtWidgets.QLineEdit("2")
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.random_scale_max_label_x)
        layout.addWidget(self.rand_scale_max_x)
        layout.addWidget(self.random_scale_max_label_y)
        layout.addWidget(self.rand_scale_max_y)
        layout.addWidget(self.random_scale_max_label_z)
        layout.addWidget(self.rand_scale_max_z)
        return layout

    def _create_random_scale_min(self):
        self.random_scale_min_Label_x = QtWidgets.QLabel("Random Scale Min X")
        self.random_scale_min_Label_y = QtWidgets.QLabel("Random Scale Min Y")
        self.random_scale_min_Label_z = QtWidgets.QLabel("Random Scale Min Z")
        self.rand_scale_min_x = QtWidgets.QLineEdit(".5")
        self.rand_scale_min_y = QtWidgets.QLineEdit(".5")
        self.rand_scale_min_z = QtWidgets.QLineEdit(".5")
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.random_scale_min_Label_x)
        layout.addWidget(self.rand_scale_min_x)
        layout.addWidget(self.random_scale_min_Label_y)
        layout.addWidget(self.rand_scale_min_y)
        layout.addWidget(self.random_scale_min_Label_z)
        layout.addWidget(self.rand_scale_min_z)
        return layout

    def _create_random_percentage(self):
        self.random_percentage_label = QtWidgets.QLabel("Percentage of "
                                                        "Vertices to scatter "
                                                        "to:")
        self.random_percentage_label.setFixedWidth(183)
        self.random_percentage = QtWidgets.QDoubleSpinBox()
        self.random_percentage.setMaximum(100.00)
        self.random_percentage.setMinimum(0.00)
        self.random_percentage.setFixedWidth(80)
        self.random_percentage.setValue(100.00)
        self.percentage_label = QtWidgets.QLabel("%")
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.random_percentage_label)
        layout.addWidget(self.random_percentage)
        layout.addWidget(self.percentage_label)
        return layout

    def _create_normal_checkbox(self):
        self.normalcheck = QtWidgets.QCheckBox()
        self.normalchecklabel = QtWidgets.QLabel("Scatter objects to align "
                                                 "with normals of the vertices"
                                                 " they're scattered to?")
        self.normalcheck.setFixedWidth(15)
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.normalcheck)
        layout.addWidget(self.normalchecklabel)
        return layout

    def _create_pushin(self):
        self.pushincheck = QtWidgets.QCheckBox()
        self.pushincheck_label = QtWidgets.QLabel("Push scattered objs into "
                                                  "their destination?")
        self.pushin_length = QtWidgets.QDoubleSpinBox()
        self.pushin_length_label = QtWidgets.QLabel("units they'll be "
                                                    "pushed in")
        self.pushincheck.setFixedWidth(15)
        self.pushincheck_label.setFixedWidth(500)
        self.pushin_length.setMinimum(-10.00)
        self.pushin_length.setMaximum(10.00)
        self.pushin_length.setFixedWidth(100)
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.pushincheck)
        layout.addWidget(self.pushincheck_label)
        layout.addWidget(self.pushin_length)
        layout.addWidget(self.pushin_length_label)
        return layout

    def _create_obj_choose(self):
        """This creates two combobox select menus for selecting recipient
        and obj to scatter"""
        self.to_scatter_label = QtWidgets.QLabel("Obj to Scatter:")
        self.scatter_on_label = QtWidgets.QLabel("Obj/Vertices to Scatter On:")
        self.to_scatter_line_edit = QtWidgets.QLineEdit()
        self.obj_to_scatter_btn = QtWidgets.QPushButton("Select Object")
        self.scatter_on_line_edit = QtWidgets.QLineEdit()
        self.scatter_on = QtWidgets.QPushButton("Select Entire Selection")
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.to_scatter_label)
        layout.addWidget(self.to_scatter_line_edit)
        layout.addWidget(self.obj_to_scatter_btn)
        layout.addWidget(self.scatter_on_label)
        layout.addWidget(self.scatter_on_line_edit)
        layout.addWidget(self.scatter_on)
        return layout

    def _create_button_ui(self):
        self.scatter_btn = QtWidgets.QPushButton("Scatter")
        self.cancel_btn = QtWidgets.QPushButton("Cancel")
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.scatter_btn)
        layout.addWidget(self.cancel_btn)
        return layout

    def create_connections(self):
        """TO DO: CONNECT THE BUTTONS"""
        self.cancel_btn.clicked.connect(self.cancel)

        self.obj_to_scatter_btn.clicked.connect(self.select_scatter)

        self.scatter_on.clicked.connect(self.select_to_scatter_verts)

        self.scatter_btn.clicked.connect(self.scatter)

    @QtCore.Slot()
    def scatter(self):
        self.scat.set_scale_and_rot_x(self.rand_scale_max_x.text(),
                                      self.rand_scale_min_x.text(),
                                      self.rand_rot_max_x.text(),
                                      self.rand_rot_min_x.text())
        self.scat.set_scale_and_rot_y(self.rand_scale_max_y.text(),
                                      self.rand_scale_min_y.text(),
                                      self.rand_rot_max_y.text(),
                                      self.rand_rot_min_y.text())
        self.scat.set_scale_and_rot_z(self.rand_scale_max_z.text(),
                                      self.rand_scale_min_z.text(),
                                      self.rand_rot_max_z.text(),
                                      self.rand_rot_min_z.text())
        self.scat.set_percentage(self.random_percentage.value())
        self.scat.set_checkbox_normals(self.normalcheck.isChecked())
        self.scat.set_pushin(self.pushincheck.isChecked(),
                             self.pushin_length.value())
        self.scat.set_random_checks(self.random_rot_checkbox.isChecked(),
                                    self.random_scale_checkbox.isChecked())
        self.scat.scatter_func()

    @QtCore.Slot()
    def select_to_scatter_obj(self):
        self.scatter_on_line_edit.setText(
            self.scat.select_an_object_to_scatter_to())

    @QtCore.Slot()
    def select_to_scatter_verts(self):
        # TODO create error thingie if user selected objs and then pressed
        # this button
        self.scatter_on_line_edit.setText(
            self.scat.select_verts_to_scatter_to())

    @QtCore.Slot()
    def select_scatter(self):
        self.to_scatter_line_edit.setText(self.scat.select_obj_to_scatter())

    @QtCore.Slot()
    def cancel(self):
        """quits the dialogue"""
        self.close()


class Scatter(object):
    def __init__(self):
        self.obj_to_scatter = ''
        self.obj_to_scatter_on = ''
        self.verts_to_scatter_on = ''
        self.scale_max_x = 2
        self.scale_max_y = 2
        self.scale_max_z = 2
        self.scale_min_x = 0.5
        self.scale_min_y = 0.5
        self.scale_min_z = 0.5
        self.rot_max_x = 180
        self.rot_max_y = 180
        self.rot_max_z = 180
        self.rot_min_x = 0
        self.rot_min_y = 0
        self.rot_min_z = 0
        self.percentage_to_scatter_to = 100.00
        self.verts_picked = list()
        self.number_of_verts = 0
        self.align_to_normals_value = False
        self.push_in_objs = False
        self.push_in_length = 0
        self.rotate_checked = False
        self.scale_checked = True

    def set_random_checks(self, rot_checked, scale_checked):
        self.rotate_checked = rot_checked
        self.scale_checked = scale_checked

    def set_scale_and_rot_x(self, scalemax, scalemin, rotmax, rotmin):
        self.scale_max_x = float(scalemax)
        self.scale_min_x = float(scalemin)
        self.rot_max_x = float(rotmax)
        self.rot_min_x = float(rotmin)

    def set_scale_and_rot_y(self, scalemax, scalemin, rotmax, rotmin):
        self.scale_max_y = float(scalemax)
        self.scale_min_y = float(scalemin)
        self.rot_max_y = float(rotmax)
        self.rot_min_y = float(rotmin)

    def set_scale_and_rot_z(self, scalemax, scalemin, rotmax, rotmin):
        self.scale_max_z = float(scalemax)
        self.scale_min_z = float(scalemin)
        self.rot_max_z = float(rotmax)
        self.rot_min_z = float(rotmin)

    def set_percentage(self, percentage_chosen):
        self.percentage_to_scatter_to = float(percentage_chosen)
        self.percentage_to_scatter_to = self.percentage_to_scatter_to/100

    def set_checkbox_normals(self, checked):
        self.align_to_normals_value = checked

    def set_pushin(self, checked, length):
        self.push_in_objs = checked
        self.push_in_length = length

    def random_scale_instance(self, instance):
        random_x = self.random_change_in_direction(self.scale_max_x,
                                                   self.scale_min_x)
        random_y = self.random_change_in_direction(self.scale_max_y,
                                                   self.scale_min_y)
        random_z = self.random_change_in_direction(self.scale_max_z,
                                                   self.scale_min_z)
        cmds.scale(random_x, random_y, random_z, instance)

    def choose_percentage_of_vertices(self):
        self.number_of_verts = 0
        self.verts_picked = []
        self.number_of_verts = int(self.verts_to_scatter_on.__len__() *
                                   self.percentage_to_scatter_to)
        verts_length = self.verts_to_scatter_on.__len__()
        for i in range(self.number_of_verts):
            self.choose_random_vertex_not_already_chosen()

    def choose_random_vertex_not_already_chosen(self):
        num = 0
        chosen_new_number = False
        while(chosen_new_number is False):
            chosen_new_number = True
            num = rand.randint(0, (self.verts_to_scatter_on.__len__() - 1))
            for x in self.verts_picked:
                if(self.verts_to_scatter_on[num] == x):
                    chosen_new_number = False

        self.verts_picked.append(self.verts_to_scatter_on[num])

    def random_rotate_instance(self, instance):
        random_x = self.random_change_in_direction(self.rot_max_x,
                                                   self.rot_min_x)
        random_y = self.random_change_in_direction(self.rot_max_y,
                                                   self.rot_min_y)
        random_z = self.random_change_in_direction(self.rot_max_z,
                                                   self.rot_min_z)
        cmds.rotate(random_x, random_y, random_z, instance, objectSpace=True,
                    relative=True)

    def random_change_in_direction(self, max, min):
        scale_random = rand.random()
        old_range = (1 - 0)
        new_range = max - min
        scale_val = (((scale_random - 0) * new_range) / old_range) + min
        return scale_val

    def align_and_rotate_to_normals_function(self, instance, vertex):
        constraint = cmds.normalConstraint(vertex, instance)
        cmds.delete(constraint)

    def move_instance(self, instance, vert):
        pos_list = cmds.pointPosition(vert)
        pos_1 = pos_list[0]
        pos_2 = pos_list[1]
        pos_3 = pos_list[2]
        cmds.move(pos_1, pos_2, pos_3, instance)

    def push_in_instance(self, instance):
        cmds.move(-self.push_in_length, 0, 0, instance, objectSpace=True,
                  relative=True)

    def select_verts_to_scatter_to(self):
        things_selected = cmds.ls(sl=True, flatten=True)
        things_selected = cmds.polyListComponentConversion(
            things_selected, toVertex=True)
        self.verts_to_scatter_on = cmds.filterExpand(things_selected, sm=31)
        return str(self.verts_to_scatter_on)

    def select_obj_to_scatter(self):
        self.selected_objs = cmds.ls(sl=True)
        self.obj_to_scatter = self.selected_objs[0]
        return str(self.obj_to_scatter)

    def scatter_func(self):
        # need to modify verts to scatter on with percentage
        if(self.percentage_to_scatter_to == 100.00):
            pass
        elif(self.percentage_to_scatter_to == 0.00):
            return 0
        else:
            self.choose_percentage_of_vertices()

        for vertex in self.verts_picked:
            self.instanced_obj = cmds.instance(self.obj_to_scatter,
                                               smartTransform=True)

            if(self.scale_checked):
                self.random_scale_instance(self.instanced_obj)

            self.move_instance(self.instanced_obj, vertex)

            if(self.align_to_normals_value):
                self.align_and_rotate_to_normals_function(self.instanced_obj,
                                                          vertex)
                if (self.push_in_objs):
                    self.push_in_instance(self.instanced_obj)
            elif (self.push_in_objs):
                self.align_and_rotate_to_normals_function(self.instanced_obj,
                                                          vertex)
                self.push_in_instance(self.instanced_obj)
                if(self.rotate_checked):
                    self.random_rotate_instance(self.instanced_obj)
            elif(self.rotate_checked):
                self.random_rotate_instance(self.instanced_obj)

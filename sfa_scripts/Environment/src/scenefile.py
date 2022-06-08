import logging

import pymel.core as pnc
from pymel.core.system import Path

log = logging.getLogger(__name__)


class SceneFile(object):
    """An abstract representation of a Scene file."""
    def __init__(self, path=None):
        self.folder_path = Path()
        self.descriptor = 'main'
        self.task = None
        self.ver = 1
        self.ext = '.ma'
        scene = pnc.system.sceneName()
        if not path:
            path = scene
        if not path and not scene:
            log.warning("Unable to initialize SceneFile object from a new"
                        "scene. Please specify a path.")
            return
        self._init_from_path(path)

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
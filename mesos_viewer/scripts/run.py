#!/usr/bin/env python
# -*- coding: utf-8 -*-
from mesos_viewer import gui
from mesos_viewer.cachemanager import CacheManager

print('Loading Frameworks...')
cache_manager = CacheManager()
mesos_gui = gui.MesosGui(cache_manager )
mesos_gui.main()

# -*- coding: utf-8 -*-
import os
import pickle
import datetime

from mesos_viewer.config import Config
from mesos_viewer.mesosapi import MesosAPI



class CacheManager(object):
    def __init__(self, cache_path=None):
        self.cache_path = cache_path
        if cache_path is None:
            self.config = Config()
            self.cache_path = self.config.parser.get('settings', 'cache')
        
        self.cache_age = int(self.config.parser.get('settings', 'cache_age'))

        self.mesos_api = MesosAPI()
        self.master_ip = self.config.parser.get('mesos', 'master_ip')
        self.master_port = self.config.parser.get('mesos', 'master_port')
        self.mesos_frameworks_url = self.config.parser.get('mesos', 'mesos_frameworks_url')
        self.mesos_metrics_url = self.config.parser.get('mesos', 'mesos_metrics_url')
        self.mesos_redirect_url = self.config.parser.get('mesos', 'mesos_redirect_url')

    def is_outdated(self, which="frameworks"):
        return True

    def refresh(self, which="frameworks"):
        pass

    def get_frameworks(self, which="frameworks"):
        return self.mesos_api.get_frameworks(
            self.mesos_api.get_url(
                self.master_ip,
                self.master_port,
                self.mesos_frameworks_url,
                self.mesos_redirect_url
                ))

    def get_metrics(self):
        return self.mesos_api.get_metrics(
            self.mesos_api.get_url(
                self.master_ip,
                self.master_port,
                self.mesos_metrics_url,
                self.mesos_redirect_url
                ))

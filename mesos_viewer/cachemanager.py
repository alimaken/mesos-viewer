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

        if not os.path.exists(self.cache_path):
            self.refresh()

    def is_outdated(self, which="frameworks"):
        if not os.path.exists(self.cache_path):
            return True

        try:
            cache = pickle.load(open(self.cache_path, 'rb'))
        except:
            cache = {}
        if not cache.get(which, False):
            return True

        cache_age = datetime.datetime.today() - cache[which]['date']
        if cache_age.seconds > self.cache_age * 1:
            return True
        else:
            return False

    def refresh(self, which="frameworks"):
        if which == "frameworks":
            frameworks = self.mesos_api.get_frameworks(
                self.mesos_api.get_url(
                    self.master_ip,
                    self.master_port,
                    self.mesos_frameworks_url
                    ))
        else:
            raise Exception('Bad value')

        cache = {}
        if os.path.exists(self.cache_path):
            try:
                cache = pickle.load(open(self.cache_path, 'rb'))
            except:
                pass

        cache[which] = {'frameworks': frameworks, 'date': datetime.datetime.today()}
        pickle.dump(cache, open(self.cache_path, 'wb'))

    def get_frameworks(self, which="frameworks"):
        cache = []
        if os.path.exists(self.cache_path):
            # print("reading from cache @ [{}]".format(self.cache_path))
            try:
                cache = pickle.load(open(self.cache_path, 'rb'))
            except:
                cache = {}

        if not cache.get(which, False):
            return []
        else:
            return cache[which]['frameworks']

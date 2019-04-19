# -*- coding: utf-8 -*-
import time
import datetime
import requests


class MesosException(Exception):
    """
    MesosException is exactly the same as a plain Python Exception.

    The MesosException class exists solely so that you can identify
    errors that come from MesosCLI as opposed to from your application.
    """
    pass


class MesosAPI:
    """
    The class for parsing Mesos JSON response in to objects.
    """

    def parse_raw_frameworks(self, raw_frameworks):
        frameworks = []
        for raw_framework in raw_frameworks:
            if raw_framework["name"] == "marathon" or raw_framework["name"] == "chronos":
                continue
            frameworks.append(self.parse_raw_framework(raw_framework))
        return frameworks

    @staticmethod
    def parse_raw_framework(framework_raw):
        framework = Framework()
        resources = framework_raw["resources"]
        framework.name = framework_raw["name"]

        framework.memory = int(resources["mem"])
        framework.memory_str = str(int(resources["mem"])) + "MB"
        framework.cpus = int(resources["cpus"])
        framework.url = framework_raw["webui_url"]
        framework.tasks = framework_raw["tasks"]
        framework.tasks_len = str(len(framework.tasks))
        ts_epoch = int(framework_raw["registered_time"])
        now = time.time()
        diff = (now - ts_epoch)
        framework.uptime = datetime.datetime.fromtimestamp(ts_epoch).strftime('%Y-%m-%d %H:%M:%S')
        framework.uptime_descriptive = str(datetime.timedelta(seconds=diff))
        framework.upsince = datetime.timedelta(seconds=diff)
        return framework

    @staticmethod
    def get_json(url):
        resp = requests.get(url=url)
        json = resp.json()
        return json

    def get_frameworks(self):
        url = "http://odhecx52:5040/master/frameworks"
        data = self.get_json(url)
        frameworks = self.parse_raw_frameworks(data["frameworks"])
        return frameworks

    def get_framework_by_id(self, framework_id):
        url = "http://odhecx52:5040/master/frameworks?framework_id={}".format(framework_id)
        data = self.get_json(url)
        frameworks = self.parse_raw_frameworks(data["frameworks"])
        return frameworks


class Framework:
    """
    A class representing a framework on Mesos.
    """
    id = 0  # The ID of a framework.
    name = ""  # Framework name
    memory = None  # Memory allocated
    memory_str = None  # Memory allocated
    cpus = None  # CPU Cores.
    tasks_len = None  # Number of running tasks.
    tasks = None  # tasks of framework
    uptime = ""  # Framework registration time
    uptime_descriptive = ""  # Framework registration time since
    upsince = None
    url = ""  # The URL of framework UI.

    def print_details(self):
        """
        Prints details of the framework.
        """
        print("[{}]".format(self.name))
        print("ID: " + str(self.id))
        print("name: %s" % self.name)
        print("URL: %s" % self.url)
        print("CPUs: " + str(self.cpus) + " cores")
        print("Mem: " + self.memory_str)
        print("Tasks: " + str(self.tasks_len))
        print("Uptime %s" + self.uptime)
        print("Uptime Descriptive %s" + self.uptime_descriptive)
        print(" ")

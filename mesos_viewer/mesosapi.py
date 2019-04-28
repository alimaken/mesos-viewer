# -*- coding: utf-8 -*-
import time
import datetime
import requests
import sys

from eliot import start_action, to_file
from .framework import Framework
from .metrics import Metrics

# redirect_url = "/master/redirect"

class MesosAPI(object):
    """
    The class for parsing Mesos JSON response in to objects.
    """

    def __init__(self):
        to_file(open("mesos-viewer.log", "w"))
        # self.redirect_url = ""
        self.current_master = ""

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
    def parse_metrics(metrics_raw):

        metrics = Metrics()

        # RESOURCES

        metrics.resources_master_cpus_percent = metrics_raw["master/cpus_percent"]
        metrics.resources_master_cpus_total = metrics_raw["master/cpus_total"]
        metrics.resources_master_cpus_used = metrics_raw["master/cpus_used"]
        metrics.resources_master_mem_percent = metrics_raw["master/mem_percent"]
        metrics.resources_master_mem_total = metrics_raw["master/mem_total"]
        metrics.resources_master_mem_used = metrics_raw["master/mem_used"]

        # MESSAGES

        metrics.messages_master_messages_deactivate_framework = metrics_raw["master/messages_deactivate_framework"]
        metrics.messages_master_messages_decline_offers = metrics_raw["master/messages_decline_offers"]
        metrics.messages_master_messages_executor_to_framework = metrics_raw["master/messages_executor_to_framework"]
        metrics.messages_master_messages_exited_executor = metrics_raw["master/messages_exited_executor"]
        metrics.messages_master_messages_framework_to_executor = metrics_raw["master/messages_framework_to_executor"]
        metrics.messages_master_messages_kill_task = metrics_raw["master/messages_kill_task"]
        metrics.messages_master_messages_launch_tasks = metrics_raw["master/messages_launch_tasks"]
        metrics.messages_master_messages_register_framework = metrics_raw["master/messages_register_framework"]
        metrics.messages_master_messages_reregister_framework = metrics_raw["master/messages_reregister_framework"]
        metrics.messages_master_messages_reregister_slave = metrics_raw["master/messages_reregister_slave"]
        metrics.messages_master_messages_unregister_framework = metrics_raw["master/messages_unregister_framework"]
        metrics.messages_master_messages_unregister_slave = metrics_raw["master/messages_unregister_slave"]

        # TASKS

        if "master/task_failed/source_slave/reason_container_launch_failed" in metrics_raw:
            metrics.tasks_master_task_failed_source_slave_reason_container_launch_failed = \
                metrics_raw["master/task_failed/source_slave/reason_container_launch_failed"]
        if "master/task_failed/source_slave/reason_container_limitation_memory" in metrics_raw:
            metrics.tasks_master_task_failed_source_slave_reason_container_limitation_memory = \
                metrics_raw["master/task_failed/source_slave/reason_container_limitation_memory"]
        if "master/task_killed/source_master/reason_framework_removed" in metrics_raw:
            metrics.tasks_master_task_killed_source_master_reason_framework_removed = \
                metrics_raw["master/task_killed/source_master/reason_framework_removed"]
        if "master/task_lost/source_master/reason_slave_removed" in metrics_raw:
            metrics.tasks_master_task_lost_source_master_reason_slave_removed = \
                metrics_raw["master/task_lost/source_master/reason_slave_removed"]
        if "master/task_running/source_executor/reason_task_health_check_status_updated" in metrics_raw:
            metrics.tasks_master_task_running_source_executor_reason_task_health_check_status_updated = \
                metrics_raw["master/task_running/source_executor/reason_task_health_check_status_updated"]
        if "master/task_unreachable/source_master/reason_slave_removed" in metrics_raw:
            metrics.tasks_master_task_unreachable_source_master_reason_slave_removed = \
                metrics_raw["master/task_unreachable/source_master/reason_slave_removed"]
        metrics.tasks_master_tasks_dropped = metrics_raw["master/tasks_dropped"]
        metrics.tasks_master_tasks_error = metrics_raw["master/tasks_error"]
        metrics.tasks_master_tasks_failed = metrics_raw["master/tasks_failed"]
        metrics.tasks_master_tasks_finished = metrics_raw["master/tasks_finished"]
        metrics.tasks_master_tasks_gone = metrics_raw["master/tasks_gone"]
        metrics.tasks_master_tasks_gone_by_operator = metrics_raw["master/tasks_gone_by_operator"]
        metrics.tasks_master_tasks_killed = metrics_raw["master/tasks_killed"]
        metrics.tasks_master_tasks_killing = metrics_raw["master/tasks_killing"]
        metrics.tasks_master_tasks_lost = metrics_raw["master/tasks_lost"]
        metrics.tasks_master_tasks_running = metrics_raw["master/tasks_running"]
        metrics.tasks_master_tasks_staging = metrics_raw["master/tasks_staging"]
        metrics.tasks_master_tasks_starting = metrics_raw["master/tasks_starting"]
        metrics.tasks_master_tasks_unreachable = metrics_raw["master/tasks_unreachable"]

        # MASTER

        metrics.master_uptime_secs = metrics_raw["master/uptime_secs"]
        metrics.master_frameworks_active = metrics_raw["master/frameworks_active"]
        metrics.master_frameworks_connected = metrics_raw["master/frameworks_connected"]
        metrics.master_frameworks_disconnected = metrics_raw["master/frameworks_disconnected"]
        metrics.master_frameworks_inactive = metrics_raw["master/frameworks_inactive"]
        metrics.master_outstanding_offers = metrics_raw["master/outstanding_offers"]

        return metrics


    @staticmethod
    def get_json(url):
        try:
            resp = requests.get(url=url, timeout = 5)
            resp.raise_for_status()
            json = resp.json()
            return json
        except requests.exceptions.HTTPError as errh:
            print ("Http Error:",errh)
        except requests.exceptions.ConnectionError as errc:
            print ("Error Connecting:",errc)
        except requests.exceptions.Timeout as errt:
            print ("Timeout Error:",errt)
        except requests.exceptions.RequestException as err:
            print ("OOps: Something Else",err)
        print ("Exiting now.")
        sys.exit(1)
        

    def get_frameworks(self, url):
        with start_action(action_type="get_frameworks: get_json", url=url):
            data = self.get_json(url)
            with start_action(action_type="parse_raw_frameworks"):
                frameworks = self.parse_raw_frameworks(data["frameworks"])
                return frameworks

    def get_framework_by_id(self, url, framework_id):
        framework_url = "{}?framework_id={}".format(url, framework_id)
        data = self.get_json(framework_url)
        frameworks = self.parse_raw_frameworks(data["frameworks"])
        return frameworks

    def get_metrics(self, url):
        with start_action(action_type="get_metrics: get_json", url=url):
            data = self.get_json(url)
            with start_action(action_type="parse_metrics"):
                return self.parse_metrics(data)

    def get_url(self, host, port, url, redirect_url):
        with start_action(action_type="get_url", host=host, port=port, url=url, redirect_url=redirect_url):
            self.current_master = self.get_master("http://{}:{}{}".format(host, port, redirect_url))
            return "http://{}{}".format(self.current_master, url)

    @staticmethod
    def get_master(url):
        with start_action(action_type="get_master", url=url):
            resp = requests.get(url=url, timeout = 5, allow_redirects=False)
            return resp.headers['Location'].replace('/','')

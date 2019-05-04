# -*- coding: utf-8 -*-
from .common.helpers import Helpers as helpers


class Metrics(object):
    """
    A class representing a framework on Mesos.
    """

    def __init__(self):
        self.resources_master_cpus_percent = None
        self.resources_master_cpus_total = None
        self.resources_master_cpus_used = None
        self.resources_master_mem_percent = None
        self.resources_master_mem_total = None
        self.resources_master_mem_used = None
        self.messages_master_messages_deactivate_framework = None
        self.messages_master_messages_decline_offers = None
        self.messages_master_messages_executor_to_framework = None
        self.messages_master_messages_exited_executor = None
        self.messages_master_messages_framework_to_executor = None
        self.messages_master_messages_kill_task = None
        self.messages_master_messages_launch_tasks = None
        self.messages_master_messages_register_framework = None
        self.messages_master_messages_reregister_framework = None
        self.messages_master_messages_reregister_slave = None
        self.messages_master_messages_unregister_framework = None
        self.messages_master_messages_unregister_slave = None
        self.tasks_master_task_failed_source_slave_reason_container_launch_failed = 0
        self.tasks_master_task_failed_source_slave_reason_container_limitation_memory = 0
        self.tasks_master_task_killed_source_master_reason_framework_removed = 0
        self.tasks_master_task_lost_source_master_reason_slave_removed = 0
        self.tasks_master_task_running_source_executor_reason_task_health_check_status_updated = 0
        self.tasks_master_task_unreachable_source_master_reason_slave_removed = 0
        self.tasks_master_tasks_dropped = None
        self.tasks_master_tasks_error = None
        self.tasks_master_tasks_failed = None
        self.tasks_master_tasks_finished = None
        self.tasks_master_tasks_gone = None
        self.tasks_master_tasks_gone_by_operator = None
        self.tasks_master_tasks_killed = None
        self.tasks_master_tasks_killing = None
        self.tasks_master_tasks_lost = None
        self.tasks_master_tasks_running = None
        self.tasks_master_tasks_staging = None
        self.tasks_master_tasks_starting = None
        self.tasks_master_tasks_unreachable = None
        self.master_uptime_secs = None
        self.master_frameworks_active = None
        self.master_frameworks_connected = None
        self.master_frameworks_disconnected = None
        self.master_frameworks_inactive = None
        self.master_outstanding_offers = None

    def print_details(self):
        """
        Prints details of the framework.
        """
        print("resources_master_cpus_percent = " + str(helpers.get_percent(str(self.resources_master_cpus_percent))))
        print("resources_master_cpus_total = " + str(self.resources_master_cpus_total))
        print("resources_master_cpus_used = " + str(self.resources_master_cpus_used))
        print("resources_master_mem_percent = " + str(self.resources_master_mem_percent))
        print("resources_master_mem_total = " + str(self.resources_master_mem_total))
        print("resources_master_mem_used = " + str(self.resources_master_mem_used))
        print("messages_master_messages_deactivate_framework = " + str(self.messages_master_messages_deactivate_framework))
        print("messages_master_messages_decline_offers = " + str(self.messages_master_messages_decline_offers))
        print("messages_master_messages_executor_to_framework = " + str(self.messages_master_messages_executor_to_framework))
        print("messages_master_messages_exited_executor = " + str(self.messages_master_messages_exited_executor))
        print("messages_master_messages_framework_to_executor = " + str(self.messages_master_messages_framework_to_executor))
        print("messages_master_messages_kill_task = " + str(self.messages_master_messages_kill_task))
        print("messages_master_messages_launch_tasks = " + str(self.messages_master_messages_launch_tasks))
        print("messages_master_messages_register_framework = " + str(self.messages_master_messages_register_framework))
        print("messages_master_messages_reregister_framework = " + str(self.messages_master_messages_reregister_framework))
        print("messages_master_messages_reregister_slave = " + str(self.messages_master_messages_reregister_slave))
        print("messages_master_messages_unregister_framework = " + str(self.messages_master_messages_unregister_framework))
        print("messages_master_messages_unregister_slave = " + str(self.messages_master_messages_unregister_slave))
        print("tasks_master_task_failed_source_slave_reason_container_launch_failed = " + str(self.tasks_master_task_failed_source_slave_reason_container_launch_failed))
        print("tasks_master_task_failed_source_slave_reason_container_limitation_memory = " + str(self.tasks_master_task_failed_source_slave_reason_container_limitation_memory))
        print("tasks_master_task_killed_source_master_reason_framework_removed = " + str(self.tasks_master_task_killed_source_master_reason_framework_removed))
        print("tasks_master_task_lost_source_master_reason_slave_removed = " + str(self.tasks_master_task_lost_source_master_reason_slave_removed))
        print("tasks_master_task_running_source_executor_reason_task_health_check_status_updated = " + str(self.tasks_master_task_running_source_executor_reason_task_health_check_status_updated))
        print("tasks_master_task_unreachable_source_master_reason_slave_removed = " + str(self.tasks_master_task_unreachable_source_master_reason_slave_removed))
        print("tasks_master_tasks_dropped = " + str(self.tasks_master_tasks_dropped))
        print("tasks_master_tasks_error = " + str(self.tasks_master_tasks_error))
        print("tasks_master_tasks_failed = " + str(self.tasks_master_tasks_failed))
        print("tasks_master_tasks_finished = " + str(self.tasks_master_tasks_finished))
        print("tasks_master_tasks_gone = " + str(self.tasks_master_tasks_gone))
        print("tasks_master_tasks_gone_by_operator = " + str(self.tasks_master_tasks_gone_by_operator))
        print("tasks_master_tasks_killed = " + str(self.tasks_master_tasks_killed))
        print("tasks_master_tasks_killing = " + str(self.tasks_master_tasks_killing))
        print("tasks_master_tasks_lost = " + str(self.tasks_master_tasks_lost))
        print("tasks_master_tasks_running = " + str(self.tasks_master_tasks_running))
        print("tasks_master_tasks_staging = " + str(self.tasks_master_tasks_staging))
        print("tasks_master_tasks_starting = " + str(self.tasks_master_tasks_starting))
        print("tasks_master_tasks_unreachable = " + str(self.tasks_master_tasks_unreachable))
        print("master_uptime_secs = " + str(self.master_uptime_secs))
        print("master_frameworks_active = " + str(self.master_frameworks_active))
        print("master_frameworks_connected = " + str(self.master_frameworks_connected))
        print("master_frameworks_disconnected = " + str(self.master_frameworks_disconnected))
        print("master_frameworks_inactive = " + str(self.master_frameworks_inactive))
        print("master_outstanding_offers = " + str(self.master_outstanding_offers))
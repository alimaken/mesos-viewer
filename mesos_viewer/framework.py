
class Framework(object):
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

    def __init__(self):
        pass

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

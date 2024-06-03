# from __future__ import unicode_literals
import json
import shlex

from cwmaya.nodes.cw_submission import cwSubmission
from cwstorm.dsl.cmd import Cmd
from cwstorm.dsl.task import Task
from cwstorm.dsl.upload import Upload
from cwstorm.serializers import default as serializer

from ciocore.package_environment import PackageEnvironment
from ciocore import data as coredata

# pylint: disable=import-error
import maya.api.OpenMaya as om

MAX_FILES_PER_UPLOAD = 4


def maya_useNewAPI():
    pass


class cwSmokeSubmission(cwSubmission):
    # pass

    aWorkTask = None
    aNotifyTask = None

    id = om.MTypeId(0x880503)

    def __init__(self):
        """Initialize the class."""
        super(cwSmokeSubmission, self).__init__()

    @staticmethod
    def creator():
        return cwSmokeSubmission()

    @classmethod
    def isAbstractClass(cls):
        return False

    @classmethod
    def initialize(cls):
        """Create the static attributes."""
        om.MPxNode.inheritAttributesFrom("cwSubmission")

        cls.aWorkTask = cls.initializeTaskAttributes("wrk", "wk")
        cls.aNotifyTask = cls.initializeTaskAttributes("nfy", "nf")

    def compute(self, plug, data):
        """Compute output json from input attribs."""
        if not ((plug == self.aOutput)):
            return None

        job = self.computeJob(data)

        work_task = Task("Worker")
        work_task = self.computeCommonTask(data, self.aWorkTask, work_task)

        notify_task = Task("Notify")
        notify_task = self.computeCommonTask(data, self.aNotifyTask, notify_task)

        job.add(notify_task)
        notify_task.add(work_task)
        result = json.dumps(serializer.serialize(job))

        handle = data.outputValue(self.aOutput)
        handle.setString(result)

        data.setClean(plug)
        return self

    @classmethod
    def computeCommonTask(cls, data, attribute, task):
        """Compute the common task."""
        task_values = cls.getTaskValues(data, attribute)

        task.hardware(task_values["instance_type"])
        task.preemptible(task_values["preemptible"])
        for command in task_values["commands"]:
            task.commands(Cmd(*shlex.split(command)))
        software_list = task_values["software"]
        
        package_ids, environment = cls.get_packages_data(software_list)
        environment += task_values["environment"]
        env_dict = cls.composeEnvVars(environment)
        task.env(env_dict)
        task.packages(*package_ids)
        task.lifecycle({"minsec": 30, "maxsec": 1500})
        task.initial_state("START")
        task.output_path(task_values["output_path"])
        for uploadTask in cls.generateUploadTasks(
            task_values["extra_assets"], MAX_FILES_PER_UPLOAD
        ):
            task.add(uploadTask)
        return task

    @classmethod
    def get_packages_data(cls, software_list):
        """Get package IDs and env based on selected software.

        When making queries to the package tree, we must qualify host and plugin paths with the
        platform. The platform was previously stripped away because it was not needed in a single
        platform environment. We don't want to have the word linux next to every entry in the
        dropdown.

        * "maya 1.0.0" must be "maya 1.0.0 linux"
        * "maya 1.0.0 linux/arnold 5.0.0" must be "maya 1.0.0 linux/arnold 5.0.0 linux"
        """
        tree_data = coredata.data().get("software")

        package_ids = []
        environment = []
        print("software_list", software_list)
        for package in filter(
            None, [tree_data.find_by_path(path) for path in software_list if path]
        ):
            if package:
                package_ids.append(package["package_id"])
                for entry in package["environment"]:
                    if entry["merge_policy"].endswith("pend"):

                        environment.append(
                            {
                                "key": f"[{entry['name']}]",
                                "value": entry["value"],
                            }
                        )
                    else:
                        environment.append(
                            {
                                "key": entry["name"],
                                "value": entry["value"],
                            }
                        )
        package_ids = list(set(package_ids))
        print("package_ids", package_ids)
        return package_ids, environment

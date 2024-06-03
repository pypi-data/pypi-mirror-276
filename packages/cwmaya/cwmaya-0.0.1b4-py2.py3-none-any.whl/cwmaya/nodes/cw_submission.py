import json
import os
from cwstorm.dsl.upload import Upload

import maya.api.OpenMaya as om


from cwstorm.dsl.job import Job


def maya_useNewAPI():
    pass


class cwSubmission(om.MPxNode):
    aLabel = None
    aDescription = None
    aProjectName = None
    aMetadata = None
    aMetadataKey = None
    aMetadataValue = None
    aCurrentTime = None
    aLocationTag = None
    aAuthor = None
    aOutput = None

    id = om.MTypeId(0x880501)

    @staticmethod
    def creator():
        return cwSubmission()

    @classmethod
    def isAbstractClass(cls):
        return True

    @classmethod
    def initialize(cls):

        cls.aLabel = cls.makeStringAttribute("label", "lbl")
        cls.aDescription = cls.makeStringAttribute("description", "desc")
        cls.aProjectName = cls.makeStringAttribute("projectName", "prn")
        cls.aCurrentTime = cls.makeTimeAttribute("currentTime", "ct")
        cls.aLocationTag = cls.makeStringAttribute("location", "loc")
        cls.aAuthor = cls.makeStringAttribute("author", "ath")

        metadata = cls.makeKvPairsAttribute("metadata", "mtd")
        cls.aMetadata = metadata["compound"]
        cls.aMetadataKey = metadata["key"]
        cls.aMetadataValue = metadata["value"]

        cls.aOutput = cls.makeStringAttribute(
            "output",
            "out",
            hidden=True,
            writable=False,
            keyable=False,
            storable=False,
            readable=True,
        )

        om.MPxNode.addAttribute(cls.aLabel)
        om.MPxNode.addAttribute(cls.aDescription)
        om.MPxNode.addAttribute(cls.aProjectName)
        om.MPxNode.addAttribute(cls.aCurrentTime)
        om.MPxNode.addAttribute(cls.aLocationTag)
        om.MPxNode.addAttribute(cls.aAuthor)
        om.MPxNode.addAttribute(cls.aMetadata)

        om.MPxNode.addAttribute(cls.aOutput)

        om.MPxNode.attributeAffects(cls.aLabel, cls.aOutput)
        om.MPxNode.attributeAffects(cls.aDescription, cls.aOutput)
        om.MPxNode.attributeAffects(cls.aProjectName, cls.aOutput)
        om.MPxNode.attributeAffects(cls.aMetadata, cls.aOutput)
        om.MPxNode.attributeAffects(cls.aCurrentTime, cls.aOutput)
        om.MPxNode.attributeAffects(cls.aLocationTag, cls.aOutput)
        om.MPxNode.attributeAffects(cls.aAuthor, cls.aOutput)

    @classmethod
    def initializeTaskAttributes(cls, longPrefix, shortPrefix):
        """Create the static attributes for the export column."""
        result = {}

        result["instanceType"] = cls.makeStringAttribute(
            f"{longPrefix}InstanceType", f"{shortPrefix}it"
        )
        result["preemptible"] = cls.makeBoolAttribute(
            f"{longPrefix}Preemptible", f"{shortPrefix}pt"
        )
        result["software"] = cls.makeStringAttribute(
            f"{longPrefix}Software", f"{shortPrefix}sw", array=True
        )
        result["commands"] = cls.makeStringAttribute(
            f"{longPrefix}Commands", f"{shortPrefix}cm", array=True
        )
        environment = cls.makeKvPairsAttribute(
            f"{longPrefix}Environment", f"{shortPrefix}nv"
        )
        result["environment"] = environment["compound"]
        result["environmentKey"] = environment["key"]
        result["environmentValue"] = environment["value"]
        result["extraAssets"] = cls.makeStringAttribute(
            f"{longPrefix}ExtraAssets", f"{shortPrefix}ea", array=True
        )
        result["output_path"] = cls.makeStringAttribute(
            f"{longPrefix}OutputPath", f"{shortPrefix}op"
        )

        om.MPxNode.addAttribute(result["instanceType"])
        om.MPxNode.addAttribute(result["preemptible"])
        om.MPxNode.addAttribute(result["software"])
        om.MPxNode.addAttribute(result["commands"])
        om.MPxNode.addAttribute(result["environment"])
        om.MPxNode.addAttribute(result["extraAssets"])
        om.MPxNode.addAttribute(result["output_path"])

        om.MPxNode.attributeAffects(result["instanceType"], cls.aOutput)
        om.MPxNode.attributeAffects(result["preemptible"], cls.aOutput)
        om.MPxNode.attributeAffects(result["software"], cls.aOutput)
        om.MPxNode.attributeAffects(result["commands"], cls.aOutput)
        om.MPxNode.attributeAffects(result["environment"], cls.aOutput)
        om.MPxNode.attributeAffects(result["extraAssets"], cls.aOutput)
        om.MPxNode.attributeAffects(result["output_path"], cls.aOutput)
        return result

    @classmethod
    def makeIntAttribute(cls, attr_name, short_name, **kwargs):
        """
        Create an int attribute.
        """
        default = kwargs.get("default", 0)
        attr = om.MFnNumericAttribute()
        result = attr.create(attr_name, short_name, om.MFnNumericData.kInt, default)
        attr.writable = kwargs.get("writable", True)
        attr.keyable = kwargs.get("keyable", True)
        attr.storable = kwargs.get("storable", True)
        if "min" in kwargs:
            attr.setMin(kwargs["min"])
        if "max" in kwargs:
            attr.setMax(kwargs["max"])
        return result

    @classmethod
    def makeBoolAttribute(cls, attr_name, short_name, **kwargs):
        """
        Create a bool attribute.
        """
        default = kwargs.get("default", True)
        attr = om.MFnNumericAttribute()
        result = attr.create(attr_name, short_name, om.MFnNumericData.kBoolean, default)
        attr.writable = kwargs.get("writable", True)
        attr.keyable = kwargs.get("keyable", True)
        attr.storable = kwargs.get("storable", True)
        return result

    @classmethod
    def makeStringAttribute(cls, attr_name, short_name, **kwargs):
        attr = om.MFnTypedAttribute()
        result = attr.create(attr_name, short_name, om.MFnData.kString)
        attr.hidden = kwargs.get("hidden", False)
        attr.writable = kwargs.get("writable", True)
        attr.readable = kwargs.get("readable", True)
        attr.keyable = kwargs.get("keyable", True)
        attr.storable = kwargs.get("storable", True)
        attr.array = kwargs.get("array", False)
        return result

    @classmethod
    def makeKvPairsAttribute(cls, attr_name, short_name, **kwargs):
        cAttr = om.MFnCompoundAttribute()
        tAttr = om.MFnTypedAttribute()

        result_key = tAttr.create(
            f"{attr_name}Key", f"{short_name}k", om.MFnData.kString
        )
        result_value = tAttr.create(
            f"{attr_name}Value", f"{short_name}v", om.MFnData.kString
        )
        result_compound = cAttr.create(attr_name, short_name)
        cAttr.hidden = kwargs.get("hidden", False)
        cAttr.writable = kwargs.get("writable", True)
        cAttr.array = True
        cAttr.addChild(result_key)
        cAttr.addChild(result_value)
        return {"compound": result_compound, "key": result_key, "value": result_value}

    @classmethod
    def makeTimeAttribute(cls, attr_name, short_name, **kwargs):
        attr = om.MFnUnitAttribute()
        result = attr.create(attr_name, short_name, om.MFnUnitAttribute.kTime)
        attr.writable = kwargs.get("writable", True)
        attr.keyable = kwargs.get("keyable", True)
        attr.storable = kwargs.get("storable", True)
        return result

    def compute(self, plug, data):
        pass
        """Compute output json from input attribs."""
        if not ((plug == self.aOutput)):
            return None

    # INDIFIDUAL JOB ACCESSOR METHODS
    @classmethod
    def getDescription(cls, data):
        return data.inputValue(cls.aDescription).asString()

    @classmethod
    def getLabel(cls, data):
        return data.inputValue(cls.aLabel).asString()

    @classmethod
    def getProjectName(cls, data):
        return data.inputValue(cls.aProjectName).asString()

    @classmethod
    def getMetadata(cls, data):
        metadata = {}
        array_handle = data.inputArrayValue(cls.aMetadata)
        while not array_handle.isDone():
            key = array_handle.inputValue().child(cls.aMetadataKey).asString().strip()
            value = (
                array_handle.inputValue().child(cls.aMetadataValue).asString().strip()
            )
            metadata[key] = value
            array_handle.next()
        return metadata

    @classmethod
    def getCurrentTime(cls, data):
        return data.inputValue(cls.aCurrentTime).asTime().asUnits(om.MTime.uiUnit())

    @classmethod
    def getLocation(cls, data):
        return data.inputValue(cls.aLocationTag).asString()

    @classmethod
    def getAuthor(cls, data):
        return data.inputValue(cls.aAuthor).asString()

    #################

    # TASK ACCESSOR METHOD
    @classmethod
    def getTaskValues(cls, data, aTask):
        result = {}
        # result["perTask"] = data.inputValue(aTask["perTask"]).asInt()

        result["instance_type"] = data.inputValue(aTask["instanceType"]).asString()
        result["preemptible"] = data.inputValue(aTask["preemptible"]).asBool()
        
        result["output_path"] = data.inputValue(aTask["output_path"]).asString()

        result["software"] = []
        array_handle = data.inputArrayValue(aTask["software"])
        while not array_handle.isDone():
            software = array_handle.inputValue().asString().strip()
            if software:
                result["software"].append(software)
            array_handle.next()

        result["commands"] = []
        array_handle = data.inputArrayValue(aTask["commands"])
        while not array_handle.isDone():
            cmd = array_handle.inputValue().asString().strip()
            if cmd:
                result["commands"].append(cmd)
            array_handle.next()

        result["environment"] = []
        array_handle = data.inputArrayValue(aTask["environment"])
        while not array_handle.isDone():
            key = (
                array_handle.inputValue()
                .child(aTask["environmentKey"])
                .asString()
                .strip()
            )
            value = (
                array_handle.inputValue()
                .child(aTask["environmentValue"])
                .asString()
                .strip()
            )
            if key and value:
                result["environment"].append({"key": key, "value": value})
            array_handle.next()

        result["extra_assets"] = []
        array_handle = data.inputArrayValue(aTask["extraAssets"])
        while not array_handle.isDone():
            path = array_handle.inputValue().asString().strip()
            if path:
                result["extra_assets"].append(path)
            array_handle.next()
            
 
    
        return result

    @classmethod
    def getJobValues(cls, data):
        result = {}
        result["label"] = cls.getLabel(data) or None
        result["description"] = cls.getDescription(data)
        result["project_name"] = cls.getProjectName(data)
        result["metadata"] = cls.getMetadata(data)
        result["current_time"] = cls.getCurrentTime(data)
        result["location"] = cls.getLocation(data)
        result["author"] = cls.getAuthor(data)
        return result

    @staticmethod
    def composeEnvVars(env_vars):
        """
        Processes a list of environment variables and composes a dictionary of key-value pairs.

        The function handles keys both with and without square brackets:
        - If a key is enclosed in square brackets and already exists in the result dictionary,
        the new value is concatenated to the existing value using a colon as a separator.
        - If a key is enclosed in square brackets and does not exist in the result dictionary,
        it is added without the brackets.
        - If a key is not enclosed in brackets, it is added to the dictionary directly, and any
        existing value under the same key is overwritten.

        Args:
            env_vars (list of dict): A list of dictionaries where each dictionary has a 'key' and 'value'
                                    indicating the environment variable's name and value respectively.

        Returns:
            dict: A dictionary with environment variable keys as dictionary keys and the corresponding values.
                If keys are enclosed in brackets and repeated, their values are concatenated.

        Example:
            >>> composeEnvVars([{"key": "[PATH]", "value": "/usr/bin"}, {"key": "[PATH]", "value": "/bin"}])
            {'PATH': '/usr/bin:/bin'}
            >>> composeEnvVars([{"key": "USER", "value": "root"}, {"key": "SHELL", "value": "/bin/bash"}])
            {'USER': 'root', 'SHELL': '/bin/bash'}
        """
        result = {}
        for env_var in env_vars:
            key = env_var["key"]
            value = env_var["value"]

            if key.startswith("[") and key.endswith("]"):
                stripped_key = key[1:-1]
                if stripped_key in result:
                    result[stripped_key] = f"{result[stripped_key]}:{value}"
                else:
                    result[stripped_key] = value
            else:
                result[key] = value

        return result

    @classmethod
    def generateUploadTasks(cls, files, max_files_per_upload=10):
        """Generate the upload tasks."""
        for i in range(0, len(files), max_files_per_upload):
            u = Upload()
            for f in files[i : i + max_files_per_upload]:
                path = f.strip()
                size = os.path.getsize(path)
                u.push_files({"path": path, "size": size})
            yield u

 


    # Helper functions to compute the job and tasks
    @classmethod
    def computeJob(cls, data):
        """Compute the job."""
        job_values = cls.getJobValues(data)
        job = Job(job_values["label"])
        job.metadata(job_values["metadata"])
        job.project(job_values["project_name"])
        job.comment(job_values["description"])
        job.author(job_values["author"])
        job.location(job_values["location"])
        return job

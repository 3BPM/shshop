#!/usr/bin/env python
# -*- coding:utf-8 -*-
from apps.web import models


class BaseDeploy(object):
    def __init__(self, parent=None):
        self.parent = parent


class StartDeploy(BaseDeploy):
    text = '开始'

    def initial(self):
        start_object = models.Diagram.objects.create(task=task_object, text=self.text)

    def deploy(self):
        pass


class DownloadDeploy(BaseDeploy):
    text = '下载'

    def initial(self):
        pass

    def deploy(self):
        pass


class ZipDeploy(BaseDeploy):
    text = '打包'

    def initial(self):
        pass

    def deploy(self):
        pass


class ServerDeploy(BaseDeploy):
    text = '开始'

    def initial(self):
        pass

    def deploy(self):
        pass


class DeployFactory(object):
    def __init__(self, task_object):
        self.task_object = task_object
        self.deploy_object_list = [StartDeploy(), DownloadDeploy()]

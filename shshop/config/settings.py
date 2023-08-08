#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件    :sh.py
@说明    :默认配置文件
@时间    :2023/02/20 11:18:49
@作者    :幸福关中&轻编程
@版本    :1.0
@微信    :baywanyun
'''

"""
本项目的默认配置项都设置在 SH_SHOP 的设置字典中！
例如，需要覆盖本项目的默认配置,只需要在django项目的默认settings.py文件中配置如下：
SH_SHOP = {
    'SH_TITLE': 'ShShop我爱你！'
}

这样便会覆盖掉默认的配置，实现自定义配置的功能！

该模块提供了一个`sh_settings`的实例化对象，用于访问SH_SHOP中的设置，先检查用户设置，再回退到默认设置！

"""


from django.conf import settings
from django.test.signals import setting_changed
from shshop.config.defaults import SH_DEFAULTS


class ShSettings:

    """
    一个设置对象，允许 SH_SHOP 设置在项目中随意加载。
    例如需要引用配置中的项，如下：

        from shshop.conf.sh import sh_settings
        print(sh_settings.SH_TITLE)

    备注：这是一个仅与命名空间设置兼容的内部类在 SH_SHOP 名称下。
    """

    def __init__(self, user_settings=None, defaults=None) -> None:
        self.defaults = defaults or SH_DEFAULTS
        self._cached_attrs = set()

    @property
    def user_settings(self):
        if not hasattr('self', '_user_settings'):
            self._user_settings = getattr(settings, 'SH_SHOP', {})
        return self._user_settings

    def __getattr__(self, attr):

        if attr not in self.defaults:
            raise AttributeError("Invalid API setting: '%s'" % attr)

        try:
            val = self.user_settings[attr]
        except KeyError:
            val = self.defaults[attr]
        self._cached_attrs.add(attr)
        setattr(self, attr, val)
        return val

    def reload(self):
        for attr in self._cached_attrs:
            delattr(self, attr)
        self._cached_attrs.clear()
        if hasattr(self, '_user_settings'):
            delattr(self, '_user_settings')


sh_settings = ShSettings(None, SH_DEFAULTS)


def reload_sh_settings(*args, **kwargs):
    setting = kwargs['setting']
    if setting == 'SH_SHOP':
        sh_settings.reload()


setting_changed.connect(reload_sh_settings)
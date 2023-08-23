#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件    :push.py
@说明    :项目初始化命令
@时间    :2023/03/20 09:42:43
@作者    :幸福关中&轻编程
@版本    :1.0
@微信    :baywanyun
'''


from django.core.management.base import BaseCommand
from django.contrib.auth.models import Permission
from django.core import management
from django.conf import settings

from shshop.models import ShPermission, ShMenu


class Command(BaseCommand):

    """ 项目初始化命令
    @params push
        python manage.py push   导入后台自定义菜单
    @params push -test
        python manage.py push -test   导入后台自定义菜单及演示数据
    """

    help = '初始化后台管理菜单以及导入测试数据'

    def add_arguments(self, parser):
        parser.add_argument('-test', '--test', action='store_true', help="导入演示数据")
        parser.add_argument('-nb', '--nb', action='store_true', help="导入演示数据1")

    def handle(self, *args, **options):
        menus_json = f"{settings.BASE_DIR}/shshop/config/db/shmenu.json"
        management.call_command('loaddata', menus_json, verbosity=0)
        menus = ShMenu.objects.all()
        perms = Permission.objects.all()
        for perm in perms:
            if perm.codename in ['view_shshopcategory', 'view_shshopspec', 'view_shshopspu', 'view_shbanner']:
                ShPermission.objects.update_or_create(permission=perm, menus=menus.filter(name="商城").first(), defaults={'permission': perm})
            elif perm.codename in ['view_group', 'view_user', 'view_shmenu', 'view_logentry']:
                ShPermission.objects.update_or_create(permission=perm, menus=menus.filter(name="认证和授权").first(), defaults={'permission': perm})
            elif perm.codename in ['view_shshoporderinfo']:
                ShPermission.objects.update_or_create(permission=perm, menus=menus.filter(name="订单").first(), defaults={'permission': perm})
            elif perm.codename in ['view_flatpage', 'view_site', 'view_sharticle', 'view_sharticlecategory']:
                ShPermission.objects.update_or_create(permission=perm, menus=menus.filter(name="内容").first(), defaults={'permission': perm})
                flatpage_json = f"{settings.BASE_DIR}/shshop/config/db/flatpage.json"
                management.call_command('loaddata', flatpage_json, verbosity=0)
        self.stdout.write(self.style.SUCCESS('Successfully "%s"' % 'push shadmin menus'))

        if options['test']:
            banners_json = f"{settings.BASE_DIR}/shshop/config/db/shbanner.json"
            management.call_command('loaddata', banners_json, verbosity=0)
            category_json = f"{settings.BASE_DIR}/shshop/config/db/shshopcategory.json"
            management.call_command('loaddata', category_json, verbosity=0)

            spec_json = f"{settings.BASE_DIR}/shshop/config/db/shshopspec.json"
            specoption_json = f"{settings.BASE_DIR}/shshop/config/db/shshopspecoption.json"
            spu_json = f"{settings.BASE_DIR}/shshop/config/db/shshopspu.json"
            spucarousel_json = f"{settings.BASE_DIR}/shshop/config/db/shspucarousel.json"
            sku_json = f"{settings.BASE_DIR}/shshop/config/db/shshopsku.json"
            # flatpage_json = f"{settings.BASE_DIR}/shshop/config/db/flatpage.json"

            management.call_command('loaddata', spec_json, verbosity=0)
            management.call_command('loaddata', specoption_json, verbosity=0)
            management.call_command('loaddata', spu_json, verbosity=0)
            management.call_command('loaddata', spucarousel_json, verbosity=0)
            management.call_command('loaddata', sku_json, verbosity=0)
        if options['nb']:
            nbjson = f"{settings.BASE_DIR}/1.json"
            management.call_command('loaddata', nbjson, verbosity=0)
            # management.call_command('loaddata', flatpage_json, verbosity=0)
            self.stdout.write(self.style.SUCCESS('Successfully "%s"' % 'push shshop test data'))

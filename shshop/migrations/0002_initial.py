# Generated by Django 4.2.2 on 2023-08-22 15:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import shshop.public.tinymce


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0012_alter_user_first_name_max_length'),
        ('contenttypes', '0002_remove_content_type_name'),
        ('shshop', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GoodPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_date', models.DateTimeField(auto_now_add=True)),
                ('pub_date', models.DateTimeField(auto_now=True)),
                ('is_del', models.BooleanField(default=False, editable=False)),
            ],
            options={
                'verbose_name': '推送商品',
            },
        ),
        migrations.CreateModel(
            name='ShArticleCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_date', models.DateTimeField(auto_now_add=True)),
                ('pub_date', models.DateTimeField(auto_now=True)),
                ('is_del', models.BooleanField(default=False, editable=False)),
                ('name', models.CharField(max_length=50, verbose_name='分类名称')),
                ('icon', models.CharField(blank=True, default='', max_length=50, verbose_name='分类icon')),
                ('img_map', models.ImageField(blank=True, help_text='图片尺寸为600 X 480', max_length=200, null=True, upload_to='category/imgMap/%Y', verbose_name='推荐图')),
                ('desc', models.CharField(blank=True, default='', max_length=150, verbose_name='分类描述')),
            ],
            options={
                'verbose_name': '用户消息分类',
                'verbose_name_plural': '用户消息分类',
                'ordering': ['-add_date'],
            },
        ),
        migrations.CreateModel(
            name='ShArticleTags',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_date', models.DateTimeField(auto_now_add=True)),
                ('pub_date', models.DateTimeField(auto_now=True)),
                ('is_del', models.BooleanField(default=False, editable=False)),
                ('name', models.CharField(max_length=50, verbose_name='名称')),
            ],
            options={
                'verbose_name': '用户消息标签',
                'verbose_name_plural': '用户消息标签',
                'ordering': ['-add_date'],
            },
        ),
        migrations.CreateModel(
            name='ShBanner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_date', models.DateTimeField(auto_now_add=True)),
                ('pub_date', models.DateTimeField(auto_now=True)),
                ('is_del', models.BooleanField(default=False, editable=False)),
                ('img', models.ImageField(max_length=200, upload_to='carousel/%Y/%m', verbose_name='轮播图')),
                ('target_url', models.CharField(blank=True, default='', max_length=200, verbose_name='跳转链接')),
                ('desc', models.CharField(blank=True, default='', max_length=150, verbose_name='描述')),
            ],
            options={
                'verbose_name': '轮播图管理',
                'verbose_name_plural': '轮播图管理',
            },
        ),
        migrations.CreateModel(
            name='ShIPAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_date', models.DateTimeField(auto_now_add=True)),
                ('pub_date', models.DateTimeField(auto_now=True)),
                ('is_del', models.BooleanField(default=False, editable=False)),
                ('ip', models.GenericIPAddressField(blank=True, null=True)),
                ('browser', models.TextField(blank=True, default='', max_length=500)),
                ('address', models.CharField(blank=True, default='', max_length=150)),
            ],
            options={
                'verbose_name': 'ShStatsIPAddress',
                'verbose_name_plural': 'ShStatsIPAddress',
            },
        ),
        migrations.CreateModel(
            name='ShMenu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_date', models.DateTimeField(auto_now_add=True)),
                ('pub_date', models.DateTimeField(auto_now=True)),
                ('is_del', models.BooleanField(default=False, editable=False)),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='菜单名称')),
                ('sort', models.PositiveSmallIntegerField(default=1, verbose_name='排序')),
                ('parent', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='shshop.shmenu')),
            ],
            options={
                'verbose_name': '菜单',
                'verbose_name_plural': '菜单',
                'ordering': ['-sort'],
            },
        ),
        migrations.CreateModel(
            name='ShShopCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_date', models.DateTimeField(auto_now_add=True)),
                ('pub_date', models.DateTimeField(auto_now=True)),
                ('is_del', models.BooleanField(default=False, editable=False)),
                ('name', models.CharField(max_length=50, verbose_name='分类名称')),
                ('icon', models.CharField(blank=True, default='', max_length=50, verbose_name='分类icon')),
                ('img_map', models.ImageField(blank=True, help_text='图片尺寸为600 X 480', max_length=200, null=True, upload_to='category/imgMap/%Y', verbose_name='推荐图')),
                ('desc', models.CharField(blank=True, default='', max_length=150, verbose_name='分类描述')),
                ('is_home', models.BooleanField(default=False, help_text='如果为True则推荐到首页楼层及出现在导航菜单', verbose_name='是否推荐')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='shshop.shshopcategory')),
            ],
            options={
                'verbose_name': '商品分类',
                'verbose_name_plural': '商品分类',
                'ordering': ['-add_date'],
            },
        ),
        migrations.CreateModel(
            name='ShShopOrderInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_date', models.DateTimeField(auto_now_add=True)),
                ('pub_date', models.DateTimeField(auto_now=True)),
                ('is_del', models.BooleanField(default=False, editable=False)),
                ('order_sn', models.CharField(blank=True, default='', editable=False, help_text='订单号', max_length=32, unique=True, verbose_name='订单号')),
                ('trade_sn', models.CharField(blank=True, editable=False, help_text='交易号', max_length=64, null=True, unique=True, verbose_name='交易号')),
                ('pay_status', models.IntegerField(choices=[(1, '待支付'), (2, '待发货'), (3, '待收货'), (4, '待评价'), (5, '已完成'), (6, '已取消')], default=1, help_text='支付状态', verbose_name='支付状态')),
                ('pay_method', models.IntegerField(blank=True, choices=[(1, '货到付款'), (2, '支付宝'), (3, '微信支付'), (4, '余额支付')], editable=False, help_text='支付方式', null=True, verbose_name='支付方式')),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='商品总金额')),
                ('order_mark', models.CharField(blank=True, default='', help_text='订单备注', max_length=100, verbose_name='订单备注')),
                ('name', models.CharField(default='', max_length=50, verbose_name='签收人')),
                ('phone', models.CharField(default='', max_length=11, verbose_name='手机号')),
                ('email', models.EmailField(blank=True, default='', max_length=50, verbose_name='邮箱')),
                ('address', models.CharField(max_length=200, verbose_name='地址')),
                ('pay_time', models.DateTimeField(blank=True, editable=False, help_text='支付时间', null=True, verbose_name='支付时间')),
                ('owner', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': '订单信息',
                'verbose_name_plural': '订单信息',
            },
        ),
        migrations.CreateModel(
            name='ShShopSpec',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_date', models.DateTimeField(auto_now_add=True)),
                ('pub_date', models.DateTimeField(auto_now=True)),
                ('is_del', models.BooleanField(default=False, editable=False)),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='规格')),
            ],
            options={
                'verbose_name': '发布区域',
                'verbose_name_plural': '发布区域',
            },
        ),
        migrations.CreateModel(
            name='ShShopSPU',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_date', models.DateTimeField(auto_now_add=True)),
                ('pub_date', models.DateTimeField(auto_now=True)),
                ('is_del', models.BooleanField(default=False, editable=False)),
                ('title', models.CharField(max_length=150, verbose_name='商品名称')),
                ('keywords', models.CharField(blank=True, default='', max_length=150, verbose_name='商品关键字')),
                ('desc', models.CharField(blank=True, default='', max_length=200, verbose_name='商品描述')),
                ('unit', models.CharField(max_length=50, verbose_name='单位')),
                ('cover_pic', models.ImageField(max_length=200, upload_to='product/cover/spu/%Y/%m', verbose_name='封面图')),
                ('freight', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=5, verbose_name='运费')),
                ('content', shshop.public.tinymce.TinymceField(blank=True, tinymce={'automatic_uploads': True, 'browser_spellcheck': True, 'contextmenu': False, 'file_picker_types': 'file image media', 'image_title': False, 'images_file_types': 'jpg,svg,webp,png,gif', 'images_reuse_filename': True, 'images_upload_url': '/upload/tinymce/', 'plugins': ['advlist', 'autolink', 'link', 'image', 'lists', 'charmap', 'preview', 'anchor', 'pagebreak', 'searchreplace', 'wordcount', 'visualblocks', 'visualchars', 'code', 'fullscreen', 'insertdatetime', 'media', 'table', 'emoticons', 'template', 'help'], 'toolbar': 'undo redo | styles | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | link image | print preview media | forecolor backcolor emoticons'}, verbose_name='商品详情')),
                ('category', models.ManyToManyField(to='shshop.shshopcategory', verbose_name='商品分类')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': '商品管理',
                'verbose_name_plural': '商品管理',
                'ordering': ['-add_date'],
            },
        ),
        migrations.CreateModel(
            name='ShUpload',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_date', models.DateTimeField(auto_now_add=True)),
                ('pub_date', models.DateTimeField(auto_now=True)),
                ('is_del', models.BooleanField(default=False, editable=False)),
                ('img', models.ImageField(max_length=200, upload_to='upload/editor/')),
            ],
            options={
                'verbose_name': '富文本编辑器图片上传',
                'verbose_name_plural': '富文本编辑器图片上传',
            },
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_date', models.DateTimeField(auto_now_add=True)),
                ('pub_date', models.DateTimeField(auto_now=True)),
                ('is_del', models.BooleanField(default=False, editable=False)),
                ('avatar', models.ImageField(blank=True, default='avatar/default.jpg', max_length=200, upload_to='avatar/', verbose_name='头像')),
                ('nickname', models.CharField(blank=True, default='', max_length=30, verbose_name='昵称')),
                ('desc', models.CharField(blank=True, default='', max_length=150, verbose_name='描述')),
                ('phone', models.CharField(blank=True, max_length=11, null=True, unique=True, verbose_name='手机号')),
                ('balance', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=8, verbose_name='余额')),
                ('owner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': '用户',
                'verbose_name_plural': '用户',
            },
        ),
        migrations.CreateModel(
            name='ShUserBalanceLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_date', models.DateTimeField(auto_now_add=True)),
                ('pub_date', models.DateTimeField(auto_now=True)),
                ('is_del', models.BooleanField(default=False, editable=False)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='金额')),
                ('change_status', models.PositiveSmallIntegerField(blank=True, choices=[(1, '增加'), (2, '支出')], null=True)),
                ('change_way', models.PositiveSmallIntegerField(choices=[(1, '线上充值'), (2, '管理员手动更改'), (3, '余额抵扣商品')], default=2)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': '余额明细',
                'verbose_name_plural': '余额明细',
            },
        ),
        migrations.CreateModel(
            name='ShStats',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_date', models.DateTimeField(auto_now_add=True)),
                ('pub_date', models.DateTimeField(auto_now=True)),
                ('is_del', models.BooleanField(default=False, editable=False)),
                ('object_id', models.PositiveIntegerField()),
                ('pv', models.BigIntegerField(default=0)),
                ('uv', models.BigIntegerField(default=0)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
            ],
            options={
                'verbose_name': 'ShStats',
                'verbose_name_plural': 'ShStatss',
            },
        ),
        migrations.CreateModel(
            name='ShSPUCarousel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_date', models.DateTimeField(auto_now_add=True)),
                ('pub_date', models.DateTimeField(auto_now=True)),
                ('is_del', models.BooleanField(default=False, editable=False)),
                ('img', models.ImageField(max_length=200, upload_to='carousel/%Y/%m', verbose_name='轮播图')),
                ('target_url', models.CharField(blank=True, default='', max_length=200, verbose_name='跳转链接')),
                ('desc', models.CharField(blank=True, default='', max_length=150, verbose_name='描述')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='shshop.shshopspu')),
            ],
            options={
                'verbose_name': 'ShSPUCarousel',
                'verbose_name_plural': 'ShSPUCarousels',
            },
        ),
        migrations.CreateModel(
            name='ShShopSpecOption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_date', models.DateTimeField(auto_now_add=True)),
                ('pub_date', models.DateTimeField(auto_now=True)),
                ('is_del', models.BooleanField(default=False, editable=False)),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='规格值')),
                ('spec', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='shshop.shshopspec', verbose_name='规格')),
            ],
            options={
                'verbose_name': '规格值',
                'verbose_name_plural': '规格值',
            },
        ),
        migrations.CreateModel(
            name='ShShopSKU',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_date', models.DateTimeField(auto_now_add=True)),
                ('pub_date', models.DateTimeField(auto_now=True)),
                ('is_del', models.BooleanField(default=False, editable=False)),
                ('cover_pic', models.ImageField(max_length=200, upload_to='cover/sku/%Y/%m', verbose_name='封面图')),
                ('price', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='售价')),
                ('cost_price', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='成本价')),
                ('org_price', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='原价')),
                ('stock', models.IntegerField(default=0, verbose_name='库存')),
                ('sales', models.PositiveIntegerField(default=0, editable=False, verbose_name='销量')),
                ('numname', models.CharField(blank=True, default='', max_length=50, verbose_name='商品成色')),
                ('weight', models.FloatField(blank=True, default=0, verbose_name='重量(KG)')),
                ('vol', models.FloatField(blank=True, default=0, verbose_name='体积(m³)')),
                ('options', models.ManyToManyField(blank=True, to='shshop.shshopspecoption', verbose_name='发布区域')),
                ('spu', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='shshop.shshopspu', verbose_name='商品')),
            ],
            options={
                'verbose_name': 'ShShopSKU',
                'verbose_name_plural': 'ShShopSKUs',
            },
        ),
        migrations.CreateModel(
            name='ShShopOrderSKU',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_date', models.DateTimeField(auto_now_add=True)),
                ('pub_date', models.DateTimeField(auto_now=True)),
                ('is_del', models.BooleanField(default=False, editable=False)),
                ('title', models.CharField(blank=True, default='', max_length=200, verbose_name='商品标题')),
                ('desc', models.CharField(blank=True, default='', max_length=200, verbose_name='商品说明')),
                ('spec', models.CharField(blank=True, default='', max_length=200, verbose_name='发布区域')),
                ('content', models.TextField(blank=True, default='', verbose_name='商品详情')),
                ('count', models.IntegerField(default=1, verbose_name='数量')),
                ('price', models.DecimalField(decimal_places=2, max_digits=18, verbose_name='单价')),
                ('is_commented', models.BooleanField(default=False, verbose_name='是否已评价')),
                ('order', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='shshop.shshoporderinfo', verbose_name='订单')),
                ('sku', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, to='shshop.shshopsku', verbose_name='订单商品')),
            ],
            options={
                'verbose_name': '订单商品',
                'verbose_name_plural': '订单商品',
            },
        ),
        migrations.CreateModel(
            name='ShShopingCart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_date', models.DateTimeField(auto_now_add=True)),
                ('pub_date', models.DateTimeField(auto_now=True)),
                ('is_del', models.BooleanField(default=False, editable=False)),
                ('num', models.PositiveIntegerField(default=0, verbose_name='数量')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
                ('sku', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='shshop.shshopsku', verbose_name='商品sku')),
            ],
            options={
                'verbose_name': '购物车',
                'verbose_name_plural': '购物车',
            },
        ),
        migrations.CreateModel(
            name='ShShopAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_date', models.DateTimeField(auto_now_add=True)),
                ('pub_date', models.DateTimeField(auto_now=True)),
                ('is_del', models.BooleanField(default=False, editable=False)),
                ('name', models.CharField(max_length=50, verbose_name='签收人')),
                ('phone', models.CharField(max_length=11, verbose_name='手机号')),
                ('email', models.EmailField(blank=True, default='', max_length=50, verbose_name='邮箱')),
                ('province', models.CharField(max_length=150, verbose_name='省')),
                ('city', models.CharField(max_length=150, verbose_name='市')),
                ('county', models.CharField(max_length=150, verbose_name='区/县')),
                ('address', models.CharField(max_length=150, verbose_name='详细地址')),
                ('is_default', models.BooleanField(default=False, verbose_name='设为默认')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': '收货地址',
                'verbose_name_plural': '收货地址',
            },
        ),
        migrations.CreateModel(
            name='ShPermission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_date', models.DateTimeField(auto_now_add=True)),
                ('pub_date', models.DateTimeField(auto_now=True)),
                ('is_del', models.BooleanField(default=False, editable=False)),
                ('url', models.CharField(blank=True, default='', editable=False, max_length=150, verbose_name='url')),
                ('icon', models.CharField(blank=True, default='', max_length=50)),
                ('is_show', models.BooleanField(default=True)),
                ('menus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shshop.shmenu')),
                ('permission', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='auth.permission', verbose_name='权限')),
            ],
            options={
                'verbose_name': '菜单权限',
                'verbose_name_plural': '菜单权限',
            },
        ),
        migrations.CreateModel(
            name='ShOrderInfoComments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_date', models.DateTimeField(auto_now_add=True)),
                ('pub_date', models.DateTimeField(auto_now=True)),
                ('is_del', models.BooleanField(default=False, editable=False)),
                ('object_id', models.PositiveIntegerField()),
                ('content', models.CharField(max_length=200, verbose_name='留言内容')),
                ('comment_choices', models.PositiveSmallIntegerField(choices=[(5, '好评'), (3, '中评'), (1, '差评')], default=5, verbose_name='评分')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': '商品评价',
                'verbose_name_plural': '商品评价',
                'ordering': ['-add_date'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ShArticle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_date', models.DateTimeField(auto_now_add=True)),
                ('pub_date', models.DateTimeField(auto_now=True)),
                ('is_del', models.BooleanField(default=False, editable=False)),
                ('title', models.CharField(max_length=150, verbose_name='标题')),
                ('desc', models.CharField(blank=True, default='', max_length=200, verbose_name='描述')),
                ('keywords', models.CharField(blank=True, default='', max_length=200, verbose_name='关键字')),
                ('content', shshop.public.tinymce.TinymceField(tinymce={'automatic_uploads': True, 'browser_spellcheck': True, 'contextmenu': False, 'file_picker_types': 'file image media', 'image_title': False, 'images_file_types': 'jpg,svg,webp,png,gif', 'images_reuse_filename': True, 'images_upload_url': '/upload/tinymce/', 'plugins': ['advlist', 'autolink', 'link', 'image', 'lists', 'charmap', 'preview', 'anchor', 'pagebreak', 'searchreplace', 'wordcount', 'visualblocks', 'visualchars', 'code', 'fullscreen', 'insertdatetime', 'media', 'table', 'emoticons', 'template', 'help'], 'toolbar': 'undo redo | styles | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | link image | print preview media | forecolor backcolor emoticons'}, verbose_name='内容')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shshop.sharticlecategory', verbose_name='用户消息分类')),
                ('owner', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('tags', models.ManyToManyField(blank=True, to='shshop.sharticletags', verbose_name='标签')),
            ],
            options={
                'verbose_name': '用户消息',
                'verbose_name_plural': '用户消息',
                'ordering': ['-add_date'],
            },
        ),
        migrations.AddConstraint(
            model_name='shshopingcart',
            constraint=models.UniqueConstraint(fields=('owner', 'sku'), name='unique_owner_sku'),
        ),
        migrations.AddIndex(
            model_name='shorderinfocomments',
            index=models.Index(fields=['content_type', 'object_id'], name='shshop_shor_content_4121b0_idx'),
        ),
    ]

from django.conf import settings
from django.urls import reverse

SH_DEFAULTS = {

    # LOGO
    "LOGO_URL": "/static/shshop/img/logo.png",

    # 搜索框默认搜索词
    "SEARCH_VALUE": "请输入搜索词...",

    # 手机号验证正则
    "PHONE_REGX": r"^1[35678]\d{9}$",

    # PC商城登陆成功后跳转地址
    "NEXT_PAGE": "shshop:home",

    # 首页楼层显示商品数量
    "HOME_GOODS_COUNT": 10,

    # 商品列表页每页显示个数
    "GOODS_PAGINATE_BY": 24,

    # 商品列表页最后一页剩余几个
    # 自动添加到上一页的个数，该值必须小于分页值
    "GOODS_PAGINATE_ORPHANS": 4,

    # 商品详情页评论每页显示数量
    "DETAIL_COMMENTS_PAGINATE_BY": 24,

    # 管理后台是否启用自定义菜单
    "ADMIN_MENUS": True,

    # 后台logo文字
    "SITE_HEADER": "SH后台管理",

    # 后台title后缀
    "SITE_TITLE": "二手商城",



    # 用户中心订单列表数量，必须大于2
    "USER_ORDERINFO_PAGINATE_BY": 5,

    # 热销显示数量
    "HOT_SPUS_LEN": 4,

    # 统计pv的间隔时间，即同一个访问者多长时间内多次刷新只记录一次pv
    "PV_TIMEOUT": 1 * 60,  # 一分钟
    # 统计uv的间隔时间，24小时内多次访问只记录一次
    "UV_TIMEOUT": 24 * 60 * 60,  # 24小时

    # tinymce富文本编辑器默认配置
    # https://www.tiny.cloud/docs/tinymce/6/basic-setup/
    "FILE_PATH": "upload/",
    # <script src="https://cdn.tiny.cloud/1/no-api-key/tinymce/6/tinymce.min.js" referrerpolicy="origin"></script>
    "TINYMCE_CDN": False,
    "TINYMCE_API_KEY": "no-api-key",  # 当TINYMCE_CDN未True时，必须设置该项为你的api-key,否则不能正确加载
    "TINYMCE_DEFAULTS": {
        # 向用户展开展示的工具栏
        'toolbar':
        'undo redo | styles | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | link image | print preview media | forecolor backcolor emoticons',
        # 选择要在加载时包含的插件
        'plugins': [
            'advlist', 'autolink', 'link', 'image', 'lists', 'charmap', 'preview', 'anchor', 'pagebreak', 'searchreplace', 'wordcount', 'visualblocks', 'visualchars', 'code', 'fullscreen',
            'insertdatetime', 'media', 'table', 'emoticons', 'template', 'help'
        ],
        "browser_spellcheck":
        True,
        "contextmenu":
        False,
        'image_title':
        False,
        'automatic_uploads':
        True,
        'images_file_types':
        'jpg,svg,webp,png,gif',
        'file_picker_types':
        'file image media',
        'images_upload_url':
        '/upload/tinymce/',
        'images_reuse_filename':
        True,  # 是否开启每次为文件生成唯一名称
    },

    # 是否开启邮件通知
    'HAS_MESSAGE_EAMIL': True
}
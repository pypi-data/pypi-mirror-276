defaultDriver = 'diskcache'  # 数据库类型
diskcache = {
    'connect': 'default',  # 默认链接
    'default': {
        'path': 'diskcache',  # 想对于runtime
        'size_limit': 100 * 1024 * 1024
    }
}

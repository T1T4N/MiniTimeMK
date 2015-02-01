routes_in = (
    ('/', '/MiniTimeMK/default/index'),
    ('/index', '/MiniTimeMK/default/index'),
    ('/update', '/MiniTimeMK/default/update'),
    ('/index_static', '/MiniTimeMK/static/index.html'),
    ('/(?P<any>crna_hronika|ekonomija|kultura|makedonija|skopje|sport|svet|tehnologija|zabava|zivot)',
     '/MiniTimeMK/static/\g<any>.html'),
)
routes_out = (
    ('/MiniTimeMK/default/index', '/'),
    ('/MiniTimeMK/default/index', '/index'),
    ('/MiniTimeMK/default/update', '/update'),
    ('/MiniTimeMK/static/index.html', '/index_static'),
    ('/MiniTimeMK/static/(?P<any>crna_hronika|ekonomija|kultura|makedonija|skopje|sport|svet|tehnologija|zabava|zivot).html',
     '/\g<any>'),
)

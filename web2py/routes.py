routes_in = (
    ('/', '/MiniTimeMK/static/index.html'),
    ('/(?P<any>index|crna_hronika|ekonomija|kultura|makedonija|skopje|sport|svet|tehnologija|zabava|zivot)',
     '/MiniTimeMK/static/\g<any>.html'),
    ('/update', '/MiniTimeMK/default/update'),
    # ('/.*$', '/MiniTimeMK/static/index.html')   # all other urls redirect to index
)
routes_out = (
    ('/MiniTimeMK/static/index.html', '/'),
    ('/MiniTimeMK/static/(?P<any>index|crna_hronika|ekonomija|kultura|makedonija|skopje|sport|svet|tehnologija|zabava|zivot).html',
     '/\g<any>'),
    ('/MiniTimeMK/default/update', '/update'),
    # ('/MiniTimeMK/static/index.html', '/.*$'),
)

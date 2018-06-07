pkg_apt = {
    'gunicorn3': {'installed': True},
}
svc_systemd = {}
files = {}

for app, app_config in sorted(node.metadata.get('gunicorn', {}).get('apps', {}).items(), key=lambda x: x[0]):
    svc_systemd['gunicorn3@{app}.socket'.format(app=app)] = {
        'needs': [
            'file:/etc/systemd/system/gunicorn3@{app}.socket'.format(app=app),
            'file:/etc/systemd/system/gunicorn3@{app}.service'.format(app=app),
            'pkg_apt:gunicorn3'
        ],
    }

    files['/etc/systemd/system/gunicorn3@{app}.service'.format(app=app)] = {
        'source': 'gunicorn3@.service',
        'owner': 'root',
        'group': 'root',
        'mode': '0644',
        'content_type': 'mako',
        'context': {
            'user': app_config.get('user', 'www-data'),
            'group': app_config.get('group', 'www-data'),
            'app_dir': app_config.get('app_dir', '/var/www/tools/{app}'.format(app=app)),
            'appname': app,
        },
    }

    files['/etc/systemd/system/gunicorn3@{app}.socket'.format(app=app)] = {
        'source': 'gunicorn3@.socket',
        'owner': 'root',
        'group': 'root',
        'mode': '0644',
    }

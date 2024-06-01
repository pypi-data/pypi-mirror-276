# Flask-Apium

There is no established Flask extension for celery. This is a first
proof of concept to that end. Let me know if it is useful. To make
clear that it is separate from the `celery` project, I took the
Latin genus name for the celery species.

## Running

First set FLASK_APP to the make_celery submodule, and then execute:

    celery -A flask_apium.make_celery worker --loglevel INFO &
    flask run

You can test with:

    import requests
    base_url = 'http://localhost:5000/'
    add_url = f'{base_url}/add'
    r = requests.post(url, data = {'a':'1','b':'2'})
    print(requests.get(f'{base_url}/result/{r.json()['result_id']}'))


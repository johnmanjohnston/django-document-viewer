from django.http import request
from django.http import HttpResponse
from django.http import FileResponse
from django.http import Http404
import requests
import os

def download_file(url):
    local_filename = url.split('/')[-1]
    try:
        with requests.get(url, stream=True) as rescode:
            rescode.raise_for_status()
            with open(local_filename, 'wb') as f:
                for chunk in rescode.iter_content(chunk_size=8192): 
                    f.write(chunk)

        return local_filename
    except Exception as ex:
        return 0


def delete_local_file(fpath):
    os.remove(fpath)


def read(request, fpath):
    if download_file(fpath) == 0:
        response = HttpResponse(f"<div>The file at {fpath} was not found; HTTP Response 404</div>")
    else:
        local_filename = fpath.split('/')[-1]

        try:
            response = FileResponse(open(local_filename, 'rb'), content_type='application/pdf')
        except FileNotFoundError:
            response = HttpResponse(f"<div>The file at {fpath} was not found; HTTP Response 404</div>")

        delete_local_file(local_filename)

    return response
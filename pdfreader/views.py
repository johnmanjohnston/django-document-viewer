from django.http import request
from django.http import HttpResponse
from django.http import FileResponse
from django.http import Http404
import requests
import os
import mammoth # .docx to html

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
        httpres = HttpResponse(f"<div>The file at {fpath} was not found; HTTP Response 404</div>")
    else:
        local_filename = fpath.split('/')[-1]

        try:
            ext = (local_filename.split(".")[len(local_filename.split(".")) - 1]).lower()

            if ext == "docx":
                with open("pdfreader/test.docx", "rb") as docx_file:
                    result = mammoth.convert_to_html(docx_file)
                    html = result.value 
                    messages = result.messages 

                    full_html = (
                        '<!DOCTYPE html><html><head><meta charset="utf-8"/></head><body>'
                        + html
                        + "</body></html>"
                    )

                    with open("test.html", "w", encoding="utf-8") as f:
                        f.write(full_html)

                    httpres = HttpResponse(full_html)

            elif ext == "pdf":
                httpres = FileResponse(open(local_filename, 'rb'), content_type='application/pdf')

        except FileNotFoundError:
            httpres = HttpResponse(f"<div>The file at {fpath} was not found; HTTP Response 404</div>")
        except ValueError:
            httpres = HttpResponse(f"<div>Invalid file extension</div>")

        delete_local_file(local_filename)

    return httpres
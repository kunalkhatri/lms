import subprocess, os, pathlib
from django.http import HttpResponse
def update_codebase(request):
    update_script_dir = pathlib.Path(os.getcwd()).parent
    update_process = subprocess.Popen(["bash","update_codebase.sh"], stdout=subprocess.PIPE, cwd=update_script_dir)

    update_process.wait()
    output = update_process.stdout.readlines()
    output_text = ""
    for line in output:
        output_text =output_text + line.decode() + "<br>"
    return HttpResponse(output_text)
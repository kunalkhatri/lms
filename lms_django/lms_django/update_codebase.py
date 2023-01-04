import subprocess, os, pathlib
from django.http import HttpResponse
def update_codebase(request):
    try:
        #additional line here
        # antoher line
        update_script_dir = pathlib.Path(os.getcwd()).parent
        update_process = subprocess.Popen(["bash","update_codebase.sh"], stdout=subprocess.PIPE, cwd=update_script_dir, shell=True)

        return HttpResponse("Update code base request initiated. There shall be NO response.")
    except Exception as err:
        return HttpResponse({
            "message":str(err)
        })
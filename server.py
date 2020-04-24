import os
import shutil
import json
from django.conf.urls import url
from django.conf.urls.static import static
from django.http import HttpResponse

BASE_URL = "http://50.116.48.39:5000"

# Server code
DEBUG = True
SECRET_KEY = '4l0ngs3cr3tstr1ngw3lln0ts0l0ngw41tn0w1tsl0ng3n0ugh'
ROOT_URLCONF = __name__
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/TMHMM/"
ALLOWED_HOSTS = [BASE_URL[7:], BASE_URL[7:len(BASE_URL) - 5], BASE_DIR]
DEBUG=True

def getTMHMM(sequence):
    # write the sequence to fasta
    with open("input.fasta", "w") as outfile:
        outfile.write(sequence)

    # run the command
    os.system("cat input.fasta | tmhmm-2.0c/bin/tmhmm > output.txt")

    # read the output
    proteins = []
    lines = []
    with open("output.txt", "r") as infile:
        lines = infile.readlines()
    proteins.append({"length" : lines[0][22:len(lines[0]) - 1]})
    proteins.append({"#TMHs" : lines[1][40:len(lines[1]) - 1]})
    proteins.append({"#AAsInTMHs" : lines[2][41:len(lines[2]) - 1]})
    proteins.append({"#AAsInTMHs" : lines[2][41:len(lines[2]) - 1]})

    proteinList = []
    for i in range(5, len(lines)):
        segments = lines[i].split()
        proteinList.append({
            "location": segments[2],
            "start": segments[3],
            "end": segments[4],
            "raw": segments
        })
        
    proteins.append({"proteinList": proteinList})

    # remove the temporary files
    for f in os.listdir():
        if ("TMHMM_" in f):
            shutil.rmtree(f)

    os.remove("output.txt")
    os.remove("input.fasta")

    return proteins


def home(request):
    return HttpResponse("Send POST to /TMHMM", content_type="text/plain")

def TMHMM(request):
    # given the search parameters, return only the peptides that fit the rank
    sequence = request.POST.get("sequence")
    print(sequence)
    return HttpResponse(json.dumps(getTMHMM(sequence)), content_type='text/plain')

urlpatterns = [
    url(r'^$', home),
    url(r'^TMHMM$', TMHMM)
]

# A test case:

# print(getTMHMM('''
# MEILCEDNTSLSSIPNSLMQVDGDSGLYRNDFNSRDANSSDASNWTIDGENRTNLSFEGYLPPTCLSILHL
# QEKNWSALLTAVVIILTIAGNILVIMAVSLEKKLQNATNYFLMSLAIADMLLGFLVMPVSMLTILYGYRWP
# LPSKLCAVWIYLDVLFSTASIMHLCAISLDRYVAIQNPIHHSRFNSRTKAFLKIIAVWTISVGVSMPIPVF
# GLQDDSKVFKQGSCLLADDNFVLIGSFVAFFIPLTIMVITYFLTIKSLQKEATLCVSDLSTRAKLASFSFL
# PQSSLSSEKLFQRSIHREPGSYTGRRTMQSISNEQKACKVLGIVFFLFVVMWCPFFITNIMAVICKESCNE
# HVIGALLNVFVWIGYLSSAVNPLVYTLFNKTYRSAFSRYIQCQYKENRKPLQLILVNTIPALAYKSSQLQA
# GQNKDSKEDAEPTDNDCSMVTLGKQQSEETCTDNINTVNEKVSCV
# '''))
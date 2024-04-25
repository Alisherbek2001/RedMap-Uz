from django.shortcuts import render,get_object_or_404
from .models import Hayvon , CoordinateHayvon ,Osimlik,CoordinateOsimlik, REGIONS as viloyatlar
from sentence_transformers import SentenceTransformer, util
from PIL import Image
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from .ser import Hayvonser,Osimlikser
# model = SentenceTransformer('clip-ViT-B-32')
from django.http import Http404
from .forms import Getimage


def  index(request):
    return render(request,'index.html')

def map(request):
    return render(request,'maps.html')

def region(request):
    return render(request,'regions.html')

regions = {
    "Xorazm" : {"x":41.55333524728877,"y":60.63171458968133},
    "Andijon": {"x":40.77398304415682,"y":72.3435943043043},
    "Surxondaryo" : {"x":37.229946780719374,"y":67.28245085330633},
    "Buxoro"  : {"x":39.767552900235394,"y":64.4231326},
    "Toshkent" : {"x":41.312336300425486,"y":69.2787079},
    "Navoiy": {"x":40.10345820028124,"y":65.37342209999998},
    "Fargona":{"x":40.37708320031709,"y":71.7918491},
    "Nukus" : {"x":42.46002290051553,"y":59.6176603},
    "Jizzax" : {"x":40.12416731068046 ,"y":67.8400189951009},
    "Qarshi" : {"x":38.8399800001027 ,"y":65.79279479999998},
    "Namangan" : {"x":40.99964820039211,"y":71.6726238},
    "Samarqand": {"x":39.65500170021967,"y":66.9756953999999},
    "Sirdaryo" : {"x":40.84361 ,"y":68.66167},
}


def hayvonview(request,id):
    hayvon = get_object_or_404(Hayvon,id=id)
    return render(request,"hayvon_detail.html",{"hayvon":hayvon})

def osimlikview(request,id):
    osimlik = get_object_or_404(Osimlik,id=id)
    return render(request,"osimlik_detail.html",{"osimlik":osimlik})


def regionListView(request):
    Hayvonlar =Osimliklar= []
    reg = request.GET.get("region","")
    if reg == "Farg'ona":
        reg = "Fargona"
    if reg != "" and reg != "O'zbekiston":
        Hayvonlar = CoordinateHayvon.objects.filter(region = reg)
        Osimliklar = CoordinateOsimlik.objects.filter(region = reg)
        reg = regions.get(reg)
        print(type(reg))
        reg["zoom"]= 8
    else:
        Hayvonlar = CoordinateHayvon.objects.all()
        Osimliklar = CoordinateOsimlik.objects.all()
        reg = {"x":41.765073,"y":63.150127,"zoom":1}
    Hayvonlar = [ { "id":i.nomi.id,"x":i.x,"y":i.y, "img":i.nomi.img.url,"name":i.nomi.nomi,"type": "hayvon" } for i in Hayvonlar ]
    for i in Osimliklar:
        Hayvonlar.append({ "id":i.nomi.id,"x":i.x,"y":i.y,"img":i.nomi.img.url,"name":i.nomi.nomi,"type": "osimlik" })
    context = {
            "hayvonlar":Hayvonlar,
            "viloyatlar":viloyatlar,
            "reg":reg,
        }

    return render(request,"regions.html",context)

def searchImage(request):
    form = Getimage(request.POST or None,request.FILES or None)
    # if not form.is_valid():
    #     raise Http404
    print(form)
    file_temp = form.cleaned_data["image"]
    print(file_temp)
    res = []
    hayvonlar = Hayvon.objects.all()
    osimliklar = Osimlik.objects.all()
    for h in hayvonlar:
        try:
            encoded_image = model.encode([Image.open(h.img.url) ,Image.open(file_temp)], batch_size=128, convert_to_tensor=True, show_progress_bar=False)
            processed_images = util.paraphrase_mining_embeddings(encoded_image)

            for score, image_id1, image_id2 in processed_images:
                score = "{:.3f}".format(score * 100)
                res.append([score,h.img.url,h.id,"hayvon"])
        except:
            continue
    for h in osimliklar:
        try:
            encoded_image = model.encode([Image.open(h.img.url) ,Image.open(file_temp)], batch_size=128, convert_to_tensor=True, show_progress_bar=False)
            processed_images = util.paraphrase_mining_embeddings(encoded_image)

            for score, image_id1, image_id2 in processed_images:
                score = "{:.3f}".format(score * 100)
                res.append([score,h.img.url,h.id,"osimlik"])
        except:
            continue
                
    res.sort(key=lambda x: float(x[0]),reverse=True)
    res = res[:5]
    
    return render(request,"search.html",{"images":res,"form":Getimage()})
    
def searchName(request):
    search = request.GET.get("search","")
    if search=="":
        searchhayvon = Hayvon.objects.all()
        searchosimlik = Osimlik.objects.all()
        natija = [{ "id":i.id,"img":i.img.url,"name":i.nomi,"type": "hayvon" } for i in searchhayvon]
        
        for i in searchosimlik:

            natija.append({ "id":i.id,"img":i.img.url,"name":i.nomi,"type": "osimlik" } )
        return render(request,"search.html",{"natija":natija,"form":Getimage()}) 
    else:
        searchhayvon = Hayvon.objects.filter(nomi__icontains=search)
        searchosimlik = Osimlik.objects.filter(nomi__icontains=search)
        natija = [{ "id":i.id,"img":i.img.url,"name":i.nomi,"type": "hayvon" } for i in searchhayvon]
        for i in searchosimlik:

            natija.append({ "id":i.id,"img":i.img.url,"name":i.nomi,"type": "osimlik" } )
        return render(request,"search.html",{"natija":natija,"form":Getimage()}) 
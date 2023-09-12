from core.models import Catagory

def extras(request):
        catagories=Catagory.objects.all()
       
        return {'catagories':catagories}
from django.forms import ModelForm
from models import Par, Image

class ParForm(ModelForm):
  class Meta:
    model = Par
    exclude = ('hidden','created','left','right')

class ImageForm(ModelForm):
  class Meta:
    model = Image
    exclude = ('seen','image','dead',)

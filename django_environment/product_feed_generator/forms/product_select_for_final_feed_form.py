from django import forms
from product_feed_generator.models import Serverkast_Product

class ProductSelectForFinalFeedForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(ProductSelectForFinalFeedForm, self).__init__(*args, **kwargs)
        for i, q in enumerate(Serverkast_Product.objects.all()):
            self.fields[q.name] = forms.BooleanField(required=False)
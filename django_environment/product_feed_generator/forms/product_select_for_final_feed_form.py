from django import forms
from product_feed_generator.models import Serverkast_Product

class ProductSelectForFinalFeedForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(ProductSelectForFinalFeedForm, self).__init__(*args, **kwargs)
        self.label_suffix = ""
        for i, q in enumerate(Serverkast_Product.objects.all()):
            # has to be identical to field in product_feed_generator/views/product_selection_view.py
            self.fields["%s ––– %s"%(q.ean,q.name)] = forms.BooleanField(required=False)
from django.views import View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import DeletionMixin


class DeleteView(DeletionMixin, SingleObjectMixin, View):
    pass
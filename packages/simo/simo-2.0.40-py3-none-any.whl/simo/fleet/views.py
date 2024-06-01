from django.http import HttpResponse, Http404
from django.db.models import Q
from dal import autocomplete
from simo.core.utils.helpers import search_queryset
from .models import Colonel, ColonelPin, Interface


def colonels_ping(request):
    return HttpResponse('pong')


class PinsSelectAutocomplete(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        if not self.request.user.is_staff:
            return ColonelPin.objects.none()

        try:
            colonel = Colonel.objects.get(
                pk=self.forwarded.get("colonel")
            )
        except:
            return ColonelPin.objects.none()

        qs = ColonelPin.objects.filter(colonel=colonel)

        if self.forwarded.get('self'):
            qs = qs.filter(
                Q(occupied_by_id=None) | Q(
                    id=int(self.forwarded['self'])
                )
            )
        else:
            qs = qs.filter(occupied_by_id=None)

        if self.forwarded.get('filters'):
            qs = qs.filter(**self.forwarded.get('filters'))

        if self.q:
            qs = search_queryset(qs, self.q, ('label', ))

        return qs


class InterfaceSelectAutocomplete(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        if not self.request.user.is_staff:
            return Interface.objects.none()

        try:
            colonel = Colonel.objects.get(
                pk=self.forwarded.get("colonel")
            )
        except:
            return Interface.objects.none()

        qs = Interface.objects.filter(colonel=colonel)

        if self.forwarded.get('filters'):
            qs = qs.filter(**self.forwarded.get('filters'))

        return qs

from rest_framework.filters import BaseFilterBackend

class ServiceDateFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):

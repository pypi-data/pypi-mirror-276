from django.shortcuts import get_object_or_404

from ..models import ImportSetup


class ImportSetupParentMixin:
    def get_import_setup(self):
        return get_object_or_404(
            klass=ImportSetup, pk=self.kwargs['import_setup_id']
        )

    def get_source_queryset(self):
        import_setup = self.get_import_setup()
        return import_setup.items.all()

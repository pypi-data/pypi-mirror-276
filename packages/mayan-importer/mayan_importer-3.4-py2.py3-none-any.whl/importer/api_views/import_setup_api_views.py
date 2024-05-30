from mayan.apps.rest_api import generics

from ..models import ImportSetup
from ..permissions import (
    permission_import_setup_create, permission_import_setup_delete,
    permission_import_setup_edit, permission_import_setup_process,
    permission_import_setup_view
)
from ..serializers import ImportSetupSerializer
from ..tasks import task_import_setup_populate, task_import_setup_process


class APIViewImportSetupClear(generics.ObjectActionAPIView):
    """
    post: Delete all the items of the specified import setup.
    """
    lookup_url_kwarg = 'import_setup_id'
    mayan_object_permissions = {
        'POST': (permission_import_setup_process,)
    }
    source_queryset = ImportSetup.objects.all()

    def object_action(self, request, serializer):
        self.object.clear()


class APIViewImportSetupPopulate(generics.ObjectActionAPIView):
    """
    post: Populate all the items of the specified import setup.
    """
    lookup_url_kwarg = 'import_setup_id'
    mayan_object_permissions = {
        'POST': (permission_import_setup_process,)
    }
    source_queryset = ImportSetup.objects.all()

    def object_action(self, request, serializer):
        task_import_setup_populate.apply_async(
            kwargs={'import_setup_id': self.object.pk}
        )


class APIViewImportSetupProcess(generics.ObjectActionAPIView):
    """
    post: Process all the items of the specified import setup.
    """
    lookup_url_kwarg = 'import_setup_id'
    mayan_object_permissions = {
        'POST': (permission_import_setup_process,)
    }
    source_queryset = ImportSetup.objects.all()

    def object_action(self, request, serializer):
        task_import_setup_process.apply_async(
            kwargs={'import_setup_id': self.object.pk}
        )


class APIViewImportSetupDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    delete: Delete the selected import setup.
    get: Return the details of the selected import setup.
    patch: Edit the selected import setup.
    put: Edit the selected import setup.
    """
    lookup_url_kwarg = 'import_setup_id'
    mayan_object_permissions = {
        'DELETE': (permission_import_setup_delete,),
        'GET': (permission_import_setup_view,),
        'PATCH': (permission_import_setup_edit,),
        'PUT': (permission_import_setup_edit,)
    }
    source_queryset = ImportSetup.objects.all()
    serializer_class = ImportSetupSerializer

    def get_serializer(self, *args, **kwargs):
        if not self.request:
            return None

        return super().get_serializer(*args, **kwargs)


class APIViewImportSetupList(generics.ListCreateAPIView):
    """
    get: Returns a list of all the import setups.
    post: Create a new import setup.
    """
    mayan_object_permissions = {'GET': (permission_import_setup_view,)}
    mayan_view_permissions = {'POST': (permission_import_setup_create,)}
    serializer_class = ImportSetupSerializer
    source_queryset = ImportSetup.objects.all()

    def get_serializer(self, *args, **kwargs):
        if not self.request:
            return None

        return super().get_serializer(*args, **kwargs)

from mayan.apps.rest_api import generics

from ..permissions import (
    permission_import_setup_edit, permission_import_setup_view
)
from ..serializers import ImportSetupItemSerializer

from .api_view_mixins import ImportSetupParentMixin


class APIViewImportSetupItemDetail(
    ImportSetupParentMixin, generics.RetrieveUpdateDestroyAPIView
):
    """
    delete: Delete the selected import setup items.
    get: Return the details of the selected import setup items.
    """
    lookup_url_kwarg = 'import_setup_item_id'
    mayan_object_permissions = {
        'DELETE': (permission_import_setup_edit,),
        'GET': (permission_import_setup_view,),
        'PATCH': (permission_import_setup_edit,),
        'PUT': (permission_import_setup_edit,),
    }
    serializer_class = ImportSetupItemSerializer

    def get_serializer(self, *args, **kwargs):
        if not self.request:
            return None

        return super().get_serializer(*args, **kwargs)


class APIViewImportSetupItemList(ImportSetupParentMixin, generics.ListAPIView):
    """
    get: Returns a list of all the import setup items.
    """
    mayan_object_permissions = {'GET': (permission_import_setup_view,)}
    serializer_class = ImportSetupItemSerializer

    def get_serializer(self, *args, **kwargs):
        if not self.request:
            return None

        return super().get_serializer(*args, **kwargs)

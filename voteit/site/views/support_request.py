from pyramid.view import view_config

from voteit.core import security
from voteit.core.models.interfaces import ISiteRoot
from voteit.core.views.base_view import BaseView

from voteit.site import SiteMF as _
from voteit.site.models.interfaces import ISupportStorage 


class SupportView(BaseView):
    @view_config(name = 'support_requests', context=ISiteRoot, renderer="templates/support_requests.pt", permission=security.MANAGE_SERVER, )
    def support_requests(self):
        adapter = self.request.registry.getAdapter(self.context, ISupportStorage)
        self.response['support_storage'] = adapter.support_storage.values()
        return self.response

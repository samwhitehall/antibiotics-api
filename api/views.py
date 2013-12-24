from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse

def vis_tool(request, **kwargs):
    url = reverse('specific-individual-tree', kwargs=kwargs)
    return render_to_response('tree-vis.html', {'tree_url' : url })

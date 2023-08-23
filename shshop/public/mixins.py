from django.urls import reverse_lazy, reverse
from django.http import JsonResponse
from django.contrib.auth.mixins import (
    LoginRequiredMixin as BaseLoginRequiredMixin
)
from django.views.generic.detail import SingleObjectTemplateResponseMixin
from django.views.generic.detail import BaseDetailView
from django.views.generic import TemplateView


class LoginRequiredMixin(BaseLoginRequiredMixin):
    # 验证类登录
    login_url = reverse_lazy('shshop:login')
    redirect_field_name = 'redirect_to'


class JsonLoginRequiredMixin(LoginRequiredMixin):

    def dispatch(self, request, *args, **kwargs):
        if (not self.request.accepts('text/html')) and (not request.user.is_authenticated):
            return JsonResponse({'code':'err', 'message': '请登录后操作！', 'login_url': reverse('shshop:login')})
        return super().dispatch(request, *args, **kwargs)



class JsonableResponseMixin:
    """
    Mixin to add JSON support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """
    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.accepts('text/html'):
            return response
        else:
            errors = {'code':'err', 'message': f'{form.errors}'}
            # return JsonResponse(errors, status=400)
            return JsonResponse(errors)

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super().form_valid(form)
        if self.request.accepts('text/html'):
            return response
        else:
            data = {
                'pk': self.object.pk,
                'code': 'ok',
                'message': '保存成功！'
            }
            return JsonResponse(data)


class JSONResponseMixin:
    """
    A mixin that can be used to render a JSON response.
    """
    def render_to_json_response(self, context, **response_kwargs):
        """
        Returns a JSON response, transforming 'context' to make the payload.
        """
        return JsonResponse(
            self.get_data(context),
            **response_kwargs
        )

    def get_data(self, context):
        """
        Returns an object that will be serialized as JSON by json.dumps().
        """
        # Note: This is *EXTREMELY* naive; in reality, you'll need
        # to do much more complex handling to ensure that arbitrary
        # objects -- such as Django model instances or querysets
        # -- can be serialized as JSON.
        return context


class JSONView(JSONResponseMixin, TemplateView):
    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, **response_kwargs)


class JSONDetailView(JSONResponseMixin, BaseDetailView):
    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, **response_kwargs)


class HybridDetailView(JSONResponseMixin, SingleObjectTemplateResponseMixin, BaseDetailView):

    def render_to_response(self, context):
        # Look for a 'format=json' GET argument
        if self.request.GET.get('format') == 'json':
            return self.render_to_json_response(context)
        else:
            return super().render_to_response(context)
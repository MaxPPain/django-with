#coding:utf-8
from django.contrib.auth.decorators import login_required,permission_required
from django.utils.decorators import method_decorator
from django.shortcuts import HttpResponseRedirect, reverse


class LoginRequiredMixin(object):
    """用户登录验证"""
    @method_decorator(login_required(login_url='/login/'))
    def dispatch(self, request, *args, **kwargs):
        deny_url = ('/look/',
                    )
        if request.path in deny_url:
            if not request.user.nickname:
                return HttpResponseRedirect(reverse('user:login'))
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)
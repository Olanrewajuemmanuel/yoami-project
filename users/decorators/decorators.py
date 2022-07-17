from django.shortcuts import redirect

def redirect_if_loggedin(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('store_main:index')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func
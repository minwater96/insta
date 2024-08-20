from django.shortcuts import redirect

def main_page(request):
    return redirect('posts:index')
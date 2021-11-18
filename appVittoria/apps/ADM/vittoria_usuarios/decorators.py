def dispatch_decorator(function):
    def wrap(request):
        print("hola decorador")
        function(request)
        # return function(request)
    return wrap
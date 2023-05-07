# class CustomAcceptHeaderMiddleware:
#     def __init__(self, response):
#         self.response = response
#
#     def __call__(self, request):
#         response = self.response(request)
#         response['Accept'] = f"{response['Content-Type']}; version={request.version}"
#         return response

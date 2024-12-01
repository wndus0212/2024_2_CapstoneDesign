class DisableCOOPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response['Cross-Origin-Opener-Policy'] = 'same-origin-allow-popups'

        # 디버깅용 로그 출력
        print("COOP header added to response:", response['Cross-Origin-Opener-Policy'])

        return response
# minifier/views.py

from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from htmlmin import minify as html_minify
from csscompressor import compress as compress_css
from rjsmin import jsmin
import re

class MinifyView(View):
    def get(self, request):
        return render(request, 'minify.html')

    def post(self, request):
        code_text = request.POST.get('code_text', '')
        code_file = request.FILES.get('code_file')

        content = code_text or ''
        if code_file:
            content = code_file.read().decode('utf-8')

        if not content:
            return HttpResponse('No code provided.', status=400)

        try:
            minified_content = ''
            if '<html' in content or '</html>' in content:
                minified_content = re.sub(r'>\s+<', '><', content)
                minified_content = re.sub(r'\s+', ' ', minified_content)
                minified_content = html_minify(minified_content, remove_comments=True, remove_empty_space=True)
            elif content.strip().startswith(('/*', 'body', '.')):
                minified_content = compress_css(content)
            elif content.strip().startswith(('function', 'var', 'let', 'const')):
                minified_content = jsmin(content)
            else:
                return HttpResponse('Unsupported file type or content.', status=400)
        except Exception as e:
            return HttpResponse(f'Error during minification: {str(e)}', status=500)

        return HttpResponse(minified_content, content_type='text/plain')

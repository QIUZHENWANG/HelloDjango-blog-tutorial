from .base import CommentDataTestCase
from django.template import Context, Template
from ..forms import CommentForm
from ..templatetags.comments_extras import show_comment_form
from django.http import HttpResponse

class CommentExtraTestCase(CommentDataTestCase):
    def test_show_commet_form_with_invalid_bound_form(self):
        template = Template (
            '{% load comments_extras %}'
            '{% show_comment_form post form %}'
        )
        invalid_data = {
            'name':'test',
            'email': 'qq@qq.com',
            'url':'www.test.com',
            'text':'test',
        }
        form = CommentForm(data=invalid_data)
        self.assertTrue(form.is_valid())
        context = Context(show_comment_form(self.ctx, self.post, form=form))
        expected_html = template.render(context)
        
        for field in form:
           # print(field)
            label = '<label for="{}">{}：</label>'.format(field.id_for_label, field.label)
            #print(label)
            self.assertInHTML(label, expected_html)
            self.assertInHTML(str(field), expected_html)
            self.assertInHTML(str(field.errors), expected_html)
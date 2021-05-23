from django.test import TestCase

class HighlighterTestCase(TestCase):
    def test_highlight(self):
        document = "这是一个比较长的标题，用于测试关键词高亮但不被截断。"
        #highlighter = Highlighter("标题")

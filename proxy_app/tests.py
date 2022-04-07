from django.test import TestCase
from .views import transform_text, find_words_with_6_letters, \
    generate_content, STATIC_URL, BASE_URL
from bs4 import BeautifulSoup
import os


class ProxyModelTest(TestCase):

    def test_transform_text(self):
        """Check if the text is being transformed in correct way."""
        self.assertEqual(
            transform_text('I’m not a native English speaker so pardon me please'),
            'I’m not a native™ English speaker so pardon™ me please™'
        )

    def test_content_generated_correctly(self):
        """Check if any 6-letter word in generated content is followed by ™"""
        generated_content = generate_content()
        bs = BeautifulSoup(generated_content, 'lxml')

        for tag in bs.find_all():
            if tag.string and not tag.find_all():
                words = find_words_with_6_letters(tag.string)
                for word in words:
                    self.assertIn(word + '™', tag.string)

    def test_generated_content_uses_right_static(self):
        """Check if the generated content uses right static."""
        generated_content = generate_content()
        bs = BeautifulSoup(generated_content, 'lxml')
        content = bs.decode()

        self.assertIn(os.path.join(STATIC_URL, 'news.css'), content)
        self.assertIn(os.path.join(STATIC_URL, 'favicon.ico'), content)
        self.assertIn(os.path.join(STATIC_URL, 'hh.js'), content)
        self.assertIn(os.path.join(STATIC_URL, 'y18.gif'), content)
        self.assertNotIn(BASE_URL[:-1], content)

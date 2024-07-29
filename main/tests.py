# main/tests.py

from django.test import TestCase
from .models import Author, Article
from django.urls import reverse


class AuthorModelTest(TestCase):
    def setUp(self):
        self.author = Author.objects.create(name="John Doe")

    def test_author_str(self):
        self.assertEqual(str(self.author), "John Doe")

class ArticleModelTest(TestCase):
    def setUp(self):
        self.author = Author.objects.create(name="John Doe")
        self.article = Article.objects.create(title="Test Article", content="This is a test article.")
        self.article.authors.add(self.author)

    def test_article_str(self):
        self.assertEqual(str(self.article), "Test Article")

    def test_article_authors(self):
        self.assertIn(self.author, self.article.authors.all())

class ViewsTest(TestCase):
    def setUp(self):
        self.author = Author.objects.create(name="John Doe")
        self.article = Article.objects.create(title="Test Article", content="This is a test article.")
        self.article.authors.add(self.author)

    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/index.html')

    def test_article_view(self):
        response = self.client.get(reverse('get_article', args=[self.article.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/article.html')
        self.assertContains(response, self.article.title)

    def test_author_view(self):
        response = self.client.get(reverse('get_author', args=[self.author.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/author.html')
        self.assertContains(response, self.author.name)

    def test_create_article_view(self):
        response = self.client.post(reverse('create_article'), {
            'title': 'New Article',
            'content': 'Content for new article',
            'author': self.author.pk
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/create_article.html')
        self.assertContains(response, 'success')
        new_article = Article.objects.get(title='New Article')
        self.assertIn(self.author, new_article.authors.all())

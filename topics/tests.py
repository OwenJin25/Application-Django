from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile
from .models import Topic
from .models import Comment

class ProfileModelTests(TestCase):
    def test_profile_creation_signal(self):
        """
        Um Profile deve ser criado automaticamente quando um User é criado.
        """
        user = User.objects.create_user(username='testuser', password='12345')
        self.assertTrue(Profile.objects.filter(user=user).exists())

    def test_profile_str_representation(self):
        """
        O método __str__ de Profile deve retornar 'username's Profile'.
        """
        user = User.objects.create_user(username='testuser', password='12345')
        profile = Profile.objects.get(user=user)
        self.assertEqual(str(profile), "testuser's Profile")


class TopicModelTests(TestCase):
    def test_topic_creation(self):
        """
        Deve ser possível criar um tópico com um autor e título válidos.
        """
        user = User.objects.create_user(username='testauthor', password='12345')
        topic = Topic.objects.create(
            title="Test Topic",
            description="This is a test description",
            author=user
        )
        self.assertEqual(topic.title, "Test Topic")
        self.assertEqual(topic.author, user)

    def test_topic_str_representation(self):
        """
        O método __str__ de Topic deve retornar o título do tópico.
        """
        user = User.objects.create_user(username='testauthor', password='12345')
        topic = Topic.objects.create(
            title="Test Topic",
            description="This is a test description",
            author=user
        )
        self.assertEqual(str(topic), "Test Topic")

class CommentModelTests(TestCase):
    def test_comment_creation(self):
        """
        Deve ser possível criar um comentário associado a um tópico e um autor válidos.
        """
        user = User.objects.create_user(username='testcommenter', password='12345')
        topic = Topic.objects.create(
            title="Test Topic",
            description="This is a test description",
            author=user
        )
        comment = Comment.objects.create(
            topic=topic,
            text="This is a test comment",
            author=user
        )
        self.assertEqual(comment.text, "This is a test comment")
        self.assertEqual(comment.topic, topic)
        self.assertEqual(comment.author, user)

    def test_comment_str_representation(self):
        """
        O método __str__ de Comment deve retornar 'Comments on {topic} by {author}'.
        """
        user = User.objects.create_user(username='testcommenter', password='12345')
        topic = Topic.objects.create(
            title="Test Topic",
            description="This is a test description",
            author=user
        )
        comment = Comment.objects.create(
            topic=topic,
            text="This is a test comment",
            author=user
        )
        expected_str = f"Comments on {topic.title} by {user.username}"
        self.assertEqual(str(comment), expected_str)

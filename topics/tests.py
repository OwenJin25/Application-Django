from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile, Topic, Comment
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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

class ForumFunctionalTests(LiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)
        User.objects.create_user(username='testuser', password='12345')

    def tearDown(self):
        self.driver.quit()

    def login_user(self):
        self.driver.get(f'{self.live_server_url}/admin/login/')
        self.driver.find_element(By.NAME, 'username').send_keys('testuser')
        self.driver.find_element(By.NAME, 'password').send_keys('12345')
        self.driver.find_element(By.XPATH, '//input[@type="submit"]').click()

    # TF01 - Teste de Login
    def test_login(self):
        self.login_user()
        welcome_message = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'welcome-message'))
        )
        self.assertIn('Bem-vindo, testuser', welcome_message.text)

    # TF02 - Criar um Tópico
    def test_create_topic(self):
        self.login_user()
        self.driver.get(f'{self.live_server_url}/topic/new/')
        self.driver.find_element(By.NAME, 'title').send_keys('culinária')
        self.driver.find_element(By.NAME, 'description').send_keys('comida')
        self.driver.find_element(By.XPATH, '//input[@type="submit"]').click()

        topic_title = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'h1'))
        )
        self.assertEqual(topic_title.text, 'culinária')

    # TF03 - Adicionar Comentário
    def test_add_comment(self):
        self.test_create_topic()
        self.driver.get(f'{self.live_server_url}/topic/1/')
        self.driver.find_element(By.NAME, 'text').send_keys('Bom aspeto!')
        self.driver.find_element(By.XPATH, '//input[@type="submit"]').click()

        comment_text = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'comment-text'))
        )
        self.assertEqual(comment_text.text, 'Bom aspeto!')

class IntegrationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.topic = Topic.objects.create(
            title="topico2", 
            description="Descrição tópico 2", 
            author=self.user
        )

    # TI01 - Validação de Comentário Instantâneo
    def test_comment_integration(self):
        comment = Comment.objects.create(
            topic=self.topic, 
            text="Gostei!", 
            author=self.user
        )
        self.assertIn(comment, self.topic.comment_set.all())

    # TI02 - Atualização Automática de Lista de Tópicos
    def test_topic_list_update(self):
        Topic.objects.create(
            title="topico2.1", 
            description="Descrição Atualizada", 
            author=self.user
        )
        topics = Topic.objects.all()
        self.assertEqual(topics.count(), 2)

class RegressionTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

    # TR01 - Adicionar Comentários após Mudança no BD
    def test_comment_regression(self):
        topic = Topic.objects.create(
            title="regressão", 
            description="descrição regressão", 
            author=self.user
        )
        comment = Comment.objects.create(
            topic=topic, 
            text="Comentário após atualização", 
            author=self.user
        )
        self.assertIn(comment, topic.comment_set.all())

    # TR02 - Login Após Alteração de Layout
    def test_login_regression(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200)

    # TR03 - Criação de Tópico Após Alteração no Modelo
    def test_topic_creation_regression(self):
        topic = Topic.objects.create(
            title="Novo Tópico", 
            description="Descrição após atualização", 
            author=self.user
        )
        self.assertTrue(Topic.objects.filter(title="Novo Tópico").exists())


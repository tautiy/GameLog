from django.conf import settings
from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=128, verbose_name='Название жанра')

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Developer(models.Model):
    name = models.CharField(max_length=128, verbose_name='Студия')

    class Meta:
        verbose_name = 'Разработчик'
        verbose_name_plural = 'Разработчики'

    def __str__(self):
        return self.name


class Publisher(models.Model):
    name = models.CharField(max_length=128, verbose_name='Издательство')

    class Meta:
        verbose_name = 'Издатель'
        verbose_name_plural = 'Издатели'

    def __str__(self):
        return self.name


class Platform(models.Model):
    name = models.CharField(max_length=128, verbose_name='Игровая платформа')

    class Meta:
        verbose_name = 'Платформа'
        verbose_name_plural = 'Платформы'

    def __str__(self):
        return self.name


class Game(models.Model):
    title = models.CharField(max_length=128, verbose_name='Название')
    genre = models.ManyToManyField(Genre, verbose_name='Жанры')
    developer = models.ManyToManyField(Developer, verbose_name='Разработчик')
    platform = models.ManyToManyField(Platform, verbose_name='Платформы')
    released_at = models.DateField(
        null=True,
        blank=True,
        verbose_name='Дата выхода'
    )

    class Meta:
        verbose_name = 'Игра'
        verbose_name_plural = 'Игры'

    def __str__(self):
        return self.title


class GamePublisher(models.Model):
    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
        related_name='game_publishers'
    )
    publisher = models.ForeignKey(
        Publisher,
        on_delete=models.CASCADE,
        related_name='published_games'
    )
    region = models.CharField(
        max_length=64,
        verbose_name='Регион'
    )

    class Meta:
        verbose_name = 'Издатель игры'
        verbose_name_plural = 'Издатели игр'


class UserGame(models.Model):
    STATUS_CHOICES = [
        ('planned', 'Запланировано'),
        ('playing', 'Играю'),
        ('completed', 'Пройдено'),
        ('dropped', 'Заброшено'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='user_games',
    )
    rawg_id = models.PositiveIntegerField(verbose_name='ID игры в RAWG')
    title = models.CharField(max_length=256, verbose_name='Название')
    status = models.CharField(
        max_length=16,
        choices=STATUS_CHOICES,
        default='planned',
        verbose_name='Статус',
    )
    added_at = models.DateTimeField(auto_now_add=True, verbose_name='Добавлено')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')

    class Meta:
        verbose_name = 'Игра пользователя'
        verbose_name_plural = 'Игры пользователя'
        unique_together = ('user', 'rawg_id')

    def __str__(self):
        return f'{self.user.username} — {self.title} ({self.get_status_display()})'


class Wishlist(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='wishlist',
    )
    rawg_id = models.PositiveIntegerField(verbose_name='ID игры в RAWG')
    title = models.CharField(max_length=256, verbose_name='Название')
    added_at = models.DateTimeField(auto_now_add=True, verbose_name='Добавлено')

    class Meta:
        verbose_name = 'Желаемое'
        verbose_name_plural = 'Список желаемого'
        unique_together = ('user', 'rawg_id')

    def __str__(self):
        return f'{self.user.username} — {self.title}'

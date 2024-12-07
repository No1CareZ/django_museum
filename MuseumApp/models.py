from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class AbstractFieldsModel(models.Model):
    """Abstract model to inherit description and title fields\n"""

    title = models.CharField(
        verbose_name='Заголовок',
        max_length=256
    )
    description = models.TextField(
        verbose_name='Описание'
    )

    def __str__(self) -> str:
        return self.title

    class Meta():
        abstract = True


class Exposition(AbstractFieldsModel):
    """Exposition model has basic fields. Considered to be\n
     Model for all Expostions local (choice 1-3) and locations\n
     like other museums (choice -1) and storage unit (choice 0)\n"""

    POSITION_CHOICES = {
        0: "Запасник",
        1: "Первый этаж",
        2: "Второй этаж",
        3: "Третий этаж",
        4: "Другой музей"
    }

    position = models.SmallIntegerField(
        verbose_name='Размещение',
        choices=POSITION_CHOICES,
        default=POSITION_CHOICES.get(-1)
    )

    on_restoration = models.BooleanField(
        verbose_name='На рестоврации',
        default=False
    )

    open = models.BooleanField(
        verbose_name='Открыта',
        default=False
    )

    @classmethod
    def get_default(cls):
        storage, created = cls.objects.get_or_create(
            title='Запансник музея',
            description="""Запасник музея специально
             предназначенный для хранения экспонатов.
             ВНИМАНИЕ!!! Данная модель не удаляемая,
             она будет восстанавливаться в целях
             сохранения работы данной системы!""",
            position=0
        )
        return storage

    def save(self, *args, **kwargs):  # save method override
        if self.on_restoration:
            self.open = False
        super(Exposition, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return f'museum/exposition/{self.pk}/'

    class Meta():
        verbose_name = 'экспозиция'
        verbose_name_plural = 'Экспозиции'


class Exhibit(AbstractFieldsModel):
    """Exhibit model has basic fields. Could be placed in\n
     expostion, storage or send to be restored using field\n
     location\n"""

    placement = models.ForeignKey(
        to=Exposition,
        on_delete=models.SET_DEFAULT,
        default=Exposition.get_default,
        related_name='exhibit'
    )

    image = models.ImageField(
        verbose_name='Изображение',
        upload_to="media/",
        null=True,
        blank=True
    )

    def get_absolute_url(self):
        return f'museum/exhibit/{self.pk}/'

    class Meta():
        verbose_name = 'экспонат'
        verbose_name_plural = 'Экспонаты'

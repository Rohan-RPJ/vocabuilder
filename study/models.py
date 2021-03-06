from django.conf import settings
from django.db import models
from django.utils import timezone

# Create your models here.

# class Study(models.Model):


class List(models.Model):
    list_type = models.CharField(max_length=10)

    def __str__(self):
        return self.list_type


class WordListManager(models.Manager):

    learn_q = 5

    def get_words(self, username, list):
        words_in_progress = Progress.objects.all().filter(user__username=username, word_id__word_id__contains=list).values_list('word_id__word', flat=True)
        get_words = self.filter(word_id__contains=list)
        return get_words.exclude(word__in=words_in_progress)[:self.learn_q]


class WordList(models.Model):
    word = models.CharField(max_length=30)
    definition = models.CharField(max_length=200)
    word_id = models.CharField(max_length=100, primary_key=True)
    objects = WordListManager()

    def __str__(self):
        return self.word_id


class ProgressManager(models.Manager):

    def get_lwords(self, user_name, list):
        # print(user_name, list)
        a = models.Q(word_id__word_id__contains=list)
        b = models.Q(user__username=user_name)
        c = models.Q(learned=True)
        return self.filter(a & b & c)

    def get_review_words(self, user_name, list):
        current_time = timezone.now
        a = models.Q(word_id__word_id__contains=list)
        b = models.Q(user__username=user_name)
        c = models.Q(learned=False)
        return self.filter(a & b & c).filter(interval__lte=current_time())

    def get_total_words_count(self, list):
        return self.filter(word_id__word_id__contains=list).count()

    def get_unwords_count(self, user_name, list):
        count = self.get_lwords(self, user_name, list).count()
        total = self.get_total_words_count(self, list)

        return total - count


class Progress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    word_id = models.ForeignKey(WordList, on_delete=models.CASCADE, null=True)
    learned = models.BooleanField(default=False)
    correct = models.IntegerField(default=0)
    wrong = models.IntegerField(default=0)
    interval = models.DateTimeField(default=timezone.now)
    objects = ProgressManager()

    def __str__(self):
        return str((self.word_id, self.learned, self.correct, self.wrong))


class CurrentWord(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    current_lword_no = models.IntegerField(default=0)
    current_rword_no = models.IntegerField(default=0)
    category = models.CharField(max_length=10)

    def __str__(self):
        return str((self.category, self.current_lword_no, self.current_rword_no))


# Assigns an id to the test
'''
def assign_test_id():
		return Test.objects.all().count()+1	
'''
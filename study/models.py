from django.db import models
from django.contrib.auth.models import User
from .utils import get_link
from markdown import markdown

# Create your models here.
class Subject(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	name = models.CharField(max_length=200, blank=False)
	# desc = models.CharField(max_length=700, blank=False)
	desc = models.TextField(blank=False)
	thumb_img = models.URLField(blank=True)

	def __str__(self):
		return self.name

	def custom_desc(self):
		return markdown(self.desc)

class Note(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='my_note')
	title = models.CharField(max_length=200, blank=False)
	# desc = models.CharField(max_length=700, blank=True)
	desc = models.TextField(blank=False)
	video_link = models.URLField(blank=True)
	pdf_link = models.URLField(blank=True)

	def __str__(self):
		return self.title

	def custom_desc(self):
		return markdown(self.desc)

	def get_stream_link(self):
		if self.video_link.strip() != '' and len(self.video_link) > 5:
			try:
				return get_link(self.video_link)
			except:
				return '#'

	def get_pdf_link(self):
		if self.pdf_link.strip() != '' and len(self.pdf_link) > 5:
			try:
				return get_link(self.pdf_link)
			except:
				return '#'

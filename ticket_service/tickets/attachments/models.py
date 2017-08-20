from django.db import models

class BaseAttachment (models.Model):
    pic = models.ImageField(upload_to = 'pic_folder/', default = 'pic_folder/None/no-img.jpg')
    description = models.TextField(null = True, blank = True)
    class Meta:
        abstract = True

    def cache(self):
        result = urllib.urlretrieve(self.url)
        self.pic.save(
            os.path.basename(self.url),
            File(open(result[0]))
        )
        self.save()

class PublicAttachment (BaseAttachment):
    ticket = models.ForeignKey('Ticket')

class PrivateAttachment (BaseAttachment):
    ticket = models.ForeignKey('PrivateTicket')

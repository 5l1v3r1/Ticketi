from django.db import models

class BaseAttachment (models.Model):
    attached_file = models.FileField(upload_to = 'attachments/', default = 'attachments/None/') #TODO: filter file types
    description = models.TextField(null = True, blank = True)
    class Meta:
        abstract = True

    def cache(self):
        result = urllib.urlretrieve(self.url)
        self.attached_file.save(
            os.path.basename(self.url),
            File(open(result[0]))
        )
        self.save()

class PublicAttachment (BaseAttachment):
    ticket = models.ForeignKey('Ticket')

class PrivateAttachment (BaseAttachment):
    ticket = models.ForeignKey('PrivateTicket')

from django.db import models

class Gallery(models.Model):
    '''
    Represents a gallery object uses some principes from
    https://github.com/jdriscoll/django-photologue/blob/master/photologue/models.py
    '''

    class Meta:
        #Allows models.py to be split up across multiple files
        app_label = 'gallery'
        verbose_name_plural = "Galleries"
        unique_together = (('title', 'family'),)

    title = models.CharField(max_length=50, db_index = True, null=False, blank=False)
    family = models.ForeignKey('family_tree.Family', null=False, db_index=True) #Use of model string name to prevent circular import

    description = models.TextField(blank=True)

    thumbnail = models.ImageField(blank=True, null=False)

    #Tracking
    creation_date = models.DateTimeField(auto_now_add=True, db_index=True)
    last_updated_date = models.DateTimeField(auto_now=True)

    def __str__(self): # __unicode__ on Python 2
        return str(self.family_id) + ': ' + self.title


    def delete_all_images(self):
        '''
        Deletes all related images in the gallery
        '''
        from gallery.models import Image

        images = Image.objects.filter(gallery_id = self.id)

        try:
            #Delete actual files
            for im in images:
                im.delete_image_files()

            #Delete database records
            images.delete()
        except:
            pass
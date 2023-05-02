from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import default_storage

class Place(models.Model):
    # name the other table using string, user cant be null or empty, instructions if the user is deleted
    user = models.ForeignKey('auth.User', null=False, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    visited = models.BooleanField(default=False)

    # blank is allowing a field to be empty
    notes = models.TextField(blank=True, null=True)
    date_visited = models.DateField(blank=True, null=True)

    # upload_to = the directory that the image get uploaded through
    photo = models.ImageField(upload_to='user_images/', blank=True, null=True)

    # delete a photo from the file system when the user deletes it in the program
    def save(self, *args, **kwargs):
        # get the place object that's being updated
        old_place = Place.objects.filter(pk=self.pk).first()
        # if the old place has a photo
        if old_place and old_place.photo:
            # if the old place's photo is different than the new photo
            if old_place.photo != self.photo:
                # delete the photo
                self.delete_photo(old_place.photo)

        super().save(*args, **kwargs)

    
    def delete_photo(self, photo):
        # check to see if a photo exists
        if default_storage.exists(photo.name):
            default_storage.delete(photo.name)


    def __str__(self):
        # photo.url is the filename for the photo
        photo_str = self.photo.url if self.photo else 'no photo'
        notes_str = self.notes[100:] if self.notes else 'no notes'
        return f'{self.name} visited? {self.visited} on {self.date_visited}. Notes: {notes_str}. Photo {photo_str}'

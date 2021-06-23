from .image import Image
from .ImageFormatter import ImageFormatter
from .galleryDatabaseHelper import GalleryDatabaseHelper

class GalleryController:
    def __init__(self, db):
        self.DB = GalleryDatabaseHelper(db)
        self.images = self.DB.getAllImages()
        self.formatter = ImageFormatter()
        self.imageIndex = 0 if len(self.images) > 0 else -1
        
    
    def addImage(self,image):
        image = self.DB.addImage(image)
        self.images.append(image)
        if self.imageIndex == -1:
            self.imageIndex = 0;
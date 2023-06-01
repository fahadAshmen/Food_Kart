from django.core.exceptions import ValidationError
import os


def validate_image(value):
    ext = os.path.splitext(value.name)[1] # cover-image.jpg jpg is [1]
    print(ext)
    valid_extensions = ['.png', '.jpg', '.jpeg']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension. Allowed extensions:' +str(valid_extensions))




# def validate_image(image):
#     """
#     Custom validation for the image field.
#     """
#     file_extension = image.name.split('.')[-1]
        
#     allowed_extensions = ['jpg', 'jpeg', 'png']
#     if file_extension not in allowed_extensions:
#         raise ValidationError("Invalid file format. Only JPG, JPEG, and PNG formats are allowed.")
    
#     # Check the file size
#     max_size = 5 * 1024 * 1024  # 5MB
#     if image.size > max_size:
#         raise ValidationError("File size exceeds the limit of 5MB.")
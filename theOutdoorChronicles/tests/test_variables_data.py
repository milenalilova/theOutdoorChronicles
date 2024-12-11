from datetime import date

from django.core.files.uploadedfile import SimpleUploadedFile

user_data = {
    'username': 'testuser',
    'email': 'pepi@pepi.com',
    'password': 'pass1234'
}

photo_data = {
    'image': 'images/photo_uploads/image.jpg',
    'description': 'A beautiful trail photo.',
    'date_uploaded': date(2000, 12, 25)
}

fake_image = SimpleUploadedFile(
    name='test_image.jpg',
    content=b'fake image content',
    content_type='image/jpeg'
)

trail_data = {
    'image': fake_image,
    'name': 'TestTrail',
    'location': 'France',
    'length': 15,
    'elevation_gain': 125,
    'difficulty': 'Easy',
    'route_type': 'Loop',
    'description': 'Difficult'
}

animal_data = {
    'image': 'images/photo_uploads/image.jpg',
    'common_name': 'sparrow',
    'species': 'some_name',
    'conservation_status': 'CB',
    'description': 'Some description',
    'wikipedia_page': 'https://en.wikipedia.org/wiki/House_sparrow',
}

first_log_data = {
    'title': 'Nice Walk',
    'date_completed': date(2000, 12, 25),
    'notes': 'It was a good walk'
}
second_log_data = {
    'title': 'Another Nice Walk',
    'date_completed': date(2000, 12, 28),
    'notes': 'It was another good walk'
}

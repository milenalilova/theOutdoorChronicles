# import os
# from datetime import date
#
# import django
# from django.contrib.auth import get_user_model
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'theOutdoorChronicles.settings')
# django.setup()
#
# from theOutdoorChronicles.trails.models import Trail
# from theOutdoorChronicles.animals.models import Animal
# from theOutdoorChronicles.trail_logs.models import TrailLog
#
# UserModel = get_user_model()
#
# '''
# This file creates few database records for testing. Feel free to create more if needed.
#
# Please note that Trail and Animal objects can only be created by a staff user with permissions,
# or a supersuser. A regular user can only create TraiLLogs.
#
# 1. Users are created, if they do not exist yet.
# 2. Trails objects are created if they do not exist yet.
# 3. Animals objects  are created.
# 4. Animals and trails relations are set
# 5. Trail logs objects are created and relations with users and trails are set.
#
# Use images from mediafiles folder to upload from a trail, an animal or a rail log details page
#
#
# '''
#
#
# # Create users
# def create_users():
#     if not UserModel.objects.filter(username='first_user').exists():
#         user_one = UserModel.objects.create_user(
#             username='first_user',
#             email='first@first.com',
#             password='111111mm'
#         )
#     else:
#         user_one = UserModel.objects.get(username='first_user')
#     if not UserModel.objects.filter(username='second_user').exists():
#         user_two = UserModel.objects.create_user(
#             username='second_user',
#             email='second@second.com',
#             password='111111mm'
#         )
#     else:
#         user_two = UserModel.objects.get(username='second_user')
#
#     if not UserModel.objects.filter(username='third_user').exists():
#         user_tree = UserModel.objects.create_user(
#             username='third_user',
#             email='third@third.com',
#             password='111111mm'
#         )
#     else:
#         user_tree = UserModel.objects.get(username='third_user')
#
#     return [user_one, user_two, user_tree]
#
#
# # Create Trail objects
# def create_trails():
#     trail_data = [
#         {
#             'image': 'images/trails_images/Molokoi.png',  # Image path relative to MEDIA_ROOT
#             'name': 'Molokoi1',
#             'location': 'Cacao',
#             'length': 19.00,
#             'elevation_gain': 805,
#             'difficulty': 'Hard',
#             'route_type': 'One Way',
#             'description': 'Molokoi is a renowned hiking trail...',
#         },
#         {
#             'image': 'images/trails_images/DALL.E.webp',
#             'name': 'Lamirande1',
#             'location': 'French Guiana',
#             'length': 7.00,
#             'elevation_gain': 230,
#             'difficulty': 'Moderate',
#             'route_type': 'Loop',
#             'description': 'La Mirande is a captivating hiking trail...',
#         },
#         {
#             'image': 'images/trails_images/Sange.webp',
#             'name': 'Montagne des Singes1',
#             'location': 'Roura, French Guiana',
#             'length': 4.00,
#             'elevation_gain': 180,
#             'difficulty': 'Hard',
#             'route_type': 'Loop',
#             'description': 'La Montagne des Singes, or Monkey Mountain, is a remarkable hiking destination...'
#         },
#         {
#             'image': 'images/trails_images/Amazonian_Jungle.webp',
#             'name': 'Rorota1',
#             'location': 'Remire',
#             'length': 5.00,
#             'elevation_gain': 128,
#             'difficulty': 'Easy',
#             'route_type': 'Loop',
#             'description': 'La Rorota is an iconic hiking trail located near the town of Rémire-Montjoly...',
#         },
#         {
#             'image': 'images/trails_images/Musala.webp',
#             'name': 'Musala1',
#             'location': 'Bulgaria',
#             'length': 50.00,
#             'elevation_gain': 2800,
#             'difficulty': 'Hard',
#             'route_type': 'One Way',
#             'description': 'Musala Peak is the highest peak in Bulgaria and the Balkan Peninsula...',
#         },
#
#     ]
#
#     created_trails = []
#
#     for trail in trail_data:
#         if not Trail.objects.filter(name=trail['name']).exists():
#             created_trail = Trail.objects.create(**trail)
#             created_trails.append(created_trail)
#         else:
#             created_trail = Trail.objects.get(name=trail['name'])
#             created_trails.append(created_trail)
#
#     return created_trails
#
#
# # Create Animal objects
# def create_animals():
#     animal_data = [
#         {
#             'image': 'images/animal_images/bushmaster_2.jpg',
#             'common_name': 'South American Bushmaster1',
#             'species': 'Lachesis muta',
#             'conservation_status': 'LC',
#             'description': 'Adults grow to an average of 2 to 2.5 m (6½-8 feet), although 3 m (10 feet) is not too unusual. The largest recorded specimen was 3.65 m (almost 12 feet) long, making the species the largest of all vipers and the longest venomous snake in the Western Hemisphere. Lachesis muta is the third longest venomous snake in the world, exceeded in length only by the king cobra and the black mamba.',
#             'wikipedia_page': 'https://en.wikipedia.org/wiki/Lachesis_muta',
#             'additional_info': 'https://www.inaturalist.org/taxa/73840-Lachesis-muta',
#         },
#         {
#             'image': 'images/animal_images/Eastern-Coral-Snake.jpg',
#             'common_name': 'Coral Snake1',
#             'species': 'Micrurus lemniscatus',
#             'conservation_status': 'LC',
#             'description': 'M. lemniscatus is a thin and brightly colored species. Adults measure 60–90 cm (24–35 in) in length, the maximum previously reported was 145 cm (57 in). The snout is black, followed by a narrow white crossband in front of the eyes, then a wider black band including the eyes.',
#             'wikipedia_page': 'https://en.wikipedia.org/wiki/Micrurus_lemniscatus',
#             'additional_info': '',
#         },
#         {
#             'image': 'images/animal_images/Green-snake.jpg',
#             'common_name': 'Green snake1',
#             'species': 'Opheodrys vernalis',
#             'conservation_status': 'LC',
#             'description': 'The smooth green snake (Opheodrys vernalis) is a species of North American nonvenomous snake in the family Colubridae. The species is also referred to as the grass snake. It is a slender, "small medium" snake that measures 36–51 cm (14–20 in) as an adult.',
#             'wikipedia_page': 'https://en.wikipedia.org/wiki/Smooth_green_snake',
#             'additional_info': '',
#         },
#         {
#             'image': 'images/animal_images/great_tit.jpg',
#             'common_name': 'Great tit1',
#             'species': 'parus major',
#             'conservation_status': 'LC',
#             'description': 'The great tit is a distinctive bird with a black head and neck, prominent white cheeks, olive upperparts and yellow underparts, with some variation amongst the numerous subspecies. It is predominantly insectivorous in the summer, but will consume a wider range of food items in the winter months.',
#             'wikipedia_page': 'https://en.wikipedia.org/wiki/Great_tit',
#             'additional_info': 'https://www.inaturalist.org/taxa/203153-Parus-major',
#         },
#         {
#             'image': 'images/animal_images/eurasian_wolf.jpg',
#             'common_name': 'Wolf1',
#             'species': 'canis lupus',
#             'conservation_status': 'LC',
#             'description': 'Of all members of the genus Canis, the wolf is most specialized for cooperative game hunting as demonstrated by its physical adaptations to tackling large prey, its more social nature, and its highly advanced expressive behaviour, including individual or group howling.',
#             'wikipedia_page': 'https://en.wikipedia.org/wiki/Wolf',
#             'additional_info': '',
#         },
#     ]
#
#     # Create Animal objects
#     for animal in animal_data:
#         Animal.objects.create(**animal)
#
#
# # Assign animals to trails
# def assign_animals_to_trails():
#     molokoi_trail = Trail.objects.get(name='Molokoi1')
#     lamirande_trail = Trail.objects.get(name='Lamirande1')
#     rorota_trail = Trail.objects.get(name='Rorota1')
#     montagne_sange_trail = Trail.objects.get(name='Montagne des Singes1')
#     musala_trail = Trail.objects.get(name='Musala1')
#
#     bushmaster = Animal.objects.get(common_name='South American Bushmaster1')
#     coral_snake = Animal.objects.get(common_name='Coral Snake1')
#     green_snake = Animal.objects.get(common_name='Green snake1')
#     great_tit = Animal.objects.get(common_name='Great tit1')
#     wolf = Animal.objects.get(common_name='Wolf1')
#
#     bushmaster.trails.add(lamirande_trail, montagne_sange_trail, molokoi_trail)
#     coral_snake.trails.add(rorota_trail, lamirande_trail)
#     green_snake.trails.add(montagne_sange_trail)
#     great_tit.trails.add(musala_trail)
#     wolf.trails.add(musala_trail)
#
#
# # Create trail logs
# def create_trail_logs():
#     current_date = date.today()
#
#     users = create_users()
#     trails = create_trails()
#
#     trail_log_data = [
#         {
#             'title': 'Sunny day',
#             'date_completed': current_date,
#             'notes': 'The sun was shining',
#             'user': users[0],
#             'trail': trails[0],
#         },
#         {
#             'title': 'Hard day hiking',
#             'date_completed': current_date,
#             'notes': 'Long walk but felt good',
#             'user': users[1],
#             'trail': trails[1],
#         },
#         {
#             'title': 'Rainy day',
#             'date_completed': current_date,
#             'notes': 'It was raining',
#             'user': users[2],
#             'trail': trails[2],
#         },
#     ]
#
#     for trail_log in trail_log_data:
#         TrailLog.objects.create(**trail_log)
#
#
# # Run the function
# if __name__ == "__main__":
#     create_users()
#     create_trails()
#     create_animals()
#     assign_animals_to_trails()
#     create_trail_logs()

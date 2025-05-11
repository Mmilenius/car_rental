from django.shortcuts import render

def catalog(request):
    context = {
        'title': 'Home - Каталог ',
        'cars': [

    {'image': 'deps/images/cars/toyota_camry.jpg',
    'name': 'Toyota Camry',
    'description': 'Комфортний седан бізнес-класу з автоматичною коробкою передач та економною витратою пального.',
    'price': 85.00,},

    {'image': 'deps/images/cars/bmw_x5.jpg',
     'name': 'BMW X5',
     'description': 'Преміум SUV з повним приводом, потужним двигуном та розкішним салоном.',
     'price': 130.00,},

    {'image': 'deps/images/cars/tesla_model3.jpg',
     'name': 'Tesla Model 3',
     'description': 'Електромобіль із автопілотом, швидкою зарядкою та високим рівнем безпеки.',
     'price': 110.00,},

    {'image': 'deps/images/cars/hyundai_elantra.jpg',
     'name': 'Hyundai Elantra',
     'description': 'Сучасний седан з автоматичною КПП, чудовий вибір для міських поїздок.',
     'price': 60.00,},

    {'image': 'deps/images/cars/mercedes_s_class.jpg',
     'name': 'Mercedes-Benz S-Class',
     'description': 'Флагманський седан із максимальним комфортом і сучасними технологіями.',
     'price': 150.00,},

    {'image': 'deps/images/cars/audi_a4.jpg',
     'name': 'Audi A4',
     'description': 'Елегантний і динамічний седан із переднім приводом і якісним інтер’єром.',
     'price': 95.00,},

    {'image': 'deps/images/cars/kia_sportage.jpg',
     'name': 'KIA Sportage',
     'description': 'Надійний кросовер з економним двигуном і великим багажником.',
     'price': 70.00,},

    {'image': 'deps/images/cars/ford_mustang.jpg',
     'name': 'Ford Mustang',
     'description': 'Легендарне купе з потужним мотором і спортивною зовнішністю.',
     'price': 120.00,},

    {'image': 'deps/images/cars/renault_logan.jpg',
     'name': 'Renault Logan',
     'description': 'Бюджетний автомобіль для щоденних поїздок із низькою витратою пального.',
     'price': 45.00,},

    {'image': 'deps/images/cars/volkswagen_passat.jpg',
     'name': 'Volkswagen Passat',
     'description': 'Просторий і зручний седан з високою надійністю.',
     'price': 80.00,},
    ]
    }



    return render(request, 'cars/catalog.html', context)

def car(request):
    return render(request, 'cars/car.html')
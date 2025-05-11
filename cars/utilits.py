from django.db.models import Q
from cars.models import Cars


def q_search(query):
    if query.isdigit() and len(query) <= 5:
        return Cars.objects.filter(id=int(query))

    keywords = [word for word in query.split() if len(word) > 2]

    q_objects = Q()

    for tiken in keywords:
        q_objects |= Q(name__icontains=tiken)
        q_objects |= Q(description__icontains=tiken)

    return Cars.objects.filter(q_objects)
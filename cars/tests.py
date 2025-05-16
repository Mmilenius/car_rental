from django.test import TestCase

from cars.models import Cars, Categories
def test_category_creation():
    """
    Test that a category can be created with required fields.
    """
    category = Categories.objects.create(
        name="Sedan",
        slug="sedan"
    )
    assert category.name == "Sedan"
    assert category.slug == "sedan"
    assert str(category) == "Sedan"

def test_catalog_view_all_cars(client):
    """
    Test catalog view showing all cars.
    """
    response = client.get('/cars/all/')
    assert response.status_code == 200
    assert 'cars' in response.context

def test_catalog_view_category_filter(client, category):
    """
    Test catalog view filtered by category.
    """
    response = client.get(f'/cars/{category.slug}/')
    assert response.status_code == 200
    assert len(response.context['cars']) == Cars.objects.filter(category=category).count()

def test_catalog_view_pagination(client):
    """
    Test catalog view pagination.
    """
    response = client.get('/cars/all/?page=1')
    assert response.status_code == 200
    assert response.context['cars'].number == 1
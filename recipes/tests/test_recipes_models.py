import json


def test_recipe_listing(recipe):
    tags = [tag.meal_tag for tag in recipe.meal_tags.all()]
    assert recipe.name == "Pierogi"
    assert recipe.portions == "5"
    assert json.loads(recipe.method) == ["paragraph1", "paragraph2"]
    assert json.loads(recipe.ingredients) == ["500 g ingredient1", "30 ml ingredient2"]
    assert 'obiad' in tags
    assert 'kolacja' in tags



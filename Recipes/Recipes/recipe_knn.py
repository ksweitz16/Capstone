from sklearn.neighbors import NearestNeighbors
from .nlp_filter import parse_ingredients
from .models import Recipe


def match_recipe(user_ingredients):
    recipes = Recipe.objects.all()
    if not recipes.exists():
        return None, None

    data = []
    recipe_objs = []
    for recipe in recipes:
        raw_ingredients = recipe.ingredients.split(',')
        cleaned = parse_ingredients([i.strip() for i in raw_ingredients])
        data.append(cleaned)    # groups of ingredients per recipe
        recipe_objs.append(recipe)

    # Build vocab
    vocab = sorted(set(i for sublist in data for i in sublist))

    def vectorize(ingredients):
        return [1 if i in ingredients else 0 for i in vocab]

    recipe_vectors = [vectorize(ing) for ing in data]
    user_vector = [vectorize(user_ingredients)]

    if sum(user_vector[0]) == 0:
        return None, None

    # Fit k-NN
    knn = NearestNeighbors(n_neighbors=min(5, len(recipe_vectors)), metric='cosine')
    # knn = NearestNeighbors(n_neighbors=5, metric='cosine')
    knn.fit(recipe_vectors)

    distances, indices = knn.kneighbors(user_vector)
    scored_matches = []

    for idx, dist in zip(indices[0], distances[0]):
        recipe = recipe_objs[idx]
        recipe_ingredients = data[idx]
        overlap = len(set(recipe_ingredients) & set(user_ingredients))
        similarity_score = 1 - dist  # cosine similarity (1 = identical, 0 = opposite)

        # Combined match score: more overlap and more similarity
        # You can tweak weights here
        match_score = (overlap / len(user_ingredients)) * 0.7 + similarity_score * 0.3

        scored_matches.append((match_score, overlap, similarity_score, recipe))
    # Sort by match_score descending
    scored_matches.sort(reverse=True, key=lambda x: x[0])

    # Best match
    best_match = scored_matches[0]  # score
    best = scored_matches[0][3] if scored_matches else None
    print(
        f"Best Match: #{best.id} {best.title} | Score: {best_match[0]:.3f} | Overlap: {best_match[1]} | Similarity: {best_match[2]:.3f}")

    next_best = None
    for score, overlap, sim, rec in scored_matches[1:]:
        if rec != best:
            next_best = rec
            print(f"Next Best: #{rec.id} {rec.title} | Score: {score:.3f} | Overlap: {overlap} | Similarity: {sim:.3f}")
            break

    return best, next_best, scored_matches
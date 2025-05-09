import matplotlib.pyplot as plt

def graph_matches(scored_matches, user_ingredients):
    if user_ingredients:
        titles = [match[3].title for match in scored_matches]
        overlaps = [match[1] for match in scored_matches]
        similarities = [match[2] for match in scored_matches]
        scores = [match[0] for match in scored_matches]

    # plt.figure(figsize=(10, 6))
    # scatter = plt.scatter(
    #     overlaps, similarities, s=[score * 300 for score in scores],
    #     c=scores, cmap='viridis', edgecolors='k', alpha=0.7
    # )
    #
    # for i, title in enumerate(titles):
    #     plt.text(overlaps[i]+0.05, similarities[i]+0.01, title)
    #
    # plt.colorbar(scatter, label="Match Score")
    # plt.xlabel("ingredient Overlap")
    # plt.ylabel("Cosine Similarity")
    # plt.title("Recipe Matching Visual")
    # plt.grid(True)

        x = range(len(titles))
        fig, ax1 = plt.subplots(figsize=(10, 6))
        ax1.bar(x, overlaps, color='skyblue', label='Ingredient Overlap')
        ax1.set_ylabel('Overlap Count', color='skyblue')
        ax1.set_ylim(0, max(overlaps) + 1)
        ax1.set_xticks(x)
        ax1.set_xticklabels(titles, rotation=20, ha='right')

        ax2 = ax1.twinx()
        ax2.plot(x, similarities, color='orange', marker='o', label='Cosine Similarity')
        ax2.set_ylabel('Cosine Similarity', color='orange')
        ax2.set_ylim(0, 1)

        for i, score in enumerate(scores):
            ax2.text(i, similarities[i] + 0.02, f"{score:.2f}", ha='center', fontsize=9)

        plt.title("Recipe Matching Visual")
        plt.show()


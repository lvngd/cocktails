## Cocktail Generator

This is a cocktail generator class written in Python, and the idea is to generate cocktail ideas from a list of input ingredients.

## CocktailSuggester class

*   Takes a list of input ingredients.
*   Takes an optional ratio to create partial matches and suggest cocktails even if you're missing a couple of ingredients.
*   It creates a graph of cocktail ingredients from a list of recipes in `cocktails.txt`.
*   Searches for cocktail matches with depth-first search through the graph from each input ingredient.

## Visualization

The visualization is in D3.js.

Call `prepare_d3js_data()` on a `CocktailSuggester` instance to generate JSON data for the visualization.

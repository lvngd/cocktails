import json

from cocktails import CocktailSuggester



if __name__=='__main__':
	input_ingredients = ['cointreau', 'cola', 'lemon juice', 'vodka','ginger beer', 'rum', 'lime juice', 'orange juice', 'tequila','grenadine']

	cocktails_test = CocktailSuggester(input_ingredients, ratio=0.5)
	#test that certain cocktails are matches for these ingredients
	assert(cocktails_test.cocktail_matches == set(['cuba libre', 'screwdriver', 'moscow mule', 'tequila sunrise', 'dark and stormy', 'rum and coke']))

	input_two = ['cointreau', 'cola', 'lemon juice', 'vodka','ginger beer', 'rum', 'lime juice']

	input_three = ['fake ingredient', 'rum', 'cola', 'lemon juice', 'ginger beer', 'vodka']
	cocktails = CocktailSuggester(input_three, ratio=0.5,visualization=True)
	for option in cocktails.cocktail_matches:
		#test that cocktail matches are not also listed in partial_cocktails
		assert(option not in cocktails.partial_cocktails)

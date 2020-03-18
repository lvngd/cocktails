import json

"""

CocktailSuggester class to suggest cocktails to make from a list of input ingredients.


inputs: list of ingredients, separated by commas
		optional: ratio - ratio of ingredients it must have
		for example, 0.5 means it must have 50% of recipe ingredients
"""

class CocktailSuggester:
	def __init__(self, ingredients, ratio=0,visualization=False):
		self.ratio = ratio
		self.visualization = visualization
		self.ingredients = self.format_ingredients(ingredients)
		self.cocktails_to_ingredients, self.ingredients_to_cocktails, self.compatible_ingredients = self.get_cocktail_lookups()
		self.cocktail_matches = set()
		self.partial_cocktails = {}
		self.options = self.make_cocktail()

	def format_ingredients(self, ingredients):
		"""format and normalize ingredients for better matching"""
		to_replace = {'cointreau': 'triple sec', '&': 'and'}
		updated_ingredients = []
		for i in ingredients:
			i = i.lower().strip()
			if i in to_replace:
				ingredient = to_replace[i]
			else:
				ingredient = i
			updated_ingredients.append(ingredient)
		return updated_ingredients

	def get_cocktail_lookups(self):
		with open('cocktails.txt','r') as read:
			data = read.read().splitlines()
		cocktails_ingredients = {}
		ingredients_to_cocktails = {}
		#compatible ingredients are any ingredients that are found in a recipe together
		compatible_ingredients = {}
		for row in data:
			cocktail_recipe = row.split(',')
			cocktail_name = cocktail_recipe[0]
			ingredients = cocktail_recipe[1:]
			cocktails_ingredients[cocktail_name] = set(ingredients)
			for count,ingredient in enumerate(ingredients):
				if ingredient not in ingredients_to_cocktails:
					ingredients_to_cocktails[ingredient] = set([cocktail_name])
				else:
					ingredients_to_cocktails[ingredient].add(cocktail_name)
				if ingredient not in compatible_ingredients:
					compatible_ingredients[ingredient] = set([i for i in ingredients if i != ingredient])
				else:
					compatible_ingredients[ingredient].update([i for i in ingredients if i != ingredient])
		return cocktails_ingredients, ingredients_to_cocktails, compatible_ingredients

	def ingredients_pointing_to(self,ingredient):
		"""get ingredients pointing to this ingredient and return sorted list of ingredients in order of which has the most other ingredients pointing to it"""
		top_sorted = sorted(self.compatible_ingredients[ingredient],key=lambda x:len(self.compatible_ingredients[x]),reverse=True)
		return top_sorted

	def valid_cocktail(self,cocktail_ingredients):
		"""
		return True if the ingredients can form a valid cocktail
		"""
		if len(cocktail_ingredients) > 1:
			first_ingredient = None
			for ingredient in cocktail_ingredients:
				if not first_ingredient:
					first_ingredient = ingredient
				else:
					cocktail_list = self.ingredients_to_cocktails[first_ingredient]
					next_ingredient = ingredient
					next_cocktails = self.ingredients_to_cocktails[next_ingredient]
					#find common cocktails for each cocktail ingredient(set intersection)
					result_set = cocktail_list.intersection(next_cocktails)
					if not result_set:
						return False
		return True

	def matching_cocktails(self,ingredients):
		"""returns True if there is a cocktail match and False if not"""
		for cocktail,recipe_ingredients in self.cocktails_to_ingredients.items():
			if cocktail in self.partial_cocktails and cocktail in self.cocktail_matches:
				#remove full cocktail  matches from partial dictionary
				del self.partial_cocktails[cocktail]
			if ingredients == recipe_ingredients:
				self.cocktail_matches.add(cocktail)
				return True
			else:
				#check if ingredients make up part of a cocktail
				missing_ingredients = recipe_ingredients - ingredients
				ratio = len(missing_ingredients) / len(recipe_ingredients)
				if ratio > 0 and ratio < self.ratio:
					if cocktail not in self.partial_cocktails:
						self.partial_cocktails[cocktail] = missing_ingredients
					else:
						self.partial_cocktails[cocktail].update(missing_ingredients)
		return False

	def make_cocktail(self):
		"""

		depth first search starting with each input ingredient to find cocktail matches
		visualization=True means to stop after a couple of matches are found

		"""
		#steps for visualization
		steps = []
		count = 0
		matches_count = 0
		for ingredient in self.ingredients:
			if ingredient not in self.compatible_ingredients:
				print("can't find {} in any recipe - skipping".format(ingredient))
			else:
				ingredients_tried = []
				#initialize dfs stack with current input ingredient
				ingredients_to_try = [ingredient]
				#set of ingredients to check for valid ingredient combinations
				cocktail_recipe = set()
				while ingredients_to_try:
					current = ingredients_to_try.pop()
					count += 1
					steps.append({"node": current, "color": "possible"})
					cocktail_recipe.add(current)
					ingredients_tried.append(current)
					#get neighbors
					potential_ingredients = self.ingredients_pointing_to(current)
					for ing in potential_ingredients:
						count += 1
						#make sure it's an ingredient we have
						if ing in self.ingredients:
							cocktail_recipe.add(ing)
							count += 1
							steps.append({"node": ing, "color": 'possible'})
							if self.valid_cocktail(cocktail_recipe):
								count += 1
								found_match = self.matching_cocktails(cocktail_recipe)
								#for visualization
								if found_match:
									matches_count += 1
									for ingredient in cocktail_recipe:
										steps.append({"node": ingredient, "color": 'match'})
									if matches_count > 2:
										if self.visualization:
											self.animation_steps = steps
											return
								#add to stack
								if ing not in ingredients_tried and ing not in ingredients_to_try:
									ingredients_to_try.append(ing)
							steps.append({"node": ing, "color": 'no_match'})
							count += 1
							cocktail_recipe.remove(ing)
					steps.append({"node": current, "color": "no_match"})
		self.animation_steps = steps
		return

	def prepare_d3js_data(self):
		"""creates nodes and links of compatible ingredients for graph"""
		node_numbers = {} 
		#count is the node ID
		count = 0 
		nodes = []
		links = []
		for ing1,compatible in cocktails.compatible_ingredients.items(): 
			if ing1 not in node_numbers: 
				source_id = count
				node_numbers[ing1] = source_id
				nodes.append({"id": "{}".format(source_id), "name": "{}".format(ing1)})
				count += 1 
			else:
				source_id = node_numbers[ing1]
			for c in compatible: 
				if c not in node_numbers: 
					node_id = count
					node_numbers[c] = node_id
					nodes.append({"id": "{}".format(node_id), "name": "{}".format(c)})
					count += 1 
				else:
					#get node id number
					node_id = node_numbers[c]
				links.append({"source": "{}".format(source_id), "target": "{}".format(node_id)})
		data = {"nodes": nodes, "links": links, "steps": self.animation_steps}
		with open('cocktails.json','w') as write: 
			json.dump(animation_data,write)
		return data
		

if __name__=='__main__':
	input_ingredients = ['rum', 'cola', 'lemon juice', 'ginger beer', 'vodka']
	cocktails = CocktailSuggester(input_ingredients, ratio=0.5,visualization=True)
	for option in cocktails.cocktail_matches:
		print(option)
	for partial_cocktail,missing_ingredients in cocktails.partial_cocktails.items():
		print("if you had {} you could make {}".format(missing_ingredients,partial_cocktail))

	#uncomment below to write D3.js JSON data to file in same directory.
	#cocktails.prepare_d3js_data()

	
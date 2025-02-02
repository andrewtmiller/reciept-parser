from bs4 import BeautifulSoup
import sys

sys.dont_write_bytecode = True
CATEGORIES = {
    "Personal": ["shampoo","tampons","conditioner","toothpaste","deoderant","eyeliner","blush","lotion","cosmetics","mascara","makeup","face serum","facial","scalp treatment"],
    "Groceries": ["pasta", "turkey", "tomato", "yeast", "baking powder", "baking soda", "flour", "noodles", "peanut", "preserves","cereal","grape","hot dog","yogurt","sugar","sausage","bread","cheese","banana","milk","ham","dressing","butter","whipping cream","pretzel","juice","dough","mushroom","beef","potato","chicken","ground cinnamon","trail mix","pickle","pie crust","eggs","lunchable","peppermint extract","instant coffee","beans","applesauce","chips","sprinkle","rice", "pineapple", "quinoa","onions","parsley","snacks","corn starch","pizza","lime","baking cocoa", "tofu","apples","clementines","bok choy","ginger root","carrots","chocolate","marshmallows","broth","cooking spray","pure pumpkin","coconut flakes","pecans","avocado","egg whites","cake batter flavor","bacon","salsa","cilantro","distilled water","drinking water","coca-cola","nutritional shake","zbar","fruit roll","water"],
    "Clothing": ["sweater","socks","t-shirt","underwear","shoe","shirt","body suit","tights","gloves","boots","pullover","clogs","leggings","ballet flats"],
    "Home Supplies": ["dryer sheets","bowls","straws","coffee filter","laundry","ziploc","snack bag","plate","batteries","extension cord","command strips","outlet","aluminum foil","parchment paper","dish soap", "command 8pk heavy phs adhesives","toiletwand"],
    "Pharmacy": ["cough drops", "throat drops"],
    "Baby Supplies": ["diapers"],
    "Gifts": ["wrapping paper", "gift wrap", "inflatables yard","christmas tree","nutcraker"],
    "Furnishings": ["curtain"],
    "Other": []
}

def get_content(f):
    with open(f,'r', encoding="utf-8") as file:
        return BeautifulSoup(file.read(), 'html.parser')

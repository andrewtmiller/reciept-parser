from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Category, Term
from organizer import CategoryOrganizer

# SQLite database URL
DATABASE_URL = "sqlite:///categories.db"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Create tables
Base.metadata.create_all(engine)

# Migrate data from CategoryOrganizer
organizer = CategoryOrganizer()
for category_name, terms in organizer.categories.items():
    category = Category(name=category_name)
    session.add(category)
    session.flush()  # Assigns an ID to the category
    for term in terms:
        session.add(Term(name=term, category_id=category.id))
session.commit()
print("Migration complete!")

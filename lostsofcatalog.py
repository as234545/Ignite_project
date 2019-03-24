
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, CatalogItem, User

engine = create_engine('sqlite:///catalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

User1 = User(name="Aura M", email="mmq1114@gmail.com",
             picture='https://lh3.googleusercontent.com/a-/AAuE7mDzT5ws-XUJisun8vx5j5HsZqyUlUrzMWSztsyLEA=s192')
session.add(User1)
session.commit()

# Menu for UrbanBurger

CatalogItem1 = CatalogItem( user_id=1, title="Kobo  book service",
                           content=" If you have a 50+ minute commute each way every day you can use Kobo app . Kobo plans are cheaper than Audible and you can buy additional credits whenever you want (in bulks of 3). We have a big library.", catalog_type="Education")

session.add(CatalogItem1)
session.commit()


CatalogItem2 = CatalogItem( user_id=1, title="A farming-style game",
                           content=" The premise of the game is that you have been sent out from your community after a nuclear war has devastated the world in order to provide food for your community. Your community is nearing on starvation as supplies scavenged from supermarkets and homes are becoming increasingly scarce", catalog_type="Games")

session.add(CatalogItem2)
session.commit()

CatalogItem3 = CatalogItem( user_id=1, title="Shared 3D Printing",
                           content=" Users can upload parts to print, and owners of 3D printers (in the nearby area) can print them for a small fee. Each user would receive ratings which would help reduce the number of users printing who don't know what they are doing.", catalog_type="Comany")


session.add(CatalogItem3)
session.commit()


# Menu for Super Stir Fry

CatalogItem4 = CatalogItem( user_id=1, title="Face and Fingerprint Recognition Security Device",
                           content=" What do you guys think about a Face and Fingerprint Device that unlocks your doors? I saw something about this somewhere online, where it would be affordable and all that. Just thought it would be a cool startup idea for some people.", catalog_type="Comany")

session.add(CatalogItem4)
session.commit()


print("added catalog items!") 

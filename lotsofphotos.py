from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db_setup import Photo, Base, Species, User

engine = create_engine('sqlite:///animalphotos.db')
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


# Create dummy user
user1 = User(username="Mohamed Essam", email="el3os@fakemail.com",
             picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(user1)
session.commit()

# Photos for Cats
species1 = Species(name="Cats")

session.add(species1)
session.commit()

photo1 = Photo(user_id=1, title="Woman Yelling at Cat Meme Takes Over", description="The cat with the attitude is named Smudge, also referred to as Smudge the Table Cat.  He first found fame when his owner posted a picture of him to Tumbler as he lounged on a table with the caption: “he no like vegetables”. Apparently the owner saw something in the way of talent with her fur baby and started Smudge an Instagram page, @smudge_lord, that  now has 1.1million followers.",
                     url="https://townsquare.media/site/87/files/2019/11/Woman-Cat-Meme.jpg", user=user1, species=species1)

session.add(photo1)
session.commit()


photo2 = Photo(user_id=1, title="The Face That Launched A Million Memes", description="Grumpy Cat was rather like the real-life incarnation of Garfield, whose entire appeal rests on being a cat who dislikes Mondays (despite not having a job). The Garfield brand has permeated every conceivable merchandising and media niche, and the fictional feline (perhaps inevitably) paired up with his grumpy counterpart in a book series.",
                     url="https://thumbor.forbes.com/thumbor/960x0/https%3A%2F%2Fspecials-images.forbesimg.com%2Fdam%2Fimageserve%2Fb510ccc8012f4718bd691a6b78b70921%2F960x0.jpg", user=user1, species=species1)

session.add(photo2)
session.commit()

photo3 = Photo(user_id=1, title="How cute this is !!",
                     url="https://live.staticflickr.com/3689/8989851909_9b78222fbb.jpg", user=user1, species=species1)

session.add(photo3)
session.commit()

photo4 = Photo(user_id=1, title="The Best Stitch <3",
                     url="https://i.ibb.co/YZmQSFq/stitch.png", user=user1, species=species1)

session.add(photo4)
session.commit()

photo5 = Photo(user_id=1, title="The laughing cat",
                     url="https://farm1.staticflickr.com/969/41428417955_03d64e2a02_b.jpg", user=user1, species=species1)

session.add(photo5)
session.commit()

photo6 = Photo(user_id=1, title="Stitch the real moon",
                     url="https://i.ibb.co/DK4KyJr/stitch.jpg", user=user1, species=species1)

session.add(photo6)
session.commit()

photo7 = Photo(user_id=1, title="Cats are Cute !!",
                     url="https://dreamastromeanings.com/wp-content/uploads/2019/07/Cat-Crying-at-Night-Superstition-and-Meaning.jpg", user=user1, species=species1)

session.add(photo7)
session.commit()

# Photos for Turtles
species2 = Species(name="Turtles")

session.add(species2)
session.commit()


photo1 = Photo(user_id=1, title="Green Sea Turtle!", description="The green sea turtle is an endangered species with a population that is, unfortunately, on the decline. However, they can be seen on the Great Barrier Reef and Lady Elliot Island, at the southern end of the reef. This is a perfect place to see these oceanic reptiles. While snorkelling, with my camera in an underwater housing, this inquisitive turtle decided to have a closer look, investigating me and my camera. It was an incredible experience and wonderful to photograph this creature in the wild.",
                     url="https://cdn11.bigcommerce.com/s-s5d5u8bn61/images/stencil/1280x1280/products/238/1076/0E3A7368-1_Lagoon_green_turtle__75795.1548630091.jpg", user=user1, species=species2)

session.add(photo1)
session.commit()

photo2 = Photo(user_id=1, title="A very young turtle", description="Reports of tiny turtles being given away as prizes for a carnival game at the San Juan County Fair spread across the island community’s social media groups on Friday, Aug. 16. Islanders claimed to have seen teenagers throw the shelled reptiles off of the Zipper, a carnival attraction that takes riders more than 50 feet into the air.",
                     url="http://www.islandssounder.com/wp-content/uploads/2019/08/18147278_web1_TSR-Turtletroubles-JSJ-190821.jpg", user=user1, species=species2)

session.add(photo2)
session.commit()

photo3 = Photo(user_id=1, title="The lovely Pep",
                     url="https://i.ibb.co/nj3tJk4/stitch.png", user=user1, species=species2)

session.add(photo3)
session.commit()

photo4 = Photo(user_id=1, title="How beautiful is this!",
                     url="https://www.wthr.com/sites/default/files/styles/article_image/public/2019/06/28/boxturtle970ss.jpg", user=user1, species=species2)

session.add(photo4)
session.commit()


# Photos for Dogs
species3 = Species(name="Dogs")

session.add(species3)
session.commit()


photo1 = Photo(title="Cute Dog Kiss Of The Day", description="With how cute I am I could be charging a fortune. But I am a simple dog. All I need are kisses and a full food dish.",
                     url="https://i.pinimg.com/originals/3e/8a/d9/3e8ad9163e7633370687539efb9d8378.jpg", user=user1, species=species3)

session.add(photo1)
session.commit()

photo2 = Photo(title="your daily cute puppy",
                     url="https://static.standard.co.uk/s3fs-public/thumbnails/image/2019/03/15/17/pixel-dogsofinstagram-3-15-19.jpg", user=user1, species=species3)

session.add(photo2)
session.commit()

photo3 = Photo(title="Cute Dog !",
                     url="https://s1.ibtimes.com/sites/www.ibtimes.com/files/styles/embed/public/2018/08/26/cute-dog.jpg", user=user1, species=species3)

session.add(photo3)
session.commit()

photo4 = Photo(title="Having a flight with a dog",
                     url="https://cdn.cnn.com/cnnnext/dam/assets/180316113418-travel-with-a-dog-3.jpg", user=user1, species=species3)

session.add(photo4)
session.commit()

photo5 = Photo(title="An Adorable puppy",
                     url="https://assets.blog.slice.ca/imageserve/wp-content/uploads/2019/01/10142947/cute-dog-names-ideas-cardi/x.jpg", user=user1, species=species3)

session.add(photo5)
session.commit()




# Photos for Birds
species1 = Species(name="Birds")

session.add(species1)
session.commit()


photo5 = Photo(title="Baby Hawk", description="oh my goodness cute baby hawk *cough* *cough* I mean adult peregrine falcon.",
                     url="https://i.pinimg.com/originals/c3/f8/08/c3f808a94c3ceaec34e854e470f57748.jpg", user=user1, species=species1)

session.add(photo5)
session.commit()

photo6 = Photo(title="Hedwig",
                     url="https://i.pinimg.com/564x/75/71/6a/75716ace36067e0f34709a01830ad826.jpg", user=user1, species=species1)

session.add(photo6)
session.commit()

photo7 = Photo(title="Hedwig",
                     url="https://i.pinimg.com/564x/75/71/6a/75716ace36067e0f34709a01830ad826.jpg", user=user1, species=species1)

session.add(photo7)
session.commit()

photo8 = Photo(title="Hens are the best",
                     url="https://image.freepik.com/free-photo/big-nice-beautiful-white-black-hens-feeding-outdoors-green-meadow_127089-67.jpg", user=user1, species=species1)

session.add(photo8)
session.commit()

photo9 = Photo(title="Nice looking birds",
                     url="http://exporters.com.tr/data/frontFiles/b2b/product_images/1%20Nice%20birs.jpg", user=user1, species=species1)

session.add(photo9)
session.commit()

print("added menu items!")
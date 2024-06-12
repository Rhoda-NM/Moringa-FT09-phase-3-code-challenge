from database.setup import create_tables, drop_tables
from database.connection import get_db_connection
from models.article import Article
from models.author import Author
from models.magazine import Magazine


def main():
    drop_tables()
    create_tables()
    Author1=Author("Linda")
    Author2=Author("Rowling")
    magazine1=Magazine("Vogue","Fashion")
    magazine2=Magazine("Forbes","Business")
    article1 =Article(Author1,magazine1,"The upcoming met gala")
    article2 =Article(Author2,magazine2,"The rapid growth of sustainable business models in Asia ")
    #print(article1.get_Author(),article1.get_magazine())
    #print(article2.get_Author(),article2.get_magazine())
    #print(Author1.articles())
    print(Author1.magazines())
    print(magazine1.articles())
    print(magazine1.contributors())
    print(magazine1.article_titles())
    print(magazine1.contributing_authors())

if __name__ == "__main__":
    main()

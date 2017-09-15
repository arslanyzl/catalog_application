# coding=utf-8
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from database_setup import League, Base, Club, User
 
engine = create_engine('sqlite:///soccerteam.db')

Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)

session = DBSession()

# Create dummy user
User1 = User(name="Arslan Yazlyyev", email="arslanyazly@gmail.com", picture="https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png")
session.add(User1)
session.commit()

#league
league1 = League(user_id=1, name = "England Premier League")

session.add(league1)
session.commit()

team1 = Club(user_id=1, name = "Arsenal",
             founded = "1886",
             description = "Stadium: Emirates Stadium,  Manager: Arsene Wenger,  Location: London, United Kingdom",
             league = league1)

session.add(team1)
session.commit()

team2 = Club(user_id=1, name = "Chelsea",
             founded = "1905",
             description = "Stadium: Stamford Bridge,  Manager: Antonio Conte,  Location: London, United Kingdom",
             league = league1)

session.add(team2)
session.commit()


team3 = Club( user_id=1, name = "Manchester United",
             founded = "1878",
             description = "Stadium: Old Trafford,  Manager: Jose Mourinho,  Location: Manchester, United Kingdom",
             league = league1)

session.add(team3)
session.commit()


team4 = Club(user_id=1, name = "Liverpool",
             founded = "1892",
             description = "Manager: Jurgen Klopp,  Arena/Stadium: Anfield,  Location: Liverpool, United Kingdom",
             league = league1)

session.add(team4)
session.commit()


team5 = Club(user_id=1, name = "Manchester City",
             founded = "1894",
             description = "Manager: Pep Guardiola,  Stadium: Etihad Stadium Location:  Manchester, United Kingdom",            
             league = league1)

session.add(team5)
session.commit()

league2 = League(user_id=1, name = "Spain La Liga")

session.add(league1)
session.commit()

team1 = Club(user_id=1, name = "Barcelona",
             founded = "1886",
             description = "Stadium: Camp Nou,  Manager: Ernesto Valverde,  Location: Barcelona, Spain",            
             league = league2)

session.add(team1)
session.commit()


team2 = Club(user_id=1, name = "Real Madrid",
             founded = "1905",
             description = "Stadium: Santiago Bernabeu Stadium,  Manager: Zinedine Zidane,  Location: Madrid, Spain",
             league = league2)

session.add(team2)
session.commit()


team3 = Club(user_id=1, name = "Valencia",
             founded = "1878",
             description = "Manager: Marcelino Garcia Toral,  Stadium: Mestalla Stadium,  Location: Madrid, Spain",
             league = league2)

session.add(team3)
session.commit()


team4 = Club(user_id=1, name = "Atletico Madrid",
             founded = "1892",
             description = "Stadium: Wanda Metropolitano,  Manager: Diego Simeone,  Location: Madrid, Spain",
             league = league2)

session.add(team4)
session.commit()


team5 = Club(user_id=1, name = "Sevilla",
             founded = "1894",
             description = "Manager: Eduardo Berizzo,  Stadium: Ramon Sanchez Pizjuan Stadium,  Location: Seville, Spain",
             league = league2)

session.add(team5)
session.commit()

league3 = League(user_id=1, name = "Germany Bundesliga")

session.add(league3)
session.commit()

team1 = Club(user_id=1, name = "Bayern Munich",
             founded = "1900",
             description = "Stadium: Allianz Arena,  Manager: Carlo Ancelotti,  Location: Munich, Germany",
             league = league3)

session.add(team1)
session.commit()

team2 = Club(user_id=1, name = "Borussia Dortmund",
             founded = "1909",
             description = "Stadium: Westfalenstadion,  Manager: Peter Bosz,  Location: Dortmund, Germany",
             league = league3)

session.add(team2)
session.commit()


team3 = Club( user_id=1, name = "Schalke 04",
             founded = "1904",
             description = "Stadium: Veltins-Arena,  Manager: Domenico Tedesco,  Location: Gelsenkirchen, Germany",
             league = league3)

session.add(team3)
session.commit()


team4 = Club(user_id=1, name = "Wolfsburg",
             founded = "1945",
             description = "Stadium: Volkswagen Arena,  Manager: Andries Jonker,  Location: Wolfsburg, Germany",
             league = league3)

session.add(team4)
session.commit()


team5 = Club(user_id=1, name = "Werder Bremen",
             founded = "1894",
             description = "Stadium: Weser-Stadion,  Manager: Alexander Nouri,  Location: Bremen, Germany",            
             league = league3)

session.add(team5)
session.commit()


league4 = League(user_id=1, name = "Italy Seria A")

session.add(league4)
session.commit()

team1 = Club(user_id=1, name = "Juventus",
             founded = "1897",
             description = "Manager: Massimiliano Allegri,  Stadium: Juventus Stadium,  Location: Turin, Italy",
             league = league4)

session.add(team1)
session.commit()

team2 = Club(user_id=1, name = "AC Milan",
             founded = "1899",
             description = "Stadium: San Siro Stadium,  Manager: Vincenzo Montella,  Location: Milan, Italy",
             league = league4)

session.add(team2)
session.commit()


team3 = Club( user_id=1, name = "Inter",
             founded = "1908",
             description = "Stadium: San Siro Stadium,  Manager: Luciano Spalletti,  Location: Milan, Italy",
             league = league4)

session.add(team3)
session.commit()


team4 = Club(user_id=1, name = "Roma",
             founded = "1927",
             description = "Stadium: Stadio Olimpico,  Manager: Eusebio Di Francesco,  Location: Roma, Italy",
             league = league4)

session.add(team4)
session.commit()


team5 = Club(user_id=1, name = "Napoli",
             founded = "1926",
             description = "Manager: Maurizio Sarri,  Stadium: Stadio San Paolo,  Location: Napoli, Italy",            
             league = league4)

session.add(team5)
session.commit()

print "added Soccer teams!"

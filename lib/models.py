from sqlalchemy import ForeignKey, Column, Integer, String, Boolean, MetaData, create_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)

class Audition(Base):
    __tablename__ = "auditions"

    id = Column(Integer, primary_key=True)
    actor = Column(String())
    location = Column(String())
    hired = Column(Boolean, default=False)

    role_id = Column(Integer(), ForeignKey('roles.id'))
    role = relationship('Role', back_populates='auditions')  

    def call_back(self):
        self.hired = True

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key = True)
    character_name = Column(String())

    auditions = relationship('Audition', back_populates='role')

    def actors(self):
        return [audition.actor for audition in self.auditions]
    
    def locations(self):
        return [audition.location for audition in self.auditions]
    
    def lead(self):
        hired_auditions = [audition for audition in self.auditions if audition.hired]
        return hired_auditions[0].actor if hired_auditions else "no actor has been hired for this role"

    def understudy(self):
        hired_auditions = [audition for audition in self.auditions if audition.hired]  
        return hired_auditions[1].actor if len(hired_auditions) > 1 else "no actor has been hired for understudy for this role"
    
# Database Setup
engine = create_engine("sqlite:///moringa_theater.db")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
session.query(Audition).delete()
session.query(Role).delete()
session.commit()

# Adding sample data
role1 = Role(character_name="Samantha")
role2 = Role(character_name="Benny")

session.add_all([role1, role2])
session.commit()

audition1 = Audition(actor="Sam Griffins", location="Nairobi", role_id=role2.id)
audition2 = Audition(actor="Janet Gayle", location="Nairobi", role_id=role1.id)
audition3 = Audition(actor="Kylie Smith", location="Nairobi", role_id=role1.id)

session.add_all([audition1, audition2, audition3])
session.commit()

#Test outputs
print("All Roles:")
for role in session.query(Role).all():
    print(f"{role.id}: {role.character_name}")

print("\nAll Auditions:")
for audition in session.query(Audition).all():
    print(f"{audition.actor} auditioned for {audition.role.character_name} in {audition.location}")

# Testing Methods
print("\nActors for Samantha:", role1.actors())
print("Locations for Samantha:", role1.locations())
audition1.call_back()
session.commit()
print("Lead for Benny:", role2.lead())

# Test: Role.auditions returns all associated auditions
print("\nAuditions for Samantha:")
for audition in role1.auditions:
    print(f"{audition.actor} auditioned in {audition.location}")

print("\nAuditions for Benny:")
for audition in role2.auditions:
    print(f"{audition.actor} auditioned in {audition.location}")

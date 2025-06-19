import factory
from sqlalchemy.orm import Session

from src.models.user import User, Role, UserRole
from src.models.activity import Activity


class BaseFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        abstract = True
        sqlalchemy_session = None  # Will be set by test_db fixture
        sqlalchemy_session_persistence = "commit"


class RoleFactory(BaseFactory):
    class Meta:
        model = Role

    name = factory.Iterator(["client", "coach", "admin"])


class UserFactory(BaseFactory):
    class Meta:
        model = User

    email = factory.Sequence(lambda n: f"user{n}@example.com")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    phone = factory.Faker("msisdn")
    hashed_password = (
        "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"  # "password"
    )

    @factory.post_generation
    def roles(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for role in extracted:
                self.roles.append(role)
        else:
            # Default to client role if none specified
            self.roles.append(RoleFactory())


class ActivityFactory(BaseFactory):
    class Meta:
        model = Activity

    name = factory.Faker("sentence", nb_words=3)
    description = factory.Faker("paragraph")
    coach = None
    start_time = factory.Faker("date_time_this_year", after_now=True)
    end_time = factory.LazyAttribute(
        lambda o: factory.Faker(
            "date_time_between", start_date=o.start_time, end_date="+2h"
        ).evaluate(None, None, {"locale": "en"})
    )
    credits_required = factory.Faker("random_int", min=1, max=3)
    max_capacity = factory.Faker("random_int", min=3, max=30)


def set_sqlalchemy_session(session: Session):
    """Set the SQLAlchemy session for all factories."""
    BaseFactory._meta.sqlalchemy_session = session
    # Ensure the session is available for any sub-factories
    for factory_class in BaseFactory.__subclasses__():
        if hasattr(factory_class._meta, "sqlalchemy_session"):
            factory_class._meta.sqlalchemy_session = session

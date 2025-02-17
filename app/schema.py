import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from app.models import db, User, Donation

class UserType(SQLAlchemyObjectType):
    class Meta:
        model = User

class DonationType(SQLAlchemyObjectType):
    class Meta:
        model = Donation

class Query(graphene.ObjectType):
    users = graphene.List(UserType)
    donations = graphene.List(DonationType, user_id=graphene.Int())

    def resolve_users(self, info):
        return User.query.all()

    def resolve_donations(self, info, user_id):
        return Donation.query.filter_by(user_id=user_id).all()

class CreateUser(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        password_hash = graphene.String(required=True)
        custom_url = graphene.String(required=True)

    user = graphene.Field(UserType)

    def mutate(self, info, username, email, password_hash, custom_url):
        user = User(username=username, email=email, password_hash=password_hash, custom_url=custom_url)
        db.session.add(user)
        db.session.commit()
        return CreateUser(user=user)

class CreateDonation(graphene.Mutation):
    class Arguments:
        user_id = graphene.Int(required=True)
        amount = graphene.Float(required=True)
        donor_name = graphene.String()

    donation = graphene.Field(DonationType)

    def mutate(self, info, user_id, amount, donor_name=None):
        donation = Donation(user_id=user_id, amount=amount, donor_name=donor_name)
        db.session.add(donation)
        db.session.commit()
        return CreateDonation(donation=donation)

class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    create_donation = CreateDonation.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)

import graphene
from graphene_django import DjangoObjectType
from .models import Todo 

class TodoType(DjangoObjectType):
    class Meta:
        model = Todo


class AddTodoMutation(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        description = graphene.String(required=True)

    todo = graphene.Field(TodoType)

    @classmethod
    def mutate(cls,root,info,title,description):
        todo = Todo(title=title,description=description)
        todo.save()
        return AddTodoMutation(todo=todo)

class UpdateTodoMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        title = graphene.String(required=True)
        description = graphene.String(required=True)
        completed = graphene.Boolean()

    todo = graphene.Field(TodoType)

    @classmethod
    def mutate(cls,root,info,id,title,description,completed):
        todo = Todo.objects.get(id=id)
        todo.title = title,
        todo.description = description,
        todo.completed = completed
        todo.save()
        return UpdateTodoMutation(todo=todo)

class DeleteTodoMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
    todo = graphene.Field(TodoType)

    @classmethod
    def mutate(cls,root,info,id):
        todo = Todo.objects.get(id=id)
        todo.delete()
        

class Query(graphene.ObjectType):
    todos = graphene.List(TodoType)
    todo = graphene.Field(TodoType,id=graphene.Int())

    def resolve_todos(root,info):
        return Todo.objects.all()

    def resolve_todo(root,info,id):
        return Todo.objects.get(pk=id)


class Mutation(graphene.ObjectType):
    add_todo = AddTodoMutation.Field()
    update_todo = UpdateTodoMutation.Field()
    delete_todo = DeleteTodoMutation.Field()

schema = graphene.Schema(query=Query,mutation=Mutation)

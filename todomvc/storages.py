class ToDoStorage(object):
    # Stores a list of todos, such that retrieval, replacement and deletion is fast O(time taken to look up in a dictionary)
    # Also a list of todos can be retrieved in O(n) time, n being the number of todos.
    def __init__(self):
        self.max_todo_id = 0
        self.todos = {}

    def create(self, todo):
        todo_id = self.max_todo_id + 1
        self.max_todo_id = todo_id
        todo['id'] = todo_id
        self.todos[todo_id] = todo
        return todo_id

    def update(self, todo):
        self.todos[todo['id']] = todo

    def delete(self, todo_id):
        del self.todos[todo_id]

    def get(self, todo_id):
        return self.todos[todo_id]

    def list(self):
        return self.todos.values()


class SessionStorage(object):
    def __init__(self):
        self.sessions = {}

    def new_session(self, user_name):
        session_id = 182352
        self.sessions[session_id] = user_name
        return session_id
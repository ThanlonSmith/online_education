class Router:
    def db_for_read(self, model, **hints):
        return 'remote_mysql'

    def db_for_write(self, model, **hints):
        return 'default'

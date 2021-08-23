class MDMRouter:
    """
    A router to control all database operations on models in the
    auth and contenttypes applications.
    """
    route_app_labels = {'mdm_parametrizaciones','mdm_clientes','mdm_facturas','mdm_negocios','mdm_prospectosClientes'}


    def db_for_read(self, model, **hints):
        """
        Attempts to read auth and contenttypes models go to vittoria_mdm_db.
        """
        if model._meta.app_label in self.route_app_labels:
            return 'vittoria_mdm_db'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write auth and contenttypes models go to vittoria_mdm_db.
        """
        if model._meta.app_label in self.route_app_labels:
            return 'vittoria_mdm_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the auth or contenttypes apps is
        involved.
        """
        if (
            obj1._meta.app_label in self.route_app_labels or
            obj2._meta.app_label in self.route_app_labels
        ):
           return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the auth and contenttypes apps only appear in the
        'vittoria_mdm_db' database.
        """
        if app_label in self.route_app_labels:
            return db == 'vittoria_mdm_db'
        return None

class MDPRouter:
    """
    A router to control all database operations on models in the
    auth and contenttypes applications.
    """
    route_app_labels = {'mdp_parametrizaciones','mdp_categorias','mdp_productos','mdp_fichaTecnicaProductos','mdp_subCategorias'}

    def db_for_read(self, model, **hints):
        """
        Attempts to read auth and contenttypes models go to vittoria_mdp_db.
        """
        if model._meta.app_label in self.route_app_labels:
            return 'vittoria_mdp_db'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write auth and contenttypes models go to vittoria_mdp_db.
        """
        if model._meta.app_label in self.route_app_labels:
            return 'vittoria_mdp_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the auth or contenttypes apps is
        involved.
        """
        if (
            obj1._meta.app_label in self.route_app_labels or
            obj2._meta.app_label in self.route_app_labels
        ):
           return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the auth and contenttypes apps only appear in the
        'vittoria_mdp_db' database.
        """
        if app_label in self.route_app_labels:
            return db == 'vittoria_mdp_db'
        return None

class MDORouter:
    """
    A router to control all database operations on models in the
    auth and contenttypes applications.
    """
    route_app_labels = {'mdo_parametrizaciones','mdo_generarOferta','mdo_prediccionCrosseling','mdo_prediccionProductosNuevos','mdo_prediccionRefil'}

    def db_for_read(self, model, **hints):
        """
        Attempts to read auth and contenttypes models go to vittoria_mdo_db.
        """
        if model._meta.app_label in self.route_app_labels:
            return 'vittoria_mdo_db'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write auth and contenttypes models go to vittoria_mdo_db.
        """
        if model._meta.app_label in self.route_app_labels:
            return 'vittoria_mdo_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the auth or contenttypes apps is
        involved.
        """
        if (
            obj1._meta.app_label in self.route_app_labels or
            obj2._meta.app_label in self.route_app_labels
        ):
           return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the auth and contenttypes apps only appear in the
        'vittoria_mdo_db' database.
        """
        if app_label in self.route_app_labels:
            return db == 'vittoria_mdo_db'
        return None

class GDORouter:
    """
    A router to control all database operations on models in the
    auth and contenttypes applications.
    """
    route_app_labels = {'gdo_parametrizaciones','gdo_gestionOferta'}

    def db_for_read(self, model, **hints):
        """
        Attempts to read auth and contenttypes models go to vittoria_gdo_db.
        """
        if model._meta.app_label in self.route_app_labels:
            return 'vittoria_gdo_db'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write auth and contenttypes models go to vittoria_gdo_db.
        """
        if model._meta.app_label in self.route_app_labels:
            return 'vittoria_gdo_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the auth or contenttypes apps is
        involved.
        """
        if (
            obj1._meta.app_label in self.route_app_labels or
            obj2._meta.app_label in self.route_app_labels
        ):
           return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the auth and contenttypes apps only appear in the
        'vittoria_gdo_db' database.
        """
        if app_label in self.route_app_labels:
            return db == 'vittoria_gdo_db'
        return None

class GDERouter:
    """
    A router to control all database operations on models in the
    auth and contenttypes applications.
    """
    route_app_labels = {'gde_parametrizaciones','gde_gestionEntrega'}

    def db_for_read(self, model, **hints):
        """
        Attempts to read auth and contenttypes models go to vittoria_gde_db.
        """
        if model._meta.app_label in self.route_app_labels:
            return 'vittoria_gde_db'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write auth and contenttypes models go to vittoria_gde_db.
        """
        if model._meta.app_label in self.route_app_labels:
            return 'vittoria_gde_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the auth or contenttypes apps is
        involved.
        """
        if (
            obj1._meta.app_label in self.route_app_labels or
            obj2._meta.app_label in self.route_app_labels
        ):
           return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the auth and contenttypes apps only appear in the
        'vittoria_gde_db' database.
        """
        if app_label in self.route_app_labels:
            return db == 'vittoria_gde_db'
        return None
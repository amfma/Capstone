from flask_admin.contrib.sqla import ModelView


class ComunaAdmin(ModelView):
    column_hide_backrefs = False
    columns = ('nombre', 'region')
    form_columns = columns

class DireccionAdmin(ModelView):
    column_hide_backref = False
    columns = ('comuna', 'usuario', 'calle', 'numero', 'comentario')
    form_columns = columns
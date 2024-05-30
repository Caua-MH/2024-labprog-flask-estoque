from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms.fields.choices import SelectField
from wtforms.fields.numeric import IntegerField, DecimalField
from wtforms.fields.simple import StringField, BooleanField, SubmitField
from wtforms.validators import InputRequired, Length, NumberRange


class ProdutoForm(FlaskForm):
    nome = StringField(label="Nome do produto",
                       validators=[InputRequired("É obrigatório definir o nome de produto"),
                                   Length(max=100, message="O produto pode ter até 100 caracteres")])
    preco = DecimalField(label="Preço", places=2,
                         validators=[InputRequired("O produto precisa ter um preço"),
                                     NumberRange(min=0.00,
                                                 message="Os preços devem ser positivos")])
    estoque = IntegerField(label="Estoque",
                           validators=[InputRequired(message="É preciso definir o estoque"),
                                       NumberRange(min=0, message="O estoque precisa ser positivo")])
    ativo = BooleanField(label="Ativo?",
                         validators=[InputRequired(message="É preciso dizer se o produto está ou não ativo")])
    foto = FileField(label="Foto do produto",
                     validators=[FileAllowed(['jpg', 'png'], message = "Apenas arquivos JPG ou PNG")])
    categoria = SelectField(label="categoria do produto",
                            validators=[InputRequired(message="Selecione uma categoria")])
    submit = SubmitField()
import uuid
from base64 import b64decode
import io
from typing import Optional

from PIL import Image

from sqlalchemy import Boolean, DECIMAL, ForeignKey, Integer, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base_mixin import BasicRepositoryMixin, TimeStampMixin
from src.modules import db


class Produto(db.Model, TimeStampMixin, BasicRepositoryMixin):
    __tablename__ = 'produtos'
    id: Mapped[Uuid] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    preco: Mapped[DECIMAL] = mapped_column(DECIMAL(10, 2), default=0.00)
    estoque: Mapped[Integer] = mapped_column(Integer, nullable=False, default=0)
    estoque_critico: Mapped[Integer] = mapped_column(Integer, nullable=True, default=1)
    ativo: Mapped[Boolean] = mapped_column(Boolean, default=True)
    categoria_id: Mapped[Uuid] = mapped_column(Uuid(as_uuid=True), ForeignKey('categorias.id'))
    foto_base64: Mapped[Optional[Text]] = mapped_column(Text, nullable=True)
    foto_mime: Mapped[String] = mapped_column(String(64), nullable=True)
    possui_foto: Mapped[Boolean] = mapped_column(Boolean, default=False)

    categoria = relationship('Categoria', back_populates='lista_de_produtos')

    @property
    def imagem(self):
        if not self.possui_foto:
            saida = io.BytesIO()
            entrada = Image.new('RGB', (480, 480), (128, 128, 128))
            formato = "PNG"
            entrada.save(saida, format=formato)
            conteudo = saida.getvalue()
            tipo = 'image/png'
        else:
            conteudo = b64decode(self.foto_base64)
            tipo = self.foto_mime
        return conteudo, tipo

    def thumbnail(self, size: int = 128):
        if not self.possui_foto:
            saida = io.BytesIO()
            entrada = Image.new('RGB', (size, size), (128, 128, 128))
            formato = "PNG"
            entrada.save(saida, format=formato)
            conteudo = saida.getvalue()
            tipo = 'image/png'
        else:
            arquivo = io.BytesIO(b64decode(self.foto_base64))
            saida = io.BytesIO()
            entrada = Image.open(arquivo)
            formato = entrada.format
            (largura, altura) = entrada.size
            fator = min(size / largura, size / altura)
            novo_tamanho = (int(largura * fator), int(altura * fator))
            entrada.thumbnail(novo_tamanho)
            entrada.save(saida, format=formato)
            conteudo = saida.getvalue()
            tipo = self.foto_mime
        return conteudo, tipo

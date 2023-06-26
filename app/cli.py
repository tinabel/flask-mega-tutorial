import os
import click

def register(app):
    @app.cli.group()
    def translate():
      # Translation and localization commands.
      pass

    @translate.command()
    @click.argument('lang')
    def init(lang):
      # Initializes a new language.
      if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
        raise RuntimeError('init command failed')
      os.remove('messages.pot')

      @translate.command()
      def update():
        # Updates all languages.
        if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
          raise RuntimeError('extract command failed')
        if os.system('pybabel update -i messages.pot -d app/translations'):
          raise RuntimeError('update command failed')
        os.remove('messages.pot')

      @translate.command()
      def compile():
        # Compiles all languages.
        if os.system('pybabel compile -d app/translations'):
          raise RuntimeError('compile command failed')
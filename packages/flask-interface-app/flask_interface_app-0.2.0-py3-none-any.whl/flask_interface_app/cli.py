import os
import shutil
import click

TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), 'templates')

def copy_files(src, dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    shutil.copytree(src, dest)

@click.command()
@click.argument('app_name')
def create_flask_app(app_name):
    app_dir = os.path.join(os.getcwd(), app_name)
    if not os.path.exists(app_dir):
        os.makedirs(app_dir)
    copy_files(os.path.join(TEMPLATES_DIR, 'app'), os.path.join(app_dir, 'app'))
    # Additional setup logic as needed

if __name__ == '__main__':
    create_flask_app()

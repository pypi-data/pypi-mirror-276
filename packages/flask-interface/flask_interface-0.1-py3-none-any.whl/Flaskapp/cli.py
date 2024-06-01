import os
import click
import shutil

TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), 'templates')

def copy_files(src, dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    shutil.copytree(src, dest)

@click.command()
@click.argument('app_name')
def create_flask_app(app_name):
    """Create a new Flask app with the given APP_NAME."""
    app_dir = os.path.join(os.getcwd(), app_name)
    
    if os.path.exists(app_dir):
        click.echo(f"Directory {app_name} already exists!")
        return

    os.makedirs(app_dir)
    copy_files(os.path.join(TEMPLATES_DIR, 'app'), os.path.join(app_dir, 'app'))
    shutil.copy(os.path.join(TEMPLATES_DIR, 'config.py'), app_dir)
    shutil.copy(os.path.join(TEMPLATES_DIR, 'app.py'), app_dir)
    click.echo(f"Flask app '{app_name}' created successfully!")

if __name__ == '__main__':
    create_flask_app()

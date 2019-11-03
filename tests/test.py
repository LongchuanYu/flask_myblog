import click
@click.command('init-db')
def hello():
	click.echo('hello')
if __name__=="__main__":
	hello()
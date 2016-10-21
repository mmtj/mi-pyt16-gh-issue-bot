#! /usr/bin/env python3

import click
from issuebot import IssueBot
from flaskapp import webapp

@click.group()
def cli():
    pass

@cli.command()
@click.option('--auth', default='auth.cfg', help='File with github credentials')
@click.option('--rules', default='rules', help='Rules definition file')
def web(auth, rules):
    """Run bot as web app"""
    #robot.init_basic(auth, rules)
    
    webapp.run(debug=True)

@cli.command()
@click.option('--repo', help='GitHub repository to check (format username/reponame)')
@click.option('--sleep', help='Number of second before another check')
@click.option('--auth', default='auth.cfg', help='File with github credentials')
@click.option('--config', default='settings.cfg', help='Main config file')
@click.option('--rules', default='rules', help='Rules definition file')
def console (repo, sleep, auth, config, rules):
    """Run bot locally from command line """
    robot = IssueBot()
    robot.init_basic(auth, rules)
    robot.start(repo, sleep, config)

if __name__ == '__main__':
    cli()

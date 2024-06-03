import datetime
import sys
import time
import traceback

import ckan.model as model

import click


from . import jobs


@click.command()
def list_circles():
    """List all circles/organizations"""
    groups = model.Group.all()
    for grp in groups:
        if grp.is_organization:
            click.echo(f"{grp.id}\t{grp.name}\t({grp.title})")


@click.command()
def list_collections():
    """List all collections/groups"""
    groups = model.Group.all()
    for grp in groups:
        if not grp.is_organization:
            click.echo(f"{grp.id}\t{grp.name}\t({grp.title})")


@click.command()
@click.argument("group_id_or_name")
def list_group_resources(group_id_or_name):
    """List all resources (active/draft/deleted) for a circle or collection"""
    # We cannot just use model.group.Group.packages(), because this does
    # not include resources from draft or deleted datasets.
    group = model.Group.get(group_id_or_name)
    if group is None:
        click.secho(f"Group '{group_id_or_name}' not found", fg="red")
        return sys.exit(1)
    else:
        # print the list of resources of that group
        query = model.meta.Session.query(model.package.Package).\
            filter(model.group.group_table.c["id"] == group.id)
        # copy-pasted from CKAN's model.group.Group.packages()
        query = query.join(
            model.group.member_table,
            model.group.member_table.c["table_id"] == model.package.Package.id)
        query = query.join(
            model.group.group_table,
            model.group.group_table.c["id"]
            == model.group.member_table.c["group_id"])

        for dataset in query.all():
            for resource in dataset.resources:
                click.echo(resource.id)


@click.option('--last-activity-weeks', default=12,
              help='Only list users with no activity for X weeks')
@click.command()
def list_zombie_users(last_activity_weeks=12):
    """List zombie users (no activity, no datasets)"""
    users = model.User.all()
    for user in users:
        # user is admin?
        if user.sysadmin:
            continue
        # user has datasets?
        if user.number_created_packages(include_private_and_draft=True) != 0:
            # don't list users with datasets
            continue
        # user has been active?
        if (user.last_active is not None
                and user.last_active.timestamp() >= (
                        time.time() - 60*60*24*7*last_activity_weeks)):
            # don't delete users that did things
            continue
        click.echo(user.name)


@click.option('--modified-days', default=-1,
              help='Only run for datasets modified within this number of days '
                   + 'in the past. Set to -1 to apply to all datasets.')
@click.command()
def run_jobs_dcor_schemas(modified_days=-1):
    """Set .rtdc metadata and SHA256 sums and for all resources

    This also happens for draft datasets.
    """
    datasets = model.Session.query(model.Package)

    if modified_days >= 0:
        # Search only the last `days` days.
        past = datetime.date.today() - datetime.timedelta(days=modified_days)
        past_str = time.strftime("%Y-%m-%d", past.timetuple())
        datasets = datasets.filter(model.Package.metadata_modified >= past_str)

    nl = False  # new line character
    for dataset in datasets:
        try:
            nl = False
            click.echo(f"Checking dataset {dataset.id}\r", nl=False)
            for resource in dataset.resources:
                res_dict = resource.as_dict()
                if jobs.set_format_job(res_dict):
                    if not nl:
                        click.echo("")
                        nl = True
                    click.echo(f"Updated format for {resource.name}")
                if jobs.set_sha256_job(res_dict):
                    if not nl:
                        click.echo("")
                        nl = True
                    click.echo(f"Updated SHA256 for {resource.name}")
                if jobs.set_dc_config_job(res_dict):
                    if not nl:
                        click.echo("")
                    click.echo(f"Updated config for {resource.name}")
        except BaseException as e:
            click.echo(
                f"\nEncountered {e.__class__.__name__} for {dataset.id}!",
                err=True)
            click.echo(traceback.format_exc(), err=True)
    if not nl:
        click.echo("")
    click.echo("Done!")


def get_commands():
    return [
        list_circles,
        list_collections,
        list_group_resources,
        list_zombie_users,
        run_jobs_dcor_schemas]

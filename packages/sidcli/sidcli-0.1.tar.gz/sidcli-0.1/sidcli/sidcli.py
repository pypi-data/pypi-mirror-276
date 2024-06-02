import os
import click
import boto3
import subprocess

@click.command()
@click.argument('aws_profile', default='dev', required=False)
@click.argument('db_user_name', required=False)
def sidcli(aws_profile, db_user_name):
    session = boto3.Session(profile_name=aws_profile)
    sts_client = session.client('sts')
    ecs_client = session.client('ecs')
    rds_client = session.client('rds')

    if not db_user_name:
        caller_identity = sts_client.get_caller_identity()
        db_user_name = caller_identity.get('UserId')

    if not db_user_name:
        click.echo("Do not skip the database username as it is an identity to log you into the database. Exiting...")
        exit(1)

    sslrootcertificate = os.path.expanduser('~/us-east-1-bundle.pem')
    if not os.path.isfile(sslrootcertificate):
        click.echo("File is not present hence downloading...")
        download_certificate()

        if not os.path.isfile(sslrootcertificate):
            click.echo("Couldn't download the file. Something's wrong with the link!! Exiting!")
            exit(1)
        else:
            click.echo("PEM file for RDS authentication downloaded successfully.")
    else:
        click.echo(f"RDS connection certificate is present in {os.path.expanduser('~')}.")

    click.echo(f"Selected Username = {db_user_name}")
    cluster_name = select_cluster(ecs_client, aws_profile)

    dash_service_name = get_dash_service_name(ecs_client, cluster_name, aws_profile)
    db_host, db_port, db_name = get_db_details(ecs_client, dash_service_name, aws_profile)

    check_vars(db_name=db_name, db_port=db_port, db_host=db_host, db_user_name=db_user_name)

    pg_password = rds_client.generate_db_auth_token(
        DBHostname=db_host,
        Port=db_port,
        Region='us-east-1',
        DBUsername=db_user_name
    )

    click.echo("******************************************************************************************")
    click.echo(f"1. RDS Database Username    : {db_user_name}")
    click.echo(f"2. RDS Database Hostname    : {db_host}")
    click.echo(f"3. RDS Database Port        : {db_port}")
    click.echo(f"4. RDS Database Name        : {db_name}")
    click.echo("******************************************************************************************")
    click.echo("##### DASH Database Password is on the next line. Make sure that you are not copying extra white spaces. #####")
    click.echo(f"{pg_password}")

def download_certificate():
    url = 'https://truststore.pki.rds.amazonaws.com/us-east-1/us-east-1-bundle.pem'
    destination = os.path.expanduser('~/us-east-1-bundle.pem')
    subprocess.run(['curl', '-o', destination, url])

def select_cluster(ecs_client, aws_profile):
    response = ecs_client.list_clusters()
    clusters = [arn.split('/')[-1] for arn in response['clusterArns']]
    clusters.sort()

    click.echo("Select a cluster:")
    for i, cluster in enumerate(clusters, 1):
        click.echo(f"{i}. {cluster}")

    cluster_index = click.prompt("Enter the cluster number", type=int)
    if 1 <= cluster_index <= len(clusters):
        selected_cluster = clusters[cluster_index - 1]
        click.echo(f"You have selected {selected_cluster}")
        return selected_cluster
    else:
        click.echo(f"{cluster_index} is not a valid cluster number. Exiting...")
        exit(1)

def get_dash_service_name(ecs_client, cluster_name, aws_profile):
    response = ecs_client.list_services(cluster=cluster_name)
    service_arns = response['serviceArns']
    dash_service_name = [arn for arn in service_arns if 'graphql' not in arn and 'sbff' not in arn and 'dashtp' not in arn]
    return dash_service_name[0] if dash_service_name else None

def get_db_details(ecs_client, dash_service_name, aws_profile):
    response = ecs_client.list_tags_for_resource(resourceArn=dash_service_name)
    tags = {tag['key']: tag['value'] for tag in response['tags']}
    db_host = tags.get('DB_HOST')
    db_port = tags.get('DB_PORT')
    db_name = tags.get('DB_NAME')
    return db_host, db_port, db_name

def check_vars(**kwargs):
    for var_name, value in kwargs.items():
        if not value:
            click.echo(f"{var_name} is unset.")
            exit(1)
    return True

if __name__ == '__main__':
    sidcli()

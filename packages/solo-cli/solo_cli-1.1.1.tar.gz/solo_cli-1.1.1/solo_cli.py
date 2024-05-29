import click
import os
import subprocess
import shutil

@click.group()
def cli():
    pass

@cli.command()
def install():
    """Install Ollama"""
    if not shutil.which("curl"):
        click.echo("Please install curl to continue.")
        return

    click.echo("Installing Ollama...")
    subprocess.run(["curl", "-fsSL", "https://ollama.com/install.sh", "|", "sh"], check=True)
    setup_service()

def setup_service():
    """Set up Ollama as a systemd service"""
    service_content = """
    [Unit]
    Description=Ollama Service
    After=network-online.target

    [Service]
    ExecStart=/usr/bin/ollama serve
    User=ollama
    Group=ollama
    Restart=always
    RestartSec=3

    [Install]
    WantedBy=default.target
    """
    
    with open("/etc/systemd/system/ollama.service", "w") as f:
        f.write(service_content)

    subprocess.run(["sudo", "systemctl", "daemon-reload"], check=True)
    subprocess.run(["sudo", "systemctl", "enable", "ollama"], check=True)
    subprocess.run(["sudo", "systemctl", "start", "ollama"], check=True)
    click.echo("Ollama service installed and started.")

@cli.command()
def update():
    """Update Ollama"""
    click.echo("Updating Ollama...")
    subprocess.run(["curl", "-fsSL", "https://ollama.com/install.sh", "|", "sh"], check=True)

@cli.command()
def logs():
    """View Ollama logs"""
    subprocess.run(["journalctl", "-e", "-u", "ollama"])

@cli.command()
def uninstall():
    """Uninstall Ollama"""
    click.echo("Uninstalling Ollama...")
    subprocess.run(["sudo", "systemctl", "stop", "ollama"], check=True)
    subprocess.run(["sudo", "systemctl", "disable", "ollama"], check=True)
    subprocess.run(["sudo", "rm", "/etc/systemd/system/ollama.service"], check=True)
    subprocess.run(["sudo", "rm", "/usr/bin/ollama"], check=True)
    subprocess.run(["sudo", "rm", "-r", "/usr/share/ollama"], check=True)
    subprocess.run(["sudo", "userdel", "ollama"], check=True)
    subprocess.run(["sudo", "groupdel", "ollama"], check=True)
    click.echo("Ollama uninstalled.")

@cli.command()
def serve():
    """Serve OpenUI with ngrok"""
    click.echo("Cloning the OpenUI repository...")
    subprocess.run(["git", "clone", "https://github.com/open-webui/open-webui.git"], check=True)
    
    os.chdir("open-webui")
    
    click.echo("Copying required .env file...")
    subprocess.run(["cp", "-RPp", ".env.example", ".env"], check=True)
    
    click.echo("Building frontend using Node...")
    subprocess.run(["npm", "i"], check=True)
    subprocess.run(["npm", "run", "build"], check=True)
    
    os.chdir("./backend")
    
    click.echo("Setting up backend...")
    subprocess.run(["pip", "install", "-r", "requirements.txt", "-U"], check=True)
    
    click.echo("Starting backend...")
    subprocess.run(["bash", "start.sh"], check=True)
    
    click.echo("Setting up ngrok...")
    if not shutil.which("ngrok"):
        click.echo("ngrok not found, installing ngrok...")
        subprocess.run(["curl", "-s", "https://ngrok-agent.s3.amazonaws.com/ngrok.asc", "|", "sudo", "tee", "/etc/apt/trusted.gpg.d/ngrok.asc"], check=True)
        subprocess.run(["echo", '"deb https://ngrok-agent.s3.amazonaws.com buster main"', "|", "sudo", "tee", "/etc/apt/sources.list.d/ngrok.list"], check=True)
        subprocess.run(["sudo", "apt", "update"], check=True)
        subprocess.run(["sudo", "apt", "install", "ngrok"], check=True)

    click.echo("Starting ngrok tunnel...")
    subprocess.run(["ngrok", "http", "5000"], check=True)

@cli.command()
def web():
    """Run OpenUI frontend and serve it with ngrok"""
    click.echo("Checking Docker installation...")
    if not shutil.which("docker"):
        click.echo("Please install Docker to continue.")
        return

    click.echo("Checking if Docker container 'open-webui' is running...")
    container_status = subprocess.run(["docker", "ps", "-q", "-f", "name=open-webui"], capture_output=True, text=True).stdout.strip()
    
    if container_status:
        click.echo("Docker container 'open-webui' is already running. Stopping and removing it...")
        subprocess.run(["docker", "stop", "open-webui"], check=True)
        subprocess.run(["docker", "rm", "open-webui"], check=True)

    click.echo("Running OpenUI Docker container...")
    subprocess.run([
        "docker", "run", "-d", "-p", "3000:8080", "--add-host=host.docker.internal:host-gateway",
        "-v", "open-webui:/app/backend/data", "--name", "open-webui", "--restart", "always",
        "ghcr.io/open-webui/open-webui:main"
    ], check=True)

    click.echo("Setting up ngrok...")
    if not shutil.which("ngrok"):
        click.echo("ngrok not found, installing ngrok...")
        subprocess.run(["curl", "-s", "https://ngrok-agent.s3.amazonaws.com/ngrok.asc", "|", "sudo", "tee", "/etc/apt/trusted.gpg.d/ngrok.asc"], check=True)
        subprocess.run(["echo", '"deb https://ngrok-agent.s3.amazonaws.com buster main"', "|", "sudo", "tee", "/etc/apt/sources.list.d/ngrok.list"], check=True)
        subprocess.run(["sudo", "apt", "update"], check=True)
        subprocess.run(["sudo", "apt", "install", "ngrok"], check=True)

    click.echo("Starting ngrok tunnel...")
    subprocess.run(["ngrok", "http", "3000"], check=True)

if __name__ == "__main__":
    cli()

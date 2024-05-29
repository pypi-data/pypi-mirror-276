import subprocess
import sys

def run_command(command):
    """Run a shell command and check for errors."""
    result = subprocess.run(command, shell=True, text=True, capture_output=True)
    if result.returncode != 0:
        print(f"Command failed: {command}")
        print(f"Error: {result.stderr}")
        sys.exit(1)
    else:
        print(f"Command succeeded: {command}")
        print(result.stdout)

def setup_selenium():
    """Set up Selenium and ChromeDriver on a Linux machine."""
    commands = [
        # Add debian buster
        "cat > /etc/apt/sources.list.d/debian.list <<'EOF'\n"
        "deb [arch=amd64 signed-by=/usr/share/keyrings/debian-buster.gpg] http://deb.debian.org/debian buster main\n"
        "deb [arch=amd64 signed-by=/usr/share/keyrings/debian-buster-updates.gpg] http://deb.debian.org/debian buster-updates main\n"
        "deb [arch=amd64 signed-by=/usr/share/keyrings/debian-security-buster.gpg] http://deb.debian.org/debian-security buster/updates main\n"
        "EOF",

        # Add keys
        "apt-key adv --keyserver keyserver.ubuntu.com --recv-keys DCC9EFBF77E11517",
        "apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 648ACFD622F3D138",
        "apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 112695A0E562B32A",
        "apt-key export 77E11517 | gpg --dearmour -o /usr/share/keyrings/debian-buster.gpg",
        "apt-key export 22F3D138 | gpg --dearmour -o /usr/share/keyrings/debian-buster-updates.gpg",
        "apt-key export E562B32A | gpg --dearmour -o /usr/share/keyrings/debian-security-buster.gpg",

        # Prefer debian repo for chromium* packages only
        "cat > /etc/apt/preferences.d/chromium.pref << 'EOF'\n"
        "Package: *\n"
        "Pin: release a=eoan\n"
        "Pin-Priority: 500\n\n"
        "Package: *\n"
        "Pin: origin \"deb.debian.org\"\n"
        "Pin-Priority: 300\n\n"
        "Package: chromium*\n"
        "Pin: origin \"deb.debian.org\"\n"
        "Pin-Priority: 700\n"
        "EOF",

        # Update and install chromium and selenium
        "apt-get update",
        "apt-get install -y chromium chromium-driver",
        "pip3 install selenium"
    ]

    for command in commands:
        run_command(command)
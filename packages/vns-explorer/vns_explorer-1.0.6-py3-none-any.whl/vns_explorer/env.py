import os
from IPython.display import display, Image, Markdown

def write_shell_script():
    """Write the shell script to set up Selenium and ChromeDriver in the /content/ directory."""
    script_content = """#!/bin/bash

# Add debian buster
cat > /etc/apt/sources.list.d/debian.list <<'EOF'
deb [arch=amd64 signed-by=/usr/share/keyrings/debian-buster.gpg] http://deb.debian.org/debian buster main
deb [arch=amd64 signed-by=/usr/share/keyrings/debian-buster-updates.gpg] http://deb.debian.org/debian buster-updates main
deb [arch=amd64 signed-by=/usr/share/keyrings/debian-security-buster.gpg] http://deb.debian.org/debian-security buster/updates main
EOF

# Add keys
apt-key adv --keyserver keyserver.ubuntu.com --recv-keys DCC9EFBF77E11517
apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 648ACFD622F3D138
apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 112695A0E562B32A

apt-key export 77E11517 | gpg --dearmour -o /usr/share/keyrings/debian-buster.gpg
apt-key export 22F3D138 | gpg --dearmour -o /usr/share/keyrings/debian-buster-updates.gpg
apt-key export E562B32A | gpg --dearmour -o /usr/share/keyrings/debian-security-buster.gpg

# Prefer debian repo for chromium* packages only
# Note the double-blank lines between entries
cat > /etc/apt/preferences.d/chromium.pref << 'EOF'
Package: *
Pin: release a=eoan
Pin-Priority: 500

Package: *
Pin: origin "deb.debian.org"
Pin-Priority: 300

Package: chromium*
Pin: origin "deb.debian.org"
Pin-Priority: 700
EOF

# Update and install chromium and selenium
apt-get update
apt-get install -y chromium chromium-driver
pip3 install selenium
"""

    script_path = '/content/setup_selenium.sh'
    with open(script_path, 'w') as file:
        file.write(script_content)
    
    # Make the script executable
    os.chmod(script_path, 0o755)
    message = f"### Please run the following command in a code cell to complete the setup:\n\n```bash\n" + f"!bash {script_path}\n```"
    display(Markdown(message))

def setup_selenium():
    """Detect environment and write shell script if in Colab."""
    if "COLAB_GPU" in os.environ:
        write_shell_script()

if __name__ == "__main__":
    setup_selenium()
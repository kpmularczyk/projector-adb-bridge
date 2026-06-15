1. connect to wifi and upgrade:

	sudo nmcli device wifi rescan
	nmcli device wifi list
	sudo nmcli device wifi connect "YourWiFiSSID" password "YourWiFiPassword"
	
	sudo apt get update
	sudo apt get upgrade

2. install prerequisites:
	
    sudo apt install git
    sudo apt install android-sdk-platform-tools
    sudo apt install tesseract-ocr

3. create application directory, own it and cd into it:

    sudo mkdir -p /opt/adb-panel-agent
    sudo chown -R amanita:amanita /opt/adb-panel-agent
    cd /opt/adb-panel-agent

4. setup storing credentials in git:

    git config --global credential.helper store

5. clone application (providing username and pat):

    git clone https://github.com/kpmularczyk/adb-panel-agent.git .

6. configure venv:

    python -m venv venv
    source venv/bin/activate

7. install requirements:

    pip install -r requirements.txt

8. setup .env (rename .env.example and fill it)

9. install application as a linux service:

    cd services
    chmod +x install_service.sh
    ./install_service.sh

10. setup nopassword for reboot and NetworkManager:

    sudo visudo

    # add at the end of the file:
    amanita ALL=(ALL) NOPASSWD: /usr/sbin/reboot
    amanita ALL=(ALL) NOPASSWD: /usr/bin/systemctl restart NetworkManager
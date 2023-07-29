import platform
import subprocess
import shutil

def install_grafana():
    command1 = "sudo apt-get install -y adduser libfontconfig1"
    subprocess.run(command1, shell=True, check=True)
    command2 = "wget https://dl.grafana.com/oss/release/grafana_9.5.3_amd64.deb"
    subprocess.run(command2, shell=True, check=True)
    command3 = "sudo dpkg -i grafana_9.5.3_amd64.deb"
    subprocess.run(command3, shell=True, check=True)
    command4 = "sudo systemctl start grafana-server.service"
    subprocess.run(command4, shell=True, check=True)
    return

def install_influxdb():
    command1 = "wget -q https://repos.influxdata.com/influxdata-archive_compat.key"
    subprocess.run(command1, shell=True, check=True)
    command2 = "echo '393e8779c89ac8d958f81f942f9ad7fb82a25e133faddaf92e15b16e6ac9ce4c influxdata-archive_compat.key' | sha256sum -c && cat influxdata-archive_compat.key | gpg --dearmor | sudo tee /etc/apt/trusted.gpg.d/influxdata-archive_compat.gpg > /dev/null"
    subprocess.run(command2, shell=True, check=True)
    command3 = "echo 'deb [signed-by=/etc/apt/trusted.gpg.d/influxdata-archive_compat.gpg] https://repos.influxdata.com/debian stable main' | sudo tee /etc/apt/sources.list.d/influxdata.list"
    subprocess.run(command3, shell=True, check=True)
    command4 = "sudo apt-get update && sudo apt-get install -f influxdb"
    subprocess.run(command4, shell=True, check=True)
    command5 = "sudo systemctl unmask influxdb.service"
    subprocess.run(command5, shell=True, check=True)
    command6 = "sudo systemctl start influxdb"
    subprocess.run(command6, shell=True, check=True)
    return


def configure_influxdb():
    command1 = "influx -execute \"CREATE DATABASE telegraf_measurements\""
    subprocess.run(command1, shell=True, check=True)
    command2 = "influx -execute \"CREATE USER admin WITH PASSWORD 'admin' WITH ALL PRIVILEGES\""
    subprocess.run(command2, shell=True, check=True)
    return

def install_telegraf():
    command1 = "wget -q https://repos.influxdata.com/influxdata-archive_compat.key"
    subprocess.run(command1, shell=True, check=True)
    command2 = """echo '393e8779c89ac8d958f81f942f9ad7fb82a25e133faddaf92e15b16e6ac9ce4c influxdata-archive_compat.key' | sha256sum -c && cat influxdata-archive_compat.key | gpg --dearmor | sudo tee /etc/apt/trusted.gpg.d/influxdata-archive_compat.gpg > /dev/null"""
    subprocess.run(command2, shell=True, check=True, executable="/bin/bash")
    command3 = """echo 'deb [signed-by=/etc/apt/trusted.gpg.d/influxdata-archive_compat.gpg] https://repos.influxdata.com/debian stable main' | sudo tee /etc/apt/sources.list.d/influxdata.list"""
    subprocess.run(command3, shell=True, check=True, executable="/bin/bash")
    command4 = "sudo apt-get update && sudo apt-get install -f telegraf"
    subprocess.run(command4, shell=True, check=True)
    return


def configure_telegraf():
    command = f"sudo rm /etc/telegraf/telegraf.conf"
    subprocess.run(command, shell=True, check=True)
    source_file = "./installation_files/telegraf.conf"  # Path to the source file in your Python directory
    destination_file = "/etc/telegraf/telegraf.conf"  # Path to the destination file
    shutil.copyfile(source_file, destination_file)
    command = "sudo systemctl start telegraf"
    subprocess.run(command, shell=True, check=True)


if platform.system() == "Linux":
    print("Operating system is Linux.\nAttempting to install Grafana")
    install_grafana()
    print("Attemtping to install influxdb..")
    install_influxdb()
    configure_influxdb()
    print("Attempting to install telegraf")
    install_telegraf()
    configure_telegraf()
else:
    print("Operating system is not Linux, this script was built for Linux purposes.")

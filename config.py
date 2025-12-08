import os
import subprocess
import yaml

''' This file loads configuration from config.yaml '''

def load_config():
    """Load configuration from config.yaml based on the current OS and environment"""
    
    # Determine release, and whether we are on Windows Subsystem for Linux (WSL)
    release = subprocess.check_output("""sh -c '. /etc/os-release; echo "$NAME"'""", shell=True,
        universal_newlines=True).strip()
    are_we_on_wsl = os.path.exists("/mnt/c/Windows/System32/wsl.exe")
    
    # Load the YAML configuration file
    config_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config.yaml')
    with open(config_path, 'r') as config_file:
        all_configs = yaml.safe_load(config_file)
    
    # Determine which configuration to use
    if 'Kali' in release:
        config = all_configs['Kali']
    elif 'Ubuntu' in release and are_we_on_wsl:
        config = all_configs['Ubuntu-WSL']
    elif 'Ubuntu' in release:
        config = all_configs['Ubuntu']
    else:
        raise Exception(f"Unsupported OS: {release}")
    
    # Set personal_repo_directory to $HOME if it's null
    if config['personal_repo_directory'] is None:
        config['personal_repo_directory'] = os.getenv("HOME")
    
    return config

# Load the configuration
_config = load_config()

# Export configuration variables for backward compatibility
directories_to_remove = _config['directories_to_remove']
packages_to_install = _config['packages_to_install']
packages_to_remove = _config['packages_to_remove']
pip_packages = _config['pip_packages']
gem_packages = _config['gem_packages']
golang_install_directory = _config.get('golang_install_directory', '/opt')
golang_modules_to_install = _config['golang_modules_to_install']
external_tools_directory = _config['external_tools_directory']
ext_repositories_to_sync = _config['ext_repositories_to_sync']
personal_repo_directory = _config['personal_repo_directory']
personal_repositories_to_sync = _config['personal_repositories_to_sync']

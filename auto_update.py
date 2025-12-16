#!/usr/bin/env python3
"""
Auto Update Script for Linux Systems
Automatically updates the system using the appropriate package manager.
Supports apt (Debian/Ubuntu), dnf (Fedora/RHEL), and pacman (Arch).
"""

import subprocess
import sys
import os
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.expanduser('~/auto_update.log')),
        logging.StreamHandler()
    ]
)

class SystemUpdater:
    """Handles system updates for different Linux distributions."""
    
    def __init__(self):
        self.package_manager = self._detect_package_manager()
        
    def _detect_package_manager(self):
        """Detect which package manager is available on the system."""
        managers = {
            'apt': '/usr/bin/apt',
            'dnf': '/usr/bin/dnf',
            'pacman': '/usr/bin/pacman'
        }
        
        for name, path in managers.items():
            if os.path.exists(path):
                logging.info(f"Detected package manager: {name}")
                return name
        
        logging.error("No supported package manager found!")
        return None
    
    def _run_command(self, command):
        """Execute a shell command and return the result."""
        try:
            logging.info(f"Executing: {' '.join(command)}")
            result = subprocess.run(
                command,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=3600  # 1 hour timeout
            )
            logging.info("Command executed successfully")
            return True, result.stdout
        except subprocess.TimeoutExpired:
            logging.error(f"Command timed out after 3600 seconds")
            return False, "Command timed out"
        except subprocess.CalledProcessError as e:
            logging.error(f"Command failed: {e.stderr}")
            return False, e.stderr
        except Exception as e:
            logging.error(f"Unexpected error: {str(e)}")
            return False, str(e)
    
    def _check_root(self):
        """Check if the script is running with root privileges."""
        if os.geteuid() != 0:
            logging.error("This script requires root privileges!")
            print("Error: Please run with sudo or as root")
            return False
        return True
    
    def update_apt(self):
        """Update system using apt package manager."""
        logging.info("Starting apt update process...")
        
        # Update package lists
        success, output = self._run_command(['apt', 'update'])
        if not success:
            return False
        
        # Upgrade packages
        success, output = self._run_command(['apt', 'upgrade', '-y'])
        if not success:
            return False
        
        # Auto-remove unnecessary packages
        success, output = self._run_command(['apt', 'autoremove', '-y'])
        if not success:
            logging.warning("Autoremove failed, but continuing...")
        
        # Clean up
        success, output = self._run_command(['apt', 'autoclean'])
        if not success:
            logging.warning("Autoclean failed, but continuing...")
        
        logging.info("APT update completed successfully")
        return True
    
    def update_dnf(self):
        """Update system using dnf package manager."""
        logging.info("Starting dnf update process...")
        
        # Update all packages
        success, output = self._run_command(['dnf', 'upgrade', '-y'])
        if not success:
            return False
        
        # Auto-remove unnecessary packages
        success, output = self._run_command(['dnf', 'autoremove', '-y'])
        if not success:
            logging.warning("Autoremove failed, but continuing...")
        
        logging.info("DNF update completed successfully")
        return True
    
    def update_pacman(self):
        """Update system using pacman package manager."""
        logging.info("Starting pacman update process...")
        
        # Sync and update all packages
        success, output = self._run_command(['pacman', '-Syu', '--noconfirm'])
        if not success:
            return False
        
        logging.info("Pacman update completed successfully")
        return True
    
    def update_system(self):
        """Update the system using the detected package manager."""
        if not self.package_manager:
            print("Error: No supported package manager found!")
            print("Supported: apt (Debian/Ubuntu), dnf (Fedora/RHEL), pacman (Arch)")
            return False
        
        if not self._check_root():
            return False
        
        print(f"\n{'='*60}")
        print(f"Linux System Auto-Updater")
        print(f"Package Manager: {self.package_manager}")
        print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}\n")
        
        # Execute update based on package manager
        update_methods = {
            'apt': self.update_apt,
            'dnf': self.update_dnf,
            'pacman': self.update_pacman
        }
        
        success = update_methods[self.package_manager]()
        
        if success:
            print(f"\n{'='*60}")
            print("✓ System update completed successfully!")
            print(f"Finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"{'='*60}\n")
            return True
        else:
            print(f"\n{'='*60}")
            print("✗ System update failed. Check the log for details.")
            print(f"Log file: ~/auto_update.log")
            print(f"{'='*60}\n")
            return False

def main():
    """Main entry point for the script."""
    try:
        updater = SystemUpdater()
        success = updater.update_system()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nUpdate cancelled by user.")
        logging.info("Update cancelled by user (Ctrl+C)")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error: {str(e)}")
        logging.error(f"Unexpected error in main: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()

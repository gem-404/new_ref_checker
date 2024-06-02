### Python Initial Setup:

Install Python from the official website or use an existing Python installation if you have one.
Add the Python installation directory to the system path.

Open a command prompt and type "python" to check if Python is installed and working properly.

```bash
python --version
```
### Virtual Environments:

Install virtualenv package by running pip install virtualenv in the command prompt.

Create a new virtual environment by running virtualenv venv in the command prompt. Replace "venv" with the name of your virtual environment.
Activate the virtual environment on Windows by running:
```cmd
venv\Scripts\activate

```
Activate the virtual environment on macOSX/Linux by running:
```bash
venv/bin/activate
``` 
Install necessary Python packages within the virtual environment in command prompt/terminal:
```bash
pip install <package>
```
or
```bash
pip install -r requirements.txt
```

Deactivate the virtual environment by running deactivate in the command prompt.

# Database Initial Setup
## Installing mongodb on Arch Linux
1. Update the package manager.

```bash
sudo pacman -Syu
```

2. Install the MongoDB package.


```bash
sudo pacman -S mongodb
```

3. Start the MongoDB service.

```bash
sudo systemctl start mongodb
```

4. Enable the MongoDB service to start automatically at boot.

```bash
sudo systemctl enable mongodb
```

5. Verify that MongoDB service is running.

```bash
sudo systemctl status mongodb
```

6. Optionally, install the MongoDB command-line tools.

```bash
sudo pacman -s mongodb-tools
```

## Installing MongoDB on Debian Distros in Linux
1. Add the MongoDB repository to your system's package manager.

  - Find instructions at [mongodb link](https://docs.mongodb.com/manual/administration/install-on-linux/)

2. Update the package manager.

 ```bash
 sudo apt update
 ```

3. Install the MongoDB package.

 ```
 sudo apt install mongodb
 ```

4. Start the MongoDB service.

```bash
sudo systemctl start mongodb
```

5. Enable the MongoDB service to start automatically at boot.

```bash
sudo systemctl enable mongodb
```

6. Verify that MongoDB service is running.

```bash
sudo systemctl status mongodb
```

7. Optionally, install the MongoDB command-line tools.

```bash
sudo apt install mongodb-clients
```

## Installing MongoDB on Windows.
1. Download the MongoDB Community Server from the official MongoDB website [link](https://www.mongodb.com/try/download/community).

2. Run the installer and follow the prompts to install MongoDB. You can choose
   the complete or custom installation options as per your requirements.

3. During the installation process, you will be asked to choose the installation
directory and data directory. You can accept the default values or choose a
custom location.

4. After the installation is complete, create a directory for MongoDB data
storage. By default, MongoDB stores data in the C:\data\db directory. You can
create this directory using the following command in the Command Prompt:

```cmd
mkdir C:\data\db
```

5. Add the MongoDB bin directory to your system's PATH environment variable.
   This will allow you to run the MongoDB command-line tools from any directory
   in the Command Prompt. To add the bin directory to your PATH, follow these
   steps:

6. Open the Start menu and search for "Environment Variables".

7. Click on "Edit the system environment variables".

8. Click on the "Environment Variables" button.

9. Under "System variables", find the "Path" variable and click on "Edit".

10. Click on "New" and add the path to the MongoDB bin directory. The default
    path is C:\Program Files\MongoDB\Server\<version>\bin, where <version> is
    the version of MongoDB you have installed.

11. Click on "OK" to close all windows.

12. Start the MongoDB service using the following command in the Command Prompt:

```cmd
mongod
```

13. Verify that the MongoDB service is running by opening another Command
    Prompt window and running the mongo command. This will connect to the local
    MongoDB instance and open a MongoDB shell. You can exit the shell by typing
    exit.


# ReferenceChecker

ReferenceChecker web application is a Reference checker for Documents.  The
ReferenceChecker checks the intext citation of the freelancer and checks the
similarity of two given strings that is both the authors and the statement used
by the freelancer.  



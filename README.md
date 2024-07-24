# ICT Proficiency System

## Description
A web system built with Flask and Bootstrap for managing applicant records. This application have admin that could create, read, update, and delete applicant records.

## Table of Contents
1. [Installation](#installation)
2. [Usage](#usage)
3. [Contributing](#contributing)
4. [License](#license)
5. [Contact](#contact)

## Installation

### Prerequisites
- Python 3.12
- Flask
- Bootstrap

### Setup
1. Clone the repository:
    ```bash
    git clone https://github.com/Mowpey/ICT_Proficiency.git
    cd ICT_Proficiency
    ```

2. Create a virtual environment:

    For Linux or macOS
    ```bash
    python3 -m venv myvenv 
    ```
    For Windows
   ```bash
    python -m venv myvenv
    source myvenv/bin/activate # On Windows use `myvenv\Scripts\activate`
    ```

4. Install the required packages:
    ```bash
    pip install flask
    pip install flask-login
    pip install flask-sqlalchemy
    ```

5. Run the application:
    ```bash
    flask run
    ```
    If the above command doesn't work try the command below
   
    ```bash
    flask --app main.py --debug run
    ```

## Usage
1. Open your browser and navigate to `http://localhost:5000`.
2. Use the interface to manage applicant records.

## Contributing
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact
If you have any questions or feedback, please contact us at [manuelmarkangelo22@gmail.com](mailto:manuelmarkangelo22@gmail.com).

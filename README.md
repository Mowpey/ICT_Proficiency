# ICT Proficiency System

## Description

A web system built with Flask and Bootstrap for managing applicant records. This application has an admin interface that allows creating, reading, updating, and deleting applicant records.

## Table of Contents

1. [Installation](#installation)
2. [Usage](#usage)
3. [Contributing](#contributing)
4. [License](#license)
5. [Contact](#contact)

## Installation

### Prerequisites

- Python 3.12

### Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/Mowpey/ICT_Proficiency.git
   cd ICT_Proficiency
   ```

2. Create a virtual environment:

   For Linux or macOS:

   ```bash
   python3 -m venv myvenv
   source myvenv/bin/activate
   ```

   For Windows:

   ```bash
   python -m venv myvenv
   myvenv\Scripts\activate
   ```

3. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   flask --app main.py --debug run
   ```

## Usage

1. Open your browser and navigate to `http://localhost:5000`.
2. Use the interface to manage applicant records.

## Create an Admin Account
1. To Create an admin account, access directly the sign up page using "/sign_up" in the browser

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

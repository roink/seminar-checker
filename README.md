# Seminar Date Checker

This Python script checks for new seminar dates on specific websites and sends email notifications if new dates are found or if a link becomes invalid.

## Features
- Monitors seminar websites for new dates.
- Sends email notifications for new dates or if the webpage becomes unavailable.
- Supports multiple seminar URLs.

## Requirements

- Python 3.x
- `requests` library
- `beautifulsoup4` library
- `python-dotenv` library

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/roink/seminar-checker.git
cd seminar-checker
```

### 2. Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables

Create a `.env` file in the project root directory by copying the provided `.env.example` file:

```bash
cp .env.example .env
```

Edit the `.env` file and add your email credentials and recipient email:

```bash
EMAIL_ADDRESS=your_email@gmx.net
EMAIL_PASSWORD=your_password
TO_EMAIL=recipient@example.com
SMTP_SERVER = "smtp-relay.gmail.com"
SMTP_PORT = "465"
```

### 4. Set Up Crontab (Linux/Ubuntu)

To run the script once a day, you can use `cron`. Follow these steps:

1. Open the crontab file:

    ```bash
    crontab -e
    ```

2. Add the following line to run the script daily at 2:00 AM (adjust the time as needed):

    ```bash
    0 2 * * * /usr/bin/python3 /path/to/your_project/your_script.py >> /path/to/your_project/seminar_log.log 2>&1
    ```

   Replace `/path/to/your_project/` with the actual path to your project.

3. Save and exit the crontab editor.

### 5. Check Logs

Logs will be written to `seminar_log.log` in your project directory. Check this file to see if the script is running as expected.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

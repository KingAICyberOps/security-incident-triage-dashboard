# Security Incident Triage Dashboard

A web-based cybersecurity incident triage and awareness tool built for my CIT Capstone project.

The application allows a user to enter information about a suspicious email, message, link, or other security concern. It uses a transparent rule-based scoring system to assign a Low, Medium, or High risk level, explains the warning signs that affected the result, and gives the user basic recommended next steps.

The project is meant for initial triage and awareness. It does not replace antivirus software or professional cybersecurity analysis.



## Live Demo

Try the deployed application here:

https://KingAICyberOps.pythonanywhere.com


## Features

- Incident submission form
- Rule-based cybersecurity risk assessment
- Low, Medium, and High risk levels
- Explanation of identified warning signs
- Recommended next steps
- SQLite database storage
- Incident history
- Security dashboard with risk statistics
- Form validation
- Navigation between assessment, history, and dashboard pages

## Risk Scoring

The current scoring system uses the following warning signs:

- Urgent or threatening language: 1 point
- Request for password or account information: 3 points
- Request for money or financial information: 2 points
- Suspicious link or unexpected attachment: 3 points
- Sender or source mismatch: 2 points

Risk levels:

- Low: 0 to 2 points
- Medium: 3 to 5 points
- High: 6 or more points

## Technologies

- Python
- Flask
- SQLite
- HTML
- CSS
- Git
- GitHub
- PythonAnywhere

## Running the Project

Clone the repository and open the project folder.

Create a Python virtual environment:

```powershell
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\activate
```

Install the required packages:

```powershell
python -m pip install -r requirements.txt
```

Start the application:

```powershell
python app.py
```

Open the local application in a browser:

```text
http://127.0.0.1:5000
```

The SQLite database is created automatically when the application starts.

## Testing

The MVP was tested for:

- Required-field validation
- Low-risk assessment
- Medium-risk assessment
- High-risk assessment
- Database persistence after restarting the application
- Incident history retrieval
- Dashboard statistics
- Navigation between application pages

All core MVP tests passed.

## Privacy and Security

Local SQLite database files and the Python virtual environment are excluded from GitHub through `.gitignore`.

The application treats submitted content as data and does not automatically visit links, execute attachments, or determine with certainty that something is malicious.

## Project Status

Core MVP completed and tested as part of an individual CIT Capstone project.
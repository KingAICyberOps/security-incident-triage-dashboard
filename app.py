import sqlite3
from flask import Flask, render_template, request

app = Flask(__name__)

DATABASE = "incidents.db"


WARNING_SCORES = {
    "Urgent or threatening language": 1,
    "Requests password or account information": 3,
    "Requests money or financial information": 2,
    "Suspicious link or unexpected attachment": 3,
    "Sender or source does not match": 2
}


def get_db_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def init_database():
    connection = get_db_connection()

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            incident_type TEXT NOT NULL,
            source TEXT,
            description TEXT NOT NULL,
            warning_signs TEXT,
            risk_score INTEGER NOT NULL,
            risk_level TEXT NOT NULL,
            recommendation TEXT,
            status TEXT NOT NULL DEFAULT 'New',
            submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    connection.commit()
    connection.close()


def assess_risk(warning_signs):
    score = sum(WARNING_SCORES.get(sign, 0) for sign in warning_signs)

    if score >= 6:
        level = "High"
        recommendation = (
            "Do not click links, open attachments, send money, or provide account information. "
            "Verify the request through a trusted contact method and report the incident to IT or security."
        )

    elif score >= 3:
        level = "Medium"
        recommendation = (
            "Use caution and verify the sender or request before taking action. "
            "Avoid using links or contact information contained in the suspicious message."
        )

    else:
        level = "Low"
        recommendation = (
            "Few warning signs were identified, but continue to use caution. "
            "Verify anything unusual before providing information or taking action."
        )

    return score, level, recommendation


@app.route("/", methods=["GET", "POST"])
def home():
    result = None

    form_data = {
        "incident_type": "",
        "source": "",
        "description": ""
    }

    selected_signs = []

    if request.method == "POST":
        form_data["incident_type"] = request.form.get("incident_type", "")
        form_data["source"] = request.form.get("source", "")
        form_data["description"] = request.form.get("description", "")
        selected_signs = request.form.getlist("warning_signs")

        score, level, recommendation = assess_risk(selected_signs)

        connection = get_db_connection()

        connection.execute(
            """
            INSERT INTO incidents (
                incident_type,
                source,
                description,
                warning_signs,
                risk_score,
                risk_level,
                recommendation
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                form_data["incident_type"],
                form_data["source"],
                form_data["description"],
                " | ".join(selected_signs),
                score,
                level,
                recommendation
            )
        )

        connection.commit()
        connection.close()

        result = {
            "score": score,
            "level": level,
            "warning_signs": selected_signs,
            "recommendation": recommendation
        }

    return render_template(
        "index.html",
        result=result,
        form_data=form_data,
        selected_signs=selected_signs
    )


@app.route("/history")
def history():
    connection = get_db_connection()

    incidents = connection.execute(
        """
        SELECT
            id,
            incident_type,
            source,
            description,
            warning_signs,
            risk_score,
            risk_level,
            status,
            submitted_at
        FROM incidents
        ORDER BY id DESC
        """
    ).fetchall()

    connection.close()

    return render_template("history.html", incidents=incidents)


@app.route("/dashboard")
def dashboard():
    connection = get_db_connection()

    statistics = connection.execute(
        """
        SELECT
            COUNT(*) AS total,
            COALESCE(SUM(CASE WHEN risk_level = 'Low' THEN 1 ELSE 0 END), 0) AS low_count,
            COALESCE(SUM(CASE WHEN risk_level = 'Medium' THEN 1 ELSE 0 END), 0) AS medium_count,
            COALESCE(SUM(CASE WHEN risk_level = 'High' THEN 1 ELSE 0 END), 0) AS high_count
        FROM incidents
        """
    ).fetchone()

    recent_incidents = connection.execute(
        """
        SELECT
            id,
            incident_type,
            source,
            risk_score,
            risk_level,
            submitted_at
        FROM incidents
        ORDER BY id DESC
        LIMIT 5
        """
    ).fetchall()

    connection.close()

    return render_template(
        "dashboard.html",
        statistics=statistics,
        recent_incidents=recent_incidents
    )


init_database()


if __name__ == "__main__":
    app.run(debug=False)
from flask import Flask, render_template, request, jsonify
from werkzeug.exceptions import abort

from autobrew.measurement.measurementService import MeasurementService

app = Flask(__name__)
app.debug = True


@app.route("/")
def brew_monitor():
    return render_template(
        "main_template.html", room_temp=str(19.0), brew_temp=str(22.0)
    )


@app.route("/todo/api/v1.0/tasks", methods=["PUT"])
def set_nickname():
    if not request.json or not "name" in request.json:
        abort(400)

    measurement = MeasurementService().set_measurement_nickname(
        request.json["name"], request.json.get("nickname")
    )
    return jsonify(measurement), 201


if __name__ == "__main__":
    app.run()

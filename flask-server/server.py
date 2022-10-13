

from flask import Flask, request, send_file

from flask_cors import CORS
from app.control import Control


control = Control()
app = Flask(__name__)
CORS(app)
# Members API Route


@app.route("/")
def home():
    return "Home"


@app.route("/import_raw_data", methods=['POST'])
def import_raw_data():
    file = request.get_json()
    control.loadRawfile(file)

    print("done")

    return "Done", 201


@app.route("/get_graph", methods=['GET'])
def get_graph():
    return control.getEdgesAsJson()

@app.route("/get_true_graph", methods=['GET'])
def get_true_graph():
    return control.getEdgesAsJsonTrue()


@app.route("/get_history_graph", methods=['GET'])
def get_history_graph():
    return control.getEdgesAsJsonHistory()


@app.route("/filter", methods=['POST'])
def filter():
    filter = request.get_json()
    control.applyFilter(filter)

    print("done")

    return "Done", 201


@app.route("/get_event_log", methods=['GET'])
def get_event_log():
    return control.getEventLog()


@app.route("/change_selected_node", methods=['POST'])
def change_selected_node():
    id = request.get_json()
    control.changeLastNode(id)

    print("done")

    return "Done", 201


@app.route("/snapshot", methods=['POST'])
def create_snapshot():
    id = request.get_json()
    control.create_snapshot(id)

    print("done")

    return "Done", 201


@app.route("/downloadsnapshot")
def downloadfile():
    path = "snapshot.py"
    return send_file(path, as_attachment=True)


@app.route("/downloadrawlog")
def downloadrawlog():
    path = "rawLog.py"
    return send_file(path, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)

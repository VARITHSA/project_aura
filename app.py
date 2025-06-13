from flask import Flask, jsonify, render_template, request

from aura_engine import AuraEngine

app = Flask(__name__, template_folder='views/templates')
aura = AuraEngine()

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/run', methods=['POST'])
def run_aura():
    data = request.get_json()
    user_command = data.get("command", "")
    try:
        response = aura.process_command(user_command)
        return jsonify({"status": "success", "response": response})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)

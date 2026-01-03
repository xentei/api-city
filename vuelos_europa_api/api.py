from flask import Flask, jsonify
from .playwright_flights import get_flights_via_playwright

app = Flask(__name__)


@app.route("/vuelos-europa", methods=["GET"])
def vuelos_europa():
    try:
        vuelos = get_flights_via_playwright()
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

    vuelos_ordenados = sorted(vuelos, key=lambda v: v["precio_usd"] or 999999)

    return jsonify(
        {
            "ok": True,
            "total": len(vuelos_ordenados),
            "vuelos": vuelos_ordenados,
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)

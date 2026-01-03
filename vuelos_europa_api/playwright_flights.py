from playwright.sync_api import sync_playwright

URL = (
    "https://www.turismocity.com.ar/"
    "vuelos-baratos-region-Europa?currency=USD&flexDates=true&from=BUE"
)


def get_flights_via_playwright():
    """
    Abre la landing de Europa con Chromium, deja que se ejecute el JS
    y captura la respuesta JSON de la API GraphQL interna.
    Devuelve una lista de vuelos ya normalizados.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
            locale="es-AR",
        )
        page = context.new_page()

        flights_json: dict = {}

        def handle_response(response):
            url = response.url
            if "graphql-cdn" in url and "destinationsFeedAllTypes" in url:
                try:
                    data = response.json()
                    flights_json.clear()
                    flights_json.update(data)
                except Exception:
                    pass

        page.on("response", handle_response)

        page.goto(URL, wait_until="networkidle")
        page.wait_for_timeout(8000)

        browser.close()

        flights = flights_json.get("data", {}).get("flights", []) or []

        resultado = []
        for f in flights:
            resultado.append(
                {
                    "id": f.get("id"),
                    "origen": f.get("departure_city"),
                    "destino": f.get("arrival_city"),
                    "origen_iata": f.get("departure"),
                    "destino_iata": f.get("arrival"),
                    "precio_usd": f.get("price"),
                    "estimado": f.get("isEstimatedPrice"),
                    "es_internacional": f.get("isInternationalFlight"),
                }
            )

        return resultado


if __name__ == "__main__":
    vuelos = get_flights_via_playwright()
    vuelos = sorted(vuelos, key=lambda v: v["precio_usd"] or 999999)[:10]
    for v in vuelos:
        print(
            f"{v['destino']:15} ({v['destino_iata'] if 'destino_iata' in v else ''}) "
            f"- USD {v['precio_usd']} desde {v['origen']} ({v['origen_iata']})"
        )

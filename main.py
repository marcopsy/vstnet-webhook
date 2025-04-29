from flask import Flask, request, jsonify
import csv
import os

app = Flask(__name__)

VERIFY_TOKEN = "EAAHpmSnouBYBO0zARTgFP88OkZAAI2fEPIWfcteAZAZA8VVviQ47OpUEzsRDmqcMvObRaEKfjcGzbH8XFZCfGFUnE91xbJpRDRlFVuYoBvGZChwBVSZCrxOgqgAAqgvNfpJ19mqDDWdAIrOSJ3npkbooiT1xBmuTdGUWRUKK5nwBwzhXVJZCFfK8vNRQYAuZBHC2K00nXUhoSCFo5OLSKbSUVRu9Ny0TV0gZD"  # Você pode mudar esse token como quiser

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        # Verificação do webhook com o token da Meta
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        if token == VERIFY_TOKEN:
            return challenge
        return "Token inválido", 403

    if request.method == "POST":
        data = request.json

        # Extração de dados recebidos
        try:
            for entry in data.get("entry", []):
                for change in entry.get("changes", []):
                    value = change.get("value", {})
                    messages = value.get("messages", [])
                    for message in messages:
                        phone_number = message["from"]
                        msg_body = message["text"]["body"]

                        print(f"Mensagem recebida de {phone_number}: {msg_body}")

                        # Salva no CSV
                        file_exists = os.path.isfile("respostas.csv")
                        with open("respostas.csv", mode="a", newline='', encoding="utf-8") as file:
                            writer = csv.writer(file)
                            if not file_exists:
                                writer.writerow(["Telefone", "Mensagem"])
                            writer.writerow([phone_number, msg_body])
        except Exception as e:
            print("Erro ao processar a mensagem:", e)

        return "OK", 200

if __name__ == "__main__":
    app.run(port=5000, debug=True)

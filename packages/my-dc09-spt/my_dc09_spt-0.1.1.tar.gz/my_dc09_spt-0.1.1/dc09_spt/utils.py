from datetime import datetime


def convert_timestamp_to_dc09_datetime(timestamp):
    # Convertir le timestamp en secondes
    timestamp_in_seconds = timestamp / 1000

    # Créer un objet datetime à partir du timestamp
    dt_object = datetime.fromtimestamp(timestamp_in_seconds)

    # Formater l'objet datetime en chaîne de caractères
    formatted_timestamp = dt_object.strftime("%H:%M:%S,%d-%m-%Y")

    return formatted_timestamp

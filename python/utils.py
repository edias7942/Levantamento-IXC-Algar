import sys


def filter_object_attributes(obj, required_attributes=[]):

    filtred_object = {item: obj[item] for item in obj if item in required_attributes}

    return filtred_object


def refresh_progress_bar(total: int, progressado: int, tamanho: int = 50):

    progresso = progressado / total
    barra = "█" * int(progresso * tamanho)
    espaços = " " * (tamanho - len(barra))
    percent = int(progresso * 100)

    sys.stdout.write(f"\r| {barra}{espaços} | {percent}% {progressado}/{total}    ")
    sys.stdout.flush()

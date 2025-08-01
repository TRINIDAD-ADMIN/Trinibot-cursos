from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def generar_botones_categorias(categorias):
    botones = []

    for i in range(0, len(categorias), 2):
        fila = []

        cat1 = categorias[i]
        fila.append(InlineKeyboardButton(cat1["nombre"], callback_data=f"cat_{cat1['id']}"))

        if i + 1 < len(categorias):
            cat2 = categorias[i + 1]
            fila.append(InlineKeyboardButton(cat2["nombre"], callback_data=f"cat_{cat2['id']}"))

        botones.append(fila)

    return InlineKeyboardMarkup(botones)
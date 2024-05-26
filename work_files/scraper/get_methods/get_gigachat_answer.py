def get_gigachat_answer(answer):
    """
    Обрабатывает ответ от GigaChat API и извлекает текстовое содержание.

    Parameters
    ----------
    answer : dict
        Ответ от GigaChat API в формате словаря.

    Returns
    -------
    list of str
        Список строк, содержащих текстовое содержание из ответа GigaChat.
    """
    text = []
    try:
        for key in answer:
            content = answer[key]['choices'][0]['message']['content']
            text.append(content)
        return text
    except Exception as e:
        print(f'Ошибка в обработке ответа GigaChat: {e}')
        return []

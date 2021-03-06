from django.http import HttpResponse
from django.shortcuts import render



articles_list = [
    [1, "Айви Яптанго", 2020, "Самые шикарные парочки знаменитостей 2019 года", ["красота", "гороскопы"]],
    [2, "Лео Месси", 2014, "Un Abrazo a Todos", ["лайфстайл", "недвижимость"]],
    [3, "Гэри Паска", 2016, "Продаётся дом в Южной Флориде за $2,695", ["недвижимость", "коучинг", "howto"]],
    [4, "Роби Тобинсон", 1967, "7 лет я применял этот трюк и назад пути нет", ["лайфхак", "коучинг", "howto"]],
    [5, "Металлий Вутко", 2017, "Let Me Speak From My Heart", ["футбол", "допинг"]],
    [6, "Роби Тобинсон", 1977, "Беспроигрышная древнеримская техника обольщения", ["отношения", "история", "howto"]],
    [7, "Роби Тобинсон", 2022, "3 способа установить девайс от храпа", ["здоровье", "коучинг", "howto"]],
    [8, "Роби Тобинсон", 1975, "Интимная проблема, которой втайне озабочены все ваши друзья", ["отношения", "здоровье", "howto"]],
    [9, "Elina Shake", 2008, "Представления, основанные на классах", ["python", "howto", "лайфхак"]],
    [10, "Бен Франклин", 1753, "Электрические стодолларовые купюры", ["фондовая биржа", "рынки", "электричество"]],
    [11, "Роби Тобинсон", 2012, "5 забавных Django Apps, о которых говорят все", ["django", "IT", "howto"]],
    [12, "Металлий Вутко", 2017, "No Problems, No Criminality", ["допинг", "недвижимость"]],
    [13, "Роби Тобинсон", 1987, "7 способов до смерти напугать своего босса в пятницу 13-го", ["работа", "мистика", "howto"]],
    [14, "Твентин Карантино", 2007, "Четыре сервера", ["кино", "django", "мистика"]],
]


def get_token(request):
    request.META["CSRF_COOKIE_USED"] = True
    return request.META.get('CSRF_COOKIE', None)


def generate_html(articles):
    if len(articles) == 0:
        return '<h1>По вашему запросу не найдено ни одной статьи!</h1>'
    else:
        base_html = '<h1>Статьи по вашему запросу:</h1> <ul>'
        for article in articles:
            list_item = f'<li><ul>' \
                        f'<li><strong>{article[3]}</strong></li>' \
                        f'<li>автор: {article[1]}</li>' \
                        f'<li>год: {article[2]}</li>' \
                        f'<li>теги: {", ".join(article[4])}</li>' \
                        f'</ul></li>'
            base_html += list_item
        base_html += '</ul>'
        return base_html


# на случай, если в адресе не указан год - установим значение year=-1
def dashboard(request, year=-1):
    found_articles = []
    if year == -1:
        # если в адресе не указан год,
        # записываем в found_articles все статьи нашего блога
        found_articles = articles_list
    else:
        for article in articles_list:
            if year == article[2]:
                found_articles.append(article)
    beautiful_html = generate_html(found_articles)
    return HttpResponse(beautiful_html)


def article_by_id(request, id):
    found_articles = []
    for article in articles_list:
        if id == article[0]:
            found_articles.append(article)
    beautiful_html = generate_html(found_articles)
    return HttpResponse(beautiful_html)


def get_articles_by_tag(tag):
    found_articles = []
    for article in articles_list:
        if tag in article[4]:
            found_articles.append(article)
    beautiful_html = generate_html(found_articles)
    return HttpResponse(beautiful_html)




def search(request):
    if request.method == 'GET':
        name = request.GET['name']
        year = int(request.GET['year'])
        found_articles = []
        for article in articles_list:
            if name == article[1] and year == article[2]:
                found_articles.append(article)
        beautiful_html = generate_html(found_articles)
        return HttpResponse(beautiful_html)

html_template = '''<!DOCTYPE html>
<html lang = "ru">
<head>
    <meta charset="UTF-8">
    <title>MY training project</title>
</head>
<body>
    <form action="{where}" method="post">
        Введите ID статьи и имя нового тега<br><br>
        ID статьи: <input type="text" name="id"><br><br>
        Новый тег: <input type="text" name="new_tag"><br><br>
        <input type="submit" value="Добавить тег">
    </form>
</body>
</html>'''

def add_tag(request):
    if request.method == 'GET':
        html = html_template.format(where=request.path)
        resp = HttpResponse(html)
        return resp
    elif request.method == 'POST':
        article_id = int(request.POST['id'])
        new_tag = request.POST['new_tag']
        for article in articles_list:
            if article_id == article[0]:
                article[4].append(new_tag)
        return article_by_id(request, article_id)

def check_age(request):
    if request.method == 'GET':
        user_age = int(request.GET['age'])
        if user_age < 18:
            return render(request, 'yandex_courses_django/templates/articles/access_denied.html')
        else:
            login = request.GET['login']
            tag = request.GET['tag']
            articles = get_articles_by_tag(tag)
            context = {
                'username': login,
                'age': user_age,
                'articles': articles
            }
            return render(request, 'yandex_courses_django/templates/articles/access_granted.html', context)

def subscribe(request):
    if request.method == 'GET':
        context = {
            'where': request.path
        }
        resp = render(request, 'yandex_courses_django/templates/articles/subscribe_form.html', context)
        return resp
    elif request.method == 'POST':
        author = request.POST['author']
        user_email = request.POST['email']
        author_article = []
        for article in articles_list:
            if author in article[1]:
                author_article.append(article)

        context  = {
            'author': author,
            'email': user_email,
            'articles': generate_html(author_article)
        }
        return render(request, 'yandex_courses_django/templates/articles/subscribe.html', context)
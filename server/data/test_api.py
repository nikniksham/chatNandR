import datetime
import json
from flask import jsonify, request
from flask_restful import Resource
from server.data.test_parser import test_parser


class TestResourceUsual(Resource):
    def get(self):
        return jsonify({"message": ["don't look this", "calculating you address", "police getting to you"]})


class TestResourcePost(Resource):
    def post(self, some_data):
        print(some_data)
        print(test_parser.parse_args())
        return jsonify({"okay": "i forgive you"})


"""
def find_by_id(id, session):
    newspage = session.query(Newspage).get(id)
    if not newspage:
        raise_error(f"Страница не найдена", session)
    return newspage, session


class NewspageResource(Resource):
    def put(self, newspage_id):
        args, count_params = parser_newspage.parse_args(), 0
        if not all(args[key] is not None for key in ['admin_email', 'action', 'admin_password']):
            raise_error('Пропущены некоторые важные аргументы')
        admin, session = check_admin_status(args['admin_email'], args["admin_password"])
        newspage, session = find_by_id(newspage_id, session)
        if args["action"] == "get":
            news_dict = newspage.to_dict(
                only=('id', 'heading', 'text', 'link', 'image', 'tags', 'created_date', 'author_id'))
            news_dict["mini_text"] = mini_text(newspage.text)
            news_dict["text_render"] = text_transform(newspage.text, newspage.image.split("//"), path)
            session.close()
            return jsonify(news_dict)
        elif args["action"] == "delete":
            session.delete(newspage)
            session.commit()
            add_auditlog("Удаление", f"{admin.name} {admin.surname} удаляет новостную страницу: {newspage.heading}", admin,
                         datetime.datetime.now())
            session.close()
            return jsonify({"success": f"Новостная страница {newspage.heading} успешно удалена"})
        elif args["action"] == "put":
            page_dict = newspage.to_dict(only=('heading', 'text', 'image', 'tags'))
            keys = list(filter(lambda key: args[key] is not None and key in page_dict and args[key] != page_dict[key], list(args.keys())))
            for key in keys:
                count_params += 1
                if key == 'image':
                    print(args['image'])
                    newspage.image = args['image']
                if key == 'heading':
                    newspage.heading = args["heading"]
                    link, count = trans_link(args["heading"]), 0
                    while session.query(Newspage).filter(Newspage.link == link).first() is not None:
                        if link[-len(str(count)):] == str(count):
                            link = link[:-len(str(count))] + str(count + 1)
                            count += 1
                        else:
                            link += str(count)
                    newspage.link = link
                if key == "text":
                    newspage.text = args["text"]
                if key == "tags":
                    newspage.tags = args["tags"]
            if count_params == 0:
                return raise_error("Пустой запрос", session)
            page_dict_2 = newspage.to_dict(only=('heading', 'text', 'image', 'tags'))
            list_chang = [f'изменяет {key} с {page_dict[key]} на {page_dict_2[key]}' if key != "image" else "изменяет изображения" for key in keys]
            session.commit()
            add_auditlog("Изменение",
                         f"{admin.name} {admin.surname} изменяет новостную страницу {newspage.heading}: {', '.join(list_chang)}",
                         admin, datetime.datetime.now())
            session.close()
            return jsonify({"success": f"Новостная страница {newspage.heading} успешно изменена"})
        raise_error("Неизвестный метод", session)


class NewspageResourceUsual(Resource):
    def get(self, newspage_id):
        session = db_session.create_session()
        newspage, session = find_by_id(newspage_id, session)
        session.close()
        news_dict = newspage.to_dict(only=('id', 'heading', 'text', 'link', 'image', 'tags', 'created_date'))
        news_dict["mini_text"] = mini_text(newspage.text)
        news_dict["text_render"] = text_transform(newspage.text, newspage.image.split("//"), path)
        return jsonify(news_dict)


class NewspageResourceLink(Resource):
    def get(self, link):
        session = db_session.create_session()
        newspage = session.query(Newspage).filter(Newspage.link == link).first()
        session.close()
        if newspage:
            news_dict = newspage.to_dict(only=('id', 'heading', 'text', 'link', 'image', 'tags', 'created_date'))
            news_dict["mini_text"] = mini_text(newspage.text)
            news_dict["text_render"] = text_transform(newspage.text, newspage.image.split("//"), path)
            return jsonify(news_dict)
        raise_error("Новость не найдена")


class NewspageListRecourseId(Resource):
    def get(self, start_id, end_id):
        session = db_session.create_session()
        newspages = session.query(Newspage).order_by(Newspage.created_date)[::-1]
        session.close()
        if start_id > len(newspages):
            return jsonify([])
        if end_id > len(newspages):
            end_id = len(newspages)
        newspages, news_list = newspages[start_id:end_id], []
        for item in newspages:
            news_dict = item.to_dict(only=('id', 'heading', 'text', 'link', 'image', 'tags', 'created_date'))
            news_dict["mini_text"] = mini_text(item.text)
            news_dict["text_render"] = text_transform(item.text, item.image.split("//"), path)
            news_list.append(news_dict)
        return jsonify(news_list)


class NewspageListRecourseTags(Resource):
    def post(self, start_id, end_id):
        dick = {}
        params = json.loads(request.form['canvas_data'])
        text = params["text"]
        write_log(text)
        session = db_session.create_session()
        news_pages = session.query(Newspage).order_by(Newspage.created_date).all()
        if text:
            for news_page in news_pages:
                for word in text.split():
                    if news_page.tags and word.lower() in news_page.tags.lower():
                        if news_page in dick:
                            dick[news_page] += 10
                        else:
                            dick[news_page] = 10
                    if news_page.heading and word.lower() in news_page.heading.lower():
                        if news_page in dick:
                            dick[news_page] += 4
                        else:
                            dick[news_page] = 4
                    if news_page.text and word.lower() in news_page.text.lower():
                        if news_page in dick:
                            dick[news_page] += 1
                        else:
                            dick[news_page] = 1
            news_list = []
            for compare in list(set(dick.values())):
                a = []  # тут у ники случился инсульт жопы
                for key in dick.keys():
                    if dick[key] == compare:
                        a.append(key)
                a.sort(key=lambda x: x.created_date, reverse=True)
                news_list.extend(a)
        else:
            news_list = news_pages
        if start_id > len(news_list):
            return jsonify([])
        if end_id > len(news_list):
            end_id = len(news_list)
        newspages, news_list = news_list[start_id:end_id], []
        write_log(f"I am here")
        for item in newspages:
            news_dict = item.to_dict(only=('id', 'heading', 'text', 'link', 'image', 'tags', 'created_date'))
            news_dict["mini_text"] = mini_text(item.text)
            news_dict["text_render"] = text_transform(item.text, item.image.split("//"), path)
            write_log(f"Add news {news_dict['heading']}")
            news_list.append(news_dict)
        return jsonify(news_list)


class NewspageListRecourse(Resource):
    def get(self):
        session = db_session.create_session()
        newspages, news_list = session.query(Newspage).order_by(Newspage.created_date)[::-1], []
        for item in newspages:
            news_dict = item.to_dict(only=('id', 'heading', 'text', 'link', 'image', 'tags', 'created_date'))
            news_dict["mini_text"] = mini_text(item.text)
            news_dict["text_render"] = text_transform(item.text, item.image.split("//"), path)
            news_list.append(news_dict)
        session.close()
        return jsonify(news_list)


class CreateNewspageResource(Resource):
    def post(self):
        args = parser_newspage.parse_args()
        if not all(args[key] is not None for key in ['heading', 'text', 'admin_email', 'admin_password']):
            raise_error('Пропущены некоторые аргументы, необходимые для создания новостной страницы')
        admin, session = check_admin_status(args['admin_email'], args["admin_password"])
        new_newspage = Newspage()
        new_newspage.heading = args["heading"]
        new_newspage.text = args["text"]
        link, count = args["link"] if args["link"] is not None else trans_link(args["heading"]), 0
        while session.query(Newspage).filter(Newspage.link == link).first() is not None:
            if link[-len(str(count)):] == str(count):
                link = link[:-len(str(count))] + str(count + 1)
                count += 1
            else:
                link += str(count)
        new_newspage.link = link
        new_newspage.image = args['image']
        new_newspage.tags = args['tags']
        new_newspage.created_date = datetime.datetime.now()
        if args["id"] is not None:
            if session.query(Newspage).get(args["id"]) is not None:
                raise_error("Этот id уже занят")
            new_newspage.id = args["id"]
        admin.newspage.append(new_newspage)
        session.merge(admin)
        session.commit()
        params_dict = new_newspage.to_dict(only=('id', 'heading', 'text', 'link', 'tags', 'created_date', 'author_id'))
        params_dict["image"] = f'кол-во изображений: {len(args["image"].split("//"))}'
        add_auditlog("Создание",
                     f"{admin.name} {admin.surname} создаёт новостную страницу {new_newspage.heading}: {params_dict}",
                     admin, datetime.datetime.now())
        session.close()
        return jsonify({'success': f'Новостная страница {new_newspage.heading} создана', 'id': new_newspage.id})
"""
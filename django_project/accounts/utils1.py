from accounts.models import IP_addres, Category, Genre, countrys

user_menu = [{'title': "ФИЛЬМЫ", 'url_name': 'category/film'},
        {'title': "МУЛЬТФИЛЬМЫ", 'url_name': 'category/cartoon'},
        {'title': "АНИМЕ", 'url_name': 'category/anime'},
]


class DataMixin():
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip_ad = x_forwarded_for.split(',')[0]
        else:
            ip_ad = request.META.get('REMOTE_ADDR')
        obj, created = IP_addres.objects.get_or_create(ip=ip_ad)
        return obj.id

class PaginationMixin():
    paginate_by = 12
    def get_pagination_list(self, context, fff):
        a = context.get('page_obj')
        qqq1 = a.number
        qqq2 = a.number
        qqq3 = a.paginator.num_pages + 1
        i = 0
        while (qqq1 != 1 or qqq2 != qqq3) and (i < fff):
            if qqq2 != qqq3:
                qqq2 += 1
                i += 1
            if qqq1 != 1:
                qqq1 -= 1
                i += 1
        qqq = []
        for r in range(qqq1, qqq2):
            qqq.append(r)
        if qqq3 > fff:
            if qqq[0] != 1:
                qqq[0] = 1
                qqq[1] = 0
            if qqq[-1] != qqq3 - 1:
                qqq[-1] = qqq3 - 1
                qqq[-2] = 0
        # print(qqq)
        return qqq

    def get_user_context(self, **kwargs):                       #функция для формирования и динамического и статического контекста
        context = kwargs
        context['q'] = self.request.GET.get("q")
        context['qqq'] = self.get_pagination_list(context, 9)
        context['categorys'] = Category.objects.all()
        context['genres'] = Genre.objects.all()
        context['countrys'] = countrys
        context['category'] = self.request.GET.getlist("category")
        return context

class DetailMixin():
    def coment(self, a):
        """создание дерева коментариев"""
        def tree(c):
            """запись коментов в поле для детей у родительского комента"""
            for f in c:
                if f.get("children"):                               # если коментарии имеет детей
                    for item in f.get("children"):                  # проход по списку детей
                        for j in a:                                 # проход по списку а
                            if j.get("id") == item:                 # если находим id то у списка детей заменяем элемент на словарь
                                m = f.get("children")
                                ind = m.index(item)
                                m.insert(ind, j)
                                m.remove(item)
                                a.remove(j)
                                f.update(children=m)                # сохраняем элемент в списке детей
                                break
                    d = f.get("children")
                    m = tree(d)
                    f.update(children=m)
            return c

        cc = []
        for b in a:  # создание нового списка словарей с ключами где хранятся дети
            if b.get("parent_id") != None:
                for r in a:
                    if r.get("id") == b.get("parent_id"):
                        if r.get("children") == None:
                            r["children"] = []
                        tttt = r.get('children')
                        tttt.append(b.get("id"))
                        r["children"] = tttt
        v = len(a)
        i = 0
        j = 0
        while i < v:  # удаление из нового списка с коментов без детей
            if not a[j].get("parent_id"):
                cc.append(a.pop(j))
            else:
                j += 1
            i += 1
        c = tree(cc)
        return c

    def get_user_context(self, **kwargs):                       #функция для формирования и динамического и статического контекста
        context = kwargs
        context['categorys'] = Category.objects.all()
        context['genres'] = Genre.objects.all()
        context['countrys'] = countrys
        return context


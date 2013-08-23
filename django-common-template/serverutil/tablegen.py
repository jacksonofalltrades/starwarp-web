class TableGen(object):
    TABLE_META = {}

    @classmethod
    def get_table_meta(cls, tname, user, sfilter):
        if tname in cls.TABLE_META:
            return cls.TABLE_META[tname]['metafunc'](user, sfilter)
        else:
            return None

    @classmethod
    def get_table_page(cls, tname, user, sfilter, page):
        pg = cls.get_table_meta(tname, user, sfilter)
        if page <= pg.num_pages:
            curr_page = pg.page(page)
            page_objs = curr_page.object_list
            
            results = map(lambda x: cls.TABLE_META[tname]['datafunc'](x), page_objs)
        else:
            results = []
        
        return results
                
    @classmethod
    def get_table_data(cls, tname, user, sfilter, page):
        if tname in cls.TABLE_META:
            return {
                'data': cls.get_table_page(tname, user, sfilter, page),
                'row_template': cls.TABLE_META[tname]['template'],
                'columns': cls.TABLE_META[tname]['cols'],
                'empty_text': cls.TABLE_META[tname]['empty_text']
            }
        else:
            return None

    @classmethod
    def register_datasource(cls, name, stuff):
        cls.TABLE_META[name] = stuff

    @classmethod
    def get_page_num_list(cls, page, pages):
        # Meta-page size
        m = 10
        x = page
        t = pages
                
        spn = (x - x%m)
        if spn == x and spn > 1:
            spn = x - m + 1
        else:
            spn = spn + 1
        epn = spn + m - 1

        pre_start = spn - 1
        post_end = epn + 1
        
        last_page = min(epn, pages)
        
        page_list = []
        if pages > 1:
            if spn > 1:
                page_index = pre_start
                page_list.append({'text': '<<', 'page': page_index, 'selected': False})
                
            for i in range(spn, last_page+1):
                page_index = i
                selected = (page == page_index)
                page_list.append({'text': page_index, 'page': page_index, 'selected': selected})
            
            if last_page < pages:
                page_index = post_end
                page_list.append({'text': '>>', 'page': page_index, 'selected': False})
        else:
            page_list.append({'text': '1', 'page': 1, 'selected': True})
            
        return page_list

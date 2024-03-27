import redis
from django.conf import settings
from .models import Product

#Соединение с redis
r = redis.Redis(host = settings.REDIS_HOST,
                port = settings.REDIS_PORT,
                db = settings.REDIS_DB)

class Recommender:
    def get_product_key(self, id):
        return f'product:{id}:purchased_with'
    
    def products_bought(self, products):
        product_ids = [p.id for p in products]
        for product_id in product_ids:
            for with_id in product_ids:
                #Получение других товаров, купленных вместе с каждым товаром
                if product_id != with_id:
                    # увеличить бал товара
                    r.zincrby(self.get_product_key(product_id),
                              1, with_id)
    
    def suggest_products_for(self, products, max_results = 6):
        product_ids = [p.id for p in products]
        if len(product_ids) == 1:
            #только один товар
            suggestions = r.zrange(self.get_product_key(product_ids[0]),
                                   0, -1, desc = True)[:max_results]
        
        else:
            #генерация временного ключа
            flat_ids = ''.join([str(id) for id in product_ids])
            tmp_key = f'tmp_{flat_ids}'
            #объединение баллов всех товаров, сохранение полученного 
            #сортированного множества в временном ключе
            keys = [self.get_product_key(id) for id in product_ids]
            r.zunionstore(tmp_key, keys)
            # удаление идентификаторов товаров, для которых делается рекомендация
            r.zrem(tmp_key, *product_ids)
            # получение идентификаторов товаров по их количеству, сортировка по убыванию
            suggestions = r.zrange(tmp_key, 0, -1, desc = True)[:max_results]
            # удаление временного ключа
            r.delete(tmp_key)
        
        suggested_prodcuts_ids = [int(id) for id in suggestions]
        suggested_products = list(Product.objects.filter(id__in = suggested_prodcuts_ids))
        suggested_products.sort(key = lambda x: suggested_prodcuts_ids.index(x.id))
        return suggested_products
    
    def clear_prochases(self):
        for id in Product.objects.values_list('id', flat = True):
            r.delete(self.get_product_key(id))
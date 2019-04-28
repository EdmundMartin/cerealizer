from cerealizer.serializers import DictSerializer
from cerealizer.fields import PositiveInteger, URLField

if __name__ == '__main__':
    class MyData(DictSerializer):
        positive_number = PositiveInteger()
        target_url = URLField()
        related_urls = URLField(many=True)

    res = MyData()
    res.validate({'positive_number': 20, 'target_url': 'http://edmundmartin.com',
                  'related_urls': ['http://russia.com']})
    print(res.validated_data)
    print(res.is_valid)
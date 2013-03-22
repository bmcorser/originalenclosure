from datetime import datetime
import pytz
import factory
from pars.models import Par, Image

class ImageFactory(factory.Factory):

    FACTORY_FOR = Image

    source = 'http://originalenclosure.net/media/pars/6MxQsQjpgrjavaconffreeofficebarberlivewallpaper-2-0.jpgw156h156'

class ParFactory(factory.Factory):

    FACTORY_FOR = Par

    number = factory.Sequence(lambda x: '{0:04}'.format(int(x)))
    title = factory.Sequence(lambda x: 'a par number {0}'.format(x))
    @factory.lazy_attribute
    def created(self):
        return datetime.now(pytz.utc)

    @factory.lazy_attribute
    def left(self):
        return factory.SubFactory(ImageFactory)

    @factory.lazy_attribute
    def right(self):
        return factory.SubFactory(ImageFactory)


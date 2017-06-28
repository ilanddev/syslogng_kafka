import confluent_kafka


# Producer is a native C object. We cannot use unittest.mock to set attributes.
class MockProducer(confluent_kafka.Producer):
    def flush(self, timeout=0):
        return super(MockProducer, self).flush()

    def produce(self, topic, msg, callback=None):
        print("produce() on topic=%s w/ msg=%s" % topic, msg)

    def __len__(self):
        return super(MockProducer, self).__len__()


confluent_kafka.__dict__['OldProducer'] = confluent_kafka.__dict__['Producer']
confluent_kafka.__dict__['Producer'] = MockProducer


# revert to not freak out Sphynx and friends after the tests ran and monkey.
def revert():
    confluent_kafka.__dict__['Producer'] = confluent_kafka.__dict__[
        'OldProducer']
    del confluent_kafka.__dict__['OldProducer']

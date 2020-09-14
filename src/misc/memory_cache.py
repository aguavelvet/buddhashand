

from ..input_handler import InputHandler


class MemoryCache(InputHandler):
    '''
    This cache is nifty.  The cache is an input handler.  So, Cache supports all the input handlers as the input
    data source.  the InputHandler.handle simply fetches the key:values from the input record and caches in mem.
    '''
    caches = {}

    current_ns = None
    key = None
    val = None

    def __init__(self,cfg:dict):

        # populate the mem-cache.
        from ..conf.factory import Factory
        for ns,nscfg in cfg.items():
            # We need to know what our current name space is so we can populate the right mem cache.
            # Cache initialization must be an atomic operation and can not be parallelized. Naemspace name, the key
            # and values are set at the class level and handle populates the appropriate cache based on these values.
            MemoryCache.current_ns = ns
            MemoryCache.key = nscfg['key']
            MemoryCache.val = nscfg['val']

            input = Factory.create_input_provider(self, nscfg['input'])
            input.start()
            input.done()
            print(f'mem cache load complete for {ns}.  Found {len(MemoryCache.caches[ns])} entries...')


    def handle(self, irec: map):
        ''' handle the input record.'''
        if MemoryCache.current_ns is not None:
            if MemoryCache.current_ns not in MemoryCache.caches:
                MemoryCache.caches[MemoryCache.current_ns] = {}

            cache = MemoryCache.caches[MemoryCache.current_ns]
            cache[irec[MemoryCache.key]] = irec[MemoryCache.val]

    def done(self):
        # print (f'mem cache load complete.  Found {len(self.cache)} entries...')
        pass


    def get_value (ns, key):
        '''
        get the value for the given name space and the key.
        Return value for the NS:key value.
        '''
        value = None
        if ns in MemoryCache.caches:
            cache = MemoryCache.caches[ns]
            value = cache[key] if key in cache else None

        return value

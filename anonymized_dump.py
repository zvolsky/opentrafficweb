from pg_dump_anonymized.anonymized_dump import Dump as ExampleDump


class Dump(ExampleDump):
    def dump(self, *args, **kwargs):
        return super().dump(*args, **kwargs)

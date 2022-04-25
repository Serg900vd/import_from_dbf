import datetime
import dbf

# create an in-memory table
table = dbf.Table(
        filename='test',
        field_specs='name C(25); age N(3,0); birth D; qualified L',
        on_disk=False,
        )
table.open(mode=dbf.READ_WRITE)

# add some records to it
for datum in (
        ('Spanky', 7, dbf.Date.fromymd('20010315'), False),
        ('Spunky', 23, dbf.Date(1989, 7, 23), True),
        ('Sparky', 99, dbf.Date(), dbf.Unknown),
        ):
    table.append(datum)

# iterate over the table, and print the records
for record in table:
    print(record)
    print('--------')
    print(record[0:3])
    print([record.name, record.age, record.birth])
    print('--------')

# make a copy of the test table (structure, not data)
custom = table.new(
        filename='test_on_disk',
        default_data_types=dict(C=dbf.Char, D=dbf.Date, L=dbf.Logical),
        )

# automatically opened and closed
with custom:
    # copy records from test to custom
    for record in table:
        custom.append(record)
    # modify each record in custom (could have done this in prior step)
    for record in custom:
        dbf.write(record, name=record.name.upper())
        # and print the modified record
        print(record)
        print('--------')
        print(record[0:3])
        print([record.name, record.age, record.birth])
        print('--------')

table.close()


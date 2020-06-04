from pprint import pprint
import csv
import re

### Initial data provided by tutors

with open("phonebook_raw.csv") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

header = contacts_list.pop(0)

### Entering our code

def normalizing_names(name_string):

    return name_string.replace(',', ' ', ).split(' ')[: 3]


def normalizing_phones(phone_string):

    pattern = r'(8|\+7)\s*\(?(\d{3})\)?[-|\s*]?(\d{3})[-|\s*]?(\d{2})[-|\s*]?(\d{2})((\s*)\(?(доб.)\s*(\d+)\)?)?'
    new_pattern = r'+7(\2)\3-\4-\5\7\8\9'
    return re.sub(pattern, new_pattern, phone_string)

contacts_dict = {}

for item in contacts_list:
    
    name = tuple(normalizing_names(','.join(item[0: 3])))
    
    temporary_dict = {
        header[3]: '',
        header[4]: '',
        header[5]: '',
        header[6]: ''
    }
    contacts_dict.setdefault(name, temporary_dict)
    contacts_dict[name][header[3]] = contacts_dict[name][header[3]] if contacts_dict[name][header[3]] else item[3]
    contacts_dict[name][header[4]] = contacts_dict[name][header[4]] if contacts_dict[name][header[4]] else item[4]
    contacts_dict[name][header[5]] = contacts_dict[name][header[5]] if contacts_dict[name][header[5]] else \
        normalizing_phones(item[5])
    contacts_dict[name][header[6]] = contacts_dict[name][header[6]] if contacts_dict[name][header[6]] else item[6]

edited_contacts_dict = {}

for prim_issue in contacts_dict:

    if '' in prim_issue:
        for secondary_issue in contacts_dict:
            if prim_issue[0] == secondary_issue[0] and '' not in secondary_issue:
                for contact_info in contacts_dict[prim_issue]:
                    if contacts_dict[prim_issue][contact_info]:
                        contacts_dict[secondary_issue][contact_info] = contacts_dict[prim_issue][contact_info]
                edited_contacts_dict = contacts_dict.copy()
                del edited_contacts_dict[prim_issue]


edited_phonebook_list = [[*key, edited_contacts_dict[key][header[3]], edited_contacts_dict[key][header[4]],
                 edited_contacts_dict[key][header[5]], edited_contacts_dict[key][header[6]]] for key in edited_contacts_dict]
edited_phonebook_list.insert(0, header)


### Saving edited data to another file formatted as CSV


with open("phonebook.csv", "w") as f:

    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(edited_phonebook_list)
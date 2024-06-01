import time
import uuid


def get_uniq_id():
    return str(uuid.uuid4()).split("-")[-1]


class Accession:
    def __init__(self,
                 uniq_id=None,
                 lat=None,
                 lon=None,
                 alt=None,
                 sources=[],
                 IDs={},
                 passport={},
                 phenotypic={},
                 dataset={},
                 properties={},
                 **kwargs):

        self.uniq_id = str(uniq_id) if uniq_id else get_uniq_id()

        # load the coordinate
        self.lat = lat
        self.lon = lon
        self.alt = alt
        self.update_coordinate()

        # load IDs
        self.IDs = IDs if IDs else {}
        for k, v in kwargs.items():
            if k.endswith("_id"):
                if k in self.IDs:
                    if isinstance(self.IDs[k], list):
                        self.IDs[k].append(v)
                    else:
                        self.IDs[k] = v
                else:
                    self.IDs[k] = v

            if k.endswith("_id_list"):
                k = k.replace("_id_list", "_id")
                if k in self.IDs:
                    self.IDs[k].append(v)
                else:
                    self.IDs[k] = v

        # load passport
        self.passport = passport if passport else {}

        # load phenotypic
        self.phenotypic = phenotypic if phenotypic else {}

        # load dataset
        self.dataset = dataset if dataset else {}

        # load properties
        self.properties = properties if properties else {}
        for k, v in kwargs.items():
            if not k.endswith("_id") and not k.endswith("_id_list"):
                self.properties[k] = v

        # load sources
        self.sources = sources

    def __str__(self):
        return """
----------------
Accession: %s
Coordinate: Lat: %s, Lon: %s, Alt: %s
Sources: %s
----------------
""" % (
            self.uniq_id,
            self.lat if self.lat else "None",
            self.lon if self.lon else "None",
            self.alt if self.alt else "None",
            self.sources
        )

    def __repr__(self):
        return self.__str__()

    def update(self, value, level1, level2=None):
        """
        Update the value of the accession
        level1: the level of the value, it can be "coordinate", "IDs", "passport", "phenotypic", "dataset", "properties"
        level2: the key of the value, if the level1 is "coordinate", it can be "lat", "lon", "alt"
        """

        if level1 == "coordinate":
            if level2 == "lat":
                self.lat = value
            elif level2 == "lon":
                self.lon = value
            elif level2 == "alt":
                self.alt = value
            else:
                print("Error: the level2 is not valid")
            self.update_coordinate()
        elif level1 == "IDs":
            if level2 in self.IDs:
                if isinstance(value, list):
                    self.IDs[level2] += value
                    self.IDs[level2] = list(set(self.IDs[level2]))
                else:
                    self.IDs[level2] = value
            else:
                self.IDs[level2] = value
        elif level1 == "passport":
            if level2 in self.passport:
                if isinstance(value, list):
                    self.passport[level2] += value
                    self.passport[level2] = list(set(self.passport[level2]))
                else:
                    self.passport[level2] = value
            else:
                self.passport[level2] = value
        elif level1 == "phenotypic":
            if level2 in self.phenotypic:
                if isinstance(value, list):
                    self.phenotypic[level2] += value
                    self.phenotypic[level2] = list(
                        set(self.phenotypic[level2]))
                else:
                    self.phenotypic[level2] = value
            else:
                self.phenotypic[level2] = value
        elif level1 == "dataset":
            if level2 in self.dataset:
                if isinstance(value, list):
                    self.dataset[level2] += value
                    self.dataset[level2] = list(set(self.dataset[level2]))
                else:
                    self.dataset[level2] = value
            else:
                self.dataset[level2] = value
        elif level1 == "properties":
            if level2 in self.properties:
                if isinstance(value, list):
                    self.properties[level2] += value
                    self.properties[level2] = list(
                        set(self.properties[level2]))
                else:
                    self.properties[level2] = value
            else:
                self.properties[level2] = value
        elif level1 == "sources":
            self.sources += value
            self.sources = list(set(self.sources))
        else:
            print("Error: the level1 is not valid")

    def update_coordinate(self):
        self.lat = float(self.lat) if self.lat is not None else None
        self.lon = float(self.lon) if self.lon is not None else None
        self.alt = float(self.alt) if self.alt is not None else None

        if self.lat is None and self.lon is None and self.alt is None:
            self.coordinate = None
        else:
            self.coordinate = (self.lat, self.lon, self.alt)


class AccessionSet:
    def __init__(self, name, date=None, default_ID_items={}, default_passport_items={}, default_phenotypic_items={}, default_dataset_items={}, default_properties_items={}):
        """
        items is a dict to store the default items for the accession
        example:
        items_dict = {
            'unique_id': str,
            'country': str,
            'reseq': bool,
            'dataset': list,
        }
        """

        self.name = name
        self.date = date if date else time.strftime(
            "%Y-%m-%d %H:%M:%S", time.localtime())
        self.default_ID_items = default_ID_items
        self.default_passport_items = default_passport_items
        self.default_phenotypic_items = default_phenotypic_items
        self.default_dataset_items = default_dataset_items
        self.default_properties_items = default_properties_items
        self.accession_dict = {}

    def add(self, accession, keep_uniq_id=False):
        accession = self.acc_formatter(accession, keep_uniq_id=keep_uniq_id)
        self.accession_dict[accession.uniq_id] = accession

    def get(self, uniq_id):
        return self.accession_dict[uniq_id]

    def acc_formatter(self, accession, keep_uniq_id=False):
        IDs = {}
        for k in self.default_ID_items:
            if self.default_ID_items[k] is str:
                IDs[k] = str(
                    accession.IDs[k]) if k in accession.IDs and accession.IDs[k] is not None else None
            elif self.default_ID_items[k] is list:
                if k in accession.IDs:
                    if isinstance(accession.IDs[k], list):
                        IDs[k] = accession.IDs[k]
                    else:
                        IDs[k] = [accession.IDs[k]
                                  ] if accession.IDs[k] is not None else []
                else:
                    IDs[k] = []
            elif self.default_ID_items[k] is bool:
                IDs[k] = bool(
                    accession.IDs[k]) if k in accession.IDs and accession.IDs[k] is not None else None
            elif self.default_ID_items[k] is int:
                IDs[k] = int(
                    accession.IDs[k]) if k in accession.IDs and accession.IDs[k] is not None else None
            elif self.default_ID_items[k] is float:
                IDs[k] = float(accession.IDs[k]
                               ) if k in accession.IDs and accession.IDs[k] is not None else None
            elif self.default_ID_items[k] is dict:
                IDs[k] = dict(
                    accession.IDs[k]) if k in accession.IDs and accession.IDs[k] is not None else None
            else:
                print("Error: the type of the ID item is not valid")

        passport = {}
        for k in self.default_passport_items:
            if self.default_passport_items[k] is str:
                passport[k] = str(accession.passport[k]
                                  ) if k in accession.passport and accession.passport[k] is not None else None
            elif self.default_passport_items[k] is list:
                if k in accession.passport:
                    if isinstance(accession.passport[k], list):
                        passport[k] = accession.passport[k]
                    else:
                        passport[k] = [accession.passport[k]
                                       ] if accession.passport[k] is not None else []
                else:
                    passport[k] = []
            elif self.default_passport_items[k] is bool:
                passport[k] = bool(accession.passport[k]
                                   ) if k in accession.passport and accession.passport[k] is not None else None
            elif self.default_passport_items[k] is int:
                passport[k] = int(accession.passport[k]
                                  ) if k in accession.passport and accession.passport[k] is not None else None
            elif self.default_passport_items[k] is float:
                passport[k] = float(accession.passport[k]
                                    ) if k in accession.passport and accession.passport[k] is not None else None
            elif self.default_passport_items[k] is dict:
                passport[k] = dict(accession.passport[k]
                                   ) if k in accession.passport and accession.passport[k] is not None else None
            else:
                print("Error: the type of the passport item is not valid")

        phenotypic = {}
        for k in self.default_phenotypic_items:
            if self.default_phenotypic_items[k] is str:
                phenotypic[k] = str(accession.phenotypic[k]
                                    ) if k in accession.phenotypic and accession.phenotypic[k] is not None else None
            elif self.default_phenotypic_items[k] is list:
                if k in accession.phenotypic:
                    if isinstance(accession.phenotypic[k], list):
                        phenotypic[k] = accession.phenotypic[k]
                    else:
                        phenotypic[k] = [accession.phenotypic[k]
                                         ] if accession.phenotypic[k] is not None else []
                else:
                    phenotypic[k] = []
            elif self.default_phenotypic_items[k] is bool:
                phenotypic[k] = bool(accession.phenotypic[k]
                                     ) if k in accession.phenotypic and accession.phenotypic[k] is not None else None
            elif self.default_phenotypic_items[k] is int:
                phenotypic[k] = int(accession.phenotypic[k]
                                    ) if k in accession.phenotypic and accession.phenotypic[k] is not None else None
            elif self.default_phenotypic_items[k] is float:
                phenotypic[k] = float(
                    accession.phenotypic[k]) if k in accession.phenotypic and accession.phenotypic[k] is not None else None
            elif self.default_phenotypic_items[k] is dict:
                phenotypic[k] = dict(accession.phenotypic[k]
                                     ) if k in accession.phenotypic and accession.phenotypic[k] is not None else None
            else:
                print("Error: the type of the phenotypic item is not valid")

        dataset = {}
        for k in self.default_dataset_items:
            if self.default_dataset_items[k] is str:
                dataset[k] = str(accession.dataset[k]
                                 ) if k in accession.dataset and accession.dataset[k] is not None else None
            elif self.default_dataset_items[k] is list:
                if k in accession.dataset:
                    if isinstance(accession.dataset[k], list):
                        dataset[k] = accession.dataset[k]
                    else:
                        dataset[k] = [accession.dataset[k]
                                      ] if accession.dataset[k] is not None else []
                else:
                    dataset[k] = []
            elif self.default_dataset_items[k] is bool:
                dataset[k] = bool(accession.dataset[k]
                                  ) if k in accession.dataset and accession.dataset[k] is not None else None
            elif self.default_dataset_items[k] is int:
                dataset[k] = int(accession.dataset[k]
                                 ) if k in accession.dataset and accession.dataset[k] is not None else None
            elif self.default_dataset_items[k] is float:
                dataset[k] = float(accession.dataset[k]
                                   ) if k in accession.dataset and accession.dataset[k] is not None else None
            elif self.default_dataset_items[k] is dict:
                dataset[k] = dict(accession.dataset[k]
                                  ) if k in accession.dataset and accession.dataset[k] is not None else None
            else:
                print("Error: the type of the dataset item is not valid")

        properties = {}
        for k in self.default_properties_items:
            if self.default_properties_items[k] is str:
                properties[k] = str(accession.properties[k]
                                    ) if k in accession.properties and accession.properties[k] is not None else None
            elif self.default_properties_items[k] is list:
                if k in accession.properties:
                    if isinstance(accession.properties[k], list):
                        properties[k] = accession.properties[k]
                    else:
                        properties[k] = [accession.properties[k]
                                         ] if accession.properties[k] is not None else []
                else:
                    properties[k] = []
            elif self.default_properties_items[k] is bool:
                properties[k] = bool(accession.properties[k]
                                     ) if k in accession.properties and accession.properties[k] is not None else None
            elif self.default_properties_items[k] is int:
                properties[k] = int(accession.properties[k]
                                    ) if k in accession.properties and accession.properties[k] is not None else None
            elif self.default_properties_items[k] is float:
                properties[k] = float(
                    accession.properties[k]) if k in accession.properties and accession.properties[k] is not None else None
            elif self.default_properties_items[k] is dict:
                properties[k] = dict(accession.properties[k]
                                     ) if k in accession.properties and accession.properties[k] is not None else None
            else:
                print("Error: the type of the properties item is not valid")

        return Accession(
            uniq_id=accession.uniq_id if keep_uniq_id else get_uniq_id(),
            lat=accession.lat,
            lon=accession.lon,
            alt=accession.alt,
            sources=accession.sources,
            IDs=IDs,
            passport=passport,
            phenotypic=phenotypic,
            dataset=dataset,
            properties=properties
        )

    def build_index(self):
        IDs2uniq_id = {}
        for id_type in self.default_ID_items:
            IDs2uniq_id[id_type] = {}
            for uniq_id in self.accession_dict:
                if self.default_ID_items[id_type] is list:
                    for id_tmp in self.accession_dict[uniq_id].IDs[id_type]:
                        IDs2uniq_id[id_type].setdefault(id_tmp, []).append(uniq_id)
                else:
                    id_tmp = self.accession_dict[uniq_id].IDs[id_type]
                    IDs2uniq_id[id_type].setdefault(id_tmp, []).append(uniq_id)

        self.index = IDs2uniq_id

        sources_list = []
        for uniq_id in self.accession_dict:
            sources_list += self.accession_dict[uniq_id].sources
        self.sources = list(set(sources_list))

    def search(self, q_id, id_type=None):
        if q_id is None:
            return []

        id_type_list = [id_type] if id_type else list(
            self.default_ID_items.keys())
        uniq_id_list = []

        for id_type in id_type_list:
            if q_id in self.index[id_type]:
                uniq_id_list = self.index[id_type][q_id]
                break

        return uniq_id_list

    def search_with_priority(self, id_list):
        uniq_id_list = []
        for q_id in id_list:
            uniq_id_list = self.search(q_id)
            if uniq_id_list:
                break
        return uniq_id_list

    def search_by_id_list(self, id_list):
        uniq_id_dict = {q_id: self.search(q_id)
                        for q_id in id_list if self.search(q_id)}
        return uniq_id_dict

    def __str__(self):
        return """
----------------
Accession Set: %s
Date: %s
Accession Number: %d
Georeferenced Accession Number: %d
----------------
""" % (
            self.name,
            self.date,
            len(self.accession_dict),
            len([i for i in self.accession_dict if self.accession_dict[i].coordinate])
        )

    def report(self):
        if not hasattr(self, 'index'):
            self.build_index()

        head_str = """
----------------
Accession Set: %s
Date: %s
Accession Number: %d
Georeferenced Accession Number: %d
----------------
""" % (
            self.name,
            self.date,
            len(self.accession_dict),
            len([i for i in self.accession_dict if self.accession_dict[i].coordinate])
        )

        body_str = "\t\tAll sources\t" + "\t".join(self.sources) + "\n"

        count_num_list = [self.value_counter('coordinate')]
        count_num_list += [self.value_counter('coordinate', source=source)
                           for source in self.sources]

        body_str += "coordinate:\t" + \
            "\t".join([str(i) for i in count_num_list]) + "\n"

        items_dict = {
            'IDs': self.default_ID_items,
            'passport': self.default_passport_items,
            'phenotypic': self.default_phenotypic_items,
            'dataset': self.default_dataset_items,
            'properties': self.default_properties_items
        }

        for level1 in items_dict:
            body_str += "%s items:\n" % level1
            for level2 in items_dict[level1]:
                body_str += "\t%s\t" % level2
                count_num_list = [self.value_counter(level1, level2)]
                count_num_list += [self.value_counter(level1, level2, source)
                                   for source in self.sources]
                body_str += "\t".join([str(i) for i in count_num_list]) + "\n"

        print(head_str + body_str)

    def value_counter(self, level1, level2=None, source=None):
        count_num = 0

        for uniq_id in self.accession_dict:
            acc = self.accession_dict[uniq_id]
            if (source and source in acc.sources) or source is None:
                if level1 == 'coordinate':
                    if acc.coordinate:
                        count_num += 1
                else:
                    level1_dict = getattr(acc, level1)
                    if level2 in level1_dict:
                        if isinstance(level1_dict[level2], list) or isinstance(level1_dict[level2], dict):
                            if len(level1_dict[level2]) > 0:
                                count_num += 1
                        elif level1_dict[level2] is not None:
                            count_num += 1

        return count_num

    def update_items(self, ID_items={}, passport_items={}, phenotypic_items={}, dataset_items={}, properties_items={}):
        new_ID_items = merge_item_dict(self.default_ID_items, ID_items)
        new_passport_items = merge_item_dict(
            self.default_passport_items, passport_items)
        new_phenotypic_items = merge_item_dict(
            self.default_phenotypic_items, phenotypic_items)
        new_dataset_items = merge_item_dict(
            self.default_dataset_items, dataset_items)
        new_properties_items = merge_item_dict(
            self.default_properties_items, properties_items)

        new_AS = AccessionSet(
            name=self.name,
            date=self.date,
            default_ID_items=new_ID_items,
            default_passport_items=new_passport_items,
            default_phenotypic_items=new_phenotypic_items,
            default_dataset_items=new_dataset_items,
            default_properties_items=new_properties_items
        )

        for uniq_id in self.accession_dict:
            new_AS.add(self.accession_dict[uniq_id], keep_uniq_id=True)

        new_AS.build_index()

        return new_AS


def merge_item_dict(item_dict1, item_dict2):
    new_item_dict = {}
    for k in item_dict1:
        new_item_dict[k] = item_dict1[k]
    for k in item_dict2:
        if k not in new_item_dict:
            new_item_dict[k] = item_dict2[k]
    return new_item_dict


def merge_accession(acc1, acc2):
    """
    Merge two accessions
    - acc1 have the higher priority
    - if the same property is in both acc1 and acc2, the value in acc1 will be used, if value is list, acc2 value will be added
    """

    new_IDs = {}
    for k in acc1.IDs:
        new_IDs[k] = acc1.IDs[k]
    for k in acc2.IDs:
        if k not in new_IDs:
            new_IDs[k] = acc2.IDs[k]
        else:
            if isinstance(new_IDs[k], list):
                new_IDs[k] += acc2.IDs[k]
                new_IDs[k] = list(set(new_IDs[k]))
            elif new_IDs[k] is None and acc2.IDs[k] is not None:
                new_IDs[k] = acc2.IDs[k]

    new_passport = {}
    for k in acc1.passport:
        new_passport[k] = acc1.passport[k]
    for k in acc2.passport:
        if k not in new_passport:
            new_passport[k] = acc2.passport[k]
        else:
            if isinstance(new_passport[k], list):
                new_passport[k] += acc2.passport[k]
                new_passport[k] = list(set(new_passport[k]))
            elif new_passport[k] is None and acc2.passport[k] is not None:
                new_passport[k] = acc2.passport[k]

    new_phenotypic = {}
    for k in acc1.phenotypic:
        new_phenotypic[k] = acc1.phenotypic[k]
    for k in acc2.phenotypic:
        if k not in new_phenotypic:
            new_phenotypic[k] = acc2.phenotypic[k]
        else:
            if isinstance(new_phenotypic[k], list):
                new_phenotypic[k] += acc2.phenotypic[k]
                new_phenotypic[k] = list(set(new_phenotypic[k]))
            elif new_phenotypic[k] is None and acc2.phenotypic[k] is not None:
                new_phenotypic[k] = acc2.phenotypic[k]

    new_dataset = {}
    for k in acc1.dataset:
        new_dataset[k] = acc1.dataset[k]
    for k in acc2.dataset:
        if k not in new_dataset:
            new_dataset[k] = acc2.dataset[k]
        else:
            if isinstance(new_dataset[k], list):
                new_dataset[k] += acc2.dataset[k]
                new_dataset[k] = list(set(new_dataset[k]))
            elif new_dataset[k] is None and acc2.dataset[k] is not None:
                new_dataset[k] = acc2.dataset[k]

    new_properties = {}
    for k in acc1.properties:
        new_properties[k] = acc1.properties[k]
    for k in acc2.properties:
        if k not in new_properties:
            new_properties[k] = acc2.properties[k]
        else:
            if isinstance(new_properties[k], list):
                new_properties[k] += acc2.properties[k]
                new_properties[k] = list(set(new_properties[k]))
            elif new_properties[k] is None and acc2.properties[k] is not None:
                new_properties[k] = acc2.properties[k]

    new_acc = Accession(
        uniq_id=get_uniq_id(),
        lat=acc1.lat if acc1.lat is not None else acc2.lat,
        lon=acc1.lon if acc1.lon is not None else acc2.lon,
        alt=acc1.alt if acc1.alt is not None else acc2.alt,
        sources=list(set(acc1.sources + acc2.sources)),
        IDs=new_IDs,
        passport=new_passport,
        phenotypic=new_phenotypic,
        dataset=new_dataset,
        properties=new_properties
    )

    new_acc.update_coordinate()

    return new_acc


def merge_accession_sets(AS1, AS2, search_id_type_list, new_set_name=None, new_set_date=None):
    """
    Merge two accession sets
    - AS1 have the higher priority
    - if the same search_id is in both AS1 and AS2 and the value is different, the value in AS1 will be used
    - if the same search_id is in both AS1 and AS2 and the value is the same, the value in AS1 will be used
    - if the same search_id is in both AS1 and AS2 and the AS1 value is None, the value in AS2 will be used
    - if no search_id is in AS1, the value in AS2 will be add
    - uniq_id will be totally new

    skip_multihits
    - if True, when an accession in AS2 has multiple hits in AS1, it will be skipped
    - if False, when an accession in AS2 has multiple hits in AS1, it will be added to the frist hit

    if there are multiple accessions in AS2 have same hit in AS1, only the first one will be added
    """

    new_ID_items = {}
    for k in AS1.default_ID_items:
        new_ID_items[k] = AS1.default_ID_items[k]
    for k in AS2.default_ID_items:
        if k not in new_ID_items:
            new_ID_items[k] = AS2.default_ID_items[k]

    new_passport_items = {}
    for k in AS1.default_passport_items:
        new_passport_items[k] = AS1.default_passport_items[k]
    for k in AS2.default_passport_items:
        if k not in new_passport_items:
            new_passport_items[k] = AS2.default_passport_items[k]

    new_phenotypic_items = {}
    for k in AS1.default_phenotypic_items:
        new_phenotypic_items[k] = AS1.default_phenotypic_items[k]
    for k in AS2.default_phenotypic_items:
        if k not in new_phenotypic_items:
            new_phenotypic_items[k] = AS2.default_phenotypic_items[k]

    new_dataset_items = {}
    for k in AS1.default_dataset_items:
        new_dataset_items[k] = AS1.default_dataset_items[k]
    for k in AS2.default_dataset_items:
        if k not in new_dataset_items:
            new_dataset_items[k] = AS2.default_dataset_items[k]

    new_properties_items = {}
    for k in AS1.default_properties_items:
        new_properties_items[k] = AS1.default_properties_items[k]
    for k in AS2.default_properties_items:
        if k not in new_properties_items:
            new_properties_items[k] = AS2.default_properties_items[k]

    AS = AccessionSet(
        name=new_set_name if new_set_name else AS1.name + "_" + AS2.name,
        date=new_set_date if new_set_date else time.strftime(
            "%Y-%m-%d %H:%M:%S", time.localtime()),
        default_ID_items=new_ID_items,
        default_passport_items=new_passport_items,
        default_phenotypic_items=new_phenotypic_items,
        default_dataset_items=new_dataset_items,
        default_properties_items=new_properties_items
    )

    AS1.build_index()

    modified_AS1_uniq_id = []

    for as2_uniq_id in AS2.accession_dict:
        as2_acc = AS2.accession_dict[as2_uniq_id]

        search_id_list = []
        for t in search_id_type_list:
            if t in AS2.default_ID_items:
                as2_id = as2_acc.IDs[t]
                if isinstance(as2_id, list):
                    search_id_list += as2_id
                else:
                    search_id_list.append(as2_id)

        as1_uniq_id_list = AS1.search_with_priority(search_id_list)
        if len(as1_uniq_id_list) == 0:
            AS.add(as2_acc)
        elif len(as1_uniq_id_list) == 1 and as1_uniq_id_list[0] not in modified_AS1_uniq_id:
            as1_uniq_id = as1_uniq_id_list[0]
            as1_acc = AS1.accession_dict[as1_uniq_id]
            new_acc = merge_accession(as1_acc, as2_acc)
            AS.add(new_acc)
            modified_AS1_uniq_id.append(as1_uniq_id)
        
    modified_AS1_uniq_id = set(modified_AS1_uniq_id)
    for as1_uniq_id in AS1.accession_dict:
        if as1_uniq_id not in modified_AS1_uniq_id:
            AS.add(AS1.accession_dict[as1_uniq_id])

    AS.build_index()

    return AS


if __name__ == "__main__":
    # test the sample class
    acc1 = Accession('xyx1', lat=1.0, lon=2.0, alt=3.0,
                     lib_id='lib1', pi_id='pi1')
    print(vars(acc1))

    acc2 = Accession('xyx2', lat=1.0, lon=2.0, lib_id='lib2', pi_id_list=[
        'pi2', 'pi3'], is_id_list=['is2', 'is3'])
    print(vars(acc2))

    acc3 = Accession('xyx3', is_id='is3', lib_id='lib3', pi_id='pi3')
    print(vars(acc3))

    AS = AccessionSet('test', '2020-01-01',
                      default_ID_items={'lib_id': str, 'pi_id': list, 'is_id': list})
    AS.add(acc1)
    AS.add(acc2)
    AS.add(acc3)

    AS.build_index()

    for i in AS.accession_dict:
        print(vars(AS.accession_dict[i]))

    uniq_id = AS.search('lib1', 'lib_id')
    acc = AS.accession_dict[uniq_id]

    print(vars(acc))

    acc4 = merge_accession(acc1, acc2)
    print(vars(acc4))

    # test the merge_accession_sets
    AS1 = AccessionSet('AS1', '2020-01-01',
                       default_ID_items={'lib_id': str, 'pi_id': list, 'is_id': list})
    AS1.add(acc1)
    AS1.add(acc2)
    AS1.add(acc3)

    AS2 = AccessionSet('AS2', '2020-01-01',
                       default_ID_items={'lib_id': str, 'pi_id': list, 'is_id': list, 'is_id2': list})
    AS2.add(acc2)
    AS2.add(acc3)
    AS2.add(acc4)

    AS = merge_accession_sets(AS1, AS2, ['lib_id', 'pi_id', 'is_id'])
    for i in AS.accession_dict:
        print(vars(AS.accession_dict[i]))

    AS.search('lib1')

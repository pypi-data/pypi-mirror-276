from Supplychain.Generic.folder_io import FolderReader, FolderWriter
from Supplychain.Schema.adt_column_description import ADTColumnDescription
from Supplychain.Generic.timer import Timer


def write_transformed_data(reader: FolderReader, writer: FolderWriter):
    with FromTableToDictConverter(reader, writer) as converter:
        return converter.convert_all()


dataset_description = ADTColumnDescription.format


class FromTableToDictConverter(Timer):

    def __init__(self, reader: FolderReader, writer: FolderWriter, descriptor=dataset_description):
        Timer.__init__(self, "[Table -> Dict]")
        self.descriptor = descriptor
        self.reader = reader
        self.writer = writer

    def check_indices(self, name: str, indices: list):
        errors = 0
        unique_indices = set(indices)
        if len(unique_indices) < len(indices):
            duplicates = [
                (index, count)
                for index, count in zip(
                    unique_indices,
                    (indices.count(index) for index in unique_indices),
                )
                if count > 1
            ]
            n = len(duplicates)
            errors += n
            self.display_message(f"ERROR: {name} value{'s' if n > 1 else ''} defined multiple times:")
            for index, count in duplicates:
                self.display_message(f"  {', '.join(str(i) for i in index) if isinstance(index, tuple) else index}: {count}")
        return errors

    def convert_file(self, file_name: str):
        errors = 0

        file_description = dataset_description[file_name]

        entities = []
        if file_name not in self.reader.files:
            return errors

        fixed_file_to_convert = self.reader.files[file_name]

        master_key = None
        if 'id' in file_description['fixed']:
            master_key = 'id'
        elif 'Label' in file_description['fixed']:
            master_key = 'Label'

        for element in fixed_file_to_convert:
            entity = {k: v for k, v in element.items() if k in file_description['fixed']}
            extra = {k: v for k, v in element.items() if k not in file_description['fixed']}
            if extra:
                entity['extra'] = extra
            if master_key and entity.get(master_key) is None:
                continue
            entities.append(entity)

        if master_key:
            errors += self.check_indices(file_name, [entity[master_key] for entity in entities])

        if any(file_description[timed] for timed in ('event', 'change', 'quantity')):

            entity_by_id = dict()
            for entity in entities:
                entity_by_id[entity[master_key]] = entity

            time_files = dict()
            time_files[file_name + "Schedules"] = file_description['change']
            for _event_name, _event_descriptor in file_description['event'].items():
                time_files[_event_name] = _event_descriptor
            for _quantity_name, _quantity_descriptor in file_description['quantity'].items():
                time_files[_quantity_name] = _quantity_descriptor
            quantity_files = set(file_description['quantity'].keys())

            for _sheet_name, _columns in time_files.items():
                if _sheet_name not in self.reader.files or not _columns:
                    continue
                _sheet_to_convert = self.reader.files[_sheet_name]
                indices = []
                unknown_ids = set()
                invalid_timesteps = set()
                invalid_quantities = set()
                for line in _sheet_to_convert:
                    _id = line.get(master_key)
                    if _id is None:
                        continue
                    if _id not in entity_by_id:
                        unknown_ids.add(_id)
                        continue
                    try:
                        timestep = float(line.get('Timestep') or 0)
                    except ValueError:
                        invalid_timesteps.add((_id, line.get('Timestep')))
                        continue
                    if timestep != int(timestep):
                        invalid_timesteps.add((_id, line.get('Timestep')))
                        continue
                    timestep = str(int(timestep))
                    index = (_id, timestep)
                    if _sheet_name in quantity_files:
                        try:
                            quantity = float(line.get('Quantity') or 0)
                        except ValueError:
                            invalid_quantities.add((_id, line.get('Quantity')))
                            continue
                        if quantity != int(quantity):
                            invalid_quantities.add((_id, line.get('Quantity')))
                            continue
                        quantity = str(int(quantity))
                        index = (*index, quantity)
                    indices.append(index)
                    target_entity = entity_by_id[_id]
                    for column in (c for c in _columns if line.get(c) is not None):
                        if column not in target_entity:
                            target_entity[column] = dict()
                        if column in line:
                            if _sheet_name in quantity_files:
                                target_entity[column].setdefault(timestep, {})[quantity] = line[column]
                            else:
                                target_entity[column][timestep] = line[column]
                if unknown_ids:
                    n = len(unknown_ids)
                    errors += n
                    self.display_message(f"ERROR: {master_key} value{'s' if n > 1 else ''} from {_sheet_name} not found in {file_name}:")
                    for _id in unknown_ids:
                        self.display_message(f"  {_id}")
                    non_referenced_ids = set(entity_by_id.keys()) - set(index[0] for index in indices)
                    if non_referenced_ids:
                        self.display_message(f"Suggestion: {master_key} value{'s' if len(non_referenced_ids) > 1 else ''} from {file_name} not found in {_sheet_name}:")
                        for _id in non_referenced_ids:
                            self.display_message(f"  {_id}")
                if invalid_timesteps:
                    n = len(invalid_timesteps)
                    errors += n
                    self.display_message(f"ERROR: invalid Timestep value{'s' if n > 1 else ''} from {_sheet_name}:")
                    for _id, timestep in invalid_timesteps:
                        self.display_message(f"  {master_key} {_id}: {timestep}")
                if invalid_quantities:
                    n = len(invalid_quantities)
                    errors += n
                    self.display_message(f"ERROR: invalid Quantity value{'s' if n > 1 else ''} from {_sheet_name}:")
                    for _id, quantity in invalid_timesteps:
                        self.display_message(f"  {master_key} {_id}: {quantity}")
                errors += self.check_indices(_sheet_name, indices)

        for entity in entities:
            for change in file_description['change']:
                raw_values = entity.get(change)
                if not raw_values:
                    continue
                timesteps = (t for t in sorted(raw_values.keys(), key=int))
                last_timestep = next(timesteps)
                filtered_values = {last_timestep: raw_values[last_timestep]}
                for timestep in timesteps:
                    if raw_values[timestep] != filtered_values[last_timestep]:
                        filtered_values[timestep] = raw_values[timestep]
                        last_timestep = timestep
                entity[change] = filtered_values

        if entities:
            self.writer.write_from_list(entities, file_name, master_key)
        return errors

    def convert_all(self):
        errors = 0
        for _entity_type in self.descriptor.keys():
            self.display_message(f"Converting {_entity_type}")
            errors += self.convert_file(_entity_type)
            self.display_message(f"Converting {_entity_type} : Done")
        self.display_message("File is fully converted")
        return errors

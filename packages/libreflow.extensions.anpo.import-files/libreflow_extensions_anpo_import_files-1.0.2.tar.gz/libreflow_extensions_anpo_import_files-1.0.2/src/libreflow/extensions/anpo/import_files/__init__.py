import re
from kabaret import flow
from kabaret.flow.object import _Manager
from libreflow.utils.flow.import_files import ImportFilesAction as BaseImportFilesAction
from libreflow.flows.default.flow import Project
from libreflow.baseflow.film import FilmCollection
from libreflow.baseflow import ProjectSettings

from . import _version
__version__ = _version.get_versions()['version']


class ANPOImportFilesAction(BaseImportFilesAction):

    def resolve_entities(self, file_name, match_file):
        pattern_dict = dict(
            film=self.settings.film_regex.get(),
            sequence=self.settings.sequence_regex.get(),
            shot=self.settings.shot_regex.get(),
            asset_type=self.settings.asset_type_regex.get(),
            asset_family=self.settings.asset_family_regex.get(),
            asset=self.settings.asset_regex.get()
        )

        match_dict = dict(
            film=None,
            sequence=None,
            shot=None,
            asset_type=None,
            asset_family=None,
            asset=None
        )

        for key, pattern in pattern_dict.items():
            # For base entity (film and asset type)
            if key in ('film', 'asset_type'):
                if key == 'film':
                    map_items = self.root().project().films.mapped_items()
                else:
                    map_items = self.root().project().asset_types.mapped_items()

                for item in reversed(map_items):
                    regexp = pattern.format(name=item.name())

                    match = re.search(regexp, file_name)
                    if match:
                        self.session.log_info(f'[Import Files] Find matching {key} ({match.group(0)})')
                        match_dict[key] = match.group(0)
                        break

                # Set main film if parameter enabled
                if (
                    key == 'film'
                    and match_dict[key] is None
                    and self.settings.use_main_film.get()
                ):
                    match_dict[key] = self.root().project().films.mapped_items()[0].name()

            # For sequence, shot and asset
            if key in ('sequence', 'shot', 'asset_family', 'asset'):
                regexp = pattern

                # Exception for asset_family and asset
                if key == 'asset_family':
                    if match_dict['asset_type'] is not None:
                        asset_type = self.root().project().asset_types[match_dict['asset_type']]

                        if len(asset_type.asset_families.mapped_items()) > 1:
                            map_items = asset_type.asset_families.mapped_items()

                            for item in reversed(map_items):
                                regexp = pattern.format(
                                    asset_type=match_dict['asset_type'],
                                    name=item.name()
                                )

                                match = re.search(regexp, file_name)
                                if match:
                                    self.session.log_info(f'[Import Files] Find matching {key} ({match.group(0)})')
                                    match_dict[key] = match.group(0)
                                    break
                            
                            if match_dict[key]:
                                continue
                        else:
                            continue
                    else:
                        continue
                elif key == 'asset':
                    if match_dict['asset_family'] is not None or match_dict['asset_type'] is not None:
                        regexp = pattern.format(
                            asset_prev_entity=match_dict['asset_family'] or match_dict['asset_type'],
                            match_file=match_file
                        )
                    else:
                        # Use asset collection to find
                        asset_collection = self.root().project().get_entity_manager().get_asset_collection().collection_name()
                        asset_collection = self.root().project().get_entity_store().get_collection(asset_collection)

                        regexp = f'.+(?=_{match_file})' # Split matching file
                        
                        match = re.search(regexp, file_name)
                        if match:
                            asset_name = match.group(0)

                            code = False
                            # Filter with name
                            query_filter = {
                                'name': {'$regex': f'^{self.get_project_oid()}.*{asset_name}',
                                '$options': 'i'}
                            }
                            cursor = asset_collection.find(query_filter)
                            name_and_doc = [(i["name"], i) for i in cursor]

                            # Filter with code
                            if not name_and_doc:
                                code = True
                                query_filter = {
                                    'code': {'$regex': f'{asset_name}$',
                                    '$options': 'i'}
                                }
                                cursor = asset_collection.find(query_filter)
                                name_and_doc = [(i["name"], i) for i in cursor]

                            if name_and_doc:
                                if len(name_and_doc) == 1:
                                    oid = name_and_doc[0][0]

                                    match_dict['asset_type'] = re.search('(?<=asset_types\/)[^\/]*', oid).group(0)
                                    self.session.log_info(f'[Import Files] Find matching asset_type ({match_dict["asset_type"]})')

                                    # Check for Asset Family
                                    regexp = '(?<=asset_families\/)[^\/]*'
                                    match = re.search(regexp, oid)

                                    if match:
                                        match_dict['asset_family'] = match.group(0)
                                        self.session.log_info(f'[Import Files] Find matching asset_family ({match_dict["asset_family"]})')

                                if code:
                                    asset_name = asset_name.replace('-', '_')    

                                match_dict['asset'] = asset_name
                                self.session.log_info(f'[Import Files] Find matching asset ({match_dict["asset"]})')
                                
                                continue

                        continue

                match = re.search(regexp, file_name)
                if match:
                    self.session.log_info(f'[Import Files] Find matching {key} ({match.group(0)})')
                    match_dict[key] = match.group(0)

        return match_dict

    def create_entities(self, item):
        super(ANPOImportFilesAction, self).create_entities(item)
        
        # Set code for assets
        if item.entities_to_create.get().get('assets'):
            data = item.entities_to_create.get().get('assets')

            map_oid = self.get_map_oid(item.file_target_oid.get(), 'assets')
            map_object = self.root().get_object(map_oid)

            if map_object.has_mapped_name(data['name']):
                new_entity = map_object[data['name']]
                new_entity.code.set(data['name'].replace('_', '-'))

                map_object.touch()


def import_files_action(parent):
    # Hide original action
    if isinstance(parent, Project) and parent.name() == "anpo":
        r = flow.Child(flow.Object)
        r.ui(hidden=True)
        r.name = 'import_files'
        return r
    # Recreate action in a sub object
    if isinstance(parent, FilmCollection) and 'anpo' in parent.oid():
        r = flow.Child(ANPOImportFilesAction).ui(dialog_size=(800,600))
        r.name = 'import_files'
        r.index = 1
        return r
    # Relocate relation in project settings
    if isinstance(parent, ProjectSettings) and 'anpo' in parent.oid():
        action = parent.root().get_object('/anpo/films/import_files')
        parent.import_files_object.set(action)
        return


def install_extensions(session):
    return {
        "import_files": [
            import_files_action,
        ]
    }

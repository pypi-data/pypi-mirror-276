# Import libraries
import os
import yaml
import click
from shutil import copyfile
from datetime import datetime
from jinja2 import Environment, BaseLoader, FileSystemLoader 
from docsible.markdown_template import static_template, collection_template
from docsible.utils.mermaid import generate_mermaid_playbook, generate_mermaid_role_tasks_per_file
from docsible.utils.yaml import load_yaml_generic, load_yaml_files_from_dir_custom, get_task_commensts
from docsible.utils.special_tasks_keys import process_special_task_keys

DOCSIBLE_START_TAG = "<!-- DOCSIBLE START -->"
DOCSIBLE_END_TAG = "<!-- DOCSIBLE END -->"
timestamp = datetime.now().strftime('%Y%m%d%H%M%S')

def get_version():
    return "0.6.4"

def manage_docsible_file_keys(docsible_path):
    default_data = {
        'description': None,
        'requester': None,
        'users': None,
        'dt_dev': None,
        'dt_prod': None,
        'dt_update': datetime.now().strftime('%d/%m/%Y'),
        'version': None,
        'time_saving': None,
        'category': None,
        'subCategory': None,
        'aap_hub': None,
        'critical': None
    }
    if os.path.exists(docsible_path):
        with open(docsible_path, 'r') as f:
            existing_data = yaml.safe_load(f) or {}
        updated_data = {**default_data, **existing_data}
        if updated_data != existing_data:
            with open(docsible_path, 'w', encoding='utf-8') as f:
                yaml.dump(updated_data, f, default_flow_style=False)
            print(f"Updated {docsible_path} with new keys.")
    else:
        with open(docsible_path, 'w', encoding='utf-8') as f:
            yaml.dump(default_data, f, default_flow_style=False)
        print(f"Initialized {docsible_path} with default keys.")

def manage_docsible_tags(content):
    return f"{DOCSIBLE_START_TAG}\n{content}\n{DOCSIBLE_END_TAG}"

def replace_between_tags(existing_content, new_content):
    start_index = existing_content.find(DOCSIBLE_START_TAG)
    end_index = existing_content.find(DOCSIBLE_END_TAG) + len(DOCSIBLE_END_TAG)

    if start_index != -1 and end_index != -1:
        before = existing_content[:start_index].rstrip()
        after = existing_content[end_index:].lstrip()
        return f"{before}\n{new_content}\n{after}".strip()
    else:
        return existing_content + '\n' + new_content.strip()

def render_readme_template(collection_metadata, roles_info, output_path, append):
    """
    Render the collection README.md using an embedded Jinja template.
    """
    env = Environment(loader=BaseLoader())
    template = env.from_string(collection_template)
    data = {
        'collection': collection_metadata,
        'roles': roles_info
    }
    new_content = template.render(data)
    new_content = manage_docsible_tags(new_content)
    
    if os.path.exists(output_path):
        with open(output_path, 'r', encoding='utf-8') as f:
            existing_readme = f.read()
        if append:
            if DOCSIBLE_START_TAG in existing_readme and DOCSIBLE_END_TAG in existing_readme:
                final_content = replace_between_tags(existing_readme, new_content)
            else:
                final_content = f"{existing_readme}\n{new_content}"
        else:
            final_content = new_content
    else:
        final_content = new_content
    
    with open(output_path, 'w', encoding='utf-8') as readme_file:
        readme_file.write(final_content)
    print(f"Collection README.md written at: {output_path}")

def document_collection_roles(collection_path, playbook, graph, no_backup, no_docsible, comments, md_template, append, output):
    """
    Document all roles in a collection, extracting metadata from galaxy.yml or galaxy.yaml.
    """
    for root, dirs, files in os.walk(collection_path):
        galaxy_file = next((f for f in files if f in ['galaxy.yml', 'galaxy.yaml']), None)
        if galaxy_file:
            galaxy_path = os.path.join(root, galaxy_file)
            with open(galaxy_path, 'r') as f:
                collection_metadata = yaml.safe_load(f)
                if output == "README.md":
                    readme_path = os.path.join(root, collection_metadata.get('readme', output))
                else:
                    readme_path = os.path.join(root, output)

            if os.path.exists(readme_path) and not no_backup:
                backup_path = f"{ readme_path[:readme_path.lower().rfind('.md')] }_backup_{timestamp}.md"
                copyfile(readme_path, backup_path)
                print(f"Backup of existing {output} created at: {backup_path}")

            roles_dir = os.path.join(root, 'roles')
            roles_info = []
            if os.path.exists(roles_dir) and os.path.isdir(roles_dir):
                for role in os.listdir(roles_dir):
                    role_path = os.path.join(roles_dir, role)
                    if os.path.isdir(role_path):
                        if playbook:
                            playbook_content = None
                            role_playbook_path = os.path.join(role_path, playbook)
                            try:
                                with open(role_playbook_path, 'r') as f:
                                    playbook_content = f.read()
                            except FileNotFoundError:
                                print(f'{role} not found:', role_playbook_path)
                            except Exception as e:
                                print(f'{playbook} import for {role} error:', e)
                        role_info = document_role(role_path, playbook_content, graph, no_backup, no_docsible, comments, md_template, belongs_to_collection=collection_metadata, append=append, output=output)
                        roles_info.append(role_info)

            render_readme_template(collection_metadata, roles_info, readme_path, append)

@click.command()
@click.option('--role', default=None, help='Path to the Ansible role directory.')
@click.option('--collection', default=None, help='Path to the Ansible collection directory.')
@click.option('--playbook', default='tests/test.yml', help='Path to the playbook file.')
@click.option('--graph', is_flag=True, help='Generate Mermaid graph for tasks.')
@click.option('--no-backup', is_flag=True, help='Do not backup the readme before remove.')
@click.option('--no-docsible', is_flag=True, help='Do not generate .docsible file and do not include it in README.md.')
@click.option('--comments', is_flag=True, help='Read comments from tasks files')
@click.option('--md-template', default=None, help='Path to the markdown template file.')
@click.option('--append', is_flag=True, help='Append to the existing README.md instead of replacing it.')
@click.option('--output', default='README.md', help='Output readme file name.')
@click.version_option(version=get_version(), help="Show the module version.")

def doc_the_role(role, collection, playbook, graph, no_backup, no_docsible, comments, md_template, append, output):
    if collection:
        collection_path = os.path.abspath(collection)
        if not os.path.exists(collection_path) or not os.path.isdir(collection_path):
            print(f"Folder {collection_path} does not exist.")
            return
        document_collection_roles(collection_path, playbook, graph, no_backup, no_docsible, comments, md_template, append, output)
    elif role:
        role_path = os.path.abspath(role)
        if not os.path.exists(role_path) or not os.path.isdir(role_path):
            print(f"Folder {role_path} does not exist.")
            return
        playbook_content = None
        if playbook:
            try:
                with open(playbook, 'r') as f:
                    playbook_content = f.read()
            except FileNotFoundError:
                print('playbook not found:', playbook)
            except Exception as e:
                print('playbook import error:', e)
        document_role(role_path, playbook_content, graph, no_backup, no_docsible, comments, md_template, belongs_to_collection=False, append=append, output=output)
    else:
        print("Please specify either a role or a collection path.")

def document_role(role_path, playbook_content, generate_graph, no_backup, no_docsible, comments, md_template, belongs_to_collection, append, output):
    role_name = os.path.basename(role_path)
    readme_path = os.path.join(role_path, output)
    meta_path = os.path.join(role_path, "meta", "main.yml")
    docsible_path = os.path.join(role_path, ".docsible")
    if not no_docsible:
        manage_docsible_file_keys(docsible_path)

    # Check if meta/main.yml exist, otherwise try meta/main.yaml
    if not os.path.exists(meta_path):
        meta_path = os.path.join(role_path, "meta", "main.yaml")

    defaults_data = load_yaml_files_from_dir_custom(
        os.path.join(role_path, "defaults")) or []
    vars_data = load_yaml_files_from_dir_custom(
        os.path.join(role_path, "vars")) or []

    role_info = {
        "name": role_name,
        "defaults": defaults_data,
        "vars": vars_data,
        "tasks": [],
        "meta": load_yaml_generic(meta_path) or {},
        "playbook": {"content": playbook_content, "graph": 
                        generate_mermaid_playbook(yaml.safe_load(playbook_content)) if playbook_content else None},
        "docsible": load_yaml_generic(docsible_path) if not no_docsible else None,
        "belongs_to_collection": belongs_to_collection
    }

    tasks_dir = os.path.join(role_path, "tasks")
    role_info["tasks"] = []

    if os.path.exists(tasks_dir) and os.path.isdir(tasks_dir):
        for dirpath, dirnames, filenames in os.walk(tasks_dir):
            for task_file in filenames:
                if task_file.endswith(".yml") or task_file.endswith(".yaml"):
                    file_path = os.path.join(dirpath, task_file)
                    tasks_data = load_yaml_generic(file_path)
                    if tasks_data:
                        relative_path = os.path.relpath(file_path, tasks_dir)
                        task_info = {'file': relative_path, 'tasks': [], 'mermaid': [], "comments": []}
                        if comments:
                            task_info['comments'] = get_task_commensts(file_path)
                        if not isinstance(tasks_data, list):
                            print(f"Unexpected data type for tasks in {task_file}. Skipping.")
                            continue
                        for task in tasks_data:
                            if not isinstance(task, dict):
                                print(f"Skipping unexpected data in {task_file}: {task}")
                                continue
                            if task and len(task.keys()) > 0:
                                processed_tasks = process_special_task_keys(task)
                                task_info['tasks'].extend(processed_tasks)
                                task_info['mermaid'].extend([task])

                        role_info["tasks"].append(task_info)

    if os.path.exists(readme_path):
        if not no_backup:
            backup_readme_path = os.path.join(role_path, f"{ output[:output.lower().rfind('.md')] }_backup_{timestamp}.md")
            copyfile(readme_path, backup_readme_path)
            print(f'Readme file backed up as: {backup_readme_path}')
        if not append:
            os.remove(readme_path)

    mermaid_code_per_file = {}
    if generate_graph:
        mermaid_code_per_file = generate_mermaid_role_tasks_per_file(role_info["tasks"])
    
    # Render the static template
    if md_template:
        template_dir = os.path.dirname(md_template)
        template_file = os.path.basename(md_template)
        env = Environment(loader=FileSystemLoader(template_dir))
        template = env.get_template(template_file)
    else:
        env = Environment(loader=BaseLoader)
        template = env.from_string(static_template)
    new_content = template.render(role=role_info, mermaid_code_per_file=mermaid_code_per_file)
    new_content = manage_docsible_tags(new_content)
    
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            existing_readme = f.read()
        if append:
            if DOCSIBLE_START_TAG in existing_readme and DOCSIBLE_END_TAG in existing_readme:
                final_content = replace_between_tags(existing_readme, new_content)
            else:
                final_content = f"{existing_readme}\n{new_content}"
        else:
            final_content = new_content
    else:
        final_content = new_content
    
    with open(readme_path, "w", encoding='utf-8') as f:
        f.write(final_content)

    print('Documentation generated at:', readme_path)
    return role_info


if __name__ == '__main__':
    doc_the_role()

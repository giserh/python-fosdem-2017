#!/usr/bin/env python
import yaml
import jinja2
import markdown
import os
from pathlib import Path
import shutil

cwd = Path.cwd()

TARGET_DIR = cwd / 'public'
TARGET_STATIC_DIR = TARGET_DIR / 'static'
SOURCE_DIR = cwd / 'src'
STATIC_DIR = cwd / 'static'

def humanize_date(current_date):
    if isinstance(current_date, str):
        import datetime
        current_date = datetime.datetime.strptime(current_date, '%Y-%m-%d')

    return current_date.strftime('%B %d, %Y')

def main():
    if not TARGET_DIR.exists():
        os.makedirs(TARGET_DIR.as_posix())
    if TARGET_STATIC_DIR.exists():
        shutil.rmtree(TARGET_STATIC_DIR.as_posix())

    shutil.copytree(STATIC_DIR.as_posix(), TARGET_STATIC_DIR.as_posix())
        
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader('templates')
    )
    env.filters['humanize_date'] = humanize_date

    with open('conf.yaml', 'rb') as fp:
        site = yaml.load(fp)

    for input_file in SOURCE_DIR.glob('*.md'):
        file_name, file_suffix = input_file.stem, input_file.suffix

        template_name = 'index' if file_name == 'index' else 'page'

        template = env.from_string(input_file.read_text())

        rendered_md = template.render(site=site)

        page_tpl = env.get_template(template_name + '.html')

        md = markdown.Markdown(extensions=['markdown.extensions.meta'])
        content = md.convert(rendered_md)

        page = md.Meta
        
        stream = page_tpl.stream(site=site, content=content, page=page)
        
        stream.dump(
            TARGET_DIR.joinpath(file_name).with_suffix('.html').as_posix()
        )
        

if __name__ == '__main__':
    main()

import argparse
import pathlib
from box import Box

def parse_cli() -> argparse.Namespace:
  parser = argparse.ArgumentParser(
              prog='create_redirects',
              description='Create HTML redirect files')
  parser.add_argument('--html',default='_html')
  parser.add_argument('--redirects',default='redirect.yml')
  return parser.parse_args()

def read_yaml(fname: str) -> Box:
  return Box().from_yaml(fname,default_box=True,default_box_none_transform=False)

def create_files(args: argparse.Namespace, reds: Box) -> None:
  for fn,target in reds.items():
    if '/index.html' in target:
      target = target.replace('/index.html','/')
    with open(f"{args.html}/{fn}") as output:
      output.write(
f"""<!DOCTYPE html>
<meta charset="utf-8">
<title>Redirecting to {target}</title>
<meta http-equiv="refresh" content="0; URL={target}">
<link rel="canonical" href="{target}">
""")

def scan_root(path: str,reds: Box,args) -> Box:
  for fname in list(pathlib.Path(path).glob('**/*.*')):
    relpath = fname.relative_to(path)
    if not '.html' in str(fname):
      continue
    relurl = f'{args.subtree}{"/" if args.subtree else ""}{relpath}'
    target = f'{args.target}/{relpath}'
    print(f'{fname} --> {relpath}')
    reds[relurl] = target

def main() -> None:
  args = parse_cli()
  reds = read_yaml(args.output)
  create_files(args,reds)

main()

import argparse
import pathlib
from box import Box

def parse_cli() -> argparse.Namespace:
  parser = argparse.ArgumentParser(
              prog='get_urls',
              description='Generates a list of redirection URLs')
  parser.add_argument('root',nargs='?',default='../_html')
  parser.add_argument('--output',default='redirect.yml')
  parser.add_argument('--subtree',default='bgplab')
  parser.add_argument('--target',default='https://bgplab.github.io/bgplab')
  return parser.parse_args()

def read_yaml(fname: str) -> Box:
  try:
    return Box().from_yaml(fname,default_box=True,default_box_none_transform=False)
  except:
    return Box({},default_box=True,default_box_none_transform=False)

def write_yaml(fname: str, data: Box) -> None:
  data.to_yaml(filename=fname)

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
  scan_root(args.root,reds,args)
  write_yaml(args.output,reds)

main()

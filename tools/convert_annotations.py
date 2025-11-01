#!/usr/bin/env python3
"""
convert_annotations.py

Usage:
  python tools/convert_annotations.py <annotations_json> <out_dir>

Reads an annotations JSON produced by the in-browser "Download Dataset" button
(which contains entries of the form {image: dataURL, bbox:[x,y,w,h], label}).
It will decode images into files under <out_dir>/images and produce a COCO-format
annotations file at <out_dir>/annotations.json and a categories.json mapping.

This is intended as a small helper to convert the app output to a dataset that
can be uploaded to Roboflow or used with local training pipelines.
"""

import sys
import os
import json
import base64
from pathlib import Path
from PIL import Image
from io import BytesIO


def ensure_dir(p):
    os.makedirs(p, exist_ok=True)


def decode_data_url(data_url):
    # data:[<mediatype>][;base64],<data>
    if not data_url.startswith('data:'):
        raise ValueError('Not a data URL')
    header, b64 = data_url.split(',', 1)
    return base64.b64decode(b64)


def main(argv):
    if len(argv) < 3:
        print(__doc__)
        return 1
    src = Path(argv[1])
    out = Path(argv[2])
    if not src.exists():
        print('Input file not found:', src)
        return 2
    ensure_dir(out / 'images')
    data = json.loads(src.read_text())
    images = []
    annotations = []
    categories = {}
    cat_id = 1
    img_id = 1
    ann_id = 1
    for item in data:
        img_data = item.get('image')
        bbox = item.get('bbox')
        label = item.get('label', 'unknown')
        if label not in categories:
            categories[label] = cat_id
            cat_id += 1
        # decode image
        try:
            raw = decode_data_url(img_data)
        except Exception as e:
            print('Skipping image decode:', e)
            continue
        img = Image.open(BytesIO(raw)).convert('RGB')
        fname = f'image_{img_id:05d}.jpg'
        img.save(out / 'images' / fname, format='JPEG', quality=90)
        w, h = img.size
        images.append({'id': img_id, 'file_name': fname, 'width': w, 'height': h})
        # bbox is [x,y,w,h] in pixel coordinates (we saved that earlier)
        x, y, bw, bh = bbox
        annotations.append({
            'id': ann_id,
            'image_id': img_id,
            'category_id': categories[label],
            'bbox': [int(x), int(y), int(bw), int(bh)],
            'area': int(bw * bh),
            'iscrowd': 0,
            'segmentation': []
        })
        img_id += 1
        ann_id += 1
    # build categories array
    cats = [{'id': cid, 'name': name} for name, cid in categories.items()]
    coco = {'images': images, 'annotations': annotations, 'categories': cats}
    (out / 'annotations.json').write_text(json.dumps(coco, indent=2))
    (out / 'categories.json').write_text(json.dumps(cats, indent=2))
    print('Wrote', len(images), 'images to', out / 'images')
    print('Wrote COCO annotations to', out / 'annotations.json')
    return 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))

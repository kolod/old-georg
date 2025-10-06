#!/bin/python3
 
from pathlib import Path
from hashlib import new


def create_hash(path: Path):
    hash_functions = [new(x) for x in ['sha256', 'sha1', 'md5']]
    with path.open('rb') as f:
        while chunk := f.read(8192):
            for function in hash_functions:
                function.update(chunk)
    
    for function in hash_functions:
        path.with_suffix('.'+function.name).write_text(function.hexdigest())


def checksum(*paths: Path) -> int:
    result: int = 0

    for path in paths:
        for byte in path.read_bytes():
            result = (result + byte) & 0xFF
    
    print(f"{' + '.join([x.name for x in paths]):30s}=> 0x{result:02X}")
    return result


def join_files(output: Path, *inputs: Path):
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open('wb') as out_file:
        for input in inputs:
            out_file.write(input.read_bytes())


if __name__ == "__main__":
    root = Path(__file__).parent

    for path in root.rglob('*.bin'):
        create_hash(path)

    checksum(root / 'mpu.bin')
    checksum(root / 'plc1-1.bin', root / 'plc1-2.bin')
    checksum(root / 'plc2-1.bin', root / 'plc2-2.bin')
    checksum(root / 'plc3-1.bin', root / 'plc3-2.bin')
    checksum(root / 'plc4-1.bin', root / 'plc4-2.bin')
    checksum(root / 'plc5-1.bin', root / 'plc5-2.bin')
    checksum(root / 'pvc.bin')

    join_files(root / 'plc1.bin', root / 'plc1-1.bin', root / 'plc1-2.bin')
    join_files(root / 'plc2.bin', root / 'plc2-1.bin', root / 'plc2-2.bin')
    join_files(root / 'plc3.bin', root / 'plc3-1.bin', root / 'plc3-2.bin')
    join_files(root / 'plc4.bin', root / 'plc4-1.bin', root / 'plc4-2.bin')
    join_files(root / 'plc5.bin', root / 'plc5-1.bin', root / 'plc5-2.bin')

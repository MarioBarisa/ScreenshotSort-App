
def test_export_does_not_override_existing_file(tmp_path):

    input_dir=tmp_path/"samples"
    output_dir=tmp_path/"export"

    input_dir.mkdir()
    output_dir.mkdir()

    source = input_dir /"menu.png"
    destination = output_dir/"menu.png"

    source.write_bytes(b"source content")
    destination.write_bytes(b"exiting coopy")

    report={"menu.png":{}}
    export_images(input_dir, output_dir, report)

    assert  destination.read_bytes()==b"existing copy"

def test_scan_and_export_preserve_subfolders(tmp_path):
    input_dir = tmp_path / "samples"
    output_dir= tmp_path / "export"

    input_dir.mkdir()
    output_dir.mkdir()





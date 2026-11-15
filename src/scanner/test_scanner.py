from PIL import Image
from scanner import export_images, scan_images

def test_export_does_not_override_existing_file(tmp_path):

    input_dir=tmp_path/"samples"
    output_dir=tmp_path/"export"

    input_dir.mkdir()
    output_dir.mkdir()

    source = input_dir /"menu.png"
    destination = output_dir/"menu.png"

    source.write_bytes(b"source content")
    destination.write_bytes(b"existing copy")

    report={"menu.png":{}}
    export_images(input_dir, output_dir, report)

    assert  destination.read_bytes()==b"existing copy"

def test_scan_and_export_preserve_subfolders(tmp_path):
    input_dir = tmp_path / "samples"
    output_dir= tmp_path / "export"

    input_dir.mkdir(parents=True, exist_ok=True)
    (input_dir/"zelda").mkdir(parents=True, exist_ok=True)
    (input_dir/"genshin").mkdir(parents=True, exist_ok=True)

    zelda = Image.new(mode="RGB", size=(250, 250), color="green")
    zelda.save(input_dir/"zelda"/"menu.png")
    genshin = Image.new(mode="RGB", size=(250,250), color="yellow")
    genshin.save(input_dir/"genshin"/"menu.png")

    scanned= scan_images(input_dir)
    export_images(input_dir,output_dir,scanned)

    assert (output_dir/"zelda"/"menu.png").is_file()
    assert (output_dir/"genshin"/"menu.png").is_file()

def test_scan_reports_inavlid_image(tmp_path):
    fake_image = tmp_path / "fake.jpg"
    fake_image.write_text("This is not an image!")

    report = scan_images(tmp_path)

    assert report["fake.jpg"]["error"] == "UnidentifiedImageError"

def main_tests():
    test_scan_and_export_preserve_subfolders()
    test_export_does_not_override_existing_file()
    test_scan_reports_inavlid_image()

if __name__ == '__main__':
    main_tests()






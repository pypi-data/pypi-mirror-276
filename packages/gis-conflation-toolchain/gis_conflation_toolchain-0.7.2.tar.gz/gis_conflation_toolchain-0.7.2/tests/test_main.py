# pip install pytest-testinfra
# pytest


# def test_wikitext_001_jsonld():
#     assert True


# def test_wikitext_003_jsonld():
#     assert True


def test_csv2excel_cmd(host):
    cmd = host.run("csv2excel --help")
    assert cmd.rc == 0


def test_csv2geojson_cmd(host):
    cmd = host.run("csv2geojson --help")
    assert cmd.rc == 0


def test_geojsondiff_cmd(host):
    cmd = host.run("geojsondiff --help")
    assert cmd.rc == 0


# def test_nginx_running_and_enabled(host):
#     nginx = host.service("nginx")
#     assert nginx.is_running
#     assert nginx.is_enabled

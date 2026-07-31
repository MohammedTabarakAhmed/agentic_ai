from nodes.app_builder import build_basic_ui_files


def test_build_basic_ui_files_contains_centered_layout():
    files = build_basic_ui_files("travel planner")

    assert "index.html" in files
    assert "styles.css" in files
    assert "script.js" in files

    html = files["index.html"]
    css = files["styles.css"]
    script = files["script.js"]

    assert "Travel Planner" in html or "travel planner" in html.lower()
    assert "search" in html.lower()
    assert "justify-content: center" in css or "place-items: center" in css

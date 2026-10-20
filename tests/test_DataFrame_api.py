import pandas

from MSMetaEnhancer import Application


def test_load_dataframe_with_mapping():
    app = Application()
    df = pandas.DataFrame({"Name": ["a"], "cas": ["50-00-0"]})
    app.load_dataframe(df, {"Name": "compound_name"})
    assert app.data.get_metadata() == [{"compound_name": "a", "cas": "50-00-0"}]
    assert list(df.columns) == ["Name", "cas"]
    assert list(app.get_dataframe({"compound_name": "Name"}).columns) == ["Name", "cas"]

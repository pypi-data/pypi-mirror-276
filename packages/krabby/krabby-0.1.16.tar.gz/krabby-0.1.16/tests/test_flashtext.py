from krabby import KeywordProcessor, Span

def test_extract_keyword():
    kwp = KeywordProcessor(False)
    kwp.put("apple")
    kwp.put("banana")
    
    spans: list[Span] = kwp.extract("I like apple and banana.")
    assert len(spans) == 2

    assert spans[0].start == 7
    assert spans[0].end == 12
    
    assert spans[1].start == 17
    assert spans[1].end == 23

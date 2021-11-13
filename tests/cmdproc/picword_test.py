import pytest

def testget_show_word():
    from cmdproc.picword import get_show_word
    assert get_show_word("test",1) == "t***"
    assert get_show_word("test",2) == "t**t"
    assert get_show_word("test",3) == "te*t"
    assert get_show_word("test",4) == "test"
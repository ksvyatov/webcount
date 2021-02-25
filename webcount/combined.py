import requests

def most_common_word_in_web_page(words, url, user_agent=requests):
    """
    находит наиболее распространенное слово из
    списка слов на веб-странице, идентифицируемой по ее URL """
    response = user_agent.get(url)
    return most_common_word(words, response.text)

def most_common_word(words, text): 
    """
    находит наиболее распространенное слово из списка слов в фрагменте текста
    """
    word_frequency = {w: text.count(w) for w in words} 
    return sorted(words, key=word_frequency.get)[-1]

if __name__ == '__main__':
    most_common = most_common_word_in_web_page(
    ['python ', 'Python ', 'programming '],
    'https://python.org/' )
    print (most_common)



def test_most_common_word():
    assert most_common_word(['a', 'b', 'c'], 'abbbcc') == 'b', 'most_common_word with unique asnwer'

def test_most_common_word_empty_candidate():
    from pytest import raises
    with raises(Exception):
        most_common_word([], 'abc'), \
            "empty word raises"

def test_most_common_ambiguous_result():
    assert most_common_word(['a', 'b', 'c'], 'ab') in ('a', 'b'), "there might be a tie"

def test_with_test_double(): 

    class TestResponse(): 
        text = 'aa bbb c'

    class TestUserAgent(): 
        def get(self, url):
            return TestResponse()

    result = most_common_word_in_web_page( ['a', 'b', 'c'], 'https://python.org/', user_agent=TestUserAgent())
    assert result == 'b', 'most_common_word_in_web_page tested with test double'

from unittest.mock import Mock, patch
def test_with_mock():
    mock_requests = Mock() 
    mock_requests.get.return_value.text = 'aa bbb c'
    result = most_common_word_in_web_page( ['a', 'b', 'c'], 'https://python.org/', user_agent=mock_requests)
    assert result == 'b', 'most_common_word_in_web_page tested with test double' 
    assert mock_requests.get.call_count == 1
    assert mock_requests.get.call_args[0][0] == 'https://python.org/', 'called with right URL'


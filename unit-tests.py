import unittest
from afinn import SentimentCount


class TestSentimentCount(unittest.TestCase):
    def setUp(self):
        self.sentiment_count = SentimentCount('AFINN-111.txt', 'tweets.db')

    # Тестирование ф-ции clear_str
    def test_clear_str(self):
        self.assertEqual(self.sentiment_count.clear_str('Good Job'), 'good job')
        self.assertEqual(self.sentiment_count.clear_str('GoodJob'), 'goodjob')
        self.assertEqual(self.sentiment_count.clear_str('here..'), 'here')
        self.assertEqual(self.sentiment_count.clear_str('Good, Job; here...'), 'good job here')
        self.assertEqual(self.sentiment_count.clear_str('Good,Job'), 'good job')
        self.assertEqual(self.sentiment_count.clear_str('Tab    test\n  here,  \t jobs;;g;,5%'), 'tab test here jobs g')
        self.assertEqual(self.sentiment_count.clear_str('   so   MaNy  spaces h44;*ere!!!'), 'so many spaces h ere')
        self.assertEqual(self.sentiment_count.clear_str('gre,,en fud, , here'), 'gre en fud here')
        self.assertEqual(self.sentiment_count.clear_str("@fud you're scum! Can't stand with you!!"), "@fud you're scum can't stand with you")
        self.assertEqual(self.sentiment_count.clear_str("@fud you're scum! Can't stand with you' man!!"), "@fud you're scum can't stand with you man")
        self.assertEqual(self.sentiment_count.clear_str("@fud you're scum! Can't stand with you'!!"), "@fud you're scum can't stand with you")
        self.assertEqual(self.sentiment_count.clear_str("@fud you're scum! Can't stand with you'!!@ fg@"), "@fud you're scum can't stand with you fg")
        self.assertEqual(self.sentiment_count.clear_str("@fud you're scum! Can't stand with you'!!@ fg@ @"), "@fud you're scum can't stand with you fg")

    # Тестирование ф-ции sentiment_count на всем справочнике AFINN
    def test_AFINN_sentiment_count(self):
        for l in self.sentiment_count.lexicon:
            self.assertEqual(self.sentiment_count.sentiment_count(l), self.sentiment_count.lexicon[l])

    # Индивидуальные тестирования ф-ции sentiment_count
    def test_sentiment_count(self):
        self.assertEqual(self.sentiment_count.sentiment_count("niggas talk on twitter but in life they don't say shit"), -9)
        self.assertEqual(self.sentiment_count.sentiment_count("fud welcome gg pp ttt ddddd"), -1)  # fud -3, welcome 2
        self.assertEqual(self.sentiment_count.sentiment_count("fud green wash car"), -6)
        self.assertEqual(self.sentiment_count.sentiment_count("green fud"), -3)
        self.assertEqual(self.sentiment_count.sentiment_count("green fud here"), -3)
        self.assertEqual(self.sentiment_count.sentiment_count("green green wash green wash try green wash tr fud hj"), -12)
        self.assertEqual(self.sentiment_count.sentiment_count("got farce dont dont like like really grants was liked by me"), 2)
        self.assertEqual(self.sentiment_count.sentiment_count("stopstop stop stopstopstopstop stop like assets wow asset wo assets"), 10)
        self.assertEqual(self.sentiment_count.sentiment_count("@fud you're scumbag can't stand with you fg"), -7)
        self.assertEqual(self.sentiment_count.sentiment_count("fud you're scumbag can't stand with you fg"), -10)


unittest.main()

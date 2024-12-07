import unittest

from py3_tiehu.pklot import Pklot


class MyTestCase(unittest.TestCase):
    def test_pklot(self):
        pklot = Pklot(
            base_url="http://ykt.test.cxyun.net.cn:7303",
            parking_id="aa",
            app_key="aa"
        )
        s=pklot.request_with_signature(
                url="/cxzn/interface/queryPklot",
                json={
                    "parkingId": "aa",
                }
            )
        print(
            s
        )
        self.assertTrue(True, "ok")  # add assertion here


if __name__ == '__main__':
    unittest.main()

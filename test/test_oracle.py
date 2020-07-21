from component.oracle import Oracle


def test1():
    oracle = Oracle(ip='1', port=1521, instance='e', username='e', password='F')
    print(oracle.select("""
    s
    """, params={'accounting_code': 'Z01110010000000000', 'duration': '202006'}))


if __name__ == '__main__':
    test1()

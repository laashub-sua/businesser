from component import path


def test1():
    print(path.find_third_party_path())


def test2():
    print(path.find_tag_path(path_tag='data'))


if __name__ == '__main__':
    # test1()
    test2()

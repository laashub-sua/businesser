from service import database_oracle


def test1():
    print(database_oracle.call_registration('analysis_report',
                                            {"accounting_code": "Z01110010000000000", "duration": "202006"}))


if __name__ == '__main__':
    test1()

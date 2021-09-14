import tabula
import pandas as pd
import os
import logging

log = logging.getLogger()
console = logging.StreamHandler()
str_format = '%(asctime)s\t%(levelname)s -- %(processName)s %(filename)s:%(lineno)s -- %(message)s'
console.setFormatter(logging.Formatter(str_format))

log.addHandler(console)  # print to console
log.setLevel(logging.DEBUG)


def main():
    page = os.path.dirname(__file__) + '/pdf/vp-2aug21.pdf'
    table = tabula.read_pdf(page,
                            stream=True, pages='1,2,3,4',
                            area=(78.57, 84.34, 78.57+639.35, 84.34+358.49),
                            multiple_tables=False, guess=False)
    df = table[0][1:]
    try:
        log.debug(f"len cols = {len(df.columns)}")
        for i in range(2, len(df.columns)):
            log.debug(f"dropping {i}th column")
            df.drop(df.columns[i], axis=1, inplace=True)
    except IndexError:
        pass
    # df.columns = ['MP', 'Record', 'todrop']
    df.columns = ['MP', 'Record']

    df['Record'].ffill(axis=0, inplace=True)
    df['Date'] = pd.to_datetime(df['Record'].loc[df.loc[df['Record'] == 'PRESENT:'].index[0]-2])
    df = df[(df['Record'].str.strip() == 'PRESENT:') | (df['Record'].str.strip() == 'ABSENT:')]
    df = df[df['MP'].notna()]
    titles = ['Assoc', 'Dr', 'Miss', 'Mr', 'Ms', 'Mrs']
    df = df[df['MP'].str.split(' ').str[0].isin(titles)]
    log.info('Done')


if __name__ == '__main__':
    main()

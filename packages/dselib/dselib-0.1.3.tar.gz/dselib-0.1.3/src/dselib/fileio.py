# -*- coding: utf-8 -*-
# Excel,CSV, JSON 등등 파일에 대한 읽기, 쓰기 라이브러리 
# Data Factory Studio / Object Storage 에 올리는 파일포멧(CSV, JSON)으로 변환하는 기능 관련 모듈 





import os  
import re 
import pprint 
pp = pprint.PrettyPrinter(indent=2)
import json 

import pandas as pd

from ipylib2 import ifile



################################################################
# FILE I/O 
################################################################

def check_english_filename(filepath):
    filename = os.path.basename(filepath)
    # root, ext = os.path.splitext(filename)
    if check_has_korean(filename):
        print(f'ERROR | 경로를 제외한 파일명에 한글이 있으면 저장하지 않는다! 입력된 파일명: {filename}')
        return False 
    else:
        return True 


# 문자열에 한글이 있는지 없는지 체크
def check_has_korean(s):
    return True if re.search('[가-힣]+', s) is not None else False


def check_columns_are_english(cols):
    li = [c for c in cols if check_has_korean(c)]
    dic = {}
    for c in li:
        dic.update({c: ''})
    print('아래 Dictionary를 이용하여 컬럼들을 영어로 변경하라')
    pp.pprint(dic)
    return True if len(li) == 0 else False


def save_as_csv(csv_file, df):
    # 경로를 제외한 파일명에 한글이 있으면 저장하지 않는다
    filename = os.path.basename(csv_file)
    if re.search('[가-힣]+', filename) is None:
        passfail = df.to_csv(csv_file, index=False, encoding='utf-8')
        print('Pass/Fail:', passfail)
        print('Success:', csv_file)
    else:
        print(f'ERROR | 경로를 제외한 파일명에 한글이 있으면 저장하지 않는다! 입력된 파일명: {filename}')


def load_csv(topdir, filename):
    csv_file = ifile.find_file(topdir, filename)
    if os.path.exists(csv_file):
        return pd.read_csv(csv_file)
    else:
        print(f'ERROR | CSV파일의 경로를 확인하시오: {csv_file}')
            

class FilenameCleaner():

    def __init__(self):
        pass 

    # Data Factory Studio 에서 데이터 저장시, 경로 포함 파일명은 전부 English 이어야 한다
    def _clean_filename(self, filename):
        if re.search('[가-힣]+', filename) is None:
            return filename 
        else: 
            print('Data Factory Studio 에서 데이터 저장시, 경로 포함 파일명은 전부 English 이어야 한다! 원본파일명:', filename)

            # CASE.01
            if re.search('연계', filename) is not None:
                filename = re.sub('연계', repl='_related_', string=filename)
                return filename
            else:
                return None 


def normalize_columns(columns):
    colsmap = {}
    for col in columns:
        c = re.sub('_x000D_', repl='', string=col)
        c = c.lower()
        c = re.sub('[\s-]+', repl='_', string=c)
        c = re.sub("[\.']+", repl='', string=c)
        c = re.sub("^class$", repl='class_', string=c)
        c = re.sub("^matl$", repl='material', string=c)
        c = re.sub("%", repl='pct', string=c)
        c = re.sub("/", repl='_n_', string=c)
        colsmap.update({col: c})

    return colsmap


def __normalize_2depth_columns(df):
    cols_1 = list(df.columns)
    _df = df.iloc[0:1, :]
    _df = _df.fillna('')
    cols_2 = _df.values[0]
    # print(cols_1)
    # print(cols_2)
    # print(len(cols_1), len(cols_2))

    # Unnamed 컬럼은 이전값으로 채운다
    old_cols = cols_1.copy()
    for i, c in enumerate(cols_1):
        # print(i, c)
        if re.search('Unnamed', c) is not None:
            cols_1[i] = cols_1[i-1]
    # print(cols_1)
    
    new_cols = []
    for c1, c2 in zip(cols_1, cols_2):
        # print(c1, c2)
        new_cols.append(f"{c1} {c2}")
        # if len(c2) == 0:
        #     columns.update({c1: c1})
        # else:
    # print(new_cols)

    columns = {}
    for c1, c2 in zip(old_cols, new_cols):
        columns.update({c1: c2.strip()})

    df = df.rename(columns=columns)
    columns = normalize_columns(list(df.columns))
    df = df.rename(columns=columns)
    df = df.iloc[1:, :]
    return df



# 파일명으로 폴더 생성 
def create_dir_by_filename(xslx_file):
    path = os.path.dirname(xslx_file)
    filename = os.path.basename(xslx_file)
    root, ext = os.path.splitext(filename)
    new_dir = os.path.join(path, root)
    try:
        os.mkdir(new_dir)
    except OSError as e:
        print(f'ERROR: {e}')
    else:
        print(f'파일명 폴더 생성 성공: {new_dir}')
    finally:
        return new_dir


# 엑셀파일명을 DFS 패키지명으로 변환
def normalize_excelname_to_packagename(xslx_files):
    for filepath in xslx_files:
        file = os.path.basename(filepath)
        filename, ext = os.path.splitext(file)
        pkg_name = normalize_pkgname(filename)
        print(f"{file} --> {pkg_name}")
    return 


# 엑셀파일명을 DFS 패키지명으로 변환
def generate_dfs_storage_path(project_name, filepath):
    # 파일타입 
    root, ext = os.path.splitext(filepath)
    filetype = ext.replace('.', '').strip().upper()

    if filetype in ['CSV', 'JSON']:
        datatype = 'DemoData'
        filename = os.path.basename(os.path.dirname(filepath))
    elif filetype in ['XLSX', 'XLS']:
        datatype = 'RawData'
        filename, ext = os.path.splitext(os.path.basename(filepath))

    return f"{project_name}/{datatype}/{filetype}/{filename}/"


def write_json(obj, filepath):
    with open(filepath, 'w', encoding='utf-8') as fp:
        json.dump(obj, fp, ensure_ascii=False)
        fp.close()


def read_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as fp:
        js = json.load(fp)
        fp.close()
    return js 



################################################################
# Excel 
################################################################



class ExcelSheet():
    # xslx_file: 엑셀파일의 파일명 포함 전체경로
    # sheet_name: 엑셀파일 원본 시트명
    # alias_name: DFS에 업로드하기 위해 반드시 필요한 영문 시트명. 데이터모델링 시 클래스명으로 동일하게 사용하길 권장

    def __init__(self, xslx_file, sheet_name, alias_name=None):
        self.filepath = xslx_file
        
        # 시트명으로 모델명 설정
        self.name = sheet_name
        if check_has_korean(sheet_name):
            if alias_name is None:
                self.modelName = None
            else:
                if check_has_korean(alias_name):
                    self.modelName = None
                else:
                    self.modelName = alias_name
        else:
            self.name = sheet_name 
            self.modelName = sheet_name 

        if self.modelName is None:
            print("""
                WARNING | 한글 시트명을 반드시 영문으로 바꿔야 하는 이유:
                [1] DFS에 업로드하기 위해서 파일명 포함 전체 경로 문자열이 영문이 아니면 Pipeline을 사용할 수 없다.
                [2] DFS에서 데이터 모델링 시 클래스명은 반드시 영문이어야 한다. 클래스명은 '파이썬 클래스' 작명 규칙에 따라 작성해야한다.
            """)

    # 엑셀시트의 테이블을 데이터프레임으로 읽어온다
    def load_data(self):
        df = pd.read_excel(self.filepath, sheet_name=self.name)
        return df.dropna(axis=0, how='all')

    # DFS Data Modeling이 요구하는 형태로 스키마 파일구조 생성
    def gen_schema(self):
        df = self.load_data()
        df = restruct_dataframe(df)
        schema = generate_schema(df)
        return schema
    
    def parse_data(self, schema_filepath=None):
        df = self.load_data()
        if schema_filepath is None:
            # 자동으로 변환
            df = normalize_dataframe(df)
        else:
            # 사용자 지정 스키마 기준으로 변환
            # 컬럼명만 변환한다
            schema = read_json(schema_filepath)
            # pp.pprint(schema)
            columns = {}
            for col, dic in schema.items():
                columns.update({col: dic['Column Name']})
            # pp.pprint(columns)

            df = restruct_dataframe(df)
            df = df.rename(columns=columns)

        return df
    


class ExcelFile():

    def __init__(self, xslx_file, sheet_trsl_file=None):
        # 파일경로 + 파일명 + 확장자
        self.filepath = xslx_file

        # 실제 파일 경로
        self.path = os.path.dirname(xslx_file)
        # 실제 파일 (확장자 포함)
        self.file = os.path.basename(xslx_file)
        # DFS / Data Model / Package Name 으로 사용할 변수명 
        root, ext = os.path.splitext(self.file)
        self.filename = root
        self.pkg_name = normalize_pkgname(root)


        # 시트명 검사 
        self.ef = pd.ExcelFile(xslx_file)
        self.sheet_names = self.ef.sheet_names
        print('원본시트명 리스트:', self.sheet_names)
        if sheet_trsl_file is None:
            for name in self.sheet_names:
                if check_has_korean(name):
                    print("ERROR | 시트명 한/영 변환 JSON파일을 파라미터 'sheet_trsl_file'로 입력하시오.")
                    raise 
        else:
            # 시트명 한/영 변환 메타데이터
            self.sheet_trsl = read_json(sheet_trsl_file)
            for name in self.sheet_names:
                if check_has_korean(name):
                    if name in self.sheet_trsl:
                        pass 
                    else:
                        print("ERROR | 시트명 한/영 변환 JSON파일을 수정하시오.")
                        raise 
                else:
                    self.sheet_trsl.update({name: normalize_classname(name)})


    # 실제 파일명으로 신규 폴더 생성
    def make_dir(self):
        create_dir_by_filename(self.filepath)
        self.workdir = os.path.join(self.path, self.filename)

    # ExcelSheet 객체를 리턴
    def get_sheet(self, sheet_name):
        def __get_alias__(sheet_name):
            if sheet_name in self.sheet_trsl:
                return self.sheet_trsl[sheet_name]
            else:
                return sheet_name
            
        return ExcelSheet(self.filepath, sheet_name, alias_name=__get_alias__(sheet_name))


    ################################################################
    # 스키마 파일 생성
    ################################################################
    def write_schema_file(self, sheet_name):
        sheet = self.get_sheet(sheet_name)
        schema = sheet.gen_schema()

        json_file = os.path.join(self.workdir, 'SCHEMA_' + sheet_name + '.json')
        # print('스키마파일경로:', json_file)
        write_json(schema, json_file)

    # 각 시트에 대해 스키마 JSON 파일을 생성
    def generate_all_schemas(self):
        self.make_dir()
        for sheet_name in self.sheet_names:
            self.write_schema_file(sheet_name)
        print('스키마 JSON 파일 생성완료.')
    

    ################################################################
    # CSV 파일 생성
    ################################################################
    def write_csv_file(self, sheet_name):
        sheet = self.get_sheet(sheet_name)
        df = sheet.parse_data()
        csv_file = os.path.join(self.workdir, sheet.modelName + '.csv')
        save_as_csv(csv_file, df)

    # 모든시트를 CSV 파일로 저장
    def extract_all_sheets(self):
        self.make_dir()
        for sheet_name in self.sheet_names:
            self.write_csv_file(sheet_name)
        print('엑셀파일의 모든 시트를 CSV로 변환완료.')


    ################################################################
    # DFS 경로 생성
    ################################################################

    # DFS/Object Storage 에 파일을 올릴 때 사용할 경로
    def gen_rawdata_storage_path(self, project_name, provider_name):
        return f"{project_name}/Rawdata/{provider_name}/{self.pkg_name}/"
    
    def gen_demodata_storage_path(self, project_name, ftype='CSV'):
        return f"{project_name}/DemoData/{ftype}/{self.pkg_name}/"

    



    






################################################################
# General Data Parser 
################################################################

def interpret_dtype(df):
    # df.info()
    # print(df.describe())
    srs = df.dtypes
    # print(srs)
    d = srs.to_dict()
    for k,v in d.items():
        v = v.__str__()
        if re.search('object', v) is not None:
            v = 'String'
        elif re.search('int', v) is not None:
            v = 'Integer'
        elif re.search('float', v) is not None:
            v = 'Float'
        elif re.search('date', v) is not None:
            v = 'DateTime'
        elif re.search('true|false', v) is not None:
            v = 'Boolean'
        else:
            print('ERROR: (개발오류)데이터타입을 추가하시오')
            raise 
        d.update({k: v})
    # pp.pprint(d)
    return d 


def generate_schema(df):
    dtypes = interpret_dtype(df)
    # return 

    columns = list(df.columns)
    schema = {}
    for c in columns:
        schema.update({
            c: {
                'Column Name': normalize_colname(c),
                'Data Type': dtypes[c],
                'Description': '',
            }
        })
    return schema 



def clean_dataframe(df):
    # ' ' 와 같은 값은 쓰레기 값이므로, None 처리
    df = df.applymap(lambda x: None if len(str(x).strip()) == 0 else x)
    # df = df.dropna(axis=1, how='all')
    df = df.dropna(axis=0, how='all')
    return df 


def normalize_filename(s):
    c = s.strip()
    # 날짜/시간 제거
    c = re.sub("\d{8}|\d{6}", repl='', string=c)
    c = re.sub("%", repl='pct', string=c)
    c = re.sub("['-\(\)\s\.]+", repl='_', string=c)
    c = re.sub("-", repl='_', string=c)
    c = re.sub("/", repl='_n_', string=c)
    c = re.sub("__", repl='_', string=c)
    # 양끝 조정
    c = re.sub("^_|_$", repl='', string=c)
    return c 


# 파일명을 DFS Storage & DataModel 에 사용할 패키지명으로 정규화
def normalize_pkgname(s):
    c = s.strip()
    # 날짜/시간 제거
    c = re.sub("\d{8}|\d{6}", repl='', string=c)
    c = re.sub("and", repl='_', string=c)
    c = re.sub("['-\(\)\s\.]+", repl='_', string=c)
    c = re.sub("-", repl='_', string=c)
    c = re.sub("__", repl='_', string=c)
    c = re.sub("^_|_$", repl='', string=c)
    # 맨마지막에 '_' 를 제거
    c = re.sub("_", repl='', string=c)
    return c 

def normalize_classname(s):
    words = re.split('\W', s)
    words = [w for w in words if len(w.strip()) > 0]
    words = [word.capitalize() for word in words]
    print(words)
    s = "".join(words)
    # 날짜/시간 제거
    s = re.sub("\d{8}|\d{6}", repl='', string=s)
    # 양끝 조정
    s = re.sub("^_|_$", repl='', string=s)
    print('클래스명:', s)
    return s 

def normalize_sheetname(s):
    return normalize_filename(s)


def normalize_colname(col):
    c = col.strip()
    # 엑셀시트 셀내부에서 엔터키 삭제 처리
    c = re.sub('_x000D_', repl='', string=c)
    # 빈칸, 특수기호 를 언더바 처리
    c = re.sub('[\s-]+', repl='_', string=c)
    c = re.sub("[\.']+", repl='', string=c)
    # 알파벳 문자열 처리
    c = c.lower()
    c = re.sub("^class$", repl='class_', string=c)
    c = re.sub("^matl$", repl='material', string=c)
    # 특수기호 문자화 처리
    c = re.sub("%", repl='pct', string=c)
    c = re.sub("/", repl='_n_', string=c)
    c = re.sub("_nat$", repl='', string=c)
    # 마무리 처리
    c = re.sub('[\(\)]', repl='_', string=c)
    c = re.sub("__", repl='_', string=c)
    c = re.sub("^_|_$", repl='', string=c)
    return c 


def get_normalized_colmap(cols):
    columns = {}
    for col in cols:
        columns.update({col: normalize_colname(col)})

    # print('\n정규화된 컬럼명 매핑:')
    # pp.pprint(columns)
    return columns


def has_2depth_columns(df):
    result = False 
    for c in list(df.columns):
        if re.search('[Uu]nnamed', c) is not None:
            result = True 
            break 
    # print('2뎁스 여부: ', result)
    return result 


def restruct_dataframe(df):
    if has_2depth_columns(df):
        df = restruct_2depth_columns(df)
    else:
        pass 
    return df 

def normalize_dataframe(df):
    df = restruct_dataframe(df)
    columns = get_normalized_colmap(list(df.columns))
    df = df.rename(columns=columns)
    return df 

# 2depth 컬럼 구조를 1depth 구조로 변경
# FROM DATAFRAME TO DATAFRAME
def restruct_2depth_columns(df):

    DEBUG_MODE = False

    ################################################################ PHASE-1
    # 데이터 분리 -> 컬럼Lv1, 컬럼Lv2, 값데이터

    def __view_2depth_columns__(cols_1, cols_2):
        if DEBUG_MODE:
            print('\n\n')
            print(cols_1)
            print(cols_2)
            print(len(cols_1), len(cols_2))

    # Lv1 컬럼명 추출 
    cols_1 = list(df.columns)

    # Lv2 컬럼명 추출 
    _df = df.iloc[0:1, :]
    _df = _df.fillna('')
    cols_2 = _df.values[0]
    __view_2depth_columns__(cols_1, cols_2)

    # 순수 값 데이터 추출 
    _df2 = df.iloc[1:, :]
    # print(_df2.head())
    pure_data = list(_df2.values)

    ################################################################ PHASE-2
    # 컬럼명 청소

    def __view_before_after_columns__(prev, next):
        if DEBUG_MODE:
            print('\n\n')
            print('전:', len(prev), prev)
            print('후:', len(next), next)

    # Unnamed 컬럼은 이전값으로 채운다
    def __fill_lv1_columns_(cols):
        prev = cols.copy()
        for i, c in enumerate(cols):
            if re.search('Unnamed', c) is not None:
                cols[i] = cols[i-1]

        __view_before_after_columns__(prev, cols)
        return cols
    
    def __clean_lv2_columns_(cols):
        prev = cols.copy()
        
        # 컬럼명 청소
        for i, c in enumerate(cols):
            if not isinstance(c, str):
                cols[i] = ''

        __view_before_after_columns__(prev, cols)
        return cols
    
    cols_1 = __fill_lv1_columns_(cols_1)
    cols_2 = __clean_lv2_columns_(cols_2)

    # print('LEVEL-1:', cols_1)
    # print('LEVEL-2:', cols_2)
    # return 

    ################################################################ PHASE-3
    # 다중구조 컬럼명 프레임 생성

    colname_frame = []
    for i, (c1, c2) in enumerate(zip(cols_1, cols_2)):
        # print([i, c1, c2])
        colname_frame.append([c1, c2])
    colname_frame = pd.DataFrame(colname_frame, columns=['c1', 'c2'])
    
    # 컬럼순서 유지를 위한 인덱스 설정
    colname_frame = colname_frame.reset_index(drop=False).rename(columns={'index': 'idx'})
    # return colname_frame

    for n, g in colname_frame.groupby('c1', sort=False):
        # print('-'*100)
        # print([n, len(g)])
        # print(g)
        if len(g) == 1:
            # print(g)
            idx = g.idx.values[0]
            # print('idx:', idx, type(idx))
            colname_frame.at[idx, 'c2'] = ''
            colname_frame.at[idx, 'c3'] = ''
            # break
        elif len(g) > 1:
            # 2중구조 컬럼일때 
            # print(g)
            # print(g.idx.values)
            vals = g.c2.values
            vals = [v.strip() for v in vals]
            # print(vals)

            len_1 = len(vals)
            len_2 = len(set(vals))
            if len_1 == len_2:
                # 2depth 컬럼명이 서로 다 다를때
                for idx in g.idx.values:
                    colname_frame.at[idx, 'c3'] = ''
            else:
                # 2depth 컬럼명에 일정한 규칙이 없을때 
                # print('시퀀싱 처리 필요.')
                # print(g)
                # print()
                # c2 값 채우기
                g['c2'] = g.c2.apply(lambda x: x if len(x.strip()) > 0 else None).ffill()
                # print(g)
                for d in g.to_dict('records'):
                    colname_frame.at[d['idx'], 'c2'] = d['c2']
                
                # c3 값 채우기
                for n2, g2 in g.groupby(['c1','c2'], sort=False):
                    # print('GROUP BY 2:', n2, len(g2))
                    idx_li = g2.idx.values
                    c3_vals = list(range(1, len(g2)+1))
                    # print(idx_li, c3_vals)
                    for idx, c3 in zip(idx_li, c3_vals):
                        colname_frame.at[idx, 'c3'] = c3 


    # colname_frame.info()
    # return colname_frame[:60]

    # 새로운 컬럼명 추가 
    for d in colname_frame.to_dict('records'):
        idx = d.pop('idx')
        vals = d.values()
        vals = [str(v) for v in vals if len(str(v)) > 0]
        colname = "_".join(vals)
        # print('컬러명:', colname)
        colname_frame.at[idx, 'column'] = colname

    # return colname_frame

    ################################################################ PHASE-4
    # 리빌딩된 데이터프레임 생성
    df = pd.DataFrame(pure_data, columns=list(colname_frame.column), dtype='str')
    # df.info()
    return df



# FROM DATAFRAME TO DATAFRAME
def normalize_2depth_columns(df):

    DEBUG_MODE = False

    ################################################################
    # 데이터 분리 -> 컬럼Lv1, 컬럼Lv2, 값데이터

    def __view_2depth_columns__(cols_1, cols_2):
        if DEBUG_MODE:
            print('\n\n')
            print(cols_1)
            print(cols_2)
            print(len(cols_1), len(cols_2))

    # Lv1 컬럼명
    cols_1 = list(df.columns)

    # Lv2 컬럼명
    _df = df.iloc[0:1, :]
    _df = _df.fillna('')
    cols_2 = _df.values[0]
    __view_2depth_columns__(cols_1, cols_2)

    # 순수 값 데이터
    _df2 = df.iloc[1:, :]
    # print(_df2.head())
    pure_data = list(_df2.values)

    ################################################################
    # 컬럼명 청소

    def __view_before_after_columns__(prev, next):
        if DEBUG_MODE:
            print('\n\n')
            print('전:', len(prev), prev)
            print('후:', len(next), next)

    # Unnamed 컬럼은 이전값으로 채운다
    def __fill_lv1_columns_(cols):
        prev = cols.copy()
        for i, c in enumerate(cols):
            if re.search('Unnamed', c) is not None:
                cols[i] = cols[i-1]

        __view_before_after_columns__(prev, cols)
        return cols
    
    def __clean_lv2_columns_(cols):
        prev = cols.copy()
        
        # 컬럼명 청소
        for i, c in enumerate(cols):
            if not isinstance(c, str):
                cols[i] = ''

        __view_before_after_columns__(prev, cols)
        return cols
    
    cols_1 = __fill_lv1_columns_(cols_1)
    cols_2 = __clean_lv2_columns_(cols_2)

    # return 

    ################################################################
    # 다중구조 컬럼명 프레임 생성

    colname_frame = []
    # 레벨2 인덱스
    _data = []
    for i, (c1, c2) in enumerate(zip(cols_1, cols_2)):
        # print([i, c1, c2])
        _data.append([c1, c2])
    df = pd.DataFrame(_data, columns=['c1', 'c2'])
    # print('\n\n')
    # print(df)

    def __add_to_colname_frame__(df):
        for d in df.to_dict('records'):
            cols = []
            for k,v in d.items():
                if len(v) > 0:
                    cols.append(v)
            colname_frame.append(cols)

    for n, g in df.groupby('c1', sort=False):
        # print('-'*100)
        # print([n, len(g)])
        if len(g) == 1:
            __add_to_colname_frame__(g)
        elif len(g) > 1:
            # data = g.to_dict('records')
            # print(data)
            g.c2 = g.c2.apply(lambda x: None if len(x) == 0 else x)
            g = g.ffill()
            # print(g)
            for n2, g2 in g.groupby(['c1','c2'], sort=False):
                k = 0 
                if len(g2) == 1:
                    __add_to_colname_frame__(g2)
                elif len(g2) > 1:
                    _data2 = g2.to_dict('records')
                    for d in _data2:
                        k+=1 
                        d.update({'c3': str(k)})
                    _g2 = pd.DataFrame(_data2)
                    # print(_g2)
                    __add_to_colname_frame__(_g2)

    # print('\n\n')
    # print(len(colname_frame))

    ################################################################
    # 데이터베이스 컬럼명으로 강제변환

    # print('\n\n')
    # new_cols = []
    # for li in colname_frame:
    #     # print(li)
    #     new_colname = "_".join(li)
    #     norm_colname = normalize_colname(new_colname)
    #     print([new_colname, norm_colname])
    #     new_cols.append(norm_colname)
    
    # df = pd.DataFrame(pure_data, columns=new_cols)
    return df


# [PARSER-TYPE-01] 1시트/1테이블/1depth_column 타입의 데이터를 구조화해서 CSV 파일로 저장 
def generate_csv_1depth_column(csv_file, df):

    # 데이터 청소
    df = clean_dataframe(df)

    # 컬럼명 정규화
    columns = get_normalized_colmap(list(df.columns))
    df = df.rename(columns=columns)

    # CSV 저장
    save_as_csv(csv_file, df)


# [PARSER-TYPE-02] 1시트/1테이블/2depth_column 타입의 데이터를 구조화해서 CSV 파일로 저장 
def generate_csv_2depth_column(csv_file, df):

    # 데이터 청소
    df = clean_dataframe(df)

    # 컬럼명 정규화
    df = normalize_2depth_columns(df)

    # CSV 저장
    save_as_csv(csv_file, df)








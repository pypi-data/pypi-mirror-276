import time
import numpy as np
import pandas as pd
import rapidfuzz as rf
from rapidfuzz import fuzz
from rapidfuzz import process, utils
from joblib import Parallel, delayed

class NameMatch:

    def __init__(self) -> None:
        self.miles_sheet_name = "Miles Names"
        self.icra_sheet_name = "ICRA Names"


    def miles_process(self, input_, string):
        input_cg = utils.default_process(input_)
        string_cg = utils.default_process(string)
        if (string_cg.split(" ")[0] == input_cg.split(" ")[0]) and ("series" not in string_cg.split(" ")):
            if ("dir" in input_cg) or ("direct" in input_cg):
                if ("dir" in string_cg) or ("direct" in string_cg):
                    return string
            elif ("dir" not in input_cg) or ("direct" not in input_cg):
                if ("dir" not in string_cg) or ("direct" not in string_cg):
                    return string
                
    def string_proc(self, x):
        temp_1 = x.lower().replace("-"," ")
        return temp_1

    def process_funds(self, i, milesSheet_list):
        temp_ = [self.miles_process(i, x) for x in milesSheet_list]
        milesList = [x for x in temp_ if x is not None]
        result = rf.process.extract(i, milesList, scorer=fuzz.ratio, limit=1, processor=self.string_proc)
        return result


    def run(self,in_path:str, out_path:str) -> bool:

        start_time = time.time()
        
        milesSheet = pd.read_excel(in_path, sheet_name=self.miles_sheet_name).dropna()
        icraSheet = pd.read_excel(in_path, sheet_name=self.icra_sheet_name).dropna()
        
        milesSheet_list = milesSheet['Fund Name'].tolist()
        icraSheet_list = icraSheet['Fund Name'].tolist()

        results = Parallel(n_jobs=-1,verbose=1)(delayed(self.process_funds)(i, milesSheet_list) for i in icraSheet_list)
        matchResults = [x[0][0] for x in results]
        list3 = [list(a) for a in zip(icraSheet_list, matchResults)]
        results = pd.DataFrame(list3,columns = ["ICRA fund name","Miles fund name"])

        writer = pd.ExcelWriter(out_path, engine = 'openpyxl')
        icraSheet.to_excel(writer, sheet_name = 'ICRA')
        milesSheet.to_excel(writer, sheet_name = 'Miles')
        results.to_excel(writer, sheet_name = 'Result')
        writer.close()  

        print("--- %s seconds ---" % round((time.time() - start_time)/60))
from pyresparser import ResumeParser

def parse_resume(file_path):
    data = ResumeParser(file_path).get_extracted_data()
    return data
if __name__ == "__main__":
    result = parse_resume("D:\\PROJECT\\resumeanalyser\\SAMPLES\\resume1.pdf")
    print(result)

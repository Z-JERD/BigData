@app.route("/download")
async def file_download(request):
    import io
    import csv
    header = [
        "id", "division", "total_price", "unit_price", "area"
    ]

    bio = io.BytesIO()

    writer_file = io.TextIOWrapper(bio, encoding='utf-8-sig')

    writer = csv.writer(writer_file, dialect='excel', delimiter=',')

    writer.writerow(header)

    filename = "测试.xlsx"

    writer_file.flush()

    return MemoryFileResponse(filename, bio.getvalue())()
    
 
class MemoryFileResponse():

    def __init__(self, file_name, file_content):
        headers = []
        filename = urllib.parse.quote(file_name.encode('utf-8'))
        headers.append(('Content-Disposition', "attachment; filename* = UTF-8''" + filename))

        self.file_content = file_content
        self.headers = headers

    def __call__(self, *args, **kwargs):
        return raw(self.file_content, headers=self.headers)
        
 
@app.route("/upload", methods=["POST"])
async def file_upload(request):

    file_handler = request.files.get("file")
    file_name = file_handler.name
    file_body = file_handler.body

    print(file_name)
    print(file_body)

    import pandas as pd

    df = pd.read_excel(file_body)
    print(df)
    print(df.values.tolist())

    return SuccessResponse({"hello": "world"})()

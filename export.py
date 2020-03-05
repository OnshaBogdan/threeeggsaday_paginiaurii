import json
import xlsxwriter


def export(json_file_path, output_file_name):
    with open(json_file_path) as f:
        data = json.load(f)
    data = [dict(t) for t in {tuple(d.items()) for d in data}]

    column_names_list = [
        'company_name',
        'address',
        'phone',
        'timetable',
        'domain',
        'website',
        'email',
        'payment_method',
        'description',
        'search_query',
        'location',
        'url',
    ]

    with xlsxwriter.Workbook(f'{output_file_name}') as workbook:
        worksheet = workbook.add_worksheet()

        worksheet.write_row(0, 0, column_names_list)

        for row_num, data in enumerate(data):
            data_row = [data[item] for item in column_names_list]
            worksheet.write_row(row_num + 1, 0, data_row)

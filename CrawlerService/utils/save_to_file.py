def json(data, file_name='data.json'):
    with open(file_name, 'w') as f:
        f.write(str(data))
import json
import csv


def parse_contents(content, content_type):
    if content_type == "application/x-json-stream":
        lines = content.split('\n')
        return [json.loads(line) for line in lines]
    elif content_type == "application/json":
        parsed_content = json.loads(content)
        return [parsed_content] if isinstance(parsed_content, dict) else parsed_content    
    else:
        return None


def main():
    with open('test.jsonl', 'r', encoding='utf8') as jsonl_file, open('telemetry_data.csv', 'w', newline='', encoding='utf8') as csv_file:
        csv_writer = csv.writer(csv_file)
        header = ['user', 'eventName', 'languageId', 'common_extname', 'common_extversion', 'common_vscodeversion', 'common_os', 'common_platformversion']
        csv_writer.writerow(header)
    
        for line in jsonl_file:
            data = json.loads(line)
            request_content_type = data['request']['headers'].get('Content-Type', data['request']['headers'].get('content-type'))
            if request_content_type is None:
                continue

            request_contents = parse_contents(data['request']['content'], request_content_type)
            # print(f"user: {data['user']} have telemetry data count: {len(request_contents)}")
            for i, req in enumerate(request_contents):
                # print(f"telemetry data {i} eventName: {req['data']['baseData']['name']}")
                # print(f"telemetry data {i} languageId: {req['data']['baseData']['properties'].get('languageId', 'N/A')}")
                # print(f"telemetry data {i} common_extname: {req['data']['baseData']['properties']['common_extname']}")
                # print(f"telemetry data {i} common_extversion: {req['data']['baseData']['properties']['common_extversion']}")
                # print(f"telemetry data {i} common_vscodeversion: {req['data']['baseData']['properties']['common_vscodeversion']}")
                # print(f"telemetry data {i} common_os: {req['data']['baseData']['properties']['common_os']}")
                # print(f"telemetry data {i} common_platformversion: {req['data']['baseData']['properties']['common_platformversion']}")
                row = [
                    data['user'],
                    req['data']['baseData']['name'],
                    req['data']['baseData']['properties'].get('languageId', 'N/A'),
                    req['data']['baseData']['properties'].get('common_extname', 'N/A'),
                    req['data']['baseData']['properties'].get('common_extversion', 'N/A'),
                    req['data']['baseData']['properties'].get('common_vscodeversion', 'N/A'),
                    req['data']['baseData']['properties'].get('common_os', 'N/A'),
                    req['data']['baseData']['properties'].get('common_platformversion', 'N/A')
                ]
                csv_writer.writerow(row)


if __name__ == '__main__':
    main()

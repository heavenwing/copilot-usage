import json


def parse_content(content, content_type):
    if content_type == "application/x-json-stream":
        lines = content.split('\n')
        return [json.loads(line) for line in lines]
    elif content_type == "application/json":
        parsed_content = json.loads(content)
        return [parsed_content] if isinstance(parsed_content, dict) else parsed_content    
    else:
        return None


def main():
    request_contents = []
    with open('test.jsonl', 'r', encoding='utf8') as f:
        for line in f:
            data = json.loads(line)
            request_content_type = data['request']['headers'].get('Content-Type')
            if request_content_type is None:
                request_content_type = data['request']['headers'].get('content-type')
            if request_content_type is None:
                continue
            # response_content_type = data['response']['headers'].get('Content-Type')
            request_content = parse_content(data['request']['content'], request_content_type)
            # response_content = parse_content(data['response']['content'], response_content_type)
            # Now request_content and response_content are parsed according to their content types
            if request_content is not None:
                request_contents.extend(request_content)
    print(f"telemetry data count: {len(request_contents)}")
    for i, req in enumerate(request_contents):
        print(f"telemetry data {i} name: {req['data']['baseData']['name']}")
        print(f"telemetry data {i} languageId: {req['data']['baseData']['properties'].get('languageId', 'N/A')}")

        # print(f"telemetry data {i} common_extname: {req['data']['baseData']['properties']['common_extname']}")
        # print(f"telemetry data {i} common_extversion: {req['data']['baseData']['properties']['common_extversion']}")
        # print(f"telemetry data {i} common_vscodeversion: {req['data']['baseData']['properties']['common_vscodeversion']}")
        # print(f"telemetry data {i} common_os: {req['data']['baseData']['properties']['common_os']}")
        # print(f"telemetry data {i} common_platformversion: {req['data']['baseData']['properties']['common_platformversion']}")


if __name__ == '__main__':
    main()

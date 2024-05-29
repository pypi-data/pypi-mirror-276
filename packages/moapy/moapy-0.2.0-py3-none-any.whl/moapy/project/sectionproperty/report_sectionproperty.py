import base.midasutil_web as midasutil_web

url = "https://moa.rpm.kr-dv-midasit.com/backend/function-executor/python-execute/base.section_property/mdreport"

def Do(json_data):
    body = {
        "arguments": json_data
    }

    # 헤더 정의 (필요시)
    headers = {
        "Content-Type": "application/json"
    }

    # POST 요청 보내기
    response = midasutil_web.requests_json.post(url, headers=headers, jsonObj=body)
    # 응답 결과 출력
    return response

import requests
from graphql.mutations import enroll_course
from api.parsers import GraphQLResponse
from api.flows.base_flow import BaseFlow
from utils.logger import log_info, log_error, log_warning, log_result

class EnrollCourseFlow(BaseFlow):
    def __init__(self, api_url, context=None):
        super().__init__(api_url=api_url, context=context)
        self.api_url = api_url
        self.context = context

    def enroll_course(self, course_id, pw_request=None, is_error=False) -> GraphQLResponse:
        mutation = enroll_course.ENROLL_COURSE_MUTATION
        variables = {
            "input": {  
                "courseId": course_id
            }
        }
        log_info(f"Sending register course request for {course_id}")
        token = self.variables.get_variable("accessToken")
        headers = {}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        
        if pw_request:
            # 1. Chạy qua Playwright APIRequestContext (được đồng bộ Auth/Cookie/Token)
            response = pw_request.post(
                self.api_url, 
                data={'query': mutation, 'variables': variables},
                headers=headers
            )
            assert response.ok, f"API Enroll Course (Playwright) thất bại với HTTP status: {response.status}"
            response_data = response.json()
        else:
            # 2. Fallback sử dụng requests python thuần (dành cho các test API độc lập không chạy UI)
            response = requests.post(
                self.api_url, 
                json={'query': mutation, 'variables': variables},
                headers=headers
            )
            assert response.status_code == 200, f"API Enroll Course (Requests) thất bại với HTTP status: {response.status_code}"
            response_data = response.json()

        assert "errors" not in response_data, f"GraphQL Error: {response_data.get('errors')}"
        return GraphQLResponse(**response_data)
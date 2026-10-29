ENROLL_COURSE_MUTATION = """
mutation Mutation($input: CreateEnrollmentInput!) {
  enrollCourse(input: $input) {
    courseId
    enrolledAt
    id
    userId
  }
}
"""

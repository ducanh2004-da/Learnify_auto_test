REGISTER_MUTATION = """
mutation Mutation($data: RegisterInput!) {
  register(data: $data) {
    message
    success
  }
}
"""

LOGIN_MUTATION = """
mutation Login($data: LoginInput!) {
  login(data: $data) {
    accessToken
    message
    refreshToken
    success
  }
}
"""

VERIFY_USER_BY_EMAIL = """
mutation Mutation($email: String!) {
  verifyUserByEmail(email: $email) {
    message
    success
  }
}
"""

DELETE_USER_MUTATION = """
mutation DeleteUser($id: String!) {
    deleteUser(id: $id)
}
"""
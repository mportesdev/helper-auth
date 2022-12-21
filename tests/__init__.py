class HelperOutputCases:
    def case_default(self):
        return "username=github_name\npassword=github_token\n"

    def case_space_delimited(self):
        return "username = github_name\npassword = github_token\n"

    def case_additional_empty_line(self):
        return "username=github_name\n\npassword=github_token\n"

    def case_additional_non_empty_line(self):
        return "username=github_name\n# comment\npassword=github_token\n"
